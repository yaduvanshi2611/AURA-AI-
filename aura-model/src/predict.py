from pathlib import Path
import torch

from model import AURAModel
from tokenizer import AURATokenizer


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT_DIR = ROOT / "checkpoints"

tokenizer_path = CHECKPOINT_DIR / "tokenizer.json"
checkpoint_path = CHECKPOINT_DIR / "aura-prototype.pt"

tokenizer = AURATokenizer()

import json

with tokenizer_path.open(encoding="utf-8") as file:
    tokenizer.token_to_id = json.load(file)

tokenizer.token_to_id = {
    token: int(index)
    for token, index in tokenizer.token_to_id.items()
}
tokenizer.id_to_token = {
    index: token
    for token, index in tokenizer.token_to_id.items()
}

checkpoint = torch.load(
    checkpoint_path,
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

if not token_ids:
    raise ValueError("Prompt produced no tokens.")

input_ids = torch.tensor([token_ids], dtype=torch.long)

with torch.no_grad():
    logits = model(input_ids)
    next_token_id = int(logits[0, -1].argmax().item())

print("Prompt:", prompt)
print("Input token IDs:", token_ids)
print("Predicted next token:", tokenizer.decode([next_token_id]))
print("Prediction test successful.")
