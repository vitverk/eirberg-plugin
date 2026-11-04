<img src="plugins/eirberg-admin/assets/icon.png" width="96" height="96" alt="Eirberg" />

# Eirberg Store Admin

Installation package for Eirberg's staff admin plugin in ChatGPT and Codex, maintained by Vitverk.

**Staging test release.** Eirberg's independent MCP service is deployed at
`https://mcp.eirberg.app/mcp`, with the shared admin UI and Medusa staging backend.
Public connection checks pass. Each staff member must still connect their account;
native permissions and authenticated ChatGPT rendering are verified after connection.

The initial integration covers news and homepage banners: drafts, previews, reviewed
publication and operation receipts. Access is restricted to authorized Eirberg staff.
Installing the public package does not grant access to the store.

## Install in a ChatGPT workspace

Workspace admins can import this repository:

1. Open **Admin → Plugins → Add → Import marketplace**.
2. Enter `https://github.com/vitverk/eirberg-plugin` as Source.
3. Leave Path empty. Use `main` for updates, or pin a release tag.
4. Import, review the result and make **Eirberg Store Admin** available to the intended staff.

Set installation and authentication policies in the workspace UI; GitHub import does not
apply the repository's local marketplace policies.

Members install it from their workspace's Plugins tab, then complete the Eirberg
OAuth connection offered by their host. MCP plugins imported from GitHub may be
marked **Desktop only**; the import result determines the supported surfaces.
See OpenAI's [GitHub import guide](https://learn.chatgpt.com/docs/enterprise/plugin-management).

## Install in Codex

Register the marketplace:

```sh
codex plugin marketplace add vitverk/eirberg-plugin
codex plugin add eirberg-admin@vitverk-eirberg
```

Alternatively, use `/plugins` to install **Eirberg Store Admin** from **Eirberg by Vitverk**.
Start a new chat after connection. Use `main` for updates, or select a version from
the [releases](https://github.com/vitverk/eirberg-plugin/releases).

See the [plugin packaging guide](https://developers.openai.com/plugins/build/plugins).
This repository is a distribution source, not a universal Plugins Directory listing.

The earlier [alpha.1 release](https://github.com/vitverk/eirberg-plugin/releases/tag/v0.1.0-alpha.1)
uses the retired Vitverk-hosted endpoint. Alpha.2 and later use the independent
Eirberg service. Releases provide a standalone plugin ZIP and checksum; the repository's
source ZIP includes the marketplace and is not the same as the standalone plugin archive.
The package command below also builds the current standalone ZIP.
Alpha.4 corrects bundled-server discovery in Codex 0.166.0-alpha.6; update if an
older package exposes the setup skill but no Eirberg MCP connection.

## Connect your staff account

The package configures `https://mcp.eirberg.app/mcp` with OAuth discovery and dynamic
client registration. Sign in through the Eirberg connection flow with your existing
Medusa staging staff account's native email/password login. A Vitverk-only SSO session
is not reused, and this plugin does not provision passwords or staff accounts.
OAuth discovery requests read-only access by default, which is sufficient for setup.
Editing requires the host's OAuth scope configuration to request `merchant:write`
alongside `merchant:read`, followed by explicit write consent and current Medusa permission.
The hosted service lives in [`vitverk/eirberg`](https://github.com/vitverk/eirberg).
It does not require Vitverk OS, its vault, or desktop-installer provisioning.

Installations that still use the retired endpoint must update the package and connect
to the new server. The previous endpoint and its OAuth grants are not carried forward.
No password, client secret, API key or manually copied token belongs in this repository.

Package installation, an authenticated connection, and store permissions are separate
steps. If the Eirberg tools are missing, inspect the host's connection status and error.
Missing tools alone do not mean staging is inactive or that Medusa denied your account.
After the host confirms connection, start a new chat with Eirberg selected if necessary.
The setup workflow checks actual permissions with `eirberg_get_capabilities` before
opening the workspace and making a permitted read.

Run the packaged setup workflow, then try:

- “Open the Eirberg admin workspace.”
- “Show my Eirberg news drafts.”
- “Help me review changes to the Eirberg homepage banners.”

## Package contents

- `plugins/eirberg-admin/plugin.json`: portable Agent Plugins 1.0 manifest and listing.
- `plugins/eirberg-admin/mcp.json`: merchant endpoint; authentication uses OAuth discovery.
- `plugins/eirberg-admin/.codex-plugin/plugin.json` and `.mcp.json`: compatibility files.
- `plugins/eirberg-admin/skills/`: setup and merchant workflow instructions.
- `plugins/eirberg-admin/assets/`: existing Eirberg brand icon.
- `.agents/plugins/marketplace.json`: repository import and discovery.
- `scripts/`: validation and reproducible ZIP packaging using Python's standard library.

The UI remains in the Eirberg application repository and imports components and styling
from `@eirberg/ui`. This distribution package does not fork the storefront's components
or publish backend source, credentials or store data.

## Maintain the package

```sh
python3 scripts/package.py --check
python3 scripts/package.py
```

The second command creates a versioned ZIP and SHA-256 file in `dist/`. The ZIP contains
one plugin; the repository marketplace is kept outside it. CI runs the same validation.
Update both compatibility files when changing the portable manifests; validation catches drift.

With Codex installed, also run `python3 scripts/check-codex.py`. This checks the
package with the actual host loader and requires it to discover the bundled
`eirberg` server. It does not install anything, sign in or access store data.

See [activation status](docs/activation.md) and [support](SUPPORT.md).
