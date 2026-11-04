# Activation status

This is an alpha installation package. It does not deploy or activate any service.

| Item | Status on 2026-11-04 |
| --- | --- |
| Canonical merchant endpoint | `https://mcp.eirberg.app/mcp`, selected for the independent Eirberg service |
| Service source | [`vitverk/eirberg`](https://github.com/vitverk/eirberg), `apps/merchant-mcp` |
| Backend target | Medusa staging only; production access is not enabled by this package |
| Protected resource metadata | `https://mcp.eirberg.app/.well-known/oauth-protected-resource/mcp`, pending deployment verification |
| Authorization server metadata | `https://mcp.eirberg.app/.well-known/oauth-authorization-server`, pending deployment verification |
| OAuth contract | Public client, PKCE S256, dynamic registration; resource audience is the exact MCP endpoint |
| Read scope | `merchant:read` |
| Optional write scope | `merchant:write`, subject to explicit consent and native Medusa permissions |
| Live staff / ChatGPT acceptance | Pending |

Staff authenticate against Medusa through the Eirberg connection flow. Medusa remains
the authority for users, roles, record access, merchant mutations and operation receipts.
The service does not depend on Vitverk OS, its secret vault, or desktop installers.

This replaces the previous Vitverk-hosted endpoint. The alpha.1 package and its release
ZIP still reference that endpoint; update the package and create a new connection.
Previous OAuth grants are not migrated, and no compatibility redirect is promised.

Portable `mcp.json` declares the OAuth resource and read/write scopes. The Codex
`.mcp.json` overlay supplies the same HTTP endpoint and relies on host/server discovery.
Its exact scope negotiation is unverified; do not assume it grants writes. Hosts must
honor the scope actually returned by OAuth and the service's capability response.

Before announcing the plugin as usable, complete the Eirberg service's staging runbook:
deploy the independent merchant Worker, bind the reviewed UI artifact, configure required
media origins, and verify OAuth, revocation and native staff permissions. Existing Medusa
staff accounts must be used; the connection cannot provision users or assign roles. Native
MFA must work through a supported flow; an interactive-sign-in refusal must not be bypassed.

Then verify a real supported host connection, read-only access, a reviewed synthetic change
in staging, its receipt, and unavailable actions. Update this status
and the listing copy only after those checks pass. A valid ZIP or successful GitHub import
alone does not establish that the service works.

Publishing to the universal public Plugins Directory is separate from publishing this
repository. That would require the applicable OpenAI review, verified listing details,
privacy/terms pages and reviewer access; none is claimed by this release.
