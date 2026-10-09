import json
import re
from collections import Counter
from pathlib import Path


class AURATokenizer:
    PAD = "<PAD>"
    UNK = "<UNK>"
    BOS = "<BOS>"
    EOS = "<EOS>"

    def __init__(self):
        self.token_to_id = {
            self.PAD: 0,
            self.UNK: 1,
            self.BOS: 2,
            self.EOS: 3,
        }
        self.id_to_token = {
            index: token
            for token, index in self.token_to_id.items()
        }

    def tokenize(self, text):
        return re.findall(
            r"<[^>\s]+>|[\w]+(?:['’][\w]+)*|[^\w\s]",
            text,
            flags=re.UNICODE,
        )

    def fit(self, texts, min_frequency=1, max_vocab_size=None):
        counts = Counter()

        for text in texts:
            counts.update(self.tokenize(text))

        special_tokens = {
            self.PAD, self.UNK, self.BOS, self.EOS
        }

        for token, count in counts.most_common():
            if token in special_tokens or count < min_frequency:
                continue

            if (
                max_vocab_size is not None
                and len(self.token_to_id) >= max_vocab_size
            ):
                break

            if token not in self.token_to_id:
                index = len(self.token_to_id)
                self.token_to_id[token] = index
                self.id_to_token[index] = token

    def encode(self, text, add_special_tokens=False):
        tokens = self.tokenize(text)
        ids = [
            self.token_to_id.get(token, self.token_to_id[self.UNK])
            for token in tokens
        ]

        if add_special_tokens:
            ids = [self.token_to_id[self.BOS]] + ids
            ids.append(self.token_to_id[self.EOS])

        return ids

    def decode(self, ids, skip_special_tokens=True):
        tokens = []

        for index in ids:
            token = self.id_to_token.get(int(index), self.UNK)

            if skip_special_tokens and token in {
                self.PAD, self.UNK, self.BOS, self.EOS
            }:
                if token == self.UNK:
                    tokens.append(token)
                continue

            tokens.append(token)

        text = " ".join(tokens)

        # Remove spaces before common punctuation.
        text = re.sub(r"\s+([.,!?;:%)\]}])", r"\1", text)
        text = re.sub(r"([( \[{])\s+", r"\1", text)

        return text.strip()

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            json.dump(
                self.token_to_id,
                file,
                ensure_ascii=False,
                indent=2,
            )

    @classmethod
    def load(cls, path):
        tokenizer = cls()

        with Path(path).open(encoding="utf-8") as file:
            vocabulary = json.load(file)

        tokenizer.token_to_id = {
            token: int(index)
            for token, index in vocabulary.items()
        }
        tokenizer.id_to_token = {
            index: token
            for token, index in tokenizer.token_to_id.items()
        }

        return tokenizer


if __name__ == "__main__":
    data_path = Path("aura-model/data/train.txt")
    checkpoint_path = Path("aura-model/checkpoints/tokenizer.json")

    text = data_path.read_text(encoding="utf-8")

    tokenizer = AURATokenizer()
    tokenizer.fit([text])

    sample = "AURA learns from text!"
    encoded = tokenizer.encode(sample)
    decoded = tokenizer.decode(encoded)

    print("Vocabulary size:", len(tokenizer.token_to_id))
    print("Encoded:", encoded)
    print("Decoded:", decoded)

    tokenizer.save(checkpoint_path)

    loaded = AURATokenizer.load(checkpoint_path)
    assert loaded.encode(sample) == encoded

    print("Tokenizer save/load test passed.")
