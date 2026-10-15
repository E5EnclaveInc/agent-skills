#!/usr/bin/env python3
"""Copy-freeze verifier for sawdust-cinematic pages.

Method (proven on the No. 01 merged build and the five variants):
  - parse HTML with html.parser, skip script/style/noscript/svg subtrees
  - extract every block-level text node in document order,
    collapse whitespace (\\s+ -> single space, trim)
  - keep input[placeholder] values as blocks
  - de-duplicate consecutive duplicates from nested block tags
Each page's block list must EQUAL the frozen source's block list
(order preserved). Any wording change, reordering, or missing/extra
block fails loudly.

Removed fragments: when the page intentionally excludes sections
(e.g. variant comparison pages), pass --removed-fragments FILE where
each removed section's exact HTML chunk is separated by a line
containing exactly '---'. Blocks inside those chunks are excluded
from the comparison by source character offset, so identical strings
kept elsewhere are never confused with removed ones.

Usage:
  python3 bin/verify_copy.py <frozen-source.html> <page1.html> [<page2.html> ...]
  python3 bin/verify_copy.py --removed-fragments removed.html source.html v1.html
Stdlib only. Exit 0 iff every page passes.
"""
import pathlib
import sys
from html.parser import HTMLParser

BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "li", "blockquote", "title",
              "label", "span", "a", "div", "em", "strong", "button",
              "textarea"}
SKIP_TAGS = {"script", "style", "noscript", "svg"}


class BlockExtractor(HTMLParser):
    """Extracts (text, char_offset) blocks; offsets let us exclude exactly
    the blocks that lived inside removed source regions."""

    def __init__(self, line_offsets):
        super().__init__(convert_charrefs=True)
        self.line_offsets = line_offsets
        self.skip = 0
        self.buf = []
        self.buf_start = None
        self.blocks = []  # (text, offset)

    def _pos(self):
        ln, col = self.getpos()
        return self.line_offsets[ln - 1] + col

    def _flush(self):
        text = " ".join("".join(self.buf).split())
        start = self.buf_start
        self.buf = []
        self.buf_start = None
        if text and (not self.blocks or self.blocks[-1][0] != text):
            self.blocks.append((text, start))

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.skip += 1
            return
        if self.skip:
            return
        if tag == "input":
            for k, v in attrs:
                if k == "placeholder" and v and v.strip():
                    t = " ".join(v.split())
                    if not self.blocks or self.blocks[-1][0] != t:
                        self.blocks.append((t, self._pos()))
            return
        if tag in BLOCK_TAGS:
            self._flush()

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag in BLOCK_TAGS:
            self._flush()

    def handle_data(self, data):
        if not self.skip:
            if self.buf_start is None and data.strip():
                self.buf_start = self._pos()
            self.buf.append(data)


def extract(path):
    raw = pathlib.Path(path).read_text(encoding="utf-8")
    line_offsets = [0]
    for line in raw.splitlines(keepends=True):
        line_offsets.append(line_offsets[-1] + len(line))
    ex = BlockExtractor(line_offsets)
    ex.feed(raw)
    ex._flush()
    return raw, ex.blocks


def removed_spans(src_raw, fragments_path):
    """Locate each removed chunk's span inside the source, in order."""
    text = pathlib.Path(fragments_path).read_text(encoding="utf-8")
    chunks = [c for c in text.split("\n---\n") if c.strip()]
    spans = []
    cursor = 0
    for i, chunk in enumerate(chunks):
        chunk = chunk.strip()
        idx = src_raw.find(chunk, cursor)
        assert idx >= 0, f"removed fragment #{i} not found in source"
        spans.append((idx, idx + len(chunk)))
        cursor = idx + len(chunk)
    return spans


def main(argv):
    removed_path = None
    args = list(argv)
    if "--removed-fragments" in args:
        i = args.index("--removed-fragments")
        removed_path = args.pop(i + 1)
        args.pop(i)
    if len(args) < 2:
        print(__doc__, file=sys.stderr)
        return 2

    src_path, pages = args[0], args[1:]
    src_raw, src_blocks = extract(src_path)

    spans = removed_spans(src_raw, removed_path) if removed_path else []
    expected = [t for (t, off) in src_blocks
                if not any(s <= off < e for s, e in spans)]

    ok = True
    for p in pages:
        _, got_blocks = extract(p)
        got = [t for (t, _) in got_blocks]
        if got == expected:
            print(f"PASS {p}: {len(got)} blocks byte-identical to frozen "
                  f"source, order preserved")
        else:
            ok = False
            print(f"FAIL {p}: block mismatch")
            for i, (g, e) in enumerate(zip(got, expected)):
                if g != e:
                    print(f"  first divergence at block {i}: "
                          f"got {g[:70]!r} want {e[:70]!r}")
                    break
            if len(got) != len(expected):
                print(f"  counts: got {len(got)}, want {len(expected)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
