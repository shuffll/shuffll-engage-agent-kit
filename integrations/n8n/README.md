# Shuffll Engage workflows for n8n

Three inactive, manual starter workflows using standard n8n nodes. These are distribution drafts, not approved n8n template listings or a verified community node.

| Workflow | Behavior | Scope |
| --- | --- | --- |
| `discover-templates.json` | Read capabilities and first page of published templates | `templates:read` |
| `review-creation-brief.json` | List saved briefs and read one owned brief | `templates:read` |
| `create-creation-brief.json` | Save a text creation brief without generating media | `templates:write` |

## Setup

1. Obtain a dedicated organization-scoped Engage API key through authorized workspace administration. Public customer accounts require an enabled subscription and API access; marketplace reviewers receive an isolated synthetic workspace.
2. Import a workflow using **Import from File**. Select a private **Bearer Auth** credential on every HTTP Request node and store the key there. Never put credentials in workflow fields, URLs, shared exports or chat. Exports contain no keys, credential IDs or pinned data.
3. Replace the Edit Fields placeholders with your organization UUID and, for reading, an owned journey UUID. For creation, select a unique idempotency key for the intended brief and retain it for uncertain retries.
4. Run manually and inspect each output. A creation response is an operation job; queued/running is not completion. Follow `GET /api/v1/jobs/{id}` using the returned job ID and respect `pollAfterSeconds` until terminal, then inspect `result`.

## Review workspace

The review workspace contains saved synthetic briefs. Template lists can be empty because a text brief is not a published video template. These workflows never generate media, export MP4s, activate campaigns, add recipients or send messages. Reviewer access is restricted and expires; it does not grant production customer data or a free public trial.

## Pagination and privacy

List requests return at most 50 items. Continue with the exact returned `nextCursor` until null when a complete list is needed. Execution-data saving is disabled in these exports, but review the instance's logging, retention and access settings. HTTP failures stop the workflow. Requests use the fixed Engage production origin, a 30-second timeout and no redirects.

## Verification and publication

The production HTTP contracts for capabilities, template listing, brief listing/reading and brief creation have been tested with a dedicated synthetic key. Brief creation completed successfully and was read back; foreign-workspace reads are denied. Native n8n import/execution remains unverified until a signed-in instance is available. Complete that verification before submitting through the [n8n Creator Portal](https://creators.n8n.io/). A native community node needs a separate npm package, provenance and n8n review.

[Engage documentation](https://api-docs.shuffll.com/engage) · [Support](https://api-docs.shuffll.com/contact)
