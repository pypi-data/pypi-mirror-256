from dataclasses import dataclass
from datetime import datetime
from typing import List

from izihawa_textparser.utils import BANNED_SECTIONS, BANNED_SECTION_PREFIXES_REGEXP
from izihawa_textutils.utils import remove_markdown
from langchain_core.documents import Document
from ._text_splitters import (
    MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter,
)
from unstructured.cleaners.core import clean


@dataclass
class Chunk:
    document_id: str
    field: str
    chunk_id: int
    title: str
    text: str
    start_index: int
    length: int
    issued_at: int | None = None
    type: str | None = None
    language: str | None = None


@dataclass
class StoredChunk:
    document_id: str
    field: str
    chunk_id: int
    title: str
    start_index: int
    length: int
    issued_at: int
    type: str | None = None
    updated_at: int | None = None
    language: str | None = None


def extract_title_parts(document: dict, split):
    title_parts = []
    if 'title' in document:
        title_parts.append(document['title'])
    for hn in range(1, 7):
        if hn_value := split.metadata.get(f"h{hn}"):
            title_parts.append(hn_value)
    return title_parts


def length_function(text: str):
    return len(remove_markdown(text))


class DocumentChunker:
    def __init__(
        self,
        chunk_size: int = 1024,
        chunk_overlap: int = 128,
        add_metadata: bool = False,
        add_year: bool = True,
        return_each_line: bool = False,
    ):
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            keep_separator=True,
            strip_whitespace=True,
            length_function=length_function,
        )
        self._markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "h1"),
                ("##", "h2"),
                ("###", "h3"),
                ("####", "h4"),
                ("#####", "h5"),
                ("######", "h6"),
            ],
            return_each_line=return_each_line,
        )
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        self._add_metadata = add_metadata
        self._add_year = add_year

    def _splits_to_chunks(
        self, document: dict, field: str, splits
    ):
        chunks = []
        for chunk_id, split in enumerate(splits):
            page_content = str(split.page_content)
            chunk_text = clean(
                remove_markdown(page_content),
                extra_whitespace=True,
                dashes=True,
                bullets=True,
                trailing_punctuation=True,
            )
            parts = [chunk_text]
            title_parts = extract_title_parts(document, split)
            if len(chunk_text) < 128 or any(
                [((title_part.lower() in BANNED_SECTIONS)
                  or (bool(BANNED_SECTION_PREFIXES_REGEXP.match(title_part.lower()))))
                 for title_part in title_parts]
            ):
                continue
            if self._add_metadata:
                parts.append(f'TITLE: {" ".join(title_parts)}')
                if "keywords" in document.get('metadata', {}):
                    keywords = ", ".join(document['metadata']['keywords'])
                    parts.append(f"KEYWORDS: {keywords}")
                if 'tags' in document:
                    tags = ", ".join(document['tags'])
                    parts.append(f"TAGS: {tags}")
            if self._add_year and 'issued_at' in document and document['issued_at'] != -62135596800:
                issued_at = datetime.fromtimestamp(document['issued_at'], tz=None)
                parts.append(f"YEAR: {issued_at.year}")
            text = "\n".join(parts)
            chunks.append(
                Chunk(
                    document_id=document['id']['nexus_id'],
                    field=field,
                    chunk_id=chunk_id,
                    title="\n".join(title_parts),
                    text=text,
                    start_index=split.metadata["start_index"],
                    length=len(page_content),
                    issued_at=document.get('issued_at'),
                    type=document.get('type'),
                    language=document['languages'][0] if 'languages' in document else None,
                )
            )
        return chunks

    def markdown_to_splits(self, text: str) -> list[Document]:
        return self._markdown_splitter.split_text(text)

    def text_to_chunks(self, document, field):
        return self._splits_to_chunks(
            document,
            field,
            self._text_splitter.split_documents(self.markdown_to_splits(document.get(field, "")))
        )

    def document_to_chunks(self, document: dict) -> List[Chunk]:
        return [
            *self.text_to_chunks(document, "abstract"),
            *self.text_to_chunks(document, "content"),
        ]

    def splits_to_text(self, splits) -> list[str]:
        previous_header = {}
        text_parts = []
        for split in splits:
            text = ''
            current_header = split.metadata
            for i in range(1, 7):
                h = f'h{i}'
                if previous_header.get(h) == current_header.get(h):
                    continue
                else:
                    for j in range(i, 7):
                        hj = f'h{j}'
                        if hj in current_header:
                            text_parts.append('#' * j + ' ' + current_header[hj])
                        else:
                            break
                    break
            text += split.page_content
            text_parts.append(text)
            previous_header = current_header
        return text_parts
