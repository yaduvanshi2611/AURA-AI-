import torch
from torch import nn


class AURAModel(nn.Module):
    """Small causal language-model prototype for AURA."""

    def __init__(
        self,
        vocab_size,
        embedding_size=64,
        hidden_size=128,
        max_length=256,
        num_heads=4,
    ):
        super().__init__()

        if embedding_size % num_heads != 0:
            raise ValueError(
                "embedding_size must be divisible by num_heads."
            )

        self.token_embedding = nn.Embedding(
            vocab_size, embedding_size
        )
        self.position_embedding = nn.Embedding(
            max_length, embedding_size
        )

        self.attention = nn.MultiheadAttention(
            embed_dim=embedding_size,
            num_heads=num_heads,
            batch_first=True,
        )

        self.norm1 = nn.LayerNorm(embedding_size)

        self.feed_forward = nn.Sequential(
            nn.Linear(embedding_size, hidden_size),
            nn.GELU(),
            nn.Linear(hidden_size, embedding_size),
        )

        self.norm2 = nn.LayerNorm(embedding_size)
        self.output_head = nn.Linear(embedding_size, vocab_size)
        self.max_length = max_length

    def forward(self, token_ids):
        _, seq_length = token_ids.shape

        if seq_length > self.max_length:
            raise ValueError("Sequence exceeds max_length.")

        positions = torch.arange(
            seq_length, device=token_ids.device
        ).unsqueeze(0)

        x = (
            self.token_embedding(token_ids)
            + self.position_embedding(positions)
        )

        causal_mask = torch.triu(
            torch.ones(
                seq_length,
                seq_length,
                dtype=torch.bool,
                device=token_ids.device,
            ),
            diagonal=1,
        )

        attention_output, _ = self.attention(
            x,
            x,
            x,
            attn_mask=causal_mask,
            need_weights=False,
        )

        x = self.norm1(x + attention_output)
        x = self.norm2(x + self.feed_forward(x))

        return self.output_head(x)


if __name__ == "__main__":
    torch.manual_seed(42)

    model = AURAModel(vocab_size=55)
    sample = torch.randint(0, 55, (2, 9))
    output = model(sample)

    assert output.shape == (2, 9, 55)
    assert torch.isfinite(output).all()

    print("AURA causal language model initialized.")
    print("Input shape:", tuple(sample.shape))
    print("Output shape:", tuple(output.shape))
    print(
        "Parameters:",
        sum(p.numel() for p in model.parameters()),
    )
    print("Causal attention test passed.")
