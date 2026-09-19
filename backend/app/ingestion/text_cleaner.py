import re


class TextCleaner:
    """Normalize extracted document text before chunking."""

    @staticmethod
    def clean(text: str) -> str:
        if not text:
            return ""

        # Normalize Windows/Linux line endings.
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove excessive spaces while preserving newlines.
        text = re.sub(r"[ \t]+", " ", text)

        # Collapse excessive blank lines.
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove spaces surrounding newlines.
        text = re.sub(r" *\n *", "\n", text)

        return text.strip()