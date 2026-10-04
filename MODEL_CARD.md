# Parakh model card

**Task:** score an investment-related message (English / Hindi / Hinglish) for scam likelihood and explain why.
**Not for:** stock tips, price prediction, or any buy/sell/hold advice.

## Model
- Features: TF-IDF over character n-grams (2-5, word-bounded), sublinear tf, 6,000 features.
- Classifier: logistic regression (C=0.5). Weights are 136 KB JSON and run in the browser.
- Final score = 0.9 x model + 0.1 x rule engine. Alert threshold 0.45 (chosen on leave-family-out, favouring recall).
- Rules (fake broker addresses, missing SEBI number, OTP/AnyDesk requests, etc.) mainly produce the explanations.

## Data
`dataset.csv`: 3,665 template-generated messages, 7 scam families and 8 genuine families, with hard negatives
(genuine OTP SMS, SEBI warnings that mention scam words, AMC offers). **Synthetic. No real user messages used.**

## Evaluation (see `train.py`, `metrics.json`)
| Setting | Accuracy | Scam recall | Precision | AUC |
|---|---|---|---|---|
| Leave-one-family-out, rules only | 0.768 | 0.890 | 0.744 | 0.848 |
| Leave-one-family-out, final | 0.937 | 0.999 | 0.899 | 0.988 |
| 31 hand-written unseen messages, alert level 0.45 | - | 1.00 | 0.83 | 0.971 |
Random 5-fold CV gives 100% because templates repeat; it is reported but not meaningful.
JS vs Python probability difference: max 2.6e-4 (weight rounding).

## Known limits
Synthetic data, small unseen set (n=31), n-gram weights partly reflect generator style, and the model can be fooled by
rephrasing. A genuine SEBI warning can still be flagged (it mentions scam words). Needs real, consented data and
human review before public use.
