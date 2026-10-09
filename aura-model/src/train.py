from pathlib import Path
import torch
from torch import nn
from torch.optim import AdamW

from model import AURAModel
from data_loader import load_dataset, make_sequences


torch.manual_seed(42)

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT_DIR = ROOT / "checkpoints"
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)


def train():
    tokenizer, token_ids = load_dataset()
    sequences = make_sequences(token_ids, sequence_length=8)

    vocab_size = len(tokenizer.token_to_id)

    model = AURAModel(
        vocab_size=vocab_size,
        max_length=256,
    )

    optimizer = AdamW(model.parameters(), lr=0.001)
    loss_fn = nn.CrossEntropyLoss()

    inputs = sequences[:, :-1]
    targets = sequences[:, 1:]

    model.train()
    epochs = 100

    print("AURA training started.")
    print("Vocabulary size:", vocab_size)
    print("Training sequences:", len(sequences))
    print("Training examples:", inputs.shape[0])
    print("Sequence length:", inputs.shape[1])

    for epoch in range(1, epochs + 1):
        optimizer.zero_grad()

        logits = model(inputs)

        loss = loss_fn(
            logits.reshape(-1, vocab_size),
            targets.reshape(-1),
        )

        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            model.parameters(), max_norm=1.0
        )
        optimizer.step()

        if epoch % 10 == 0:
            print(
                f"Epoch {epoch}/{epochs} | "
                f"Loss: {loss.item():.6f}"
            )

    model.eval()

    checkpoint_path = (
        CHECKPOINT_DIR / "aura-prototype.pt"
    )
    tokenizer_path = CHECKPOINT_DIR / "tokenizer.json"

    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "vocab_size": vocab_size,
            "embedding_size": 64,
            "hidden_size": 128,
            "max_length": 256,
            "num_heads": 4,
        },
        checkpoint_path,
    )

    tokenizer.save(tokenizer_path)

    print("\nAURA training completed.")
    print("Model saved:", checkpoint_path)
    print("Tokenizer saved:", tokenizer_path)
    print(
        "Model parameters:",
        sum(p.numel() for p in model.parameters()),
    )


if __name__ == "__main__":
    train()
