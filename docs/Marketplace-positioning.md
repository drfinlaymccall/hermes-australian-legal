# Marketplace positioning review

Status: research and listing draft, not a catalog submission. Inspected on 8 November 2026.

## Recommendation

Position this as **Australian deal preparation with dated regulatory sources**, by Finlay McCall. Do not claim the first legal plugin, an AI lawyer, complete Australian law, or automatic contract review. The current implementation's useful distinction is the combination of a separate dated Australian instruments corpus, explicit coverage refusals, counsel-playbook readiness, transparent scenario arithmetic and literal quote checks.

Confidence: high that relevant legal tools already exist; moderate that this is a differentiated listing within the inspected snapshot. This is a positioning judgement, not evidence of superiority or market demand.

## Search coverage and limits

The live page carried 1,200 unique plugin records, including 1,168 community records. The public catalog tree contained 1,200 entry YAML files, plus its README and removal list. Its inspected tree identity was `221299121ceb16d5f392ffcc1ddd18fcf83cb167`.[1]

The browser's single-word `legal` search showed only two results. A broader programmatic search of all displayed names/descriptions found 15 candidates using legal, law, legislation, statutes, regulatory, contract, counsel, litigation, compliance and patent terms. We read the complete pinned catalog descriptions of nine relevant or plausible comparators and the marketplace README pages of the five direct comparators below. Marketplace descriptions are truncated in the inventory, so a metadata keyword miss is not proof that no capability exists.

No dedicated Australian deal-preparation listing surfaced in this bounded review. Australian legal coverage does already appear in Precleared's email-compliance entry.[9] Do not turn this finding into a global novelty claim. Open-PR searching also found proposed IAJUS Brazil/Portugal legal research connectors; those are pending remote-MCP catalog additions, not evidence of a merged plugin listing.[13]

No competitor was installed, run, benchmarked or security-certified. All competitor capability and performance statements below are descriptions from their catalog or author documentation.

## Direct comparators and their positioning

### Diké (`dike`) — Chilean citation checking

Its core promise is narrow and evidence-led: check article citations against a local, hash-identified copy of 25 Chilean statutes, returning identifiers, URLs and text hashes or an explicit unresolved result. It explicitly distinguishes citation correspondence from whether a provision supports an argument and whether a dated copy is current law.[2]

The reviewed code pin is `9780e467ec31d4635eb559e4c09bd49f17e178de`. This is our closest positioning analogue for visible limits and evidence, but our literal quote checker does **not** authenticate arbitrary citations or provide equivalent corpus-integrity guarantees. Its pinned README still says “not in the catalog yet”, despite the live catalog containing it. Current catalog state is the stronger listing evidence.

### `de-law` — source-first German and EU law

It leads with a concrete task: retrieve the wording, version status, reference and source line for one provision, plus German federal court decisions. It names practical audiences, including founders, compliance staff and legal teams. It explicitly says “Legal texts, not legal advice” and discloses current consolidated-text coverage rather than historical versions.[3]

Reviewed pin: `4be88cd048c5ae4d37491ba4e6eb88996886ae7e`. Borrow its reader-first examples and source/version presentation, not a claim that our smaller corpus has equivalent coverage.

### `jp-egov-law` — dated Japanese provision lookup

It promises official Japanese article text, law number, effective date and source links, with dated reads, revision comparisons and amendment information. It names the e-Gov API, no-key setup and concrete user questions. Its documentation also reports model bypasses and missing-tool behaviour rather than implying that instructions guarantee tool use.[4]

Reviewed pin: `2e96dd28108250b374160077d6e1d9fa4dea55f1`. Historical/date-aware retrieval is therefore **not unique to us**. Our differentiation is jurisdiction, a local Git record and the deal-preparation workflow.

### `corpus` — hosted US legal research and formation

This is a hosted US legal-research and business-formation connector with two skills. Its listing separates research from intake/formation and discloses vendor-authored marketing text, founder-data transmission and transaction gates.[5]

Reviewed pin: `53db664236201a885a3a7133ffe62476293faace`, subdirectory `plugins/corpus`. We should not imitate a broad legal-service promise or formation/payment functions that we do not implement. Our plugin makes no plugin-owned network calls and adds no formation or payment service; the host model still receives supplied conversation data.

### `crosodo` — a specific regulatory job

It targets cottage-food and home-bakery rules at US state/county level. It leads with recognisable user questions and discloses a hosted, hand-maintained dataset and no-legal-advice boundary.[6]

Reviewed pin: `0acc98a34c1d58251ff1047c67b74ed2bc1b905b`. The lesson is a clear job and jurisdiction, not a generic “legal assistant” label.

## Adjacent and false-positive matches

- **Precleared:** outbound-email legal/compliance checks, including Australian rules, using a hosted service and approval routing. Relevant to compliance positioning, not Australian acquisition preparation.[9]
- **Patsnap:** patent/prior-art and scientific-research search through a hosted service. IP-adjacent rather than a deal-review competitor.[10]
- **Ethics Filter:** rubric-based decision scoring, including compliance. Its score is not verification of legislation or legal compliance.[11]
- **Redline:** a Desktop Markdown/source-code annotation tool. The name does not mean legal contract redlining.[12]

## Proposed listing

**Display title:** Australian Deal Preparation

**Stable plugin id:** `hermes-australian-legal`

**Author/maintainer:** Finlay McCall / `drfinlaymccall`

**Opening copy:**

> Prepare Australian deal questions for counsel using dated regulatory sources. Read selected Commonwealth instruments from a local Git corpus, retain compilation commits and caveats, check review prerequisites, and calculate explicit hypothetical earn-out scenarios. Includes literal quote checks. Preparation for counsel, not legal or tax advice.

**What to show in the demo:** one real historical lookup with source/date, an after-record refusal, an ungraded result without an approved playbook, and one transparent calculation. Keep source lookup separate from a legal conclusion.

**Required limits:** selected instruments only; the inspected corpus ends on 1 September 2026; no Acts, case law, State law or tax coverage; no automatic legal applicability finding; no authenticated counsel approval; no complete document redlining, register persistence or negotiation-loop detection.

The existing 42-test and host-dispatch receipts support narrow software claims. They do not support legal-accuracy, lawyer-approved, measured-improvement or complete behavioural-reliability claims. The 16-case behavioural protocol is designed but not yet executed.

## Two different publication surfaces

Teknium's post asks people to reply with their plugin so others can browse it. That is a social showcase, not marketplace admission.[8]

Marketplace admission requires a public cloneable repository, a full reviewed commit pin, validation, a catalog YAML PR to `NousResearch/hermes-agent`, and maintainer review/merge. The plugin page is built from that entry and its pinned README. There is no self-service “add” button that makes a listing accepted.[7]

`submission/hermes-australian-legal.yaml` is a **draft** against the currently tested prototype pin. Do not submit it while the source remains private or represent it as accepted. Our product's review gates remain open; this search does not waive them. Before public release, reconcile the README's private-development language, repeat exact-pin validation and privacy review, then obtain approval for visibility, catalog PR, demo and social text.

## Invalidation and next decision

Refresh this comparison before submission if the catalog, competitor pins, our implementation or source coverage changes. New legal plugins and pending entries can change the landscape quickly. The next decision is to accept or revise the narrow positioning, then complete the outstanding release checks. No visibility change, public PR, X reply or hackathon form was made in this research step.

## Sources

[1] https://hermes-agent.nousresearch.com/marketplace?kind=plugins&tier=community — Live community marketplace inventory
[2] https://hermes-agent.nousresearch.com/marketplace/dike
[3] https://hermes-agent.nousresearch.com/marketplace/de-law
[4] https://hermes-agent.nousresearch.com/marketplace/jp-egov-law
[5] https://hermes-agent.nousresearch.com/marketplace/corpus
[6] https://hermes-agent.nousresearch.com/marketplace/crosodo
[7] https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission
[8] https://x.com/Teknium/status/2119270884800401440?a=gZW1UAuC8acYwO2lDAY&s=19
[9] https://raw.githubusercontent.com/NousResearch/hermes-agent/main/plugin-catalog/precleared.yaml — precleared catalog entry
[10] https://raw.githubusercontent.com/NousResearch/hermes-agent/main/plugin-catalog/patsnap.yaml — patsnap catalog entry
[11] https://raw.githubusercontent.com/NousResearch/hermes-agent/main/plugin-catalog/ethics-filter.yaml — ethics-filter catalog entry
[12] https://raw.githubusercontent.com/NousResearch/hermes-agent/main/plugin-catalog/redline.yaml — redline catalog entry
[13] https://github.com/NousResearch/hermes-agent/pull/142850 — Pending IAJUS Brazil and Portugal MCP entries
