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

const normalize = (value) => String(value || '').trim();

const escapeMd = (value) => normalize(value).replace(/`/g, '\\`');

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

const buildIssueBody = (lead, request) => {
  const requestId = crypto.randomUUID();
  const forwardedFor = request.headers.get('CF-Connecting-IP') || '';
  const userAgent = request.headers.get('User-Agent') || '';
  const metadata = {
    requestId,
    source: lead.source || 'high-performance-site',
    pageUrl: lead.pageUrl || '',
    submittedAt: lead.submittedAt || new Date().toISOString(),
    ip: forwardedFor,
    userAgent
  };

  return [
    '<!-- lead-record -->',
    `<!-- ${JSON.stringify(metadata)} -->`,
    '# New Lead',
    '',
    '## Contact',
    `- Name: ${escapeMd(lead.name)}`,
    `- Contact: ${escapeMd(lead.contact)}`,
    '',
    '## Motivation',
    escapeMd(lead.about),
    '',
    '## Metadata',
    `- Submitted at: ${escapeMd(metadata.submittedAt)}`,
    `- Page: ${escapeMd(metadata.pageUrl) || '-'}`,
    `- Source: ${escapeMd(metadata.source)}`,
    `- Request ID: ${requestId}`
  ].join('\n');
};

const createGitHubIssue = async (lead, request, env) => {
  const owner = normalize(env.GITHUB_OWNER);
  const repo = normalize(env.GITHUB_REPO);
  const token = normalize(env.GITHUB_TOKEN);

  if (!owner || !repo || !token) {
    throw new Error('missing_github_config');
  }

  const submittedDate = new Date(lead.submittedAt || Date.now()).toISOString().slice(0, 10);
  const title = `[lead] ${lead.name} - ${submittedDate}`;
  const body = buildIssueBody(lead, request);
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
          githubConfigured: Boolean(env.GITHUB_OWNER && env.GITHUB_REPO && env.GITHUB_TOKEN)
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

    const lead = {
      name: normalize(payload.name),
      contact: normalize(payload.contact || payload.telegram),
      about: normalize(payload.about),
      pageUrl: normalize(payload.pageUrl),
      submittedAt: normalize(payload.submittedAt),
      source: normalize(payload.source)
    };

    if (!lead.name || !lead.contact || !lead.about) {
      return jsonResponse({ ok: false, error: 'missing_required_fields' }, 400, origin);
    }

    try {
      const issue = await createGitHubIssue(lead, request, env);
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
