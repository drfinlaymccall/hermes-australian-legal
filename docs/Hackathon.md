# Hackathon preparation — not submitted

## Verified organiser instructions

The [Nous Research announcement](https://x.com/NousResearch/status/2118094256438936062) states:

- Submissions due **11 November 2026, 5 PM EST** — **12 November 2026, 9 AM AEDT in Sydney**.
- Open a plugin-catalog PR, post a working demo on X tagged `@NousResearch`, and submit both links in the [entry form](https://form.typeform.com/to/FwJLvOln).
- Keep the demo under 90 seconds.
- Judges consider usefulness, reliability, polish and creativity; they favour functionality beyond a prompt or skill.
- A form can be submitted once the PR is open. Catalog admission and judging are not guaranteed.

Check the organiser page again before submission. This document is a preparation packet, not an entry receipt.

## Proposed positioning

**Hermes Australian Legal — dated evidence, visible limits, counsel-led decisions.**

By Finlay McCall. Show the executable difference: a dated Git lookup with source metadata, an after-record refusal, an ungraded review without a playbook, and a transparent hypothetical calculation. Do not claim “an AI lawyer”, legally correct advice, complete current-law coverage or a proven improvement over Claude.

## Demo outline, 75–85 seconds

1. Introduce Finlay and the purpose: prepare better source-linked questions for Australian counsel.
2. Show `/au-legal` and the corpus's visible end date.
3. Retrieve a historical provision, showing date, compilation and source link. Retain caveats.
4. Ask for a date beyond the record. Show the refusal rather than a plausible answer from memory.
5. Demonstrate an invented clause with no approved playbook: ungraded, not a red line.
6. Show one exact-decimal earn-out scenario and its explicit assumptions.
7. Close with source credits, “not legal advice”, and the test report's actual scope.

Use only invented transaction material and public source excerpts. Do not record desktop notifications, private paths, login panels, real counterparties or privileged advice.

## Release holds

- [ ] Paired model behavioural evals executed and reviewed; scores not inferred from unit tests.
- [ ] Independent code/privacy review accepted and source licensing/credit checked.
- [ ] Qualified reviewer accepts the domain boundaries; unsupported capability claims removed.
- [ ] Full public tree, Git history, author metadata and remote issues/logs reviewed.
- [ ] Finlay approves the public repository and credit line.
- [ ] Fresh validation passes at the exact 40-character catalog pin.
- [ ] Finlay approves catalog PR text, public video and final form submission.

## Draft catalog fields

Name `hermes-australian-legal`; version `0.1.0`; maintainer `drfinlaymccall`; tier `community`; minimum Hermes `>=0.22.5`.

Use the exact published commit and verified HTTPS repository URL in the catalog entry. Declare the five native tools, no hooks/middleware/env requirements. Disclose local Git subprocesses, reads from the selected corpus, no plugin network or telemetry, and that the host LLM receives supplied evidence. Do not add an invented SHA or represent a private repository as cloneable by everyone.
