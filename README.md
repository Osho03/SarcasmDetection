# Sarcasm Detection (Headlines)

A desktop application that detects sarcasm in news headlines using a **CNN + RNN (LSTM)** deep learning model. Built with **PyQt5** and **TensorFlow/Keras**, with a neon dark-tech glassmorphism GUI.

## Features

- Load the (two) sarcasm headline datasets and merge/dedupe them
- Text pre-processing pipeline (cleaning, tokenization)
- Feature engineering with **GloVe 100d** word embeddings
- Hybrid **CNN → LSTM** classifier with 80/10/10 train/val/test split
- Live training log with accuracy/loss curves + confusion matrix / ROC plots
- Predict sarcasm on any headline instantly using the saved model
- Glassmorphism GUI with an attractive neon dark theme

## Pipeline (GUI tabs/buttons)

1. **Load Data** – loads `Sarcasm_Headlines_Dataset.json` + `_v2.json`, concatenates, drops duplicates → `Data/sarcasm.csv`
2. **PreProcess** – cleans text, drops empties → `Data/sarcasm_preprocessed.csv`
3. **Feature Engineering** – tokenizes and builds the GloVe embedding matrix → `Data/sarcasm_training.csv`, `Data/glove_embedding_matrix.pkl`
4. **Train CNN+RNN(LSTM)** – trains and saves the best model → `models/model.h5`, graphs + metrics in `models/` and `results/`
5. **Test Your Own Headline** – classify any headline text with the saved model

## Model Architecture

```
Embedding (GloVe 100d, trainable weights)
→ Conv1D (128 filters, kernel 3, ReLU, same padding)
→ MaxPooling1D (pool 2)
→ LSTM (128, return sequences)
→ LSTM (64)
→ Dense (16, ReLU)
→ Dense (2, Softmax)
```
Optimizer: **RMSprop** (lr=0.001) · Loss: binary crossentropy · 10 epochs · batch 256

## Installation

```bash
# create & activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / macOS

pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

> Note: after cloning, the repo already ships the trained model (`models/model.h5`), tokenizer (`Data/tokenizer.pkl`) and embedding matrix (`Data/glove_embedding_matrix.pkl`), so you can skip straight to **Test Your Own Headline**.

## Datasets

- Rishabh Misra, *Sarcasm Headlines Dataset* (v1 & v2) — news headlines from The Onion (sarcastic) and HuffPost (regular).
- GloVe 100d pre-trained word vectors from Stanford NLP. The raw `glove.6B.100d.txt` (~331MB) is excluded from the repo; the processed embedding matrix is committed instead.

## Results

Accuracy / Precision / Recall / F-measure and plots (accuracy, loss, confusion matrix, ROC) are generated into `models/` and `results/` after training.

## License

Scientific dataset used for educational/research purposes. The GloVe vectors are property of the Stanford NLP Group.
