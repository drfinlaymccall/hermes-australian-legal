# Design and workplan

## Product boundary

A Hermes-native evidence workbench for Australian deal preparation, led by Finlay McCall. Its user prepares a narrow, traceable pack for qualified counsel. It never presents a legal or tax conclusion as a checked result.

## Translation decisions

1. Preserve the original Claude workflow's dated-source discipline, counsel playbook requirement, tax referral and caveat retention.
2. Strengthen confidentiality: the source skill allowed a warning and continued review. This prototype blocks the preparation gate until the user attests permission and privilege review. This still cannot undo text already supplied to the host model.
3. Implement native tools rather than merely rename skills. Keep reusable logic independent of Hermes so unit tests exercise the same code.
4. Keep the regulations repository separate. Read committed Git objects, not mutable worktree law files. Do not auto-pull and do not execute code from the corpus. Use exact instrument slugs and provision paths rather than fuzzy legal guesses.
5. Add an explicit corpus end-date refusal. The inspected manifest ends on 2026-09-01; current-law claims cannot rest on this clone alone.
6. Preserve Finlay's authorship and acknowledge related upstream work. Start with clean history and synthetic examples; do not export personal legal matters.

## Native architecture

- `plugin.yaml` declares five tools, tested minimum Hermes version and authorship.
- Root `__init__.py` registers tools, the skill and a status slash command through public APIs only.
- `au_legal/corpus.py` validates corpus metadata, confines Git reads, resolves a dated tag and returns provenance plus caveats.
- `au_legal/workflow.py` provides an attestation gate, exact-decimal scenario formula and literal quotation checks.
- `skills/counsel-preparation/` describes how the host model uses those outputs and where counsel retains authority.
- `scripts/` supplies repeatable synthetic and historical smoke checks. No daemon, external API, key, automatic state write or core patch.

The callable quote checker accepts caller-supplied data. Its result is only a literal match, never authenticated legal evidence. Record integrity requires comparison with the trusted clone and official Register.

## Implemented vertical slice

Inspect coverage -> read a historical provision -> retain date and caveats -> check review prerequisites -> calculate an explicit hypothetical scenario -> prepare an unsent counsel question.

## Deliberately deferred

- Persistent matter storage and issues-register CRUD, secure deletion and retention policy.
- Automatic redline parsing, full playbook grading, negotiation-loop detection and counsel-pack export.
- Tax, Acts, case law, State legislation, global-law multi-jurisdiction adapters and current Register refresh.
- Hosted models, autonomous messages, filing, payments, credential storage, Desktop panels and background monitors.

These are not implemented simply because the Claude workflow describes them.

## Work sequence and gates

1. **Discovery:** pin source repos and licence boundaries; map public Hermes APIs and hackathon rules.
2. **Build:** write executable contracts and unit tests; implement the minimal read-only slice.
3. **Host proof:** run Plugin Doctor and catalog validation; invoke the registered handlers, not just imports.
4. **Data proof:** exercise a real historical provision and an after-record refusal; fingerprint the clone before and after.
5. **Behaviour proof:** execute the paired synthetic benchmark in the evaluation plan, retain model settings, raw traces, errors and blind scores.
6. **Review:** independent code/privacy review plus qualified legal-domain review for any accuracy or suitability claim.
7. **Publish only after approval:** private linked GitHub repo first; review public tree/history/metadata, then decide visibility, catalog PR, short video and form submission separately.

## Acceptance for this prototype

- Real runnable plugin, unit tests and narrow host/corpus smoke receipts.
- Human-scannable plan, provenance, evaluation and hackathon documents.
- No private deals, credentials, raw transcripts or legal merits claims in version control.
- Exact local paths, commit and private remote identity verified before handoff.

A prototype standup is not hackathon admission or counsel-approved software.
