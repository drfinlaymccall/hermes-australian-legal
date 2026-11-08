# Prototype verification

Executed on 8 November 2026. This is a software standup receipt, not a legal-accuracy evaluation or a completed behavioural benchmark.

## Public prototype release follow-up

Independent read-only release review found no unresolved privacy or executable-code blocker for a public experimental prototype. Both findings were addressed: the rendered README/entry explicitly disclose synthetic-only prototype scope and unrun behavioural/legal review, and the quote checker now rejects non-string or oversized source text. A new regression first failed on the original list-membership behaviour, then passed after the guard.

The updated complete suite passed **43 tests**, along with the synthetic demo, Plugin Doctor, catalog validation and real historical smoke. `hermes plugins validate . --install-deps` also passed. The retained scanner caution now points to the host-model disclosure at README line 64. The older 42-test results below describe the initial standup, not a second or larger behavioural evaluation. The earlier real host/model smoke was not repeated for the source-type guard.

## Reproducible local gates

Command:

```sh
python3 scripts/verify.py --corpus /path/to/reviewed/australia-regulations
```

Observed:

- Unit suite: **42 tests passed**. Fictional Git fixtures cover valid historical reads, date/metadata validation, path traversal and symlink refusal, bounded output/timeouts, hostile Git environment settings, caveats and unchanged corpus data.
- Workflow tests cover missing permission, absent playbook, strict booleans, capped/floored decimal calculations, explicit half-even rounding, non-finite/unsafe inputs, literal quote checking and date mismatch.
- Plugin contract tests invoke registered handlers and verify the actual skill file and slash command. Their lightweight context is not presented as a real host.
- Synthetic demonstration returned `ungraded` without an approved playbook and a hypothetical payout of `63.75` from the declared formula.
- **Hermes Plugin Doctor passed**, using host discovery, manifest parsing, import and registration in isolation: five tools and no hooks.
- **Hermes catalog validation passed**: manifest, compatibility floor, loadability, registration declarations, no tool collisions, dependency checks and no core override.
- One scanner warning remains: `context_exfil` on the README's disclosure that the host chat provider can receive supplied clause text and tool output. The plugin makes no network call. The warning was retained and reviewed as a disclosure match, not hidden or described as a clean scanner result.

Tested host: Hermes `0.22.5`, local revision `bf0203a794a0`, Linux, Python `3.14.9`. Minimum-interpreter and other-platform behaviour are not yet verified.

## Actual corpus integration

The historical smoke used:

- Corpus commit: `1c5a2ebf5c036ef32d91118e2864f48a73c95134`.
- Instrument: `competition-and-consumer-notification-of-acquisitions-determination-2025`.
- Provision file: `s-1-9.md`.
- Requested date: `2026-01-01`.
- Selected compilation commit: `4d7079ee7c4f3c433c7e8cbeec390507dcea4818`.
- Retrieved text SHA-256: `2f7b6621934ce68dd6b5569470569b51889c621ff7a951b4a66125d15b64d94b`.
- Declared record end: `2026-09-01`.
- After-record request `2099-01-01`: refused.
- Corpus status and HEAD were unchanged by the smoke. Fictional corpus tests separately compare the complete tree and Git database before and after reads.
- Caveats were retained, including derived-source status, compilation-only history, unrecorded scope and continuity limits. No legal conclusion or actual legislation excerpt is stored in this receipt.

This did not independently reproduce the corpus build, compare all words against the official Register or establish current-law coverage.

## Real Hermes tool invocation

A fresh default-profile chat was asked to call `au_legal_earnout` once with synthetic inputs: metric `125.50`, threshold `100`, rate `2.5`, cap `1000`.

The actual streamed host trace showed tool discovery, `au_legal_earnout` invocation, successful JSON output with payout `63.75`, and a final response identifying a hypothetical formula rather than legal advice. This proves one real host/model dispatch, not the whole behavioural evaluation. The model identity was not exposed in that stream and is not inferred here.

The first attempt using the advertised `--run-budget` flag was refused by the gateway CLI adapter before inference. The second used supported options, exited zero and produced the trace above. No approval bypass, model-policy change or gateway restart was used.

The local development plugin was linked and enabled in the **default profile only**. Hermes reported gateway-command reload and tools deferred to the next session. Fresh-chat dispatch succeeded. Existing chats were not reset; other profiles were not modified.

## Still not evaluated

- The paired 16-case model benchmark, repeated trials, blinded scoring and holdouts.
- Qualified Australian lawyer/adviser review, legal applicability or confidentiality/privilege assurances.
- Full Claude feature parity, persistent matter storage, automated grading, negotiation-loop detection or external delivery.
- Catalog maintainer review, hosted CI, public availability, demo video or hackathon acceptance.

The prototype is ready for bounded synthetic user testing. A public or legal-reliability claim requires the separate gates in `Evaluation-plan.md` and Finlay's explicit release approval.
