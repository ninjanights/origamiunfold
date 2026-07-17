import re


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

    def clean(self, text: str) -> str:
        text = text.strip()
        text = self.remove_tabs(text)
        text = self.remove_extra_spaces(text)
        text = self.remove_blank_lines(text)
        text = self.remove_control_characters(text)
        text = self.remove_zero_width_characters(text)

        return text
