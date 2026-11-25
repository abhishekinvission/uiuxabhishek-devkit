"""Repository validation for the Craftline skill (craftline) and its Claude Code plugin.

Standard library only. Run from anywhere:  python3 tests/validate.py [--cli]

Checks: single-skill discovery and frontmatter, Markdown links, SOURCES.md
checksums and inventory (skill and agents), license/notice mirrors, router
parsing and reference coverage, script-calling files routed with the Impeccable
adapter, routing scenarios with their expected agent plan, the plugin agents
(frontmatter, one agent per capability, read-only tools, no guidance copies),
context budget, a basic secret/executable scan, README install commands, both
release ZIPs and the plugin and marketplace manifests (built to a temporary
folder), the Git workflow commands against throwaway repositories with a mock
remote (tests/git_sandbox.py), the optional updater against a mock GitHub API
and mock Skills CLI (tests/updater_sandbox.py), and leftover references to the
pre-2.0 skill ID. --cli also runs `npx skills add . --list`, a real global
install for every documented agent into a throwaway HOME, and a migration from
the old skill ID.

Routing scenarios use a deterministic keyword simulation of SKILL.md's
signal tables. It checks that the router's signals, conditions and file
mappings are coherent; it is a proxy for, not a replacement of, an agent's
semantic judgment.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, "plugin")  # the Claude Code plugin; marketplace.json points at ./plugin
SKILL_ID = "craftline"
SKILL = os.path.join(PLUGIN, "skills", SKILL_ID)
AGENT_DIR = os.path.join(PLUGIN, "agents")
THIRD_PARTY = ("references/impeccable/", "references/apple-design/")
BASELINE_COMMIT = "036b394"  # last commit before the router rewrite
FRONTMATTER_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
REPO = "abhishekinvission/uiuxabhishek-devkit"
OLD_ID = "uiuxabhishek-design"  # skill ID before v2.0.0
OLD_ID_COMMIT = "82f5367"  # last commit that shipped it
RENAMED_ID = "uiuxabhishek-devkit"  # skill ID from v2.0.0 to v2.1.1
RENAMED_ID_COMMIT = "3a2eedc"  # v2.1.1, the last release that shipped it
FORMER_NAMES = (OLD_ID, RENAMED_ID, "UIUX Abhishek Design", "UIUX Abhishek DevKit")
# Where former names may appear anywhere: history, tests and the updater's migration code. In other
# docs they may appear only in migration/history sections or on a line that says "formerly".
FORMER_ALLOWED = ("CHANGELOG.md", "tests/", "tools/updater/", "plugin/skills/craftline/references/impeccable/",
                  "plugin/skills/craftline/references/apple-design/")
# Exact strings that contain a former ID but aren't one: the repository slug, which keeps its name,
# and the updater's folder and scheduler names, kept so existing schedules are found.
NOT_FORMER = (f"abhishekinvission/{RENAMED_ID}", f".{RENAMED_ID}", f"{RENAMED_ID}-update")
# Skills CLI tools. Claude Code gets Craftline from the plugin, so the docs never install it there with npx.
AGENTS = ("codex", "gemini-cli", "github-copilot", "antigravity")
SKILLS_CLI = "skills@1.7.6"  # the version INSTALL.md documents and the updater pins; newer CLIs change install paths
SKILLS_CLI_LATEST = "skills@1.9.0"  # discovery must also work with the newest CLI checked
UPLOAD_MAX_BYTES = 8 * 1024 * 1024  # Claude API skill upload limit
SKILL_MD_MAX_CHARS = 12000
MAX_CONTEXT_GROWTH = 13  # percent over the pre-router baseline, averaged over all scenarios (raised from 10 in 3.1.0 for the stack-independent craftforce route)
GUIDE_MAX_CHARS = 5000
UI_WORDS = {"ui", "page", "screen", "dashboard", "component", "frontend", "design", "interface", "view"}

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
    return cond


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def rel(path, base=SKILL):
    return os.path.relpath(path, base).replace(os.sep, "/")


def md_files(base=ROOT):
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in files:
            if f.lower().endswith(".md"):
                yield os.path.join(root, f)


# ---------------------------------------------------------------- discovery
def check_discovery():
    found = [p for p in md_files() if os.path.basename(p).lower() == "skill.md"]
    check([rel(p, ROOT) for p in found] == [f"plugin/skills/{SKILL_ID}/SKILL.md"],
          f"expected exactly one SKILL.md, found {[rel(p, ROOT) for p in found]}")
    text = read(os.path.join(SKILL, "SKILL.md"))
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not check(m, "SKILL.md has no frontmatter"):
        return
    top = dict(re.findall(r"^([a-z-]+):\s*(.*)$", m.group(1), re.M))
    check(set(top) <= FRONTMATTER_KEYS, f"unexpected frontmatter keys {set(top) - FRONTMATTER_KEYS}")
    check(top.get("name") == SKILL_ID, f"frontmatter name must be {SKILL_ID}")
    desc = top.get("description", "")
    check(0 < len(desc) <= 1024, f"description length {len(desc)} not in 1..1024")
    for k in ("name", "description"):
        check(not re.search(r":\s|\s#", top.get(k, "")), f"frontmatter {k} needs YAML quoting")
    print(f"discovery: 1 skill, description {len(desc)} chars")


def check_cli():
    for cli_version in (SKILLS_CLI, SKILLS_CLI_LATEST):
        try:
            out = subprocess.run(["npx", "--yes", cli_version, "add", ".", "--list"], cwd=ROOT,
                                 capture_output=True, text=True, timeout=180).stdout
        except (OSError, subprocess.TimeoutExpired) as e:
            check(False, f"skills CLI unavailable: {e}")
            return
        names = re.findall(r"^│ {4}([a-z0-9-]+)\s*$", out, re.M)
        check(names == [SKILL_ID], f"{cli_version} discovered {names}")
        print(f"skills CLI: {cli_version} discovers {names}")
    with tempfile.TemporaryDirectory() as home:
        env = dict(os.environ, HOME=home, DISABLE_TELEMETRY="1", DO_NOT_TRACK="1")
        env.pop("CLAUDE_CONFIG_DIR", None)
        env.pop("CODEX_HOME", None)
        cmd = ["npx", "--yes", SKILLS_CLI, "add", ROOT, "--skill", SKILL_ID, "-g", "-y"]
        for a in AGENTS:
            cmd += ["-a", a]
        try:
            run = subprocess.run(cmd, cwd=home, env=env, capture_output=True, text=True, timeout=300)
        except (OSError, subprocess.TimeoutExpired) as e:
            check(False, f"skills CLI install failed: {e}")
            return
        installed = [rel(os.path.join(r, "SKILL.md"), home) for r, _, fs in os.walk(home, followlinks=True)
                     if "SKILL.md" in fs and os.path.basename(r) == SKILL_ID]
        check(run.returncode == 0 and installed, f"global install for {AGENTS} failed: {run.stderr[-300:]}")
        check(not os.path.lexists(os.path.join(home, ".claude", "skills", SKILL_ID)),
              "the Skills CLI install for the four tools must not add a Claude Code copy")
        print(f"skills CLI: global install for {len(AGENTS)} agents -> {sorted(installed)}")
    check_migration()


def skill_paths(home, name):
    return sorted(rel(os.path.join(r, "SKILL.md"), home) for r, _, fs in os.walk(home, followlinks=True)
                  if "SKILL.md" in fs and os.path.basename(r) == name and "/.npm/" not in r)


def check_migration():
    """Each former ID -> the documented migration to craftline, then update and per-agent install/remove."""
    for old_id, commit in ((OLD_ID, OLD_ID_COMMIT), (RENAMED_ID, RENAMED_ID_COMMIT)):
        with tempfile.TemporaryDirectory() as tmp:
            home, old = os.path.join(tmp, "home"), os.path.join(tmp, "old-source")
            os.makedirs(home)
            os.makedirs(old)
            archive = subprocess.run(["git", "archive", commit], cwd=ROOT, capture_output=True, check=True).stdout
            subprocess.run(["tar", "-x", "-C", old], input=archive, check=True)
            env = dict(os.environ, HOME=home, DISABLE_TELEMETRY="1", DO_NOT_TRACK="1")
            env.pop("CLAUDE_CONFIG_DIR", None)
            env.pop("CODEX_HOME", None)
            agents = [x for a in AGENTS for x in ("-a", a)]

            def cli(*args):
                r = subprocess.run(["npx", "--yes", SKILLS_CLI, *args], cwd=home, env=env,
                                   capture_output=True, text=True, timeout=300)
                return r.returncode
            other = os.path.join(home, ".agents", "skills", "other-skill", "SKILL.md")
            os.makedirs(os.path.dirname(other))
            with open(other, "w") as f:
                f.write("---\nname: other-skill\ndescription: unrelated\n---\n")
            ok = cli("add", old, "--skill", old_id, "-g", *agents, "-y") == 0 and skill_paths(home, old_id)
            check(ok, f"migration: could not install {old_id} in the sandbox")
            ok = cli("remove", old_id, "-g", *agents, "-y") == 0 and cli("add", ROOT, "--skill", SKILL_ID, "-g", *agents, "-y") == 0
            new = skill_paths(home, SKILL_ID)
            check(ok and not skill_paths(home, old_id) and new and os.path.exists(other),
                  f"migration from {old_id}: old {skill_paths(home, old_id)}, new {new}")
            check(cli("update", SKILL_ID, "-g", "-y") == 0, f"migration from {old_id}: update failed")
            check(cli("remove", SKILL_ID, "-g", *agents, "-y") == 0 and not skill_paths(home, SKILL_ID),
                  f"migration from {old_id}: remove failed")
            per_agent = []
            if old_id == RENAMED_ID:
                for a in AGENTS:
                    added = cli("add", ROOT, "--skill", SKILL_ID, "-g", "-a", a, "-y") == 0 and skill_paths(home, SKILL_ID)
                    removed = cli("remove", SKILL_ID, "-g", "-a", a, "-y") == 0
                    per_agent.append(bool(added and removed))
                check(all(per_agent) and not skill_paths(home, SKILL_ID) and os.path.exists(other),
                      f"per-agent install/remove failed: {dict(zip(AGENTS, per_agent))}")
            print(f"skills CLI: migration {old_id} -> {SKILL_ID}, update and remove"
                  + (f", {sum(per_agent)}/{len(AGENTS)} per-agent install/remove" if per_agent else "") + " in a throwaway HOME")


# -------------------------------------------------------------------- links
def check_links():
    count = 0
    for path in md_files():
        for link in re.findall(r"\]\(([^)\s]+)\)", read(path)):
            if re.match(r"^(https?:|mailto:|#|<)", link):
                continue
            count += 1
            target = os.path.join(os.path.dirname(path), link.split("#")[0])
            check(os.path.exists(target), f"broken link {rel(path, ROOT)} -> {link}")
    print(f"links: {count} relative links checked")


# ---------------------------------------------------------------- integrity
def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def check_integrity():
    sources = read(os.path.join(ROOT, "SOURCES.md"))
    third, _, original = sources.partition("## Original project content")
    entries = [(os.path.join(SKILL, "references", p), h)
               for p, h in re.findall(r"^- `(\S+)  ([0-9a-f]{64})`$", third, re.M)]
    entries += [(os.path.join(PLUGIN if p.startswith(("agents/", ".claude-plugin/")) else SKILL, p), h)
                for p, h in re.findall(r"^- `(\S+)  ([0-9a-f]{64})`$", original, re.M)]
    for path, digest in entries:
        if check(os.path.exists(path), f"SOURCES.md lists missing file {rel(path)}"):
            check(sha256(path) == digest, f"checksum mismatch {rel(path)}")
    on_disk = {os.path.join(r, f) for d in ("references", "templates")
               for r, _, fs in os.walk(os.path.join(SKILL, d)) for f in fs}
    on_disk |= {os.path.join(AGENT_DIR, f) for f in os.listdir(AGENT_DIR)}
    on_disk.add(os.path.join(PLUGIN, ".claude-plugin", "icon.png"))
    listed = {p for p, _ in entries}
    check(on_disk == listed, f"inventory drift: unlisted {sorted(rel(p) for p in on_disk - listed)}")
    for name in ("LICENSE", "NOTICE.md"):
        check(read(os.path.join(ROOT, name)) == read(os.path.join(SKILL, name)), f"{name} mirror differs")
    root_lic, skill_lic = os.path.join(ROOT, "LICENSES"), os.path.join(SKILL, "LICENSES")
    check(sorted(os.listdir(root_lic)) == sorted(os.listdir(skill_lic)), "LICENSES file lists differ")
    for f in os.listdir(root_lic):
        check(sha256(os.path.join(root_lic, f)) == sha256(os.path.join(skill_lic, f)), f"LICENSES/{f} differs")
    print(f"integrity: {len(entries)} checksums, mirrors compared")


# ------------------------------------------------------------------- router
def words(text):
    out = set()
    text = re.sub(r"https?://", " ", text.lower())  # a URL scheme is not an HTTP-integration signal
    for tok in re.sub(r"[^a-z0-9.\-'_]+", " ", text).split():
        tok = tok.strip(".-'")
        if len(tok) > 3 and tok.endswith("s"):
            tok = tok[:-1]
        if tok:
            out.add(tok)
            if tok.count(".") >= 2:  # acme.atlassian.net also matches the signal atlassian.net
                out.add(".".join(tok.split(".")[-2:]))
    return out


def matches(signals, prompt_words):
    return any(words(sig) and words(sig) <= prompt_words for sig in signals.split(","))


def parse_router():
    text = read(os.path.join(SKILL, "SKILL.md"))
    modes = {m: sig for m, sig in re.findall(r"^\| `(\w+)` \| ([^|]+) \|", text.split("## 2.")[0], re.M)}
    caps, base = {}, ""
    section = text.split("## 2. Capability map")[1].split("## 3.")[0]
    for line in section.splitlines():
        b = re.search(r"bare names are in `([^`]+)`", line)
        if b:
            base = b.group(1)
        elif line.startswith("**"):
            base = ""
        row = re.match(r"^\| `([\w-]+)` \| (.+) \|$", line)
        if not row:
            continue
        segments = []
        for seg in row.group(2).split(" · "):
            cond = seg.startswith("+")
            sig, _, targets = seg.lstrip("+").partition(" → ")
            files = [p for p in re.findall(r"\]\(([^)]+)\)", targets)]
            files += [base + p for p in re.findall(r"(?<!\()`([\w./-]+\.md)`", targets)]
            if "†" in targets:
                files.append(CLI_ADAPTER)  # † = also load the Impeccable script adapter
            check(files, f"router row {row.group(1)} segment has no files: {seg}")
            for f in files:
                check(os.path.exists(os.path.join(SKILL, f)), f"router target missing: {f}")
            segments.append({"cond": cond, "signals": sig, "files": files, "raw": targets})
        caps[row.group(1)] = segments
    for cap, segs in caps.items():  # "all of `tickets`": the row also loads that capability's whole route
        for seg in list(segs):
            m = re.search(r"all of `([\w-]+)`", seg.get("raw", ""))
            if m and m.group(1) in caps:
                seg["files"] += caps[m.group(1)][0]["files"]
                segs += [dict(x) for x in caps[m.group(1)][1:]]
    never = re.search(r"\*\*Never load\*\*[^:]*:(.*)", text).group(1)
    never = {"references/impeccable/reference/" + n.rstrip("*")
             for n in re.findall(r"`([\w/.*-]+)`", never)}
    craft_floor = re.search(r"\[craft-floor\.md\]\(([^)]+)\)", text).group(1)
    groups = {}
    for name, body in re.findall(r"^\*\*(Design|Engineering)\*\*(.*?)(?=^\*\*|\Z)",
                                 section, re.S | re.M):
        groups[name] = set(re.findall(r"^\| `([\w-]+)` \|", body, re.M))
    return text, modes, caps, never, craft_floor, groups


def is_never(path, never):
    return any(path == n or (n.endswith("/") and path.startswith(n)) for n in never)


CLI_ADAPTER = "references/adapters/impeccable-without-cli.md"
AGENT_PLANS = "references/workflows/agent-plans.md"
SUB_ROUTERS = ("references/craftforce/using-craftforce.md",)  # Craftforce process index (SKILL.md §2)
SHARED_COMPANIONS = ("references/adapters/",  # loaded beside several capabilities' primary files
                     "references/workflows/ticket-delivery.md", "templates/ticket-delivery-report.md")  # tickets + ado


def check_coverage(caps, never):
    routed = {f for segs in caps.values() for s in segs for f in s["files"]}
    expected = set()
    for d in ("references/frontend", "references/workflows", "references/craftforce", "references/adapters", "templates",
              "references/impeccable/reference"):
        for r, _, fs in os.walk(os.path.join(SKILL, d)):
            expected |= {rel(os.path.join(r, f)) for f in fs if f.endswith(".md")}
    expected.add("references/apple-design/SOURCE_SKILL.md")
    expected -= {p for p in expected if is_never(p, never)}
    expected.discard("references/impeccable/reference/craft-floor.md")  # loaded by the shared UI-edit rule
    skill_text = read(os.path.join(SKILL, "SKILL.md"))
    check(f"]({AGENT_PLANS})" in skill_text.split("## 5.")[-1], f"SKILL.md §5 must link {AGENT_PLANS}")
    routed = routed | {AGENT_PLANS}  # loaded from §5 when the head plans agents
    for index in SUB_ROUTERS:  # a routed index whose own table routes, one step at a time, to its playbooks
        if index in routed:
            folder = os.path.dirname(index)
            for link in re.findall(r"\]\(([\w.-]+\.md)\)", read(os.path.join(SKILL, index))):
                routed.add(os.path.normpath(os.path.join(folder, link)))
    plans = read(os.path.join(SKILL, AGENT_PLANS)).lower()
    for phrase in ("end your turn", "approves the plan in a later message", "don't approve the plan", "parallel",
                   "one at a time", "writes last", "absolute paths", "combine duplicates", "agents never start agents"):
        check(phrase in plans, f"{AGENT_PLANS} lacks the dispatch rule {phrase!r}")
    check("stop until the user approves it" in skill_text.lower(), "SKILL.md §5 must stop for plan approval")
    check(not (expected - routed), f"unrouted references: {sorted(expected - routed)}")
    check(not {p for p in routed if is_never(p, never)}, "a never-load file is routed")
    primary = {}
    for cap, segs in caps.items():
        for s in segs:
            if not s["cond"]:
                for f in s["files"]:
                    primary.setdefault(f, set()).add(cap)
    dup = {f: c for f, c in primary.items() if len(c) > 1 and not f.startswith(SHARED_COMPANIONS)}
    check(not dup, f"files routed as primary by several capabilities: {dup}")
    # A routable file that tells the agent to run an unbundled Impeccable script must
    # always load together with the adapter that replaces those steps.
    script_call = re.compile(r"scripts/[\w.-]+\.mjs")
    unadapted = sorted({f"{cap}: {f}" for cap, segs in caps.items() for s in segs for f in s["files"]
                        if script_call.search(read(os.path.join(SKILL, f))) and CLI_ADAPTER not in s["files"]})
    check(not unadapted, f"script-calling files routed without {CLI_ADAPTER}: {unadapted}")
    print(f"coverage: {len(routed)} routed files, {len(never)} never-load entries, no duplicate primaries, "
          f"script steps always adapted")


LIMIT_AUDIT = "read-only, dry run, report only, don't change"
LIMIT_IMPLEMENT = "don't push, no pr, locally"
LIMIT_NO_FETCH = "don't fetch, do not fetch"
LIMIT_OFFLINE = "offline, no network"
ADO_OWNS_GIT = "when either is selected, don't select `git` separately"
BACKEND_RULE = "the backend part of a full-stack or `ado` task"
STRICT_AUDIT = "`audit` and `plan` never fetch or write refs"
# Prompts that name backend work and no UI select no Design or Engineering row (SKILL.md §1 Scope)
TRACKER_WORDS = {"github", "jira", "linear", "linear.app", "atlassian.net"}
BACKEND_WORDS = {"backend", "database", "sql", "migration", "microservice", "postgre", "net"}


def detect_mode(prompt, modes):
    w = words(prompt)
    if matches(LIMIT_AUDIT, w):
        return "audit"
    capped = matches(LIMIT_IMPLEMENT, w)
    order = ["answer", "plan", "deliver", "implement", "audit"]
    found = [m for m in order if matches(modes[m], w)]
    if capped:
        found = [m for m in found if m != "deliver"]
    return found[0] if found else None


def route(prompt, modes, caps, craft_floor, groups):
    w = words(prompt)
    mode = detect_mode(prompt, modes)
    selected, files = [], []
    frontend = (groups["Design"] | groups["Engineering"]) - {"ado"}
    backend_only = bool(w & BACKEND_WORDS) and not (w & UI_WORDS)
    for cap, segs in caps.items():
        hit = [s for s in segs if not s["cond"] and matches(s["signals"], w)]
        if hit and not (backend_only and cap in frontend):
            selected.append(cap)
            files += [f for s in hit for f in s["files"]]
    if "ado" in selected and "tickets" in selected:
        selected.remove("tickets")  # ado wins when both match; keep the lifecycle files ado loads itself
        ado_files = {f for s in caps["ado"] for f in s["files"]}
        files = [f for f in files if f in ado_files or f not in {f for s in caps["tickets"] for f in s["files"]}]
    if {"ado", "tickets"} & set(selected) and "git" in selected:
        selected.remove("git")  # ADO_OWNS_GIT: both load git themselves
        files = [f for f in files if f not in {f for s in caps["git"] for f in s["files"]}]
    if {"ado", "tickets"} & set(selected) and mode is None:
        mode = "audit"  # a bare ticket or work-item ID or URL is a dry run
    mode = mode or "implement"
    for cap in selected:
        for s in caps[cap]:
            if s["cond"]:
                cond = s["signals"]
                mode_cond = {m for m in ("implement", "deliver", "audit", "plan") if m in words(cond)}
                if (mode in mode_cond) if mode_cond else matches(cond, w):
                    files += s["files"]
    design = groups["Design"]
    if mode in ("implement", "deliver") and set(selected) & design:
        files.append(craft_floor)
    if not selected:
        outcome = "guide" if mode == "answer" else ("clarify" if w & UI_WORDS else "skip")
        files = ["GUIDE.md"] if outcome == "guide" else []
    elif "tickets" in selected and not (w & TRACKER_WORDS):
        outcome = "ask-tracker"  # "a ticket" with no tracker named
    else:
        outcome = "route"
    if matches(LIMIT_OFFLINE, w) and not set(selected) & groups["Design"]:
        net = "offline"  # the session is offline: no network call of any kind (an offline UI state is `harden`)
    elif matches(LIMIT_NO_FETCH, w) or mode in ("answer", "audit", "plan"):
        net = "no-fetch"  # network reads allowed, no git fetch/pull and no ref writes
    else:
        net = "fetch"
    return set(selected), mode, outcome, list(dict.fromkeys(files)), net


def tokens(paths):
    return sum(len(read(os.path.join(SKILL, p))) for p in paths) // 4


def baseline_entry_chars():
    """Impeccable's entry file as the previous router read it (3.0.2 removed its front matter from the bundle)."""
    try:
        return len(subprocess.run(["git", "show", f"{BASELINE_COMMIT}:skills/{OLD_ID}/references/impeccable/SOURCE_SKILL.md"],
                                  cwd=ROOT, capture_output=True, text=True, check=True).stdout)
    except (OSError, subprocess.CalledProcessError):
        return len(read(os.path.join(SKILL, "references", "impeccable", "SOURCE_SKILL.md")))


def baseline_tokens(old_skill_chars, files, selected, entry_chars):
    """Approximate load under the previous router (entry points read first)."""
    base = set(files) - {"GUIDE.md", "references/impeccable/SOURCE_SKILL.md"}
    entry = entry_chars if any(f.startswith("references/impeccable/") for f in files) else 0
    if "ado" in selected:
        base |= {"references/frontend/testing.md", "references/frontend/review-and-release.md"}
    return (old_skill_chars + entry) // 4 + tokens(sorted(base))


def check_scenarios(modes, caps, never, craft_floor, groups, text, roster):
    data = json.loads(read(os.path.join(ROOT, "tests", "routing_scenarios.json")))
    try:
        old = subprocess.run(["git", "show", f"{BASELINE_COMMIT}:skills/{OLD_ID}/SKILL.md"],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        old = None
    shared = {f for c, segs in caps.items() if c != "ado" for s in segs for f in s["files"]}
    ado_files = {f for s in caps["ado"] for f in s["files"]} - shared
    skill_tokens = len(text) // 4
    entry_chars = baseline_entry_chars()
    print(f"\n{'scenario':30} {'mode':10} {'capabilities':34} {'tokens':>7} {'before':>7}  result")
    total_new = total_old = 0
    for sc in data["scenarios"]:
        selected, mode, outcome, files, net = route(sc["prompt"], modes, caps, craft_floor, groups)
        errs = []
        if "net" in sc and net != sc["net"]:
            errs.append(f"network {net} != {sc['net']}")
        planned = plan_agents(selected, mode, roster, groups, caps)
        if planned != sc.get("agent"):
            errs.append(f"agent {planned} != {sc.get('agent')}")
        if selected != set(sc["caps"]):
            errs.append(f"caps {sorted(selected)} != {sorted(sc['caps'])}")
        if mode != sc["mode"]:
            errs.append(f"mode {mode} != {sc['mode']}")
        if outcome not in sc.get("outcome", ["route"]):
            errs.append(f"outcome {outcome}")
        errs += [f"missing {f}" for f in sc["must"] if f not in files]
        errs += [f"loaded forbidden {f}" for f in sc["forbid"] if f in files]
        errs += [f"loaded never-load {f}" for f in files if is_never(f, never)]
        if "ado" not in sc["caps"]:
            errs += [f"loaded ADO file {f}" for f in files if f in ado_files]
        new = skill_tokens + tokens(files + ([AGENT_PLANS] if planned != "inline" else []))
        before = baseline_tokens(len(old), files, selected, entry_chars) if old else 0
        total_new += new
        total_old += before
        check(not errs, f"scenario {sc['id']}: {'; '.join(errs)}")
        print(f"{sc['id']:30} {mode:10} {','.join(sorted(selected)) or '-':34} {new:7} {before:7}  "
              f"{'PASS' if not errs else 'FAIL'}")
    n = len(data["scenarios"])
    check(n >= 12, "need at least 12 routing scenarios")
    if total_old:
        growth = 100 * total_new / total_old - 100
        print(f"{n} scenarios: ~{total_new // n} tokens/scenario vs ~{total_old // n} before "
              f"({growth:+.1f}% context vs the pre-router baseline; budget +{MAX_CONTEXT_GROWTH}%)")
        check(growth <= MAX_CONTEXT_GROWTH, f"context growth {growth:.1f}% exceeds {MAX_CONTEXT_GROWTH}%")


# ------------------------------------------------------------------- agents
AGENT_KEYS = {"name", "description", "tools", "disallowedTools", "model", "color", "maxTurns", "skills",
              "memory", "background", "effort", "isolation"}  # documented for plugin agents (code.claude.com/docs/en/sub-agents)
WRITE_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}
AGENT_BODY_MAX_LINES = 45


def parse_roster(text, caps):
    """SKILL.md §5 list: "- `agent` (access): cap, cap" -> {agent: (access, [capability IDs])}."""
    section = text.split("## 5.")[1] if "## 5." in text else ""
    return {name: (access.strip(), [c.strip() for c in cells.split(",") if c.strip()])
            for name, access, cells in re.findall(r"^- `([\w-]+)` \(([^)]+)\): (.+)$", section, re.M)}


def frontmatter_fields(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    fields = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z]+): (.*)$", line)
        if not km:
            return None, text
        key, value = km.groups()
        if value.startswith('"'):
            try:
                value = json.loads(value)
            except ValueError:
                return None, text
        elif re.search(r":\s|\s#", value):
            return None, text  # unquoted YAML value with ": " or " #" doesn't parse
        fields[key] = value
    return fields, text[m.end():]


def parse_helpers():
    """Helper agents listed in the Craftforce index: dispatched only by its playbooks, owning no capability."""
    text = read(os.path.join(SKILL, SUB_ROUTERS[0]))
    section = text.split("## Helper agents")[1].split("\n## ")[0] if "## Helper agents" in text else ""
    return {name: (access.strip(), []) for name, access, _ in re.findall(r"^- `([\w-]+)` \(([^)]+)\): (.+)$", section, re.M)}


def check_agents(text, caps, groups):
    roster = parse_roster(text, caps)
    helpers = parse_helpers()
    check(not set(helpers) & set(roster), f"helper agents also in the SKILL.md §5 roster: {sorted(set(helpers) & set(roster))}")
    check(all(access == "read-only" for access, _ in helpers.values()), "helper agents must be read-only")
    files = sorted(f[:-3] for f in os.listdir(AGENT_DIR) if f.endswith(".md")) if os.path.isdir(AGENT_DIR) else []
    check(files == sorted({**roster, **helpers}), f"agents/ files {files} != SKILL.md §5 roster + Craftforce helpers {sorted({**roster, **helpers})}")
    owners = {}
    for name, (_, owned) in roster.items():
        for c in owned:
            owners.setdefault(c, []).append(name)
    check(not [c for c in owners if c not in caps], f"roster names unknown capabilities {[c for c in owners if c not in caps]}")
    check(not [c for c in caps if len(owners.get(c, [])) != 1],
          f"capabilities without exactly one agent: {[(c, owners.get(c, [])) for c in caps if len(owners.get(c, [])) != 1]}")
    for name in files:
        path = os.path.join(AGENT_DIR, name + ".md")
        fields, body = frontmatter_fields(read(path))
        if not check(fields is not None, f"agents/{name}.md frontmatter doesn't parse"):
            continue
        check(set(fields) <= AGENT_KEYS, f"agents/{name}.md has undocumented keys {set(fields) - AGENT_KEYS}")
        check(fields.get("name") == name and ":" not in name, f"agents/{name}.md name must match its file name")
        check(0 < len(fields.get("description", "")) <= 1024, f"agents/{name}.md description missing or too long")
        tools = {t.strip() for t in fields.get("tools", "").split(",") if t.strip()}
        denied = {t.strip() for t in fields.get("disallowedTools", "").split(",") if t.strip()}
        if tools:
            check("Agent" not in tools, f"agents/{name}.md may start other agents")
        else:
            check("Agent" in denied, f"agents/{name}.md inherits tools, so it must disallow Agent")
        if {**roster, **helpers}.get(name, ("",))[0] == "read-only":
            ok = not (tools & WRITE_TOOLS) if tools else WRITE_TOOLS - {"MultiEdit"} <= denied
            check(ok, f"read-only agent {name} has write tools")
        lines = body.strip().splitlines()
        check(len(lines) <= AGENT_BODY_MAX_LINES, f"agents/{name}.md body has {len(lines)} lines")
        check(not re.search(r"references/|templates/", body), f"agents/{name}.md contains guidance paths")
        check(not [l for l in lines if l.lstrip().startswith("|") or "→" in l], f"agents/{name}.md contains a routing table")
    print(f"agents: {len(files)} agents ({len(helpers)} Craftforce helpers), {len(owners)} capabilities each owned by exactly one agent")
    return roster


def plan_agents(selected, mode, roster, groups, caps):
    """Agents the head would dispatch; "inline" when one responsibility covers the task (SKILL.md §5)."""
    owner = {c: n for n, (_, owned) in roster.items() for c in owned}
    read_only = {n for n, (access, _) in roster.items() if access == "read-only"}
    workflows = (set(caps) - groups["Design"] - groups["Engineering"]) | {"ado"}
    chosen = set()
    for c in selected:
        agent = owner.get(c)
        if mode in ("answer", "audit", "plan") and agent not in read_only:
            agent = "design-auditor" if c in groups["Design"] else "delivery-agent" if c in workflows else "code-reviewer"
        chosen.add(agent)
    return "inline" if len(chosen) <= 1 else sorted(chosen)


# ------------------------------------------------------------------- budget
def check_budget(text):
    guide = read(os.path.join(SKILL, "GUIDE.md"))
    check(len(text) <= SKILL_MD_MAX_CHARS, f"SKILL.md {len(text)} chars > {SKILL_MD_MAX_CHARS}")
    check(len(guide) <= GUIDE_MAX_CHARS, f"GUIDE.md {len(guide)} chars > {GUIDE_MAX_CHARS}")
    check("GUIDE.md" in text, "SKILL.md must link GUIDE.md")
    print(f"budget: SKILL.md ~{len(text) // 4} tokens, GUIDE.md ~{len(guide) // 4} tokens")


# ------------------------------------------------------------------ install
def check_install_docs():
    readme = read(os.path.join(ROOT, "README.md"))
    base = f"npx skills add {REPO} --skill {SKILL_ID} -g"
    allc = base + "".join(f" -a {a}" for a in AGENTS) + " -y"
    check(allc in readme, "README lacks the four-tool global install command")
    for a in AGENTS:
        check(f"{base} -a {a} -y" in readme, f"README lacks the global install command for {a}")
    check("## Install Craftline" in readme[:5000], "install section is not near the top of README")
    check(f"/plugin install {SKILL_ID}@uiuxabhishek" in readme, "README lacks the Claude Code plugin install")
    install = read(os.path.join(ROOT, "INSTALL.md"))
    for cmd in (f"claude plugin marketplace update uiuxabhishek", f"claude plugin uninstall {RENAMED_ID}@uiuxabhishek",
                f"claude plugin install {SKILL_ID}@uiuxabhishek", f"npx skills remove {RENAMED_ID} -g",
                f"npx skills remove {OLD_ID} -g", "## Migrate to Craftline"):
        check(cmd in install, f"INSTALL.md lacks {cmd!r}")
    for doc, text in (("README.md", readme), ("INSTALL.md", install)):
        for cmd in re.findall(r"npx skills(?:@[\d.]+)? add ([^-\s]\S*)[^\n`|]*", text):
            check(cmd.split("#")[0] == REPO, f"{doc} install command uses {cmd!r}")
        for line in re.findall(r"npx skills(?:@[\d.]+)? add [^\n`|]*", text):
            check("-a claude-code" not in line, f"{doc} installs Craftline for Claude Code with npx: {line!r}")
    print(f"install docs: four-tool, {len(AGENTS)} per-tool, plugin and migration commands present")


def former_name_lines(path, text):
    """Lines that use a former name outside a migration/history section or a 'formerly' line."""
    hits, skip_level, fence = [], 0, False  # skip_level: level of the migration/history heading we're under
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            fence = not fence
        h = re.match(r"(#{1,6}) ", line) if path.endswith(".md") and not fence else None
        if h:
            level = len(h.group(1))
            if skip_level and level <= skip_level:
                skip_level = 0
            if not skip_level and re.search(r"migrat|upgrad|history|rename", line, re.I):
                skip_level = level
        skip = bool(skip_level)
        clean = line
        for keep in NOT_FORMER:
            clean = clean.replace(keep, "")
        if skip or re.search(r"\bformer(ly)?\b|renamed", clean, re.I):
            continue
        if any(name in clean for name in FORMER_NAMES):
            hits.append(f"{path}:{n}")
    return hits


def check_old_id():
    hits = []
    for r, dirs, fs in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "dist")]
        for f in fs:
            p = rel(os.path.join(r, f), ROOT)
            if p.startswith(FORMER_ALLOWED) or not f.endswith((".md", ".py", ".json", ".mjs", ".txt")):
                continue
            hits += former_name_lines(p, read(os.path.join(r, f)))
    check(not hits, f"former IDs or brands outside migration notes and history: {hits[:10]}")
    for doc in ("README.md", "INSTALL.md"):
        text = read(os.path.join(ROOT, doc))
        for old in (OLD_ID, RENAMED_ID):
            check(f"add {REPO} --skill {old}" not in text, f"{doc} still installs {old}")
        check(f"abhishekinvission/{OLD_ID}" not in text.replace(f"abhishekinvission/{OLD_ID}#", ""),
              f"{doc} still points to the old repository")
    print(f"former names: {', '.join(FORMER_NAMES)} only in migration notes, history, tests and the updater's migration")


def check_updater():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.dont_write_bytecode = True
    import updater_sandbox
    try:
        results = updater_sandbox.run_checks()
    except (OSError, AssertionError, subprocess.SubprocessError) as e:
        check(False, f"updater sandbox error: {e}")
        return
    for name, ok in results:
        check(ok, f"updater sandbox: {name}")
    check(not os.path.exists(os.path.join(SKILL, "tools")), "updater must stay outside the installable skill")
    print(f"updater sandbox: {sum(ok for _, ok in results)}/{len(results)} checks with a mock API and mock CLI")


def check_package():
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    sys.dont_write_bytecode = True
    import package_skill as pkg
    never = pkg.never_load()
    with tempfile.TemporaryDirectory() as out:
        path, digest = pkg.build(out)
        check(pkg.build(os.path.join(out, "again"))[1] == digest, "upload ZIP build is not deterministic")
        check(os.path.getsize(path) <= UPLOAD_MAX_BYTES, "upload ZIP exceeds 8 MB")
        with zipfile.ZipFile(path) as z:
            infos = z.infolist()
            names = [i.filename for i in infos]
            check(all(n.startswith(f"{SKILL_ID}/") for n in names), f"ZIP root must be {SKILL_ID}/")
            check(all((i.external_attr >> 16) & 0o777 == 0o644 for i in infos), "ZIP entries must be 0644 files")
            expected = {f"{SKILL_ID}/{r}" for _, r in pkg.files()}
            check(set(names) == expected, f"ZIP contents drift: {sorted(set(names) ^ expected)[:5]}")
            inner = [n.split("/", 1)[1] for n in names]
            check(not [n for n in inner if pkg.omitted(n, never)], "upload ZIP contains a Never load file")
            check(not [n for n in inner if n.startswith("agents/")], "upload ZIP must stay skill-only (no agents/)")
            for req in ("SKILL.md", "GUIDE.md", "LICENSE", "NOTICE.md", "LICENSES/IMPECCABLE_NOTICE.md",
                        "references/impeccable/SOURCE_SKILL.md", "templates/pr-description.md"):
                check(f"{SKILL_ID}/{req}" in names, f"ZIP lacks {req}")
            for n in names:
                data, src = z.read(n), os.path.join(SKILL, n.split("/", 1)[1])
                if n.endswith("/SKILL.md"):
                    text, orig = data.decode("utf-8"), read(src)
                    m = re.search(r"^name: (.*)$", text, re.M)
                    d = re.search(r"^description: (.*)$", text, re.M)
                    check(m and m.group(1) == SKILL_ID, "packaged SKILL.md name mismatch")
                    check(d and 0 < len(d.group(1)) <= pkg.UPLOAD_DESCRIPTION_MAX, "packaged description > 200 chars")
                    check(d and not re.search(r":\s|\s#", d.group(1)), "packaged description needs YAML quoting")
                    strip = lambda t: re.sub(r"^description: .*$", "", t, count=1, flags=re.M)
                    check(strip(text) == strip(orig), "packaged SKILL.md differs beyond its description")
                else:
                    with open(src, "rb") as f:
                        check(f.read() == data, f"ZIP copy of {n} differs")
        print(f"package: {os.path.basename(path)}, {len(names)} files, {os.path.getsize(path) // 1024} KB, "
              f"upload description {len(pkg.UPLOAD_DESCRIPTION)} chars, {len(never)} Never load entries left out")

        ppath, pdigest = pkg.build_plugin(out)
        check(pkg.build_plugin(os.path.join(out, "again"))[1] == pdigest, "plugin ZIP build is not deterministic")
        with zipfile.ZipFile(ppath) as z:
            pnames = z.namelist()
            tops = {n.split("/", 1)[0] for n in pnames}
            check(tops == {".claude-plugin", "README.md", "agents", "skills"}, f"plugin ZIP has unexpected top-level entries {tops}")
            check({".claude-plugin/plugin.json", ".claude-plugin/icon.png"} <= set(pnames)
                  and ".claude-plugin/marketplace.json" not in pnames,
                  "plugin ZIP must carry plugin.json and icon.png and not marketplace.json")
            agents_in = sorted(n for n in pnames if n.startswith("agents/"))
            check(agents_in == sorted(f"agents/{f}" for f in os.listdir(AGENT_DIR)
                                     if f.endswith(".md")), "plugin ZIP agents differ from agents/")
            skill_in = {n[len(f"skills/{SKILL_ID}/"):] for n in pnames if n.startswith("skills/")}
            check(skill_in == {r for _, r in pkg.files()}, "plugin ZIP skill files differ from the shipped set")
            check(z.read(f"skills/{SKILL_ID}/SKILL.md") == open(os.path.join(SKILL, "SKILL.md"), "rb").read(),
                  "plugin ZIP SKILL.md must be the repository copy (full description)")
            for n in pnames:
                src = os.path.join(PLUGIN, n) if not n.startswith("skills/") else os.path.join(SKILL, n.split("/", 2)[2])
                with open(src, "rb") as f:
                    check(f.read() == z.read(n), f"plugin ZIP copy of {n} differs")
        print(f"package: {os.path.basename(ppath)}, {len(pnames)} files, {len(agents_in)} agents, top level {sorted(tops)}")
    check_plugin_manifests(pkg)


def check_plugin_layout():
    """plugin/ is the single, self-contained copy that marketplaces and the Skills CLI read."""
    ls = lambda *p: sorted(n for n in os.listdir(os.path.join(PLUGIN, *p)) if n not in (".DS_Store", "Thumbs.db"))
    check(ls() == [".claude-plugin", "README.md", "agents", "skills"],
          f"plugin/ must hold only .claude-plugin, README.md, agents and skills, found {ls()}")
    check(ls(".claude-plugin") == ["icon.png", "plugin.json"], "plugin/.claude-plugin must hold only icon.png and plugin.json")
    # The plugin directory reads .claude-plugin/icon.png: a complete square PNG, 512-2048 px, under 2 MB.
    icon = os.path.join(PLUGIN, ".claude-plugin", "icon.png")
    if check(os.path.isfile(icon), "plugin/.claude-plugin/icon.png is missing"):
        with open(icon, "rb") as f:
            png = f.read()
        w, h = (int.from_bytes(png[16:20], "big"), int.from_bytes(png[20:24], "big")) if len(png) > 24 else (0, 0)
        check(png[:8] == b"\x89PNG\r\n\x1a\n" and png[12:16] == b"IHDR" and png.endswith(b"IEND\xaeB`\x82"),
              "icon.png is not a complete PNG")
        check(w == h and 512 <= w <= 2048 and len(png) < 2 * 1024 * 1024,
              f"icon.png must be square, 512-2048 px and under 2 MB, got {w}x{h}, {len(png)} bytes")
    check(ls("skills") == [SKILL_ID], "plugin/skills must hold only the one skill")
    for stale in ("skills", "agents", ".claude-plugin/plugin.json"):
        check(not os.path.exists(os.path.join(ROOT, stale)), f"{stale} must live under plugin/, not the repository root")
    links = [os.path.join(r, n) for r, ds, fs in os.walk(ROOT) if ".git" not in r.split(os.sep)
             for n in ds + fs if os.path.islink(os.path.join(r, n))]
    check(not links, f"symlinks aren't allowed: {[rel(p, ROOT) for p in links]}")
    # The plugin directory shows plugin/README.md as the listing and blocks one under 40 words outside code blocks.
    readme = re.sub(r"```.*?```", " ", read(os.path.join(PLUGIN, "README.md")), flags=re.S)
    count = len(re.findall(r"[A-Za-z0-9][\w'-]*", readme))
    check(count >= 40, f"plugin/README.md has {count} words outside code blocks; the directory needs 40")
    print(f"plugin layout: plugin/ holds .claude-plugin/plugin.json, README.md ({count} words), agents/ "
          f"and skills/{SKILL_ID}/ only")


def check_plugin_manifests(pkg):
    try:
        manifest = json.loads(read(pkg.PLUGIN_MANIFEST))
        market = json.loads(read(pkg.MARKETPLACE))
    except (OSError, ValueError) as e:
        check(False, f"plugin manifests unreadable: {e}")
        return
    for key in ("name", "version", "description", "author", "homepage", "repository", "license", "keywords"):
        check(manifest.get(key), f"plugin.json lacks {key}")
    check(manifest.get("name") == SKILL_ID, f"plugin.json name must be {SKILL_ID}")
    check(manifest.get("displayName") == "Craftline", "plugin.json displayName must be Craftline")
    check(manifest.get("privacyPolicyUrl") == f"https://github.com/{REPO}/blob/main/PRIVACY.md",
          "plugin.json privacyPolicyUrl must be PRIVACY.md on main")
    privacy = read(os.path.join(ROOT, "PRIVACY.md")) if os.path.isfile(os.path.join(ROOT, "PRIVACY.md")) else ""
    for phrase in ("telemetry", "under 18", "/issues"):
        check(phrase in privacy, f"PRIVACY.md lacks {phrase!r}")
    plugin_readme = read(os.path.join(PLUGIN, "README.md"))
    check("## What it reads and sends" in plugin_readme and manifest.get("privacyPolicyUrl", "-") in plugin_readme,
          "plugin/README.md needs 'What it reads and sends' and a link to the privacy policy")
    for key in ("documentationUrl", "supportUrl", "privacyPolicyUrl"):
        check(str(manifest.get(key, "")).startswith(f"https://github.com/{REPO}/"), f"plugin.json {key} must be a repository URL")
    check(not manifest.get("documentationUrl", "").endswith("GUIDE.md")
          or os.path.isfile(os.path.join(SKILL, "GUIDE.md")), "plugin.json documentationUrl points at a missing GUIDE.md")
    check(manifest.get("version") == pkg.version(), f"plugin.json version {manifest.get('version')} != SKILL.md {pkg.version()}")
    check(isinstance(manifest.get("author"), dict) and manifest["author"].get("name"), "plugin.json author needs a name")
    check(isinstance(manifest.get("keywords"), list), "plugin.json keywords must be a list")
    for key in ("homepage", "repository"):
        check(str(manifest.get(key, "")).startswith(f"https://github.com/{REPO}"), f"plugin.json {key} must be the repository URL")
    check(not set(manifest) & {"agents", "skills", "commands"}, "plugin.json should rely on the default agents/ and skills/ layout")
    check(market.get("name") and market.get("owner", {}).get("name"), "marketplace.json needs name and owner.name")
    entries = [p for p in market.get("plugins", []) if p.get("name") == SKILL_ID]
    if not check(len(entries) == 1 and len(market["plugins"]) == 1, "marketplace.json must list exactly this plugin"):
        return
    src = entries[0].get("source")
    check("version" not in entries[0], "marketplace entry must not set version (plugin.json owns it)")
    check(entries[0]["name"] == manifest.get("name"), "marketplace entry name must equal the plugin.json name")
    # Organization sync in the Claude app accepts github, url, git-subdir or a ./ path; not archive or npm.
    check(src == "./plugin", f"marketplace source must be the relative path ./plugin, got {src!r}")
    check(os.path.realpath(os.path.join(ROOT, str(src))) == os.path.realpath(PLUGIN)
          and os.path.isfile(os.path.join(PLUGIN, ".claude-plugin", "plugin.json")), "./plugin doesn't resolve to the plugin")
    check("pluginRoot" not in market.get("metadata", {}), "organization sync rejects bare names under metadata.pluginRoot")
    print(f"plugin: manifest {manifest.get('version')}, marketplace source {src}")


# -------------------------------------------------------------- git sandbox
def check_git_sandbox():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.dont_write_bytecode = True
    import git_sandbox
    try:
        results = git_sandbox.run_checks()
    except (OSError, AssertionError) as e:
        check(False, f"git sandbox error: {e}")
        return
    for name, ok in results:
        check(ok, f"git sandbox: {name}")
    print(f"git sandbox: {sum(ok for _, ok in results)}/{len(results)} checks in a throwaway repository")


# ----------------------------------------------------------------- security
ASSET_EXT = r"\.(?:png|jpe?g|svg|webp|gif|ico|woff2?|ttf|otf)\b"
# A download piped or substituted straight into an interpreter (the directory's RUNTIME_FETCH_EXEC warning).
FETCH = r"(?:curl|wget|iwr|irm|Invoke-WebRequest|Invoke-RestMethod|DownloadString|DownloadFile)\b"
SHELL = r"(?:sudo\s+)?(?:sh|bash|zsh|dash|ksh|fish|python3?|node|perl|ruby|iex|Invoke-Expression|pwsh|powershell)\b"
FETCH_EXEC = re.compile(rf"{FETCH}[^\n|]*\|\s*{SHELL}|{SHELL}\s+(?:-c\s+)?[\"']?[<$]\(\s*{FETCH}|"
                        rf"(?:iex|Invoke-Expression)\b[^\n]*{FETCH}", re.I)
# The directory's scan also flagged prose that puts loading and executing on one line (3.0.2 and 3.0.3). Its exact
# pattern isn't documented, so this is the conservative same-line form: a load word plus an execution word.
LOAD_WORD = re.compile(r"\bsrc\b|script-src|\bfetch\b|download|\bimport\s*\(|XMLHttpRequest|\binstall\w*", re.I)
EXEC_WORD = re.compile(r"\beval\b|unsafe-eval|new Function|\bexec(?:Sync)?\s*\(|child_process|\bon(?:error|load)\s*=|"
                       r"\bruns?\s+(?:code|scripts?)\b|\bruns?\b[^.\n]{0,40}\binstall", re.I)


def check_directory_rules():
    """Plugin directory rules the CLI doesn't run: assets named from front matter or code, and fetch-and-execute."""
    bundled = {n for r, _, fs in os.walk(PLUGIN) for n in fs if re.search(ASSET_EXT + "$", n, re.I)}
    front_ok = {os.path.join(SKILL, "SKILL.md"), os.path.join(SKILL, "references", "apple-design", "SOURCE_SKILL.md")}
    texts = 0
    for r, _, fs in os.walk(PLUGIN):
        for n in fs:
            p = os.path.join(r, n)
            if re.search(ASSET_EXT + "$", n, re.I):
                continue
            text, texts = read(p), texts + 1
            name = rel(p, ROOT)
            fm = re.match(r"---\n(.*?)\n---\n", text, re.S) if n.endswith(".md") else None
            if fm:
                check(p in front_ok or os.path.dirname(p) == AGENT_DIR,
                      f"{name} has front matter; only SKILL.md, the agents and Apple Design's entry may")
                check(not re.search(ASSET_EXT, fm.group(1), re.I), f"{name} front matter names an image or font")
                check("*" not in fm.group(1), f"{name} front matter has a wildcard the directory may expand to assets")
            for asset in bundled:
                check(asset not in text, f"{name} names the bundled asset {asset}")
            for m in FETCH_EXEC.finditer(text):
                check(False, f"{name}:{text.count(chr(10), 0, m.start()) + 1} pipes a download into an interpreter")
            for n_, line in enumerate(text.splitlines(), 1):
                if LOAD_WORD.search(line) and EXEC_WORD.search(line):
                    check(False, f"{name}:{n_} puts loading and executing on one line (directory RUNTIME_FETCH_EXEC)")
    print(f"directory rules: {texts} text files checked for front matter, {len(bundled)} bundled asset name(s) "
          "and fetch-and-execute")


def check_security():
    secret = re.compile(r"(ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY|"
                        r"(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,})", re.I)
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for f in files:
            p = os.path.join(root, f)
            check(not os.path.islink(p), f"symlink {rel(p, ROOT)}")
            check(not os.access(p, os.X_OK), f"executable file {rel(p, ROOT)}")
            r = rel(p, SKILL)
            if f.endswith((".md", ".json", ".py", ".txt", ".mjs")) and not r.startswith(THIRD_PARTY):
                check(not secret.search(read(p)), f"possible secret in {rel(p, ROOT)}")
    print("security: secret, symlink and executable scan done")


def main():
    check_discovery()
    if "--cli" in sys.argv:
        check_cli()
    check_links()
    check_integrity()
    text, modes, caps, never, craft_floor, groups = parse_router()
    check(set(modes) == {"answer", "audit", "plan", "implement", "deliver"}, f"modes {sorted(modes)}")
    limits = text.lower().replace("\u2019", "'")
    for phrase in ",".join((LIMIT_AUDIT, LIMIT_IMPLEMENT, LIMIT_NO_FETCH, LIMIT_OFFLINE)).split(","):
        check(phrase.strip() in limits, f"limit phrase {phrase.strip()!r} not documented in SKILL.md")
    check(ADO_OWNS_GIT in limits, "SKILL.md must say ado owns git")
    check(BACKEND_RULE in limits, "SKILL.md must keep frontend rows out of the backend part of a task")
    check(STRICT_AUDIT in limits, "SKILL.md must say audit and plan never fetch")
    git_guide = read(os.path.join(SKILL, "references", "workflows", "git-workflow.md")).lower().replace("’", "'")
    for phrase in ("no `git fetch`, `pull`", "don't fetch", "offline", "--no-optional-locks", "git ls-remote"):
        check(phrase in git_guide, f"git-workflow.md lacks the strict read-only rule {phrase!r}")
    check_coverage(caps, never)
    check_budget(text)
    check_security()
    check_install_docs()
    check_plugin_layout()
    check_directory_rules()
    check_package()
    check_git_sandbox()
    check_updater()
    check_old_id()
    roster = check_agents(text, caps, groups)
    check_scenarios(modes, caps, never, craft_floor, groups, text, roster)
    if failures:
        print(f"\nFAILED ({len(failures)}):")
        for f in failures:
            print(" -", f)
        sys.exit(1)
    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
