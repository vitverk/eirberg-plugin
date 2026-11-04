<img src="plugins/eirberg-admin/assets/icon.png" width="96" height="96" alt="Eirberg" />

# Eirberg Store Admin

Installation package for Eirberg's staff admin plugin in ChatGPT and Codex, maintained by Vitverk.

**Preview — service activation pending.** This package targets Eirberg's independent
MCP service at `https://mcp.eirberg.app/mcp`. The service is being prepared for Medusa
staging; deployment, live staff access and end-to-end ChatGPT installation remain
unverified. Package validation does not establish that the service is available.

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

Members install it from their workspace's Plugins tab. Authentication will remain
unavailable until the service is activated. MCP plugins imported from GitHub may be
marked **Desktop only**; the import result determines the supported surfaces.
See OpenAI's [GitHub import guide](https://learn.chatgpt.com/docs/enterprise/plugin-management).

## Install in Codex

Register the marketplace:

```sh
codex plugin marketplace add vitverk/eirberg-plugin
codex plugin add eirberg-admin@vitverk-eirberg
```

Alternatively, use `/plugins` to install **Eirberg Store Admin** from **Eirberg by Vitverk**.
Start a new chat after connection. Use `main` for this endpoint change until a new
release is published.

See the [plugin packaging guide](https://developers.openai.com/plugins/build/plugins).
This repository is a distribution source, not a universal Plugins Directory listing.

The earlier [alpha.1 release](https://github.com/vitverk/eirberg-plugin/releases/tag/v0.1.0-alpha.1)
uses the retired Vitverk-hosted endpoint. It does not contain this change. Build the
current standalone plugin ZIP with the command below; the repository's source ZIP
includes the marketplace and is not the same as the standalone plugin archive.

## Connect when the service is activated

The package configures `https://mcp.eirberg.app/mcp` with OAuth discovery and dynamic
client registration. Sign in through the Eirberg connection flow with your existing
Medusa staging staff account. The connection requests read access and offers write
access; explicit consent and current Medusa permissions determine what you can do.
The hosted service lives in [`vitverk/eirberg`](https://github.com/vitverk/eirberg).
It does not require Vitverk OS, its vault, or desktop-installer provisioning.

Existing installations must update the package and connect to the new server.
The previous endpoint and its OAuth grants are not carried forward.
No password, client secret, API key or manually copied token belongs in this repository.

Run the packaged setup workflow, then try:

- “Open the Eirberg admin workspace.”
- “Show my Eirberg news drafts.”
- “Help me review changes to the Eirberg homepage banners.”

## Package contents

- `plugins/eirberg-admin/plugin.json`: portable Agent Plugins 1.0 manifest and listing.
- `plugins/eirberg-admin/mcp.json`: OAuth-enabled merchant MCP connection.
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

See [activation status](docs/activation.md) and [support](SUPPORT.md).
