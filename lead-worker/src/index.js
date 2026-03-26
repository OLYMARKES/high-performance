const FIELD_LIMITS = Object.freeze({
  name: 80,
  contact: 120,
  email: 160,
  about: 1200,
  participantName: 80,
  participantSlug: 120,
  loadLevel: 80,
  selectedPath: 40,
  courseChoice: 240,
  personalContext: 4000,
  profileNotes: 4000,
  pageUrl: 500,
  source: 80,
  structuredString: 4000,
  objectKeys: 50,
  arrayItems: 50
});

const CONTROL_CHARS_RE = /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g;
const BIDI_CONTROL_RE = /[\u202A-\u202E\u2066-\u2069]/g;
const SUSPICIOUS_CONTENT_RE = /<script\b|<\/script>|javascript:|data:text\/html|vbscript:|onerror\s*=|onload\s*=/i;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const jsonResponse = (body, status = 200, origin = '*') =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Content-Type': 'application/json; charset=utf-8'
    }
  });

const toSingleLine = (value) => value.replace(/\s+/g, ' ').trim();

const normalize = (value, { multiline = false } = {}) => {
  const cleaned = String(value || '')
    .replace(/\r\n?/g, '\n')
    .replace(CONTROL_CHARS_RE, '')
    .replace(BIDI_CONTROL_RE, '')
    .trim();

  if (!multiline) {
    return toSingleLine(cleaned);
  }

  return cleaned
    .split('\n')
    .map((line) => line.trimEnd())
    .join('\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
};

const truncate = (value, limit) => (value.length > limit ? value.slice(0, limit) : value);

const escapeMd = (value) => normalize(value).replace(/`/g, '\\`');

const quoteMd = (value) =>
  normalize(value, { multiline: true })
    .split('\n')
    .map((line) => `> ${line || ' '}`)
    .join('\n');

const encodeBase64 = (value) => {
  const bytes = new TextEncoder().encode(value);
  let binary = '';

  bytes.forEach((byte) => {
    binary += String.fromCharCode(byte);
  });

  return btoa(binary);
};

const decodeBase64 = (value) => {
  const binary = atob(value);
  const bytes = Uint8Array.from(binary, (char) => char.charCodeAt(0));
  return new TextDecoder().decode(bytes);
};

const getAllowedOrigin = (request, env) => {
  const requestOrigin = request.headers.get('Origin') || '';
  if (!env.ALLOWED_ORIGIN) {
    return requestOrigin || '*';
  }

  return env.ALLOWED_ORIGIN;
};

const ensureAllowedOrigin = (request, env) => {
  const requestOrigin = request.headers.get('Origin') || '';
  if (!env.ALLOWED_ORIGIN || !requestOrigin) {
    return true;
  }

  return requestOrigin === env.ALLOWED_ORIGIN;
};

const sanitizeStructuredValue = (value, depth = 0) => {
  if (depth > 6) {
    return null;
  }

  if (typeof value === 'string') {
    return truncate(normalize(value, { multiline: true }), FIELD_LIMITS.structuredString);
  }

  if (typeof value === 'boolean') {
    return value;
  }

  if (typeof value === 'number') {
    return truncate(normalize(String(value)), 40);
  }

  if (Array.isArray(value)) {
    return value
      .slice(0, FIELD_LIMITS.arrayItems)
      .map((item) => sanitizeStructuredValue(item, depth + 1))
      .filter((item) => item !== null && item !== '' && !(Array.isArray(item) && item.length === 0));
  }

  if (value && typeof value === 'object') {
    return Object.entries(value)
      .slice(0, FIELD_LIMITS.objectKeys)
      .reduce((acc, [key, nestedValue]) => {
        const normalizedKey = truncate(normalize(key), 80);
        if (!normalizedKey) {
          return acc;
        }

        const sanitizedValue = sanitizeStructuredValue(nestedValue, depth + 1);
        if (
          sanitizedValue === null ||
          sanitizedValue === '' ||
          (Array.isArray(sanitizedValue) && sanitizedValue.length === 0) ||
          (typeof sanitizedValue === 'object' && !Array.isArray(sanitizedValue) && Object.keys(sanitizedValue).length === 0)
        ) {
          return acc;
        }

        acc[normalizedKey] = sanitizedValue;
        return acc;
      }, {});
  }

  return null;
};

const hasMeaningfulStructuredValue = (value) => {
  if (Array.isArray(value)) {
    return value.some(hasMeaningfulStructuredValue);
  }

  if (value && typeof value === 'object') {
    return Object.values(value).some(hasMeaningfulStructuredValue);
  }

  if (typeof value === 'boolean') {
    return value;
  }

  return Boolean(normalize(String(value || ''), { multiline: true }));
};

const buildSubmissionContext = (submission, request) => {
  const requestId = crypto.randomUUID();
  const forwardedFor = request.headers.get('CF-Connecting-IP') || '';
  const userAgent = request.headers.get('User-Agent') || '';

  return {
    requestId,
    metadata: {
      requestId,
      source: submission.source || 'high-performance-site',
      pageUrl: submission.pageUrl || '',
      submittedAt: submission.submittedAt || new Date().toISOString(),
      ip: forwardedFor,
      userAgent
    }
  };
};

const buildLeadIssuePayload = (submission, request) => {
  const { requestId, metadata } = buildSubmissionContext(submission, request);
  const leadRecord = {
    version: 1,
    kind: 'high-performance-lead',
    name: submission.name,
    contact: submission.contact,
    email: submission.email,
    about: submission.about,
    source: metadata.source,
    pageUrl: metadata.pageUrl,
    submittedAt: metadata.submittedAt,
    requestId
  };
  const encodedLeadRecord = encodeBase64(JSON.stringify(leadRecord));

  return {
    title: `[lead] ${submission.name} - ${metadata.submittedAt.slice(0, 10)}`,
    body: [
      '<!-- lead-record -->',
      `<!-- ${JSON.stringify(metadata)} -->`,
      `<!-- lead-data:v1:${encodedLeadRecord} -->`,
      '# New Lead',
      '',
      '## Contact',
      `- Name: ${escapeMd(submission.name)}`,
      `- Contact: ${escapeMd(submission.contact)}`,
      `- Email: ${escapeMd(submission.email || '-')}`,
      '',
      '## Motivation',
      quoteMd(submission.about),
      '',
      '## Metadata',
      `- Submitted at: ${escapeMd(metadata.submittedAt)}`,
      `- Page: ${escapeMd(metadata.pageUrl) || '-'}`,
      `- Source: ${escapeMd(metadata.source)}`,
      `- Request ID: ${requestId}`
    ].join('\n')
  };
};

const buildParticipantProfileIssuePayload = (submission, request) => {
  const { requestId, metadata } = buildSubmissionContext(submission, request);
  const profileRecord = {
    version: 1,
    kind: 'high-performance-participant-profile',
    participantName: submission.participantName,
    participantSlug: submission.participantSlug,
    loadLevel: submission.loadLevel,
    simplePath: submission.simplePath,
    courseChoice: submission.courseChoice,
    profileNotes: submission.profileNotes,
    source: metadata.source,
    pageUrl: metadata.pageUrl,
    submittedAt: metadata.submittedAt,
    requestId
  };
  const encodedProfileRecord = encodeBase64(JSON.stringify(profileRecord));
  const notesBlock = submission.profileNotes ? quoteMd(submission.profileNotes) : '> Без подробностей';

  return {
    title: `[lead] Participant Profile - ${submission.participantName} - ${metadata.submittedAt.slice(0, 10)}`,
    body: [
      '<!-- lead-record -->',
      `<!-- ${JSON.stringify(metadata)} -->`,
      `<!-- lead-data:v1:${encodedProfileRecord} -->`,
      '# Participant Profile',
      '',
      '## Participant',
      `- Name: ${escapeMd(submission.participantName)}`,
      `- Load level: ${escapeMd(submission.loadLevel || '-')}`,
      `- Simple path: ${submission.simplePath ? 'yes' : 'no'}`,
      `- Parallel course: ${escapeMd(submission.courseChoice || '-')}`,
      '',
      '## Notes',
      notesBlock,
      '',
      '## Metadata',
      `- Submitted at: ${escapeMd(metadata.submittedAt)}`,
      `- Page: ${escapeMd(metadata.pageUrl) || '-'}`,
      `- Source: ${escapeMd(metadata.source)}`,
      `- Participant slug: ${escapeMd(submission.participantSlug || '-')}`,
      `- Request ID: ${requestId}`
    ].join('\n')
  };
};

const buildParticipantQuestionnaireIssuePayload = (submission, request) => {
  const { requestId, metadata } = buildSubmissionContext(submission, request);
  const questionnaireRecord = {
    version: 1,
    kind: 'high-performance-participant-questionnaire',
    participantName: submission.participantName,
    participantSlug: submission.participantSlug,
    email: submission.email,
    selectedPath: submission.selectedPath,
    courseChoice: submission.courseChoice,
    personalContext: submission.personalContext,
    draftState: submission.draftState,
    responseData: submission.responseData,
    source: metadata.source,
    pageUrl: metadata.pageUrl,
    submittedAt: metadata.submittedAt,
    requestId
  };
  const encodedRecord = encodeBase64(JSON.stringify(questionnaireRecord));
  const responseData = submission.responseData || {};
  const visionBlock = responseData.visionFuture ? quoteMd(responseData.visionFuture) : '> —';
  const contextBlock = submission.personalContext ? quoteMd(submission.personalContext) : '> —';

  return {
    title: `Participant Questionnaire Record - ${submission.participantName}`,
    body: [
      '<!-- lead-record -->',
      `<!-- ${JSON.stringify(metadata)} -->`,
      `<!-- lead-data:v1:${encodedRecord} -->`,
      '# Participant Questionnaire',
      '',
      '## Participant',
      `- Name: ${escapeMd(submission.participantName)}`,
      `- Email: ${escapeMd(submission.email || '-')}`,
      `- Path: ${escapeMd(submission.selectedPath || '-')}`,
      `- Parallel course: ${escapeMd(submission.courseChoice || '-')}`,
      '',
      '## Vision',
      visionBlock,
      '',
      '## Personal Context',
      contextBlock,
      '',
      '## Metadata',
      `- Submitted at: ${escapeMd(metadata.submittedAt)}`,
      `- Page: ${escapeMd(metadata.pageUrl) || '-'}`,
      `- Source: ${escapeMd(metadata.source)}`,
      `- Participant slug: ${escapeMd(submission.participantSlug || '-')}`,
      `- Request ID: ${requestId}`
    ].join('\n')
  };
};

const buildParticipantQuestionnaireSaveEventPayload = (submission, request, storageIssueNumber) => {
  const { requestId, metadata } = buildSubmissionContext(submission, request);
  const eventRecord = {
    version: 1,
    kind: 'high-performance-participant-questionnaire-save-event',
    participantName: submission.participantName,
    participantSlug: submission.participantSlug,
    email: submission.email,
    selectedPath: submission.selectedPath,
    courseChoice: submission.courseChoice,
    pageUrl: metadata.pageUrl,
    submittedAt: metadata.submittedAt,
    requestId,
    storageIssueNumber: storageIssueNumber || null
  };
  const encodedRecord = encodeBase64(JSON.stringify(eventRecord));

  return {
    title: `[lead] Questionnaire Saved - ${submission.participantName} - ${metadata.submittedAt}`,
    body: [
      '<!-- lead-record -->',
      `<!-- ${JSON.stringify(metadata)} -->`,
      `<!-- lead-data:v1:${encodedRecord} -->`,
      '# Questionnaire Saved',
      '',
      '## Participant',
      `- Name: ${escapeMd(submission.participantName)}`,
      `- Email: ${escapeMd(submission.email || '-')}`,
      `- Path: ${escapeMd(submission.selectedPath || '-')}`,
      `- Parallel course: ${escapeMd(submission.courseChoice || '-')}`,
      `- Participant slug: ${escapeMd(submission.participantSlug || '-')}`,
      `- Record issue: ${storageIssueNumber ? `#${storageIssueNumber}` : '-'}`,
      '',
      '## Metadata',
      `- Saved at: ${escapeMd(metadata.submittedAt)}`,
      `- Page: ${escapeMd(metadata.pageUrl) || '-'}`,
      `- Source: ${escapeMd(metadata.source)}`,
      `- Request ID: ${requestId}`
    ].join('\n')
  };
};

const buildParticipantWeekTrackerIssuePayload = (submission, request) => {
  const { requestId, metadata } = buildSubmissionContext(submission, request);
  const trackerRecord = {
    version: 1,
    kind: 'high-performance-participant-week-tracker',
    participantName: submission.participantName,
    participantSlug: submission.participantSlug,
    weekKey: submission.weekKey,
    trackerState: submission.trackerState,
    source: metadata.source,
    pageUrl: metadata.pageUrl,
    submittedAt: metadata.submittedAt,
    requestId
  };
  const encodedRecord = encodeBase64(JSON.stringify(trackerRecord));
  const manifesto = normalize(submission.trackerState?.manifesto || '', { multiline: true });
  const manifestoBlock = manifesto ? quoteMd(manifesto) : '> —';

  return {
    title: `Participant Week Tracker Record - ${submission.participantName} - ${submission.weekKey || 'week-1'}`,
    body: [
      '<!-- lead-record -->',
      `<!-- ${JSON.stringify(metadata)} -->`,
      `<!-- lead-data:v1:${encodedRecord} -->`,
      '# Participant Week Tracker',
      '',
      '## Participant',
      `- Name: ${escapeMd(submission.participantName)}`,
      `- Week: ${escapeMd(submission.weekKey || 'week-1')}`,
      '',
      '## Manifesto',
      manifestoBlock,
      '',
      '## Metadata',
      `- Submitted at: ${escapeMd(metadata.submittedAt)}`,
      `- Page: ${escapeMd(metadata.pageUrl) || '-'}`,
      `- Source: ${escapeMd(metadata.source)}`,
      `- Participant slug: ${escapeMd(submission.participantSlug || '-')}`,
      `- Request ID: ${requestId}`
    ].join('\n')
  };
};

const buildIssuePayload = (submission, request) => {
  if (submission.kind === 'participant-profile') {
    return buildParticipantProfileIssuePayload(submission, request);
  }

  if (submission.kind === 'participant-questionnaire') {
    return buildParticipantQuestionnaireIssuePayload(submission, request);
  }

  if (submission.kind === 'participant-week-tracker') {
    return buildParticipantWeekTrackerIssuePayload(submission, request);
  }

  return buildLeadIssuePayload(submission, request);
};

const parseRecordFromIssueBody = (body) => {
  const match = String(body || '').match(/<!-- lead-data:v1:([^>]+) -->/);
  if (!match) {
    return null;
  }

  try {
    return JSON.parse(decodeBase64(match[1]));
  } catch {
    return null;
  }
};

const githubRequest = async (env, path, options = {}) => {
  const owner = normalize(env.GITHUB_OWNER);
  const repo = normalize(env.GITHUB_REPO);
  const token = normalize(env.GITHUB_TOKEN);

  if (!owner || !repo || !token) {
    throw new Error('missing_github_config');
  }

  const response = await fetch(`https://api.github.com/repos/${owner}/${repo}${path}`, {
    ...options,
    headers: {
      Accept: 'application/vnd.github+json',
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      'User-Agent': 'high-performance-leads-worker',
      ...(options.headers || {})
    }
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`github_request_failed:${response.status}:${errorText}`);
  }

  return response;
};

const listGitHubIssues = async (env) => {
  const response = await githubRequest(env, '/issues?state=all&per_page=100');
  return response.json();
};

const findParticipantQuestionnaireIssue = async (participantSlug, env) => {
  const slug = normalize(participantSlug);
  if (!slug) {
    return null;
  }

  const issues = await listGitHubIssues(env);
  const matches = issues
    .map((issue) => ({ issue, record: parseRecordFromIssueBody(issue.body) }))
    .filter(({ record }) => record?.kind === 'high-performance-participant-questionnaire' && record.participantSlug === slug)
    .sort((left, right) => {
      const leftDate = left.record?.submittedAt || left.issue.updated_at || '';
      const rightDate = right.record?.submittedAt || right.issue.updated_at || '';
      return rightDate.localeCompare(leftDate);
    });

  return matches[0] || null;
};

const findParticipantWeekTrackerIssue = async (participantSlug, weekKey, env) => {
  const slug = normalize(participantSlug);
  const normalizedWeekKey = normalize(weekKey || 'week-1');
  if (!slug) {
    return null;
  }

  const issues = await listGitHubIssues(env);
  const matches = issues
    .map((issue) => ({ issue, record: parseRecordFromIssueBody(issue.body) }))
    .filter(
      ({ record }) =>
        record?.kind === 'high-performance-participant-week-tracker' &&
        record.participantSlug === slug &&
        normalize(record.weekKey || 'week-1') === normalizedWeekKey
    )
    .sort((left, right) => {
      const leftDate = left.record?.submittedAt || left.issue.updated_at || '';
      const rightDate = right.record?.submittedAt || right.issue.updated_at || '';
      return rightDate.localeCompare(leftDate);
    });

  return matches[0] || null;
};

const createGitHubIssueFromPayload = async ({ title, body }, env) => {
  const labels = normalize(env.ISSUE_LABELS)
    .split(',')
    .map((value) => value.trim())
    .filter(Boolean);

  const response = await githubRequest(env, '/issues', {
    method: 'POST',
    body: JSON.stringify({
      title,
      body,
      ...(labels.length ? { labels } : {})
    })
  });

  return response.json();
};

const createGitHubIssue = async (submission, request, env) =>
  createGitHubIssueFromPayload(buildIssuePayload(submission, request), env);

const updateGitHubIssue = async (issueNumber, submission, request, env) => {
  const { title, body } = buildIssuePayload(submission, request);
  const response = await githubRequest(env, `/issues/${issueNumber}`, {
    method: 'PATCH',
    body: JSON.stringify({
      title,
      body
    })
  });

  return response.json();
};

const upsertParticipantQuestionnaireIssue = async (submission, request, env) => {
  const existing = await findParticipantQuestionnaireIssue(submission.participantSlug, env);
  let issue;
  let mode;

  if (!existing) {
    issue = await createGitHubIssue(submission, request, env);
    mode = 'created';
  } else {
    issue = await updateGitHubIssue(existing.issue.number, submission, request, env);
    mode = 'updated';
  }

  const notificationIssue = await createGitHubIssueFromPayload(
    buildParticipantQuestionnaireSaveEventPayload(submission, request, issue.number),
    env
  );

  return { issue, mode, notificationIssue };
};

const upsertParticipantWeekTrackerIssue = async (submission, request, env) => {
  const existing = await findParticipantWeekTrackerIssue(submission.participantSlug, submission.weekKey, env);
  if (!existing) {
    const issue = await createGitHubIssue(submission, request, env);
    return { issue, mode: 'created' };
  }

  const issue = await updateGitHubIssue(existing.issue.number, submission, request, env);
  return { issue, mode: 'updated' };
};

const sanitizeSubmission = (payload) => {
  const kind = normalize(payload.kind);

  if (kind === 'participant-profile') {
    return {
      kind: 'participant-profile',
      participantName: truncate(normalize(payload.participantName || payload.name), FIELD_LIMITS.participantName),
      participantSlug: truncate(normalize(payload.participantSlug), FIELD_LIMITS.participantSlug),
      loadLevel: truncate(normalize(payload.loadLevel), FIELD_LIMITS.loadLevel),
      simplePath: Boolean(payload.simplePath),
      courseChoice: truncate(normalize(payload.courseChoice), FIELD_LIMITS.courseChoice),
      profileNotes: truncate(normalize(payload.profileNotes, { multiline: true }), FIELD_LIMITS.profileNotes),
      pageUrl: truncate(normalize(payload.pageUrl), FIELD_LIMITS.pageUrl),
      submittedAt: normalize(payload.submittedAt),
      source: truncate(normalize(payload.source), FIELD_LIMITS.source)
    };
  }

  if (kind === 'participant-questionnaire') {
    return {
      kind: 'participant-questionnaire',
      participantName: truncate(normalize(payload.participantName || payload.name), FIELD_LIMITS.participantName),
      participantSlug: truncate(normalize(payload.participantSlug), FIELD_LIMITS.participantSlug),
      email: truncate(normalize(payload.email), FIELD_LIMITS.email),
      selectedPath: truncate(normalize(payload.selectedPath), FIELD_LIMITS.selectedPath),
      courseChoice: truncate(normalize(payload.courseChoice), FIELD_LIMITS.courseChoice),
      personalContext: truncate(normalize(payload.personalContext, { multiline: true }), FIELD_LIMITS.personalContext),
      draftState: sanitizeStructuredValue(payload.draftState || []),
      responseData: sanitizeStructuredValue(payload.responseData || {}),
      pageUrl: truncate(normalize(payload.pageUrl), FIELD_LIMITS.pageUrl),
      submittedAt: normalize(payload.submittedAt),
      source: truncate(normalize(payload.source), FIELD_LIMITS.source)
    };
  }

  if (kind === 'participant-week-tracker') {
    return {
      kind: 'participant-week-tracker',
      participantName: truncate(normalize(payload.participantName || payload.name), FIELD_LIMITS.participantName),
      participantSlug: truncate(normalize(payload.participantSlug), FIELD_LIMITS.participantSlug),
      weekKey: truncate(normalize(payload.weekKey || 'week-1'), 80),
      trackerState: sanitizeStructuredValue(payload.trackerState || {}),
      pageUrl: truncate(normalize(payload.pageUrl), FIELD_LIMITS.pageUrl),
      submittedAt: normalize(payload.submittedAt),
      source: truncate(normalize(payload.source), FIELD_LIMITS.source)
    };
  }

  return {
    kind: 'lead',
    name: truncate(normalize(payload.name), FIELD_LIMITS.name),
    contact: truncate(normalize(payload.contact || payload.telegram), FIELD_LIMITS.contact),
    email: truncate(normalize(payload.email), FIELD_LIMITS.email),
    about: truncate(normalize(payload.about, { multiline: true }), FIELD_LIMITS.about),
    pageUrl: truncate(normalize(payload.pageUrl), FIELD_LIMITS.pageUrl),
    submittedAt: normalize(payload.submittedAt),
    source: truncate(normalize(payload.source), FIELD_LIMITS.source)
  };
};

const validateSubmission = (submission) => {
  if (submission.kind === 'participant-profile') {
    if (!submission.participantName) {
      return 'missing_required_fields';
    }

    if (!submission.loadLevel && !submission.simplePath && !submission.courseChoice && !submission.profileNotes) {
      return 'missing_required_fields';
    }

    if (
      SUSPICIOUS_CONTENT_RE.test(
        `${submission.participantName}\n${submission.loadLevel}\n${submission.courseChoice}\n${submission.profileNotes}`
      )
    ) {
      return 'suspicious_content';
    }

    return null;
  }

  if (submission.kind === 'participant-questionnaire') {
    if (!submission.participantName || !submission.participantSlug || !submission.email) {
      return 'missing_required_fields';
    }

    if (!EMAIL_RE.test(submission.email)) {
      return 'invalid_email';
    }

    if (
      !submission.selectedPath &&
      !submission.courseChoice &&
      !submission.personalContext &&
      !hasMeaningfulStructuredValue(submission.responseData)
    ) {
      return 'missing_required_fields';
    }

    if (
      SUSPICIOUS_CONTENT_RE.test(
        `${submission.participantName}\n${submission.email}\n${submission.selectedPath}\n${submission.courseChoice}\n${submission.personalContext}\n${JSON.stringify(submission.responseData)}`
      )
    ) {
      return 'suspicious_content';
    }

    return null;
  }

  if (submission.kind === 'participant-week-tracker') {
    if (!submission.participantName || !submission.participantSlug || !submission.weekKey) {
      return 'missing_required_fields';
    }

    if (!hasMeaningfulStructuredValue(submission.trackerState)) {
      return 'missing_required_fields';
    }

    if (
      SUSPICIOUS_CONTENT_RE.test(
        `${submission.participantName}\n${submission.participantSlug}\n${submission.weekKey}\n${JSON.stringify(submission.trackerState)}`
      )
    ) {
      return 'suspicious_content';
    }

    return null;
  }

  if (!submission.name || !submission.contact || !submission.about) {
    return 'missing_required_fields';
  }

  if (submission.email && !EMAIL_RE.test(submission.email)) {
    return 'invalid_email';
  }

  if (
    SUSPICIOUS_CONTENT_RE.test(
      `${submission.name}\n${submission.contact}\n${submission.email}\n${submission.about}`
    )
  ) {
    return 'suspicious_content';
  }

  return null;
};

export default {
  async fetch(request, env) {
    const origin = getAllowedOrigin(request, env);
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return jsonResponse({ ok: true }, 200, origin);
    }

    if (request.method === 'GET') {
      if (url.pathname === '/participant-questionnaire') {
        if (!ensureAllowedOrigin(request, env)) {
          return jsonResponse({ ok: false, error: 'origin_not_allowed' }, 403, origin);
        }

        const participantSlug = normalize(url.searchParams.get('slug') || url.searchParams.get('participantSlug'));
        if (!participantSlug) {
          return jsonResponse({ ok: false, error: 'missing_participant_slug' }, 400, origin);
        }

        try {
          const match = await findParticipantQuestionnaireIssue(participantSlug, env);
          if (!match) {
            return jsonResponse({ ok: true, found: false }, 200, origin);
          }

          return jsonResponse(
            {
              ok: true,
              found: true,
              record: match.record,
              issueNumber: match.issue.number,
              issueUrl: match.issue.html_url,
              updatedAt: match.issue.updated_at
            },
            200,
            origin
          );
        } catch (error) {
          return jsonResponse(
            {
              ok: false,
              error: 'github_read_failed',
              detail: error instanceof Error ? error.message : 'unknown_error'
            },
            502,
            origin
          );
        }
      }

      if (url.pathname === '/participant-week-tracker') {
        if (!ensureAllowedOrigin(request, env)) {
          return jsonResponse({ ok: false, error: 'origin_not_allowed' }, 403, origin);
        }

        const participantSlug = normalize(url.searchParams.get('slug') || url.searchParams.get('participantSlug'));
        const weekKey = normalize(url.searchParams.get('weekKey') || 'week-1');
        if (!participantSlug) {
          return jsonResponse({ ok: false, error: 'missing_participant_slug' }, 400, origin);
        }

        try {
          const match = await findParticipantWeekTrackerIssue(participantSlug, weekKey, env);
          if (!match) {
            return jsonResponse({ ok: true, found: false }, 200, origin);
          }

          return jsonResponse(
            {
              ok: true,
              found: true,
              record: match.record,
              issueNumber: match.issue.number,
              issueUrl: match.issue.html_url,
              updatedAt: match.issue.updated_at
            },
            200,
            origin
          );
        } catch (error) {
          return jsonResponse(
            {
              ok: false,
              error: 'github_read_failed',
              detail: error instanceof Error ? error.message : 'unknown_error'
            },
            502,
            origin
          );
        }
      }

      return jsonResponse(
        {
          ok: true,
          service: 'high-performance-lead-worker',
          githubConfigured: Boolean(env.GITHUB_OWNER && env.GITHUB_REPO && env.GITHUB_TOKEN),
          supportedKinds: ['lead', 'participant-profile', 'participant-questionnaire', 'participant-week-tracker'],
          readEndpoints: ['/participant-questionnaire?slug=<participant-slug>', '/participant-week-tracker?slug=<participant-slug>&weekKey=week-1']
        },
        200,
        origin
      );
    }

    if (request.method !== 'POST') {
      return jsonResponse({ ok: false, error: 'method_not_allowed' }, 405, origin);
    }

    if (!ensureAllowedOrigin(request, env)) {
      return jsonResponse({ ok: false, error: 'origin_not_allowed' }, 403, origin);
    }

    let payload;

    try {
      payload = await request.json();
    } catch {
      return jsonResponse({ ok: false, error: 'invalid_json' }, 400, origin);
    }

    const submission = sanitizeSubmission(payload);
    const validationError = validateSubmission(submission);

    if (validationError) {
      return jsonResponse({ ok: false, error: validationError }, 400, origin);
    }

    try {
      const result =
        submission.kind === 'participant-questionnaire'
          ? await upsertParticipantQuestionnaireIssue(submission, request, env)
          : submission.kind === 'participant-week-tracker'
            ? await upsertParticipantWeekTrackerIssue(submission, request, env)
          : { issue: await createGitHubIssue(submission, request, env), mode: 'created' };
      return jsonResponse(
        {
          ok: true,
          mode: result.mode,
          issueNumber: result.issue.number,
          issueUrl: result.issue.html_url,
          notificationIssueNumber: result.notificationIssue?.number || null,
          notificationIssueUrl: result.notificationIssue?.html_url || null
        },
        200,
        origin
      );
    } catch (error) {
      return jsonResponse(
        {
          ok: false,
          error: 'github_write_failed',
          detail: error instanceof Error ? error.message : 'unknown_error'
        },
        502,
        origin
      );
    }
  }
};
