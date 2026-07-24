from backend.realtime.progress_reporter import ProgressReporter


class Deduplicator:
    def remove_duplicate_lines(
        self,
        text: str,
        progress: ProgressReporter | None = None
    ) -> str:
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

    def remove_duplicates(
        
        self, text: str, progress: ProgressReporter | None = None
    ) -> str:
        
        input_preview = text[:80] if text else "abc cde efg"
        if progress:
            progress.upload(
                "deduplicate_start",
                "Removing duplicate content",
                41,
                preview=input_preview,
                after=input_preview,
            )
        text =  self.remove_duplicate_lines(text)
        dedup_preview = text[:80] if text else "abc cde efg"
        if progress:
            progress.upload(
                "deduplicate_done",
                "Duplicate removal completed.",
                45,
                preview=input_preview,
                after=dedup_preview,
            )

        return text 
