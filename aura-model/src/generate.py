from pathlib import Path
import json
import torch

from model import AURAModel
from tokenizer import AURATokenizer

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT_DIR = ROOT / "checkpoints"

with (CHECKPOINT_DIR / "tokenizer.json").open(
    encoding="utf-8"
) as file:
    token_to_id = json.load(file)

tokenizer = AURATokenizer()
tokenizer.token_to_id = {
    token: int(index) for token, index in token_to_id.items()
}
tokenizer.id_to_token = {
    index: token for token, index in tokenizer.token_to_id.items()
}

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

prompt = "aura is"
token_ids = tokenizer.encode(prompt)

for _ in range(10):
    input_ids = torch.tensor([token_ids[-256:]], dtype=torch.long)

    with torch.no_grad():
        logits = model(input_ids)

    next_id = int(logits[0, -1].argmax().item())
    token_ids.append(next_id)

print("Generated text:")
print(tokenizer.decode(token_ids))
