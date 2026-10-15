# WCAG Contrast Method — computed, never eyeballed

Relative luminance of a color, per WCAG 2.x:

```
L = 0.2126·R + 0.7152·G + 0.0722·B
```

where each channel is the sRGB value linearized to 0–1:

```
if c <= 0.03928:  c/12.92
else:             ((c + 0.055) / 1.055) ^ 2.4
```

Contrast ratio between two colors:

```
ratio = (L_lighter + 0.05) / (L_darker + 0.05)
```

## Paste-ready stdlib Python (read-only checks — computes, never modifies)

```python
def lin(c: float) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

def contrast(fg: str, bg: str) -> float:
    l1, l2 = luminance(fg), luminance(bg)
    hi, lo = (l1, l2) if l1 >= l2 else (l2, l1)
    return (hi + 0.05) / (lo + 0.05)

# gates
assert contrast("#1c1a17", "#f4ece4") >= 7.0    # body text (target 7:1)
assert contrast("#1c1a17", "#eaddcc") >= 4.5    # tape numerals on track
assert contrast("#f4ece4", "#141312") >= 4.5    # CTA text on button
```

## Rules for this skill
- Measure the **actual pair**: foreground text color against the background it physically sits on. The No. 01 failure was a gradient fill whose left end measured 2.60:1 while a comment claimed ≥5.5:1 — comments are not measurements.
- The tape-numeral gate is always the numerals against the *track behind them*, never against the fill — in the shipped builds the fill cannot slide under the numerals by construction (WORKED_EXAMPLE.md).
- Record every required pair as `(fg hex, bg hex, ratio, threshold, pass)` into `contrast.json` beside the artifact, in the shape used by the proven verifier in the project's variants `qa/` directory (its `check_contrast.py` parses each page's own resolved tokens and the actual verdict-sub rgba from its CSS — follow that pattern for new pages rather than hand-picking colors).
- AMBER RULE floors: brand amber `#b08d3e` is decorative-only on light (2.67:1); small amber text must use `#75571f` (5.72:1) on light or `#d4af5f` (8.88:1) on dark.
