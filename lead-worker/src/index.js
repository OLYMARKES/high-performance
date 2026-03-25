const FIELD_LIMITS = Object.freeze({
  name: 80,
  contact: 120,
  email: 160,
  about: 1200,
  participantName: 80,
  participantSlug: 120,
  loadLevel: 80,
  courseChoice: 240,
  profileNotes: 4000,
  pageUrl: 500,
  source: 80
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
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
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

const buildLeadIssuePayload = (lead, request) => {
  const { requestId, metadata } = buildSubmissionContext(lead, request);
  const leadRecord = {
    version: 1,
    kind: 'high-performance-lead',
    name: lead.name,
    contact: lead.contact,
    email: lead.email,
    about: lead.about,
    source: metadata.source,
    pageUrl: metadata.pageUrl,
    submittedAt: metadata.submittedAt,
    requestId
  };
  const encodedLeadRecord = encodeBase64(JSON.stringify(leadRecord));

  return {
    title: `[lead] ${lead.name} - ${metadata.submittedAt.slice(0, 10)}`,
    body: [
      '<!-- lead-record -->',
      `<!-- ${JSON.stringify(metadata)} -->`,
      `<!-- lead-data:v1:${encodedLeadRecord} -->`,
      '# New Lead',
      '',
      '## Contact',
      `- Name: ${escapeMd(lead.name)}`,
      `- Contact: ${escapeMd(lead.contact)}`,
      `- Email: ${escapeMd(lead.email || '-')}`,
      '',
      '## Motivation',
      quoteMd(lead.about),
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
    // Preserve the [lead] prefix so existing OpenClaw watchers still notice new submissions.
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

const buildIssuePayload = (submission, request) => {
  if (submission.kind === 'participant-profile') {
    return buildParticipantProfileIssuePayload(submission, request);
  }

  return buildLeadIssuePayload(submission, request);
};

const createGitHubIssue = async (submission, request, env) => {
  const owner = normalize(env.GITHUB_OWNER);
  const repo = normalize(env.GITHUB_REPO);
  const token = normalize(env.GITHUB_TOKEN);

  if (!owner || !repo || !token) {
    throw new Error('missing_github_config');
  }

  const { title, body } = buildIssuePayload(submission, request);
  const labels = normalize(env.ISSUE_LABELS)
    .split(',')
    .map((value) => value.trim())
    .filter(Boolean);

  const response = await fetch(`https://api.github.com/repos/${owner}/${repo}/issues`, {
    method: 'POST',
    headers: {
      Accept: 'application/vnd.github+json',
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      'User-Agent': 'high-performance-leads-worker'
    },
    body: JSON.stringify({
      title,
      body,
      ...(labels.length ? { labels } : {})
    })
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`github_issue_failed:${response.status}:${errorText}`);
  }

  return response.json();
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

    if (request.method === 'OPTIONS') {
      return jsonResponse({ ok: true }, 200, origin);
    }

    if (request.method === 'GET') {
      return jsonResponse(
        {
          ok: true,
          service: 'high-performance-lead-worker',
          githubConfigured: Boolean(env.GITHUB_OWNER && env.GITHUB_REPO && env.GITHUB_TOKEN),
          supportedKinds: ['lead', 'participant-profile']
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
      const issue = await createGitHubIssue(submission, request, env);
      return jsonResponse(
        {
          ok: true,
          issueNumber: issue.number,
          issueUrl: issue.html_url
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
