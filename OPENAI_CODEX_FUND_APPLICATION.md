# OpenAI Codex Open Source Fund — Application

> **Project:** OpenDraft  
> **Applicant:** Federico De Ponte  
> **Repository:** https://github.com/federicodeponte/opendraft  
> **License:** MIT  
> **Stars:** 128

---

## 1. Project Overview

**OpenDraft** is an open-source Python engine that decomposes long-form academic writing into inspectable agent steps: source discovery, extraction, outline generation, section drafting, citation validation, polishing, and export to PDF/DOCX/LaTeX.

Unlike general-purpose LLMs that hallucinate citations 30–50% of the time, OpenDraft verifies every source against CrossRef, OpenAlex, Semantic Scholar (200M+ papers), and arXiv before inclusion. The pipeline is fully open source under the MIT license.

**Key differentiators:**
- 19 specialized agents (not a single black-box model)
- Every citation verified against real academic databases
- Human review required — not an autonomous author
- Reproducible pipeline: same topic → same inspectable steps every time

---

## 2. How We Use (or Plan to Use) OpenAI Models

OpenDraft already supports OpenAI GPT-5.5 models as one of several providers. We use OpenAI models for:

| Use Case | Current Status |
|----------|---------------|
| Research agent (literature discovery) | ✅ Active |
| Outline agent (chapter/section structure) | ✅ Active |
| Writing agent (section drafting) | ✅ Active |
| Citation verification cross-check | ✅ Active |
| Polish agent (language refinement) | ✅ Active |
| **PR review automation** | 🔄 Planned (Codex) |
| **Regression test generation** | 🔄 Planned (Codex) |
| **Issue triage & labeling** | 🔄 Planned (Codex) |
| **Contributor onboarding templates** | 🔄 Planned (Codex) |

---

## 3. How We Would Use the Grant

We would use the API credits and Codex access to improve OpenDraft **as an open-source project** — not just to generate more drafts.

### 3.1 Automated Evaluation & Regression Testing

**Problem:** Every code change to the 19-agent pipeline risks degrading citation accuracy or draft quality.

**Solution:** Build automated evaluation runs using OpenAI models as a reference benchmark.

- Generate 20 fixed-topic drafts before/after each PR
- Compare: verified citation rate, source coverage, hallucination rate, draft coherence
- Fail CI if any metric degrades >10%
- Publish results in [EVALUATION.md](EVALUATION.md)

**Credits needed:** ~500 eval runs/month = ~$150/month

### 3.2 Codex-Assisted Maintainer Workflows

**Problem:** As a solo maintainer + contributors, PR review, issue triage, and release checks consume significant time.

**Solution:** Use Codex CLI to automate OSS maintenance tasks.

- **PR review:** Codex reviews agent logic changes, prompt modifications, and citation handler updates
- **Test generation:** Codex writes regression tests for new agents or modified prompts
- **Issue triage:** Codex suggests labels, identifies duplicates, and proposes fixes
- **Release workflow:** Automated changelog generation, version bump verification, and pre-release eval runs

### 3.3 Contributor Templates & Documentation

**Problem:** New contributors struggle to understand the 19-agent pipeline.

**Solution:** Use Codex to generate and maintain contributor templates.

- Auto-generated "Add a new agent" templates with boilerplate, tests, and docs
- Auto-generated "Add a new citation validator" templates
- Auto-updated API documentation from docstrings

### 3.4 Public Reproducible Examples

**Problem:** Users can't easily inspect how the pipeline works end-to-end.

**Solution:** Use credits to generate and host public examples with full agent logs.

- 50+ reproducible research topics with complete agent traces
- Side-by-side comparison of OpenAI vs Gemini vs Claude outputs
- Public benchmark dashboard showing citation accuracy per provider

---

## 4. Why OpenDraft Fits the Fund

| OpenAI Criterion | OpenDraft Evidence |
|------------------|-------------------|
| Public open-source repo | ✅ MIT license, 128 stars, active issues/PRs |
| Real maintainer | ✅ Solo maintainer + 4 contributors, visible commit history |
| Uses AI models | ✅ Supports Gemini, Claude, OpenAI GPT-5.5 |
| OSS maintainer use case | ✅ Codex for PR review, tests, triage, release workflows |
| Public impact | ✅ Academic researchers, citation verification, transparent pipeline |
| Human review boundary | ✅ "What OpenDraft is NOT" section; not an autonomous author |

---

## 5. Project Links

- **Repository:** https://github.com/federicodeponte/opendraft
- **Hosted version:** https://openpaper.dev
- **Evaluation plan:** [EVALUATION.md](https://github.com/federicodeponte/opendraft/blob/master/EVALUATION.md)
- **Contributing guide:** [CONTRIBUTING.md](https://github.com/federicodeponte/opendraft/blob/master/CONTRIBUTING.md)
- **Security policy:** [SECURITY.md](https://github.com/federicodeponte/opendraft/blob/master/SECURITY.md)
- **Good first issues:** https://github.com/federicodeponte/opendraft/labels/good%20first%20issue

---

## 6. Maintainer Contact

- **Name:** Federico De Ponte
- **Email:** depontefede@gmail.com
- **GitHub:** @federicodeponte
- **Project:** OpenDraft / OpenPaper
