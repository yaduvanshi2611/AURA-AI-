import re
from collections import Counter


class AURATokenizer:
    def __init__(self):
        self.token_to_id = {"<PAD>": 0, "<UNK>": 1}
        self.id_to_token = {0: "<PAD>", 1: "<UNK>"}

    def tokenize(self, text):
        return re.findall(r"\w+|[^\w\s]", text.lower(), flags=re.UNICODE)

    def fit(self, texts):
        counts = Counter()
        for text in texts:
            counts.update(self.tokenize(text))

        for token, _ in counts.most_common():
            if token not in self.token_to_id:
                idx = len(self.token_to_id)
                self.token_to_id[token] = idx
                self.id_to_token[idx] = token

    def encode(self, text):
        return [
            self.token_to_id.get(token, self.token_to_id["<UNK>"])
            for token in self.tokenize(text)
        ]

    def decode(self, ids):
        return " ".join(
            self.id_to_token.get(idx, "<UNK>")
            for idx in ids
        )

    def save(self, path):
        import json
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.token_to_id, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    with open("aura-model/data/train.txt", encoding="utf-8") as file:
        text = file.read()

    tokenizer = AURATokenizer()
    tokenizer.fit([text])

    encoded = tokenizer.encode("AURA learns from text.")
    print("Vocabulary size:", len(tokenizer.token_to_id))
    print("Encoded:", encoded)
    print("Decoded:", tokenizer.decode(encoded))

    tokenizer.save("aura-model/checkpoints/tokenizer.json")
    print("Tokenizer saved successfully.")
