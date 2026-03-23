# High Performance lead intake

This setup stores leads as GitHub issues in a private repository. The site stays on GitHub Pages, while a Cloudflare Worker receives the form submission and writes each lead to GitHub using a secret token.

## Flow

1. Site form sends JSON to the Worker endpoint.
2. Worker validates the request and creates a new issue in a private GitHub repo.
3. Your cloudbot polls that repo for new issues whose title starts with `[lead]`.
4. The bot sends you Telegram updates.

## What to create

1. A private GitHub repo, for example `high-performance-leads`
2. A GitHub fine-grained token with write access to Issues for that repo
3. A Cloudflare Worker deployed from `lead-worker/`

## Worker configuration

Edit [wrangler.toml](/Users/olymarkes/Desktop/high%20perfomance%20/lead-worker/wrangler.toml):

- `GITHUB_OWNER`: your GitHub login
- `GITHUB_REPO`: the private repo that will store leads
- `ALLOWED_ORIGIN`: keep as `https://olymarkes.github.io`
- `ISSUE_LABELS`: optional labels, only use labels that already exist in the target repo

Then set the GitHub token as a secret:

```bash
cd lead-worker
wrangler secret put GITHUB_TOKEN
```

Deploy:

```bash
cd lead-worker
wrangler deploy
```

After deploy, copy the Worker URL.

## Connect the site form

In both files below, replace `const FORM_ENDPOINT = '';` with your Worker URL:

- [index.html](/Users/olymarkes/Desktop/high%20perfomance%20/index.html)
- [hyper-performance.html](/Users/olymarkes/Desktop/high%20perfomance%20/hyper-performance.html)

Example:

```js
const FORM_ENDPOINT = 'https://high-performance-leads.<your-subdomain>.workers.dev';
```

## How your cloudbot can read leads

Simplest option: poll GitHub Issues in the private repo and treat each open issue with title prefix `[lead]` as a new lead.

Suggested logic:

1. List open issues in the repo
2. Filter titles starting with `[lead]`
3. Store the latest seen issue number
4. Send new ones to Telegram
5. Optionally add a comment or close the issue after processing

## Issue format

Each lead becomes one issue with:

- contact fields in markdown
- metadata like `submittedAt`, `pageUrl`, and request id
- a hidden HTML comment containing machine-readable metadata for bot parsing

## Current site behavior

Right now the form has a fallback mode:

- if `FORM_ENDPOINT` is empty, the lead text is copied and Telegram opens manually
- if `FORM_ENDPOINT` is set, the form sends JSON to the Worker

This means the public site remains usable while you are wiring the backend.
