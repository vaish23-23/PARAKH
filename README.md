# Parakh (परख): check before you trust

A private scam-message checker for first-time investors. Paste or speak a WhatsApp / Telegram / SMS message
(English, Hindi, Hinglish) and get a risk score, highlighted warning words, plain reasons and safe next steps.
Built for the SANGYAN hackathon (Track A / E). It gives no stock tips and stores nothing.

## Run
Open `index.html` in a browser. No server, no install. Fonts fall back to system fonts when offline.

## Structure
- `index.html`: the whole app (UI, rule engine, model weights, inference) in one file.
- `ml/gen_data.py`: builds the labelled dataset (`dataset.csv`).
- `ml/prep.py`: scores texts with the app's rule engine (needed by `train.py`).
- `ml/train.py`: trains and evaluates the model, writes `model.json` and `metrics.json`.
- `ml/ood.py`: 31 hand-written messages used only for testing.
- `ml/ml.js`: browser inference code (same maths as training). `ml/parity.js` checks JS against Python.
- `ml/e2e.js`: end-to-end check on sample messages.
- `MODEL_CARD.md`: data, results and limits.

## Retrain
```
cd ml
python3 gen_data.py      # or add your own rows to dataset.csv (text,label,type)
python3 prep.py
python3 train.py         # prints results, writes model.json
node parity.js           # confirms browser output matches Python
```
Then paste the new `model.json` into `var MODEL=` in `index.html`.
Needs Python 3 (scikit-learn, numpy, pandas) and Node 18+.

## How it works
Score = 0.9 x text model (character n-gram TF-IDF + logistic regression) + 0.1 x rule engine. Alert threshold 0.45.
Training data is synthetic; see `MODEL_CARD.md` for results and limits.
Not investment advice. Not affiliated with SEBI.
