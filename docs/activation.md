# Activation status

This is an alpha installation package. It does not deploy or activate any service.

| Item | Status on 2026-11-03 |
| --- | --- |
| Canonical merchant endpoint | `https://vinnslan.eirberg.app/mcp/eirberg`, confirmed from Eirberg instance configuration and merchant route source |
| Unauthenticated endpoint probe | HTTP 404 |
| Protected resource metadata | `/.well-known/oauth-protected-resource/mcp/eirberg`, HTTP 404 |
| Authorization server metadata | `/.well-known/oauth-authorization-server`, HTTP 404 |
| OAuth design | Public client, PKCE S256, dynamic registration; separate merchant resource and consent |
| Read scope | `merchant:read` |
| Optional write scope | `merchant:write`, subject to explicit consent and native permissions |
| Live staff / ChatGPT acceptance | Pending |

The endpoint is source-confirmed, not operationally verified. Do not replace it with a
general Vitverk MCP endpoint: that is a different tool surface and authorization resource.

Portable `mcp.json` declares the OAuth resource and read/write scopes. The legacy
`.mcp.json` fallback supplies the HTTP endpoint and relies on host/server discovery.
Its exact scope negotiation is unverified; do not assume it grants writes. Hosts must
honor the scope actually returned by OAuth and the service's capability response.

Before announcing the plugin as usable, the service owner must complete an independently
authorized activation: deploy the merchant integration, bind the reviewed UI artifact,
restrict the allowed Eirberg accounts, configure required media origins, and verify OAuth,
revocation and native staff permissions. Native MFA must work through a supported flow;
an interactive-sign-in refusal must not be bypassed.

Then verify a real supported host connection, read-only access, a reviewed synthetic change
in an authorized test environment, its receipt, and unavailable actions. Update this status
and the listing copy only after those checks pass. A valid ZIP or successful GitHub import
alone does not establish that the service works.

Publishing to the universal public Plugins Directory is separate from publishing this
repository. That would require the applicable OpenAI review, verified listing details,
privacy/terms pages and reviewer access; none is claimed by this release.
