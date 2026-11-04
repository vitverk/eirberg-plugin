# Activation status

The independent service and shared UI are deployed for staging tests. This alpha
installation package connects a supported host to that service; staff authentication
and permissions are verified separately for each connection.

| Item | Status on 2026-11-04 |
| --- | --- |
| Canonical merchant endpoint | `https://mcp.eirberg.app/mcp`, deployed and responding |
| Service source | [`vitverk/eirberg`](https://github.com/vitverk/eirberg), `apps/merchant-mcp` |
| Backend target | Medusa staging only; production access is not enabled by this package |
| Protected resource metadata | `https://mcp.eirberg.app/.well-known/oauth-protected-resource/mcp`, verified HTTP 200 |
| Authorization server metadata | `https://mcp.eirberg.app/.well-known/oauth-authorization-server`, verified HTTP 200 |
| Anonymous MCP requests | Verified HTTP 401 with OAuth discovery challenge |
| Shared UI artifact | Published, downloaded and hash-verified |
| OAuth contract | Public client, PKCE S256, dynamic registration; resource audience is the exact MCP endpoint |
| Read scope | `merchant:read` |
| Optional write scope | `merchant:write`, requires an explicit host scope request, consent and native Medusa permission |
| Codex 0.166.0-alpha.6 package discovery | URL-only configuration exposes the bundled `eirberg` server |
| Live staff / ChatGPT acceptance | Pending authenticated host verification; deployment is complete |

The [staging deployment](https://github.com/vitverk/eirberg/actions/runs/41835218369)
completed for `2a7a1a56c80d9d7625f1c230bf0f90c9a48cbd94`. Seven public smoke checks
passed against that backend revision. These checks establish deployment and discovery,
not a particular staff member's connection or permissions.

Staff authenticate against Medusa through the Eirberg connection flow using their
existing native email/password login. Vitverk-only SSO sessions are not reused, and
passwords are not automatically provisioned. Medusa remains
the authority for users, roles, record access, merchant mutations and operation receipts.
The service does not depend on Vitverk OS, its secret vault, or desktop installers.

This replaces the previous Vitverk-hosted endpoint. The alpha.1 package and its release
ZIP still reference that endpoint; update the package and create a new connection.
Previous OAuth grants are not migrated, and no compatibility redirect is promised.

Portable `mcp.json` and the legacy Codex `.mcp.json` compatibility configuration supply
the same HTTP endpoint. OAuth requirements, resource audience and dynamic registration
are discovered through the server's 401 challenge and metadata. The server still
requires a valid staff grant for every merchant request.

Codex 0.166.0-alpha.6 rejects per-server `extensions` in portable `mcp.json`, leaving
the installed plugin with no bundled MCP server. Alpha.4 uses the documented URL-only
configuration, which was verified to expose `eirberg` through the installed host's
plugin reader. A compatibility overlay cannot override portable MCP discovery.
This verifies local package loading, not authenticated ChatGPT import or execution.
The repeatable check is `python3 scripts/check-codex.py`: the alpha.2 marketplace
snapshot returned no servers, while alpha.4 returns `eirberg`.

The server's discovery challenge requests `merchant:read`, so the default connection
is read-only. Editing requires the host's OAuth scope configuration to explicitly request
both `merchant:read` and `merchant:write`, followed by write consent and native Medusa
permission. Honor the scopes actually returned by OAuth and the capability response;
do not infer write access from the package's capabilities label.

Remaining acceptance uses a real supported host connection to verify staff OAuth/MFA,
native permissions and revocation, resource rendering, read-only access, and a reviewed
synthetic change with receipt recovery in staging. Existing Medusa staff accounts must
be used; the connection cannot provision users or assign roles. Native MFA must work
through a supported flow; an interactive-sign-in refusal must not be bypassed.

When tools are unavailable, first distinguish package installation, OAuth connection,
and native authorization. Record the observed host connection error rather than treating
missing tools as evidence that deployment is pending. Mark authenticated acceptance
complete only after the joined host journey passes.

Publishing to the universal public Plugins Directory is separate from publishing this
repository. That would require the applicable OpenAI review, verified listing details,
privacy/terms pages and reviewer access; none is claimed by this release.
