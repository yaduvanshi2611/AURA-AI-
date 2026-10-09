import torch
from torch import nn


class AURAModel(nn.Module):
    """AURA model foundation — initial neural network."""

    def __init__(self, input_size=128, hidden_size=256, output_size=128):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.GELU(),
            nn.Linear(hidden_size, hidden_size),
            nn.GELU(),
            nn.Linear(hidden_size, output_size),
        )

    def forward(self, x):
        return self.network(x)


if __name__ == "__main__":
    model = AURAModel()
    sample = torch.randn(1, 128)
    output = model(sample)
    print("AURA model initialized successfully")
    print("Input shape:", tuple(sample.shape))
    print("Output shape:", tuple(output.shape))
    print("Parameters:", sum(p.numel() for p in model.parameters()))
