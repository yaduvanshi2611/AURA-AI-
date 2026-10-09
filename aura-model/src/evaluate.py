import torch

from model import AURAModel
from data_loader import load_dataset, make_sequences


def evaluate():
    torch.manual_seed(42)

    tokenizer, token_ids = load_dataset()
    sequences = make_sequences(token_ids, sequence_length=8)

    checkpoint = torch.load(
        "aura-model/checkpoints/aura-prototype.pt",
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

    inputs = sequences[:, :-1]
    targets = sequences[:, 1:]

    with torch.no_grad():
        logits = model(inputs)
        predictions = logits.argmax(dim=-1)
        correct = (predictions == targets).sum().item()
        total = targets.numel()
        accuracy = 100 * correct / total

    print("Evaluation complete.")
    print("Tokens evaluated:", total)
    print("Correct predictions:", correct)
    print(f"Token accuracy: {accuracy:.2f}%")
    print("Note: This evaluates training data, not unseen questions.")


if __name__ == "__main__":
    evaluate()
