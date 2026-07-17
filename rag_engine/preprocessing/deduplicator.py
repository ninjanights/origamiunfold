class Deduplicator:
    def remove_duplicate_lines(self, text: str) -> str:
        seen = set()
        result = []

        for line in text.splitlines():
            cleaned = line.strip()
            if not cleaned:
                result.append("")
                continue
            if cleaned not in seen:
                seen.add(cleaned)
                result.append(line)

        return "\n".join(result)

    def remove_duplicates(self, text: str) -> str:
        return self.remove_duplicate_lines(text)
