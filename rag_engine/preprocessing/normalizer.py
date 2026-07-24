import re
import unicodedata
from backend.realtime.progress_reporter import ProgressReporter


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

    def normalize(self, text: str, progress=None) -> str:
        input_preview = text[:80] if text else "abc abc   def  #"
        if progress:
            progress.upload(
                "normalize_start",
                "Normalizing text",
                36,
                preview=input_preview,
                after=input_preview,
            )
        text = self.normalize_unicode(text)
        if progress:
            progress.upload(
                "normalize_symbols",
                "Normalizing symbols",
                37,
                preview=input_preview,
                after=text[:80],
            )

        text = self.normalize_quotes(text)
        text = self.normalize_dashes(text)
        text = self.normalize_ellipsis(text)

        if progress:
            progress.upload(
                "normalize_symbols",
                "Normalizing symbols",
                37,
                preview=input_preview,
                after=text[:80],
            )

        text = self.normalize_whitespace(text)
        normalized_preview = text[:80]
        if progress:
            progress.upload(
                "normalize_done",
                "Normalization completed.",
                40,
                preview=input_preview,
                after=normalized_preview,
            )

        return text
