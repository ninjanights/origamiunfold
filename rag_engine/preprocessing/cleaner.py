import re
from backend.realtime.progress_reporter import ProgressReporter


class Cleaner:
    def remove_tabs(self, text: str) -> str:
        return text.replace("\t", " ")

    def remove_extra_spaces(self, text: str) -> str:
        return re.sub(r"[ ]{2,}", " ", text)

    def remove_blank_lines(self, text: str) -> str:
        return re.sub(r"\n{3,}", "\n\n", text)

    def remove_control_characters(self, text: str) -> str:
        return re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)

    def remove_zero_width_characters(self, text: str) -> str:
        return re.sub(r"[\u200B-\u200D\uFEFF]", "", text)

    def clean(self, text: str, progress: ProgressReporter | None = None) -> str:
        raw_preview = text[:80] if text else "File 2. 'abc abc   def  #'"
        if progress:
            progress.upload(
                "clean_start",
                "Cleaning document",
                30,
                preview=raw_preview,
                after=raw_preview,
            )
        text = text.strip()
        if progress:
            progress.upload(
                "clean_whitespace",
                "Removing whitespace",
                31,
                preview=raw_preview,
                after=text[:80],
            )
        text = self.remove_tabs(text)
        text = self.remove_extra_spaces(text)
        text = self.remove_blank_lines(text)
        if progress:
            progress.upload(
                "clean_control_chars",
                "Removing hidden characters",
                33,
                preview=text[:80],
                after=text[:80],
            )
        text = self.remove_control_characters(text)
        
        text = self.remove_zero_width_characters(text)
        cleaned_preview = text[:80]
        if progress:
            progress.upload(
                "clean_done",
                "Cleaning completed.",
                35,
                preview=raw_preview,
                after=cleaned_preview,
            )

        return text
