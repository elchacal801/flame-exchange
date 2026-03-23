# Baseline: AI-Generated vs Human-Written Fraud Content Norms

```yaml
---
id: BL-0033
title: "AI-Generated vs Human-Written Fraud Content Norms"
category: Baseline
date: 2026-03-22
author: "FLAME Project (sourced from 2026 Technical Landscape Report, Stylometric Research)"
related_tps:
  - id: TP-0043
    relationship: related-to
  - id: TP-0025
    relationship: related-to
tags:
  - ai-generated-content
  - stylometric-detection
  - nlp
  - phishing-detection
  - baseline
---
```

## Summary

This baseline defines normal stylometric profiles for human-written versus AI-generated fraud content, enabling detection of AI-authored phishing emails, romance scam messages, and social engineering communications. Research demonstrates XGBoost with 60 stylometric features detects GPT-4o-generated phishing at 96% accuracy and 99% AUC. Fine-tuned BERT achieves F1=0.99 on 181,781 phishing emails. DetectGPT achieves ~0.95 AUROC via zero-shot statistical signatures. These baselines calibrate DL-0139 (stylometric detection) thresholds. AI-generated phishing achieves 43–81% click-through rates versus 18–69% for traditional methods, making detection critical.

## Normal Patterns

* **Imperative verb ratio (human-written fraud):** Human-authored phishing and scam content typically uses imperative verbs at a rate of **0.05–0.12 per token**. AI-generated content exhibits higher imperative verb density (**0.13–0.22 per token**) due to instruction-following training that produces more directive language.

* **Clause density (human-written):** Human-written fraud content averages **1.2–1.8 clauses per sentence**. AI-generated content tends toward **2.0–3.0 clauses per sentence**, producing more complex sentence structures with embedded subordinate clauses.

* **First-person pronoun ratio:** Human-authored scam communications (especially romance fraud) use first-person pronouns at **0.04–0.08 per token**. AI-generated content shows lower first-person usage (**0.02–0.04**), reflecting a more impersonal or formal writing style.

* **Sentence length variance:** Human-written content shows **high variance** in sentence length (standard deviation >8 words). AI-generated content shows **lower variance** (standard deviation 4–7 words), reflecting the model's tendency toward consistent output length.

* **Vocabulary diversity (Type-Token Ratio):** Human-written fraud content has TTR of **0.55–0.70** (moderate repetition of key terms). AI-generated content shows higher TTR (**0.70–0.85**) due to broader vocabulary deployment.

* **Urgency and authority marker frequency:** Both human and AI-generated fraud content use urgency/authority markers, but AI-generated content distributes them **more uniformly across the text** rather than concentrating them in the opening and closing paragraphs as human writers do.

## Baseline Values

| Metric | Human-Written Fraud | AI-Generated Fraud | Detection Threshold |
|---|---|---|---|
| Imperative verb ratio (per token) | 0.05–0.12 | 0.13–0.22 | >0.15 (elevated) |
| Clause density (per sentence) | 1.2–1.8 | 2.0–3.0 | >2.2 (elevated) |
| First-person pronoun ratio | 0.04–0.08 | 0.02–0.04 | <0.03 (anomalous for scam context) |
| Sentence length std deviation (words) | >8 | 4–7 | <6 (anomalously uniform) |
| Vocabulary diversity (TTR) | 0.55–0.70 | 0.70–0.85 | >0.75 (elevated) |
| Urgency marker distribution uniformity | Concentrated (opening/closing) | Uniform across text | Distribution entropy >0.8 (anomalous) |
| Composite stylometric score (XGBoost) | <0.40 | >0.75 | >0.75 (high confidence AI) |

## Measurement Methodology

Extract stylometric features using spaCy NLP pipeline for tokenization, POS tagging, and dependency parsing. Calculate imperative verb ratio by identifying verb tokens with imperative mood or sentence-initial position with base verb form. Clause density measured by counting clausal dependencies (advcl, relcl, ccomp, xcomp) per sentence. First-person pronouns identified via POS=PRON and lemma in {I, me, my, mine, myself, we, us, our, ours, ourselves}.

Sentence length variance calculated as standard deviation of word counts across all sentences in the message. Vocabulary diversity uses Type-Token Ratio (unique lemmas / total tokens) on the first 200 tokens to normalize for text length.

Composite score derived from XGBoost model trained on 60 features (as documented in research achieving 96% accuracy on GPT-4o content). Model should be retrained quarterly as LLM output characteristics evolve.

## Data Sources

* **Email security platforms:** Raw email body text for stylometric analysis.
* **Chat/messaging platforms:** Customer-facing communication transcripts for romance fraud and social engineering detection.
* **EMSCAD, Nazario phishing corpus:** Labeled datasets for model training and baseline calibration.
* **GPT-4o/Claude/Gemini output samples:** AI-generated content samples for comparative analysis.

## Application

DL-0139 should use these baselines to calibrate stylometric detection thresholds. The composite XGBoost score >0.75 threshold provides high-confidence AI-generated content detection. For lower-confidence triage, individual feature thresholds (imperative verb ratio >0.15, sentence length std dev <6, TTR >0.75) can be used independently.

These baselines require periodic recalibration as LLM output characteristics evolve. New model versions may produce content with different stylometric profiles. Quarterly retraining against fresh AI-generated samples is recommended.
