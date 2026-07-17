import re
import unicodedata


class Normalizer:
    def normalize_unicode(self, text: str) -> str:
        return unicodedata.normalize("NFKC", text)

    def normalize_quotes(self, text: str) -> str:
        replacements = {
            "“": '"',
            "”": '"',
            "‘": "'",
            "’": "'",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    def normalize_dashes(self, text: str) -> str:
        return re.sub(r"[‐-‒–—―]", "-", text)

    def normalize_ellipsis(self, text: str) -> str:
        return text.replace("…", "...")

    def normalize_whitespace(self, text: str) -> str:
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")
        lines = [line.rstrip() for line in text.split("\n")]
        return "\n".join(lines)

    def normalize(self, text: str) -> str:

        text = self.normalize_unicode(text)
        text = self.normalize_quotes(text)
        text = self.normalize_dashes(text)
        text = self.normalize_ellipsis(text)
        text = self.normalize_whitespace(text)

        return text
