import json
from pathlib import Path


class AURACharTokenizer:
    PAD = "<PAD>"
    UNK = "<UNK>"
    BOS = "<BOS>"
    EOS = "<EOS>"

    SPECIAL_TOKENS = [PAD, UNK, BOS, EOS]

    def __init__(self):
        self.token_to_id = {
            token: index
            for index, token in enumerate(self.SPECIAL_TOKENS)
        }
        self.id_to_token = {
            index: token
            for token, index in self.token_to_id.items()
        }

    def tokenize(self, text):
        return list(text.lower())

    def fit(self, texts):
        characters = sorted(
            set("abcdefghijklmnopqrstuvwxyz0123456789 .,!?;:'\"-()[]/%") | set("अआइईउऊऋएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहक्षत्रज्ञ़ंँःािीुूृेैोौंॅॉ्")
            | {
                char
                for text in texts
                for char in self.tokenize(text)
            }
        )

        for char in characters:
            if char not in self.token_to_id:
                index = len(self.token_to_id)
                self.token_to_id[char] = index
                self.id_to_token[index] = char

    def encode(self, text):
        return [
            self.token_to_id.get(char, self.token_to_id[self.UNK])
            for char in self.tokenize(text)
        ]

    def decode(self, ids, skip_special_tokens=True):
        result = []

        for index in ids:
            token = self.id_to_token.get(int(index), self.UNK)

            if skip_special_tokens and token in self.SPECIAL_TOKENS:
                continue

            result.append(token)

        return "".join(result)

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
    tokenizer = AURACharTokenizer()

    tokenizer.fit([
        "AURA is an AI assistant.",
        "AURA ek AI assistant hai.",
    ])

    sample = "AURA learns!"
    encoded = tokenizer.encode(sample)
    decoded = tokenizer.decode(encoded)

    print("Character vocabulary:", len(tokenizer.token_to_id))
    print("Input:", sample)
    print("Encoded length:", len(encoded))
    print("Decoded:", decoded)

    assert decoded == sample.lower()
    assert tokenizer.encode("NEW WORD") == tokenizer.encode("new word")

    print("Character tokenizer test passed.")
