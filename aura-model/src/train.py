import torch
from torch import nn
from torch.optim import AdamW
from model import AURAModel

torch.manual_seed(42)

model = AURAModel()
optimizer = AdamW(model.parameters(), lr=0.001)
loss_fn = nn.MSELoss()

inputs = torch.randn(256, 128)
targets = inputs.clone()

model.train()

for epoch in range(1, 21):
    optimizer.zero_grad()
    outputs = model(inputs)
    loss = loss_fn(outputs, targets)
    loss.backward()
    optimizer.step()

    if epoch % 5 == 0:
        print(f"Epoch {epoch}/20 | Loss: {loss.item():.6f}")

torch.save(model.state_dict(), "aura-model/checkpoints/aura-prototype.pt")
print("AURA prototype training test complete.")
print("Checkpoint saved: aura-model/checkpoints/aura-prototype.pt")
