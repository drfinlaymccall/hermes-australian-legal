# Hermes Australian Legal

**By Finlay McCall. A native Hermes prototype for evidence-linked Australian deal preparation.**

Read a provision as recorded on a date, retain its caveats, and prepare questions for counsel. This is **not legal or tax advice**. It is not a complete Australian legal research service and cannot certify privilege, legal applicability, or source authenticity.

## What works in this prototype

- Five native tools: corpus coverage, dated provision lookup, review prerequisites, exact-decimal scenario calculation, and literal quote checks.
- A bundled counsel-preparation skill and `/au-legal` status command.
- Read-only local Git evidence with explicit dates, source commits, official Register links, record bounds and caveats.
- A deterministic refusal for dates after the corpus record ends. An old text is never silently presented as current law.
- Runnable offline unit tests, synthetic examples, a historical corpus smoke command and an evaluation plan.

No model writes inside the plugin. Hermes's host model writes the narrative. The plugin does more than a prompt: executable checks constrain its **own tool outputs**, not every other tool or the host model. A skill is not a security sandbox.

## Related projects and provenance

- [australian-deal-review](https://github.com/drfinlaymccall/australian-deal-review): Finlay's original Claude plugin, source workflow for the Hermes adaptation. Source reviewed at `ba8e255f59c869a14de0353926724b912506046d`, Apache-2.0.
- [australia-regulations](https://github.com/drfinlaymccall/australia-regulations): separate derived Commonwealth instruments corpus. The old `australia-instruments` URL redirects here. The plugin reads its Git data and never executes its scripts. Source reviewed at `1c5a2ebf5c036ef32d91118e2864f48a73c95134`.
- [global-law](https://github.com/drfinlaymccall/global-law): related wider-law repository, a fork of [lexifina/global-law](https://github.com/lexifina/global-law). This plugin does not claim authorship of the upstream global-law project or implement its multi-jurisdiction reader.

See [Provenance](docs/Provenance.md) and [Design and workplan](docs/Design-and-workplan.md). The code uses Apache-2.0. No real deal records or legislation text are bundled in this repository.

## Try it without changing your live Hermes

The code targets Python 3.11+ and Git, with no third-party runtime dependencies. This build was exercised on Linux with Python 3.14.9; other platforms and the minimum interpreter remain unverified. The pipe reader uses Unix selector behaviour.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/demo.py
hermes plugins doctor . --ci
hermes plugins validate .
```

Run a historical evidence check against your own reviewed full corpus clone:

```sh
git clone https://github.com/drfinlaymccall/australia-regulations.git ../australia-regulations
python3 scripts/corpus-smoke.py --corpus ../australia-regulations
```

The clone command downloads public source; it is a deliberate operator setup step, not plugin behaviour. The pinned source manifest records `record_to: 2026-09-01` and `checked_on: 2026-10-31`. A successful 2026-01-01 query does **not** prove coverage of today's law. The smoke report prints metadata and hashes, not legal conclusions.

## Install for a selected Hermes profile

After reviewing the source and a pinned release, use the supported Git installer:

```sh
hermes -p default plugins install https://github.com/drfinlaymccall/hermes-australian-legal --ref FULL_REVIEWED_40_CHARACTER_SHA --no-enable
hermes -p default plugins enable hermes-australian-legal
```

Replace the placeholder with the reviewed commit; it is deliberately not a runnable SHA. The repository remains private during development. Access and a later publication decision are separate from installation. Restart a CLI session to discover the plugin. Restart a gateway only at an agreed time. Do not enable it across every profile.

For a local development checkout, a directory symlink under the selected profile's `plugins/` plus `hermes plugins enable` is sufficient. Plugin Doctor tests a local path in isolation without installing into a live profile.

In a fresh session, run `/au-legal`, load `hermes-australian-legal:counsel-preparation`, and provide the path to the reviewed corpus clone. Every corpus tool requires that path explicitly. Use invented clauses until confidentiality and privilege questions are resolved.

## Boundaries and installation disclosures

- **Network:** the plugin makes no network calls, starts no MCP server, and has no updater or telemetry. Its Git operations read local data only. The host chat provider can receive clause text and tool output supplied to a conversation. Offline retrieval does not mean confidential AI processing.
- **Reads:** the operator-selected corpus clone is outside plugin data. Tools read committed Git objects, tags and corpus metadata. They do not scan mail, client folders, browser profiles, secrets or arbitrary matter files.
- **Processes:** bounded `git` subprocesses, argv only, no shell. No long-lived services, cron jobs or background workers.
- **Writes:** tools return JSON only. They do not update a matter register, send an email, file, purchase or modify the corpus. Unit tests create disposable fictional Git repositories. Operator-run scripts print results; report redirection is explicit.
- **Credentials:** none requested or stored by this plugin. No `.env`, auth store, keychain or browser credential access.
- **Legal coverage:** selected federal instruments only. Acts, State law, case law and tax need other authoritative sources and qualified review. Derived source history and metadata can be incomplete or wrong.
- **Approval:** review-gate booleans are user attestations. This prototype cannot prove counsel signed anything and cannot block unrelated Hermes tools. It does not enforce a legal-practice workflow across the host.
- **Quote checks:** literal matching is not verification that a legal proposition follows, that a supplied source is authentic, or that a snippet is sufficient.
- **Arithmetic:** one hypothetical capped linear earn-out formula, not a parser for bespoke deal terms. Money inputs must use the same unit and currency. Round-half-even is explicit.

## Evaluation and release

See [Evaluation plan](docs/Evaluation-plan.md) for the separate software, host, corpus, LLM behaviour and qualified-review gates. Only executed tests belong in [Verification](docs/Verification.md). A passing unit suite is not legal validation.

[Hackathon preparation](docs/Hackathon.md) contains the verified entry steps, a demo outline and release holds. Public visibility, catalog PR, video post and submission form require Finlay's final approval. No entry has been submitted.
