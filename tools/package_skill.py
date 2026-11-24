"""Build the release ZIPs for UIUX Abhishek DevKit.

Standard library only. Run from anywhere:
    python3 tools/package_skill.py [out_dir] [--update-marketplace]

Two ZIPs, both deterministic (sorted entries, fixed timestamps and permissions):

- uiuxabhishek-devkit-v<version>.zip: the Claude.ai / Claude Desktop Chat upload
  (Customize > Skills). One root folder, uiuxabhishek-devkit/, with the skill only:
  no agents. Claude's upload form limits the description to 200 characters, so the
  packaged SKILL.md swaps its description for UPLOAD_DESCRIPTION.
- uiuxabhishek-devkit-plugin-v<version>.zip: the Claude Code plugin, with exactly
  .claude-plugin/plugin.json, agents/ and skills/uiuxabhishek-devkit/ at its top level.
  .claude-plugin/marketplace.json installs it from the GitHub release; with
  --update-marketplace this script writes the release URL and SHA-256 into it.

Both leave out the "Never load" files listed in SKILL.md (they need upstream
Impeccable tooling that isn't bundled); the repository keeps them. Every other file
is copied byte for byte. Maintainer files (CLAUDE.md, .claude/, tests/, tools/,
docs) are never packaged. The optional updater (tools/updater/devkit-update.mjs)
is copied beside the ZIPs as a separate release asset with its own checksum.
"""
import hashlib
import json
import os
import re
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "uiuxabhishek-devkit")
AGENTS = os.path.join(ROOT, "agents")
PLUGIN_MANIFEST = os.path.join(ROOT, ".claude-plugin", "plugin.json")
MARKETPLACE = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
NAME = "uiuxabhishek-devkit"
REPO = "abhishekinvission/uiuxabhishek-devkit"
UPLOAD_DESCRIPTION = ("UIUX Abhishek DevKit router for UI/UX design, accessibility, motion, frontend, "
                      "Figma to code, security, tests, Git, PRs and ticket-to-PR delivery. Loads only "
                      "what a task needs.")
UPLOAD_DESCRIPTION_MAX = 200
UPDATER = os.path.join(ROOT, "tools", "updater", "devkit-update.mjs")
SKIP = {".DS_Store", "Thumbs.db"}
STAMP = (2026, 1, 1, 0, 0, 0)


def version():
    with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as f:
        m = re.search(r"^  version: \"?(\d+\.\d+\.\d+)\"?$", f.read(), re.M)
    if not m:
        sys.exit("SKILL.md metadata.version is missing")
    return m.group(1)


def never_load():
    """Skill-relative paths (or folder prefixes ending in /) from SKILL.md's Never load line."""
    with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as f:
        m = re.search(r"\*\*Never load\*\*[^:]*:(.*)", f.read())
    if not m:
        sys.exit("SKILL.md has no Never load line")
    return {"references/impeccable/reference/" + n.rstrip("*") for n in re.findall(r"`([\w/.*-]+)`", m.group(1))}


def omitted(rel, excluded):
    return any(rel == n or (n.endswith("/") and rel.startswith(n)) for n in excluded)


def upload_skill_md():
    with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as f:
        text = f.read()
    new, n = re.subn(r"^description: .*$", "description: " + UPLOAD_DESCRIPTION, text, count=1, flags=re.M)
    if n != 1 or len(UPLOAD_DESCRIPTION) > UPLOAD_DESCRIPTION_MAX or re.search(r":\s|\s#", UPLOAD_DESCRIPTION):
        sys.exit("cannot set upload description")
    return new.encode("utf-8")


def walk(base):
    for root, dirs, names in os.walk(base):
        dirs.sort()
        for n in sorted(names):
            if n not in SKIP:
                p = os.path.join(root, n)
                if os.path.islink(p):
                    sys.exit(f"refusing symlink {p}")
                yield p, os.path.relpath(p, base).replace(os.sep, "/")


def files():
    """Skill files that ship: (source path, skill-relative path)."""
    excluded = never_load()
    return [(p, r) for p, r in walk(SKILL) if not omitted(r, excluded)]


def plugin_files():
    """Plugin files that ship: (source path, plugin-relative path)."""
    out = [(PLUGIN_MANIFEST, ".claude-plugin/plugin.json")]
    out += [(p, "agents/" + r) for p, r in walk(AGENTS) if r.endswith(".md")]
    out += [(p, f"skills/{NAME}/{r}") for p, r in files()]
    return out


def write_zip(path, entries):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for arcname, data in entries:
            info = zipfile.ZipInfo(arcname, STAMP)
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    write_checksum(path)
    return sha256(path)


def read_bytes(p):
    with open(p, "rb") as f:
        return f.read()


def build(out_dir):
    """Build the Chat upload ZIP and copy the updater. Returns (zip path, sha256)."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{NAME}-v{version()}.zip")
    digest = write_zip(path, [(f"{NAME}/{r}", upload_skill_md() if r == "SKILL.md" else read_bytes(p))
                              for p, r in files()])
    updater = os.path.join(out_dir, os.path.basename(UPDATER))
    with open(updater, "wb") as dst:
        dst.write(read_bytes(UPDATER))
    write_checksum(updater)
    return path, digest


def build_plugin(out_dir):
    """Build the Claude Code plugin ZIP. Returns (zip path, sha256)."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, plugin_zip_name())
    return path, write_zip(path, [(r, read_bytes(p)) for p, r in plugin_files()])


def plugin_zip_name(ver=None):
    return f"{NAME}-plugin-v{ver or version()}.zip"


def plugin_release_url(ver=None):
    ver = ver or version()
    return f"https://github.com/{REPO}/releases/download/v{ver}/{plugin_zip_name(ver)}"


def update_marketplace(digest):
    with open(MARKETPLACE, encoding="utf-8") as f:
        data = json.load(f)
    entry = next(p for p in data["plugins"] if p["name"] == NAME)
    entry["source"] = {"source": "archive", "url": plugin_release_url(), "sha256": digest}
    with open(MARKETPLACE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def sha256(path):
    return hashlib.sha256(read_bytes(path)).hexdigest()


def write_checksum(path):
    with open(path + ".sha256", "w", encoding="utf-8") as f:
        f.write(f"{sha256(path)}  {os.path.basename(path)}\n")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out_dir = args[0] if args else os.path.join(ROOT, "dist")
    skill_zip, skill_digest = build(out_dir)
    plugin_zip, plugin_digest = build_plugin(out_dir)
    print(f"{skill_zip}\nsha256 {skill_digest}\n{plugin_zip}\nsha256 {plugin_digest}")
    if "--update-marketplace" in sys.argv:
        update_marketplace(plugin_digest)
        print(f"marketplace.json now installs {plugin_release_url()}")
