from pathlib import Path
import torch

from model import AURAModel
from tokenizer import AURATokenizer


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT_DIR = ROOT / "checkpoints"
TEST_FILE = ROOT / "data" / "test.txt"


def main():
    tokenizer = AURATokenizer.load(
        CHECKPOINT_DIR / "tokenizer.json"
    )

    checkpoint = torch.load(
        CHECKPOINT_DIR / "aura-prototype.pt",
        map_location="cpu",
        weights_only=True,
    )

    model = AURAModel(
        vocab_size=checkpoint["vocab_size"],
        embedding_size=checkpoint["embedding_size"],
        hidden_size=checkpoint["hidden_size"],
        max_length=checkpoint["max_length"],
        num_heads=checkpoint["num_heads"],
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    lines = [
        line.strip()
        for line in TEST_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    correct = 0
    total = 0
    skipped = 0

    with torch.no_grad():
        for line in lines:
            ids = tokenizer.encode(line)

            if len(ids) < 2:
                continue

            # Skip examples containing unknown words.
            if tokenizer.token_to_id[tokenizer.UNK] in ids:
                skipped += 1
                continue

            input_ids = torch.tensor([ids[:-1]], dtype=torch.long)
            targets = torch.tensor(ids[1:], dtype=torch.long)

            logits = model(input_ids)[0]
            predictions = logits.argmax(dim=-1)

            correct += (predictions == targets).sum().item()
            total += targets.numel()

    print("Unseen-data evaluation complete.")
    print("Test sentences:", len(lines))
    print("Skipped due to unknown tokens:", skipped)

    if total:
        print("Tokens evaluated:", total)
        print("Correct next-token predictions:", correct)
        print(f"Token accuracy: {100 * correct / total:.2f}%")
    else:
        print("No usable test tokens. The vocabulary needs improvement.")

    print("Note: This is a tiny test set, not a reliable measure of general intelligence.")


if __name__ == "__main__":
    main()
