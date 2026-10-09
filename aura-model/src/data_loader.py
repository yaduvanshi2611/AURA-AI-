from pathlib import Path
import torch
from tokenizer import AURATokenizer


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "train.txt"


def load_dataset():
    text = DATA_FILE.read_text(encoding="utf-8")

    tokenizer = AURATokenizer()
    tokenizer.fit([text])

    token_ids = tokenizer.encode(text)

    return tokenizer, token_ids


def make_sequences(token_ids, sequence_length=8):
    sequences = []

    for start in range(0, len(token_ids) - sequence_length, sequence_length):
        chunk = token_ids[start:start + sequence_length + 1]

        if len(chunk) == sequence_length + 1:
            sequences.append(chunk)

    if not sequences:
        raise ValueError("Dataset is too small to create training sequences.")

    return torch.tensor(sequences, dtype=torch.long)


if __name__ == "__main__":
    tokenizer, token_ids = load_dataset()
    sequences = make_sequences(token_ids)

    print("Dataset tokens:", len(token_ids))
    print("Vocabulary size:", len(tokenizer.token_to_id))
    print("Training sequences:", len(sequences))
    print("First sequence:", sequences[0].tolist())
    print("Data loader test successful.")
