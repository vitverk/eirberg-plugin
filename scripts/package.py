#!/usr/bin/env python3
"""Validate the public distribution package and build a reproducible plugin ZIP."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins/eirberg-admin"
ENDPOINT = "https://mcp.eirberg.app/mcp"
FILES = {
    "plugin.json", "mcp.json", ".codex-plugin/plugin.json", ".mcp.json",
    "skills/setup/SKILL.md", "skills/manage-eirberg/SKILL.md",
    "assets/icon.png", "assets/icon.svg", "assets/README.md",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)


def contained(path):
    require(isinstance(path, str) and path.startswith("./"), "Package paths must start with ./")
    target = (PLUGIN / path).resolve()
    require(target.is_relative_to(PLUGIN.resolve()) and target.is_file(), f"Missing or escaping file: {path}")
    return target


def validate():
    paths = list(PLUGIN.rglob("*"))
    require(not any(path.is_symlink() for path in paths), "Symlinks are not package files")
    actual = {str(path.relative_to(PLUGIN)) for path in paths if path.is_file()}
    require(actual == FILES, f"Unexpected or missing plugin files: {actual ^ FILES}")
    for path in paths:
        if path.is_file():
            require(path.stat().st_size <= 5 * 1024 * 1024, f"Oversized package file: {path.name}")

    manifest = read_json(PLUGIN / "plugin.json")
    require(manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", "Wrong portable schema")
    require(manifest["name"] == PLUGIN.name, "Plugin identity differs from folder")
    require(re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", manifest["version"]), "Invalid package version")
    require(not {"skills", "apps", "interface", "mcpServers"} & manifest.keys(), "Legacy fields in portable manifest")
    extension = manifest["extensions"]["com.openai"]
    require("apps" not in extension and "hooks" not in extension, "Unexpected app binding or hook")
    contained(extension["onboardingSkill"])
    interface = extension["interface"]
    require(0 < len(interface["shortDescription"]) <= 30, "Subtitle exceeds 30 characters")
    require(0 < len(interface["displayName"]) <= 30, "Display name exceeds 30 characters")
    require(interface["category"] == "Business & Operations", "Unexpected listing category")
    require(len(interface["defaultPrompt"]) <= 3, "Too many default prompts")
    require(all(0 < len(prompt) <= 128 and "\n" not in prompt for prompt in interface["defaultPrompt"]), "Invalid default prompt")
    for field in ("logo", "composerIcon"):
        data = contained(interface[field]).read_bytes()
        require(data[:8] == b"\x89PNG\r\n\x1a\n", "Listing icon is not PNG")
        width, height = struct.unpack(">II", data[16:24])
        require(256 <= width <= 4096 and width == height, "Listing icon must be square, 256–4096px")

    compatibility = read_json(PLUGIN / ".codex-plugin/plugin.json")
    for key, value in manifest.items():
        if key not in ("$schema", "extensions"):
            require(compatibility.get(key) == value, f"Compatibility drift: {key}")
    require(compatibility["interface"] == interface, "Compatibility listing drift")
    require(compatibility["skills"] == "./skills/" and compatibility["mcpServers"] == "./.mcp.json", "Compatibility component paths differ")
    require(compatibility["extensions"]["com.openai"]["onboardingSkill"] == extension["onboardingSkill"], "Compatibility onboarding drift")

    mcp = read_json(PLUGIN / "mcp.json")
    require(mcp["$schema"] == "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json", "Wrong MCP schema")
    require(set(mcp["mcpServers"]) == {"eirberg"}, "Unexpected bundled server")
    server = mcp["mcpServers"]["eirberg"]
    require(server == {"type": "streamable-http", "url": ENDPOINT},
            "Expected the discovery-based merchant endpoint only; headers, credentials and extra server fields are not packaged")
    require(read_json(PLUGIN / ".mcp.json") == {"mcpServers": {"eirberg": {"type": "http", "url": ENDPOINT}}}, "Legacy MCP endpoint drift")

    marketplace = read_json(ROOT / ".agents/plugins/marketplace.json")
    require(marketplace["name"] == "vitverk-eirberg", "Marketplace identity drift")
    require(len(marketplace["plugins"]) == 1, "Expected one marketplace entry")
    entry = marketplace["plugins"][0]
    require(entry["name"] == manifest["name"], "Marketplace plugin identity drift")
    require(entry["source"] == {"source": "local", "path": "./plugins/eirberg-admin"}, "Wrong marketplace-relative path")
    require(entry["category"] == interface["category"], "Marketplace category drift")
    require(entry["policy"] == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, "Unexpected installation policy")

    for name in ("setup", "manage-eirberg"):
        source = (PLUGIN / f"skills/{name}/SKILL.md").read_text(encoding="utf-8")
        require(source.startswith(f"---\nname: {name}\ndescription: "), f"Invalid skill metadata: {name}")
        require("\n---\n" in source[4:], f"Missing frontmatter boundary: {name}")
    print(f"Validated {manifest['name']} {manifest['version']}: {len(FILES)} files; icon 512px; no credentials packaged")
    return manifest


def package(manifest):
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    archive = output / f"{manifest['name']}-{manifest['version']}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for name in sorted(FILES):
            entry = zipfile.ZipInfo(f"{manifest['name']}/{name}", date_time=(2020, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            bundle.writestr(entry, (PLUGIN / name).read_bytes())
    with zipfile.ZipFile(archive) as bundle:
        require(bundle.testzip() is None, "ZIP integrity failure")
        require(set(bundle.namelist()) == {f"{manifest['name']}/{name}" for name in FILES}, "ZIP inventory differs")
        require(json.loads(bundle.read(f"{manifest['name']}/plugin.json")) == manifest, "ZIP manifest differs")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(".zip.sha256").write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    print(f"Packaged {archive.name}: {archive.stat().st_size} bytes; SHA-256 {digest}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate without writing an archive")
    args = parser.parse_args()
    try:
        manifest = validate()
        if not args.check:
            package(manifest)
    except (ValueError, KeyError, OSError) as error:
        print(f"Package validation failed: {error}", file=sys.stderr)
        sys.exit(1)
