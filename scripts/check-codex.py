#!/usr/bin/env python3
"""Check bundled MCP discovery with the installed Codex host, without signing in."""

import argparse
import json
from pathlib import Path
import queue
import subprocess
import threading

ROOT = Path(__file__).resolve().parent.parent


def check(marketplace):
    process = subprocess.Popen(
        ["codex", "app-server", "--stdio"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        text=True, bufsize=1,
    )
    messages = queue.Queue()

    def receive():
        for line in process.stdout:
            messages.put(json.loads(line))
        messages.put(None)

    threading.Thread(target=receive, daemon=True).start()

    def send(message):
        process.stdin.write(json.dumps(message) + "\n")
        process.stdin.flush()

    def request(identifier, method, params):
        send({"id": identifier, "method": method, "params": params})
        while True:
            response = messages.get(timeout=30)
            if response is None:
                raise RuntimeError("Codex closed before completing plugin discovery")
            if response.get("id") == identifier:
                if "error" in response:
                    raise RuntimeError("Codex rejected " + method)
                return response["result"]

    try:
        request(1, "initialize", {
            "clientInfo": {"name": "eirberg_package_check", "version": "1"},
            "capabilities": {"experimentalApi": True, "explicitGatewayOauth": True},
        })
        send({"method": "initialized"})
        plugin = request(2, "plugin/read", {
            "marketplacePath": str(marketplace.resolve()), "pluginName": "eirberg-admin",
        })["plugin"]
        servers = plugin["mcpServers"]
        if servers != ["eirberg"]:
            raise RuntimeError(f"Expected the Eirberg MCP server; Codex discovered {servers!r}")
        return {"passed": True, "mcp_servers": servers, "authentication_tested": False}
    finally:
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--marketplace", type=Path, default=ROOT / ".agents/plugins/marketplace.json")
    arguments = parser.parse_args()
    print(json.dumps(check(arguments.marketplace)))
