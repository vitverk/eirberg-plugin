---
name: setup
description: Connect Eirberg Store Admin, check staff access and open the admin workspace after installation.
---

Help the user connect the installed Eirberg Store Admin plugin.

1. Inspect the available Eirberg tools. This alpha package targets `https://mcp.eirberg.app/mcp` and does not prove the merchant service is active. If the connection or discovery is unavailable, report that activation has not been verified; do not request passwords or suggest an unrelated MCP endpoint.
2. If authentication is required, direct the user to the host's connection flow for the packaged Eirberg server. They sign in with their existing Medusa staging staff account and choose whether to permit changes. Vitverk OS and desktop installers are not prerequisites. An installation using the previous endpoint must update and reconnect. Never handle tokens, passwords, API keys or MFA codes in chat.
3. Once tools are available, call `eirberg_get_capabilities`. Describe the permissions actually returned, including a read-only connection. Do not provision staff or change roles.
4. Call `eirberg_open_admin` to open the workspace. If the current host cannot show it, explain the surface limitation and use available read tools.
5. Verify setup with a bounded read that the user can access. Do not publish, save, upload or alter a record to test the connection.

Use the existing account's native permissions. An MFA refusal requires a supported sign-in flow; never disable or bypass MFA. Installation does not grant access to the store. If tools do not appear after connection, ask the user to start a new chat with this plugin selected.
