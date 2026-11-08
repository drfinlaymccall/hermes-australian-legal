"""Bounded, read-only Git access to a locally configured regulations corpus.

Only committed objects are trusted; corpus Python is never imported or run.
``provision`` takes an exact metadata instrument slug and a relative Markdown
filename (for example ``s-052.md`` or ``part-6/div-2.md``), not a revision,
heading search or fuzzy instrument name. Queries outside recorded continuous
coverage fail closed. Results are source material, not legal conclusions.

Supported repositories are ordinary local checkouts with a real .git directory.
No clone, fetch, update, checkout, index refresh or configuration write occurs.
Each Git command has a wall-clock timeout and bounded stdout AND stderr. An
oversize provision is rejected, never returned as an apparently complete quote.
"""
from datetime import date as _Date
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import subprocess
import time


MAX_TEXT_BYTES = 262_144
MAX_METADATA_BYTES = 131_072
MAX_GIT_OUTPUT_BYTES = 1_048_576
GIT_TIMEOUT_SECONDS = 10
MAX_INSTRUMENTS = 64
MAX_TAGS = 10_000
_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*", re.ASCII)
_OID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", re.ASCII)
_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", re.ASCII)
_SEGMENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*", re.ASCII)
_REGISTER = re.compile(r"[A-Z][0-9]{4}[A-Z][0-9]{5}", re.ASCII)
_BASE_CAVEATS = (
    "This is a derived Git copy, not the authoritative Federal Register of Legislation. "
    "Check the official register before relying on it; this is not legal advice.",
    "Only recorded compilation days are represented. Amendments commencing between "
    "compilations may appear only in a later compilation; a selected tag does not "
    "establish the law applicable to particular facts or transitional circumstances.",
    "Git history and last-change metadata are provenance, not independent proof of "
    "legal commencement, application, completeness or current validity.",
)


def _git(root, args, *, limit=MAX_GIT_OUTPUT_BYTES):
    """Run an internal argv-only Git read; never surface stderr/local paths.

    Read pipes incrementally rather than capture_output followed by slicing:
    both memory consumption and elapsed time are bounded even on bad objects.
    The fresh environment deliberately inherits no GIT_*, HOME, loader variables,
    credentials, Python settings or user-supplied executable search path.
    """
    executable = shutil.which("git", path=os.defpath)
    if executable is None:
        raise ValueError("Native Git is unavailable")
    env = {
        "PATH": os.defpath, "LANG": "C", "LC_ALL": "C",
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_CONFIG_GLOBAL": os.devnull, "GIT_ATTR_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0", "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_NO_LAZY_FETCH": "1", "GIT_TERMINAL_PROMPT": "0",
        # Also forbids promisor/lazy-fetch transport on older Git versions.
        "GIT_ALLOW_PROTOCOL": "",
    }
    argv = [
        executable, "--no-pager", "--no-optional-locks", "--no-replace-objects",
        "--literal-pathspecs", "-c", "core.hooksPath=" + os.devnull,
        "-c", "core.fsmonitor=false", "-c", "gc.auto=0",
        "-c", "maintenance.auto=false", "-c", "protocol.allow=never",
        "-C", str(root), *args,
    ]
    chunks = {"stdout": bytearray(), "stderr": bytearray()}
    deadline = time.monotonic() + GIT_TIMEOUT_SECONDS
    process = None
    try:
        process = subprocess.Popen(
            argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=env, shell=False,
        )
        with selectors.DefaultSelector() as selector:
            for name in chunks:
                stream = getattr(process, name)
                os.set_blocking(stream.fileno(), False)
                selector.register(stream, selectors.EVENT_READ, name)
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise ValueError("Git read timed out")
                events = selector.select(remaining)
                for key, _ in events:
                    block = os.read(key.fd, min(65_536, limit + 1))
                    if not block:
                        selector.unregister(key.fileobj)
                        continue
                    chunks[key.data].extend(block)
                    if len(chunks[key.data]) > limit:
                        raise ValueError("Git read exceeded the bounded output limit")
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ValueError("Git read timed out")
            if process.wait(timeout=remaining) != 0:
                raise ValueError("Git read failed; required committed corpus data may be unavailable")
        return bytes(chunks["stdout"])
    except subprocess.TimeoutExpired:
        raise ValueError("Git read timed out") from None
    except OSError:
        raise ValueError("Git read could not be completed") from None
    finally:
        if process is not None:
            if process.poll() is None:
                process.kill()
            process.wait()
            for name in chunks:
                getattr(process, name).close()


def _decode(raw):
    try:
        return raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        raise ValueError("Committed corpus content must be valid UTF-8") from None


def _date(value, label):
    if not isinstance(value, str) or not _DATE.fullmatch(value):
        raise ValueError(label + " must be a real YYYY-MM-DD date")
    try:
        _Date.fromisoformat(value)
    except ValueError:
        raise ValueError(label + " must be a real YYYY-MM-DD date") from None
    return value


def _oid(value):
    if not _OID.fullmatch(value):
        raise ValueError("Git did not return a full object identifier")
    return value


def _root(corpus_path):
    try:
        value = os.fspath(corpus_path)
        if not isinstance(value, str) or not value or "\x00" in value:
            raise ValueError("A local corpus checkout is required")
        root = Path(os.path.abspath(value))
        if root.is_symlink() or not root.is_dir():
            raise ValueError("A local corpus checkout is required")
        git_dir = root / ".git"
        if git_dir.is_symlink() or not git_dir.is_dir():
            raise ValueError("A local corpus checkout with a real Git directory is required")
        return root
    except (OSError, TypeError):
        raise ValueError("A local corpus checkout is required") from None


def _no_symlinks(root, relative):
    current = root
    try:
        for part in relative.split("/"):
            current = current / part
            if current.is_symlink():
                raise ValueError("Symlink corpus paths are not permitted")
    except OSError:
        raise ValueError("Corpus path could not be safely checked") from None


def _entry(root, commit, path, *, tree=False):
    _no_symlinks(root, path)
    raw = _git(root, ["ls-tree", "-z", commit, "--", path], limit=4096)
    entries = raw.split(b"\x00")
    if len(entries) != 2 or entries[-1] != b"":
        raise ValueError("Required regular committed corpus path is missing")
    try:
        attributes, filename = entries[0].split(b"\t", 1)
        mode, kind, oid = attributes.decode("ascii").split(" ")
    except (ValueError, UnicodeDecodeError):
        raise ValueError("Invalid committed corpus tree entry") from None
    if filename != path.encode("utf-8"):
        raise ValueError("Committed corpus path did not match exactly")
    if tree:
        valid = mode == "040000" and kind == "tree"
    else:
        valid = mode in ("100644", "100755") and kind == "blob"
    if not valid:
        raise ValueError("Symlink or non-regular committed corpus path is not permitted")
    return _oid(oid)


def _blob(root, commit, path, *, limit):
    oid = _entry(root, commit, path)
    size_text = _decode(_git(root, ["cat-file", "-s", oid], limit=64)).strip()
    if not re.fullmatch(r"[0-9]+", size_text, re.ASCII):
        raise ValueError("Invalid committed corpus object size")
    size = int(size_text)
    if size > limit:
        raise ValueError("Committed corpus content exceeds the bounded output limit; no truncated text returned")
    raw = _git(root, ["cat-file", "blob", oid], limit=limit)
    if len(raw) != size:
        raise ValueError("Committed corpus text was incomplete; no truncated text returned")
    text = _decode(raw)
    if not text.strip() or "\x00" in text:
        raise ValueError("Committed corpus content is empty or not plain text")
    return text


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate metadata key")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError("Non-finite metadata values are not permitted")


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _metadata(root, head):
    text = _blob(root, head, "corpus.json", limit=MAX_METADATA_BYTES)
    try:
        record = json.loads(text, object_pairs_hook=_unique_object, parse_constant=_invalid_constant)
    except (ValueError, RecursionError):
        raise ValueError("Committed corpus.json must contain unambiguous valid JSON metadata") from None
    if not isinstance(record, dict):
        raise ValueError("Committed corpus.json metadata must be an object")
    for key in ("corpus", "name", "record_note"):
        if not _nonempty(record.get(key)):
            raise ValueError("Missing required corpus metadata: " + key)
    start = _date(record.get("history_from"), "metadata history_from")
    end = _date(record.get("record_to"), "metadata record_to")
    checked = _date(record.get("checked_on"), "metadata checked_on")
    if not start <= end <= checked:
        raise ValueError("Corpus metadata dates are inconsistent")
    entries = record.get("instruments")
    if not isinstance(entries, list) or not 1 <= len(entries) <= MAX_INSTRUMENTS:
        raise ValueError("Missing or excessive instrument metadata")
    known = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Instrument metadata must be an object")
        slug = entry.get("folder")
        if not isinstance(slug, str) or len(slug) > 128 or not _SLUG.fullmatch(slug):
            raise ValueError("Invalid instrument folder metadata")
        if slug in known:
            raise ValueError("Duplicate instrument metadata")
        register_id = entry.get("register_id")
        if not isinstance(register_id, str) or not _REGISTER.fullmatch(register_id):
            raise ValueError("Missing or invalid official register identifier metadata")
        if not _nonempty(entry.get("name")):
            raise ValueError("Missing instrument name metadata")
        continuous = _date(entry.get("no_gaps_from"), "instrument no_gaps_from")
        if not start <= continuous <= end:
            raise ValueError("Instrument no_gaps_from is outside the corpus record")
        if "excluded_compilations" in entry:
            excluded = entry["excluded_compilations"]
            if not isinstance(excluded, list) or len(excluded) > MAX_TAGS:
                raise ValueError("Invalid excluded compilation metadata")
            for excluded_date in excluded:
                _date(excluded_date, "excluded compilation")
                if excluded_date >= continuous:
                    raise ValueError("Excluded compilation contradicts no_gaps_from metadata")
        _entry(root, head, "corpus/" + slug, tree=True)
        known[slug] = entry
    return record, known


def _context(corpus_path):
    root = _root(corpus_path)
    head = _oid(_decode(_git(root, ["rev-parse", "--verify", "HEAD^{commit}"], limit=128)).strip())
    record, known = _metadata(root, head)
    return root, head, record, known


def _caveats(record, entries):
    notes: list[str] = list(_BASE_CAVEATS)
    notes.append(record["record_note"])
    scope = record.get("scope")
    if isinstance(scope, dict) and _nonempty(scope.get("when_absent")):
        notes.append(scope["when_absent"])
    for entry in entries:
        notes.append("%s: continuous compilation coverage is asserted only from %s; "
                     "earlier gap-period queries are blocked." % (entry["folder"], entry["no_gaps_from"]))
        if "excluded_compilations" not in entry:
            notes.append(entry["folder"] + ": excluded-compilation inventory metadata is missing; completeness is not independently verified.")
        elif entry["excluded_compilations"]:
            notes.append(entry["folder"] + ": excluded compilation dates: " + ", ".join(entry["excluded_compilations"]))
    return notes


def status(corpus_path):
    """Return committed metadata and identity, never a local path or legal opinion.

    Missing/invalid critical metadata, symlinks, output limits and Git failures
    raise ValueError. Dirty worktree metadata is not substituted for HEAD.
    """
    _root_path, head, record, known = _context(corpus_path)
    return {
        "corpus_commit": head, "metadata": record,
        "instrument_slugs": sorted(known), "checked_on": record["checked_on"],
        "record_to": record["record_to"], "history_from": record["history_from"],
        "read_only": True, "caveats": _caveats(record, known.values()),
    }


def _filename(value):
    if not isinstance(value, str) or not 1 <= len(value) <= 240 or not value.endswith(".md"):
        raise ValueError("Provision must be a safe relative Markdown filename")
    parts = value.split("/")
    if len(parts) > 8 or ".." in value or any(not _SEGMENT.fullmatch(part) for part in parts):
        raise ValueError("Provision must be a safe relative Markdown filename without traversal")
    return value


def _compilations(root, slug):
    prefix = "refs/tags/" + slug + "/"
    text = _decode(_git(root, ["for-each-ref", "--format=%(refname)", prefix]))
    lines = text.splitlines()
    if len(lines) > MAX_TAGS:
        raise ValueError("Compilation tag inventory exceeds the bounded limit")
    tags = []
    for ref in lines:
        if not ref.startswith(prefix):
            raise ValueError("Unexpected compilation tag reference")
        day = _date(ref[len(prefix):], "compilation tag date")
        tags.append((day, ref))
    if not tags:
        raise ValueError("No exact dated compilation tags exist for this instrument")
    return sorted(tags)


def _last_change(root, commit, path):
    raw = _git(root, [
        "log", "--no-show-signature", "-1", "--format=%H%x00%an%x00%aI%x00%B",
        commit, "--", path,
    ], limit=32_768)
    parts = _decode(raw).split("\x00", 3)
    if len(parts) != 4:
        raise ValueError("Last-change history metadata is unavailable")
    sha, author, authored_at, body = parts
    _oid(sha)
    trailers = dict(re.findall(r"^([A-Za-z-]+): (.*)$", body, flags=re.MULTILINE))
    in_force = trailers.get("In-force")
    if in_force is not None:
        _date(in_force, "last-change In-force trailer")
    return {
        "commit": sha, "author": author, "authored_at": authored_at,
        "subject": body.splitlines()[0] if body.splitlines() else "",
        "in_force": in_force, "compilation": trailers.get("Compilation"),
        "compilation_id": trailers.get("Compilation-id"), "kind": trailers.get("Kind"),
    }


def provision(corpus_path, instrument, provision, date):
    """Read exact committed UTF-8 text for the latest <slug>/<YYYY-MM-DD> tag.

    The query must be within history_from..record_to, not before the first tag,
    and not before no_gaps_from. All are inclusive boundaries. Future tags do
    not extend record_to. Full Git identifiers anchor metadata and selected
    compilation; annotated tags are peeled to commits. Last-change retrieval
    is optional but any failure is explicitly flagged in the retained caveats.
    """
    day = _date(date, "query date")
    filename = _filename(provision)
    if not isinstance(instrument, str) or len(instrument) > 128 or not _SLUG.fullmatch(instrument):
        raise ValueError("Instrument must be an exact known instrument slug")
    root, head, record, known = _context(corpus_path)
    if instrument not in known:
        raise ValueError("Instrument must be an exact known instrument slug")
    entry = known[instrument]
    if not record["history_from"] <= day <= record["record_to"]:
        raise ValueError("Query date is outside the corpus recorded date range")
    if day < entry["no_gaps_from"]:
        raise ValueError("Query date precedes continuous coverage; gap-period queries are blocked")
    tags = _compilations(root, instrument)
    eligible = [(tag_day, ref) for tag_day, ref in tags if tag_day <= day]
    if not eligible:
        raise ValueError("Query date is before this instrument's first recorded compilation")
    compiled_from, ref = eligible[-1]
    # Never fall back across a declared coverage gap even for a later query.
    if compiled_from < entry["no_gaps_from"]:
        raise ValueError("Selected compilation predates continuous coverage; possible missing gap compilation")
    commit = _oid(_decode(_git(root, ["rev-parse", "--verify", ref + "^{commit}"], limit=128)).strip())
    path = "corpus/" + instrument + "/" + filename
    text = _blob(root, commit, path, limit=MAX_TEXT_BYTES)
    notes = _caveats(record, [entry])
    if compiled_from != day:
        notes.append("Query date %s uses the latest recorded compilation tag dated %s, "
                     "not a separately verified compilation for the query day." % (day, compiled_from))
    try:
        changed = _last_change(root, commit, path)
    except ValueError:
        changed = None
        notes.append("Last-change provenance metadata is unavailable or exceeded its safety bound; "
                     "no last-change or commencement conclusion can be drawn.")
    return {
        "instrument": instrument, "instrument_name": entry["name"], "provision": filename,
        "query_date": day, "date": day, "corpus_commit": head,
        "compilation_tag": ref[len("refs/tags/"):], "compilation_commit": commit,
        "compilation_in_force_from": compiled_from, "record_starts": tags[0][0],
        "checked_on": record["checked_on"], "record_to": record["record_to"],
        "no_gaps_from": entry["no_gaps_from"],
        "source": {"register_id": entry["register_id"],
                   "url": "https://www.legislation.gov.au/" + entry["register_id"]},
        "last_change": changed, "text": text, "truncated": False,
        "caveats": notes,
    }
