# Shuffll Engage workflows for n8n

Three importable starter workflows built from n8n's standard Manual Trigger, Edit Fields, HTTP Request and Sticky Note nodes. No community package is required. These are distribution drafts, not an n8n-verified integration or approved template listing. Authenticated execution and import in a target n8n instance remain to be verified.

| Workflow | What it does | Required scopes |
| --- | --- | --- |
| `discover-templates.json` | Inspect workspace capabilities, then list the first page of published templates | `templates:read` |
| `review-campaign-results.json` | Inspect readiness and list the first page of results for a selected campaign | `campaigns:read`, `results:read` |
| `create-draft-campaign.json` | Submit a campaign-creation job for a selected ready version; no rendering or delivery | `campaigns:write` |

## Setup

1. Use a paid Shuffll workspace with API access enabled and a dedicated organization-scoped key limited to the scopes needed by the chosen workflow. Obtain it through Shuffll's authorized administration flow.
2. In n8n, import the workflow JSON using **Import from File**. All workflows are inactive and start manually.
3. Create a private **Templated Custom Auth** credential. Define a secret field named `api_key` and the template below. Add the API key only to that private field, then select the credential on every HTTP Request node. Use `https://engage.shuffll.com/api/v1/capabilities` as a GET test URL if the credential editor offers one.

```json
{"headers":{"Authorization":"Bearer {{api_key}}"}}
```

If your n8n version does not offer Templated Custom Auth, explicitly select its supported Bearer Auth credential in each HTTP node and store the key there. Do not put keys in workflow fields, URLs or shared exports. These files contain no credentials or credential IDs.

4. Replace the Edit Fields placeholders for the campaign workflows. For creation, select an authorized ready frozen `flat-video-v1` version and choose a unique idempotency key for that intended campaign. Keep the same key when retrying an uncertain creation result; use a new key for a different campaign.
5. Run the workflow manually in a synthetic workspace first. Inspect the output of each node. A creation response is a job envelope: queued/running/failed/partially failed states are not successful campaign creation. Follow the returned job ID using `GET /api/v1/jobs/{id}`, respecting `pollAfterSeconds`, until terminal; inspect `result` before using a resource ID.

## Pagination and data

List nodes return only the first page (50 items). If `nextCursor` is non-null, add a query parameter named `cursor` to that list node using the exact returned value, and run it again in the same workspace. Continue until null. Do not treat the first page as a complete export.

Successful and failed execution-data saving and manual execution-data saving are disabled in the workflow settings. Review your instance's logging, retention and access settings before production use. Result URLs may grant access to private media; keep outputs within the authorized team. No customer data or pinned execution data is included here.

## Current limits

These workflows use documented production REST routes, while creative journey tools exposed by MCP may differ. Legacy fixed-video campaigns do not personalize rendered media from recipient names, segments or contact fields. These workflows do not generate media, send messages, create public webhooks, or make delivery/engagement claims. HTTP failures stop the execution and are not converted into successful empty results. Each HTTP request has a 30-second timeout and does not follow redirects.

## Publishing to n8n

Authenticate to the [n8n Creator Portal](https://creators.n8n.io/), execute and verify each workflow with a scoped synthetic workspace, then submit the workflow and its setup instructions to the template library. A native community-node listing is a separate project: it requires an npm package, GitHub Actions publication with provenance, and n8n review. These standard-node workflows do not establish native-node verification.

[Engage documentation](https://api-docs.shuffll.com/engage) · [Campaign workflow](https://api-docs.shuffll.com/engage/workflows) · [Support](https://api-docs.shuffll.com/contact)
