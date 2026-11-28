# OpenVEF Source-Access and Provenance Log v1.1

**As of:** 22 November 2026  
**Purpose:** Record canonical URL, version/date, what was inspected and hash status for full-text claims. The local pack does not retain the original source PDF binaries, so no source-PDF SHA-256 is invented. Where available, the SHA-256 of the local review record is supplied separately; it is not a substitute for the original PDF hash.

| Source | Canonical URL/version/date | Access record in current review | Original PDF SHA-256 | Local review-record SHA-256 / state |
|---|---|---|---|---|
| *LLM-Aided Verification Gap Detection* — Praveen Kumar Vagala | DOI: https://doi.org/10.36227/techrxiv.177069683.39144593/v1 ; v1; posted 10 Feb 2026 | The Step 3 independent audit reports access to the abstract only; detailed method claims from the earlier draft are not verified for this v1.1 provenance record. Earlier secondary notes differ on whether injection was automated or manual; because the independent audit had abstract-only access, neither description is verified from the paper text in this pack. The original PDF and a retrievable mirror/version record were not retained; page-image verification is pending. | NOT CAPTURED — obtain original PDF and compute before formal submission | Literature review record: SHA-256 0e6bd491549561d4cdf9af9c16b84980f39e3bb029dcca93477a874e4d33d974 |
| DVBench | https://arxiv.org/abs/2611.25066 ; arXiv:2611.25066v1; 18 Nov 2026 | Current review opened canonical arXiv PDF text (75 pages). Page-image review was not completed in this pass. The local working pack does not retain the PDF binary. | NOT CAPTURED — download and hash canonical v1 PDF before formal submission | Literature review record: SHA-256 0e6bd491549561d4cdf9af9c16b84980f39e3bb029dcca93477a874e4d33d974 |
| CovR | https://arxiv.org/abs/2609.19189 ; arXiv:2609.19189v2; 19 Sep 2026; MLCAD 2026; DOI 10.1145/3831599.3840347 | Current review opened canonical arXiv PDF text (15 pages). Earlier Step 3 log reports selected page images inspected. Literature must retain authors' term “RTL mutants”; note separately that MCY operates post-synthesis. PDF binary not retained locally. | NOT CAPTURED — download and hash canonical v2 PDF before formal submission | Literature review record: SHA-256 0e6bd491549561d4cdf9af9c16b84980f39e3bb029dcca93477a874e4d33d974 |
| *Verify the Verifier* | https://arxiv.org/abs/2611.26588 ; arXiv:2611.26588v1; submitted 19 Nov 2026 | Current review opened canonical arXiv PDF text (7 pages). Visual page-image verification remains pending. Prior Step 1 review and resolution artifacts are retained. | NOT CAPTURED — download and hash canonical v1 PDF before formal submission | Step 1 analysis record: SHA-256 9561e129f017b270c86adcd16b29c65326f67063721084701eefa367b7682af0; literature review record: SHA-256 0e6bd491549561d4cdf9af9c16b84980f39e3bb029dcca93477a874e4d33d974 |
| SecTB-RTL | https://arxiv.org/abs/2609.19844 ; version to reconfirm from canonical author line; 2026 | Prior Step 3 review used arXiv HTML and Google Research publication page; resolution states the exact 1,860/1,857/9 funnel. The v0.7–v0.9 passes did not independently re-open the full PDF. | NOT CAPTURED | Literature review record: SHA-256 0e6bd491549561d4cdf9af9c16b84980f39e3bb029dcca93477a874e4d33d974 |

## Access-statement reconciliation

- TechRxiv: the independent Step 3 audit reports abstract-only access. Do not rely on detailed full-text claims from the earlier draft until the exact source PDF is retrieved, versioned and inspected. The reported automated/manual injection discrepancy remains unresolved.
- DVBench: extracted text is now directly available from the canonical arXiv PDF. Visual page-image inspection is not claimed.
- CovR: earlier review states that selected page images were inspected; the full text was also extracted. This does not imply every page image was visually inspected.
- Verify the Verifier: canonical v1 PDF text is now available in the current review. Visual page-image verification remains pending. Do not describe this as “all PDF pages visually inspected.”
- SecTB-RTL: its funnel is corrected to 1,860 scheduled, 1,857 provider-accepted, 9 production-semantic-valid. The v0.7 source log still requires the exact canonical version and original PDF hash.

## Required source-provenance closure before external submission

1. Download the exact cited PDF version for each row.
2. Compute SHA-256 over the original PDF bytes and record retrieval date/time.
3. Confirm version, authors, posted date and any venue/DOI metadata from the canonical source.
4. For TechRxiv, retrieve the exact PDF, inspect it page-by-page and resolve whether the reported automated/manual mutation-injection discrepancy is real; do not guess from abstract or secondary notes.
5. For *Verify the Verifier*, inspect page images if accessible and update the Step 1 analysis matrix only where the exact content is verified.
6. Re-run forward-citation and IEEE Xplore/ACM DL searches before submission.

**Important:** A SHA-256 of a local review Markdown file authenticates that review file only; it does not authenticate the source PDF.


## v0.7 independent audit note (22 November 2026)

The v0.7 auditor explicitly did not retrieve or visually inspect any source PDF during that audit. DVBench figures remain based on the pack's recorded text-access entry; no fresh primary-source verification is claimed. Original source-PDF binaries and SHA-256 hashes remain NOT CAPTURED unless a specific row is updated with the actual file and hash. Re-check DVBench version/citations and all full-text claims before external submission.


## v0.8 independent audit note (22 November 2026)

The v0.8 auditor did not retrieve or visually inspect any source PDF. DVBench and CovR details in this pack remain based on the previously logged text-access record and were not independently re-fetched during that audit. Original source-PDF binaries and SHA-256 hashes remain NOT CAPTURED. Review-document hashes are not source-PDF hashes.


## v1.1 provenance note

The v1.0 independent auditor did not retrieve or inspect source PDFs. v1.1 does not add a new source-access claim. Original source-PDF SHA-256 values remain `NOT CAPTURED`; review-pack file hashes are not substitutes. The current audit's static fixture/package checks do not verify literature claims or provider/sandbox behavior.

---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
