# Figure Presentation Gate — the single output-verified figure/table audit

> The ONE place for every mandatory figure- and table-presentation rule. This is to figures what
> `paper-writing/author_profile/gate_mechanical.md` (M1–M18) is to prose: a numbered, non-negotiable
> checklist with a **runnable verification procedure**. Run it before any figure or table is reported
> "done," and again in any red-team/polish pass.
>
> **The core discipline: verify in the COMPILED OUTPUT, not the source and not the browser.**
> A figure defect (wrapped table header, wasted whitespace, a baked-in title, a font mismatch, a
> missing figure number, stray color) is visual. It is invisible in the `.qmd`/`.tex` source and can
> render differently in a browser than in the print PDF the reader gets. So the gate is satisfied
> only by: render → rasterize the figure's page → open the image → look. **Report what you saw and on
> which page ("inspected p.28, Fig 6.4: header on one line, no right-margin gap"), not "looks good."**
> A mental pass is not a run. A browser preview is not a run.

This gate holds the checks a rendered page can catch. Data-honesty and interpretation checks (does
the figure support the claim, is the scale honest, is a bar-of-means hiding the distribution) live in
`/viz analyze`'s Tukey/Tufte lenses. Positive "how to build it" guidance lives in the Execute mode
and `reference/matplotlib_defaults.py`.

---

## F0. Declare the target medium FIRST (it sets two defaults)

Before auditing, state the medium. It parameterizes exactly two rules — **color (F6)** and **font
family (F4)** — everything else is universal.

| Profile | Color default (F6) | Font family (F4) | Figure/table numbering |
|:--|:--|:--|:--|
| **Book / PDF (Quarto)** — this project's default | **Grayscale.** Color only when it carries information grayscale + markers/line-styles cannot. | The book **body** face (sans-serif: Source Sans Pro). Figures match body, not a serif import. | Quarto floats: `#fig-…` / `#tbl-…` + caption |
| **Conference paper (LaTeX)** | One colorblind-safe scheme allowed; still grayscale-distinguishable via markers + line styles. | The paper's body serif (Times). | `\label{fig:…}` / `\label{tab:…}` + `\caption` |

If the medium is unstated and a `.qmd`/`_quarto.yml` is present, assume **Book / PDF**. If `.tex`,
assume **Conference paper**.

---

## Part A — Universal figure rules (every figure, every medium)

Each rule states the requirement, then a wrong→right, then how to verify it.

**F1. Verified in the compiled output.** The figure has been rendered to the final PDF, the page
rasterized (`pdftoppm -png -f P -l P`), and the image opened and read. No figure is "done" on a
source edit or a browser preview alone.
- ✗ "Edited the SVG, looks right." → ✓ "Rendered `ch06_transport_v1.pdf`, rasterized p.12, opened
  `p12.png`: v14 pipe fills the column, no title bar, boxes tight."
- **Verify:** the audit block at the bottom. Report the page number and what you saw.

**F2. Numbered and captioned.** Every figure is a numbered float with a caption. This includes
**mermaid diagrams and inline SVGs**, which do NOT get a number unless you wrap them. A bare
```` ```{mermaid} ```` block or a raw `<svg>` renders as an unnumbered orphan.
- ✗ ```` ```{mermaid}\nflowchart TD ... ``` ```` (no label, no caption) → ✓ wrap it so it becomes
  `#fig-dependency-chain` with a caption (see the mermaid-float recipe in Part C).
- **Verify:** grep for bare blocks (audit block, check D); confirm "Figure N.k" prints under it in
  the PDF.

**F3. No title inside the figure.** The caption is the title. Remove titles baked at the top of the
artwork: matplotlib `ax.set_title(...)` / `fig.suptitle(...)`, an SVG `<text>` heading, a mermaid
`title` line. A title inside the figure duplicates the caption and eats vertical space.
- ✗ SVG top row: `<text ...>Bandwidth-Delay Product (BDP)…</text>` → ✓ delete it; the caption
  already says it.
- **Verify:** grep SVG for a top-anchored `<text>`; scan the rasterized page for a heading above the
  artwork.

**F4. Font size = body text; ONE font family across all figures.** Figure text sits at body size
(rule of thumb — a label should look the same size as running text, not shrunken or blown up), and
every figure in the document uses the **same** family (per F0 profile). Mixing a serif figure with a
sans body, or 6pt labels in one figure and 11pt in the next, is the most common consistency tell.
- ✗ one mermaid in the theme default sans, one SVG hand-set in Helvetica, matplotlib in Times → ✓
  all three in the book body face at body size.
- **Verify:** eyeball label size against caption/body text on the rasterized page; grep SVGs for
  `font-family` and `font-size` and confirm they agree.

**F5. No oversized boxes; no wasted whitespace.** The canvas/viewBox is cropped to content; boxes are
sized to their text (not a fixed oversized default); there is no large empty margin, especially on
the right of flowcharts and pipe diagrams. Whitespace is deliberate, not leftover.
- ✗ a `flowchart TD` with a wide empty right third; an SVG `viewBox` 200px taller than the drawing →
  ✓ tighten `nodeSpacing`/`rankSpacing`, crop the `viewBox`/`width`/`height` to the bounding box.
- **Verify:** on the rasterized page, the artwork should touch (near) all four inner margins of its
  float; flag any band of empty pixels wider than one line of text.

**F6. Grayscale-first (Book profile) / one scheme (Paper profile).** Pick ONE color scheme and keep
it identical across ALL figures. Under the Book profile that scheme is grayscale; introduce a hue
only when it encodes information that grayscale plus distinct markers and line styles cannot. Never
use red/green/blue as decorative node fills.
- ✗ mermaid `classDef failure fill:#d94a4a` / `fix fill:#4ad94a` / `constraint fill:#4a90d9` → ✓ a
  grayscale ramp: fills `#e8e8e8` / `#c8c8c8` / `#f4f4f4` with a `#333` stroke and black text; encode
  the failure-vs-fix distinction by shape or border weight, not hue.
- **Verify:** grep mermaid/SVG for non-gray hex fills; confirm on the page that a grayscale print is
  still readable.

**F7. Legible at print size.** Readable at the intended column width (single ≈ 3.5 in, double ≈ 7 in,
book text column per the theme). No overlapping tick labels, no text colliding with a box edge, no
2-pt lines that vanish.
- **Verify:** read the rasterized page at 100%; if a label is unreadable there, it is unreadable in
  print.

**F8. Interpretive caption.** The caption states the takeaway, not just the axes/parts. It should be
readable standalone by someone skimming figures.
- ✗ "Figure 6.4: BDP pipe diagram." → ✓ "Figure 6.4: Below the bandwidth-delay product the pipe runs
  underfilled and capacity is wasted; above it the buffer overflows into queuing delay."
- **Verify:** read the caption alone — does it carry a claim?

---

## Part B — Data figures (matplotlib / seaborn) — additional rules

**D1. Lab rcParams, no `sns.set_theme()` in production.** Use the `plt.rcParams.update({...})` block
from Execute mode / `reference/matplotlib_defaults.py`. `sns.set_theme()` overrides rcParams (fonts →
sans, grid → pink, spines → all on) — the #1 style violation. Import seaborn for its functions only.

**D2. Axis labels with units; no chartjunk.** Both axes labeled with units; top/right spines off;
grid dotted and light; no 3-D, no drop shadows, no gradient fills, no background fill.

**D3. No bar-of-means where a distribution is the story.** A bar chart of means hides variance and
modality. Prefer CDF/ECDF, box, or violin unless the mean is genuinely the whole point.

**D4. Grayscale-distinguishable series.** Even in the Paper profile, series differ by marker AND line
style, not color alone, so the figure survives grayscale printing (this is F6 applied to data).

*(The full data-figure craft — golden-ratio sizing, legend placement, log-scale checks — stays in
Execute mode and the Tufte lens of `/viz analyze`. D1–D4 are the mandatory subset.)*

---

## Part C — Diagram figures (mermaid / inline SVG) — additional rules

These artifacts are where the Book profile most often breaks, because the theme defaults fight the
design system.

**G1. Make it a numbered float (this is F2 for diagrams).** A bare mermaid block has no number. Wrap
it. **Quarto mermaid-float recipe:**

````markdown
::: {#fig-dependency-chain}
```{mermaid}
flowchart TD
    ...
```
The IP datagram's three properties cascade into the constraints every transport design inherits.
:::
````

The `#fig-…` div id gives the number; the trailing line is the caption. Reference it with
`@fig-dependency-chain`. (Alternatively render the diagram to a `.svg` asset and `![caption](...
){#fig-…}`, which also lets you hand-tighten the artwork — preferred when the box sizing needs work.)

**G2. Grayscale `classDef` (this is F6 for mermaid).** Replace colored `classDef` fills with one
grayscale ramp used across every diagram in the chapter. Encode categorical meaning (failure vs fix
vs constraint) by border weight or shape, keeping fills gray:
- ✗ `classDef failure fill:#d94a4a,stroke:#8a2c2c,color:white`
- ✓ `classDef failure fill:#eeeeee,stroke:#333,stroke-width:2px,color:#111`
       `classDef fix fill:#dddddd,stroke:#333,color:#111`
       `classDef constraint fill:#f6f6f6,stroke:#888,stroke-dasharray:3 2,color:#111`

**G3. Tighten spacing (this is F5 for mermaid).** Set `nodeSpacing`/`rankSpacing` via the init
directive so boxes are close but not touching, and no empty right band remains:
`%%{init: {'flowchart': {'nodeSpacing': 24, 'rankSpacing': 30}}}%%`. Prefer `TD` over `LR` when the
chain is long and would otherwise run off the right margin.

**G4. Font = body (this is F4 for diagrams).** Do not hand-set a different `font-family`/`font-size`
inside an SVG or via mermaid `themeCSS`. Let it inherit the book body face, or set it explicitly to
that face at body size so all diagrams match.

**G5. No baked-in title (this is F3 for diagrams).** No mermaid `---\ntitle: …\n---` frontmatter and
no top `<text>` heading in a hand-authored SVG. Caption only.

---

## Part D — Tables — mandatory rules

**T1. Numbered and captioned.** Every table is a numbered float. In Quarto, add a caption line with a
`#tbl-…` id so it renders "Table N.k" and is cross-referenceable with `@tbl-…`.
- ✗ a bare pipe table with no caption → ✓ add `: Pioneer diagnoses across the transport arc. {#tbl-pioneer-diagnosis}`
  immediately under the table.
- **Verify:** confirm "Table N.k" prints in the PDF.

**T2. No column header wrapping across lines.** A header cell that wraps ("Sce-nario", "Band-width")
signals the column is too narrow or the header too long. Shorten/abbreviate the header, widen the
column, or split the table — so every header sits on one line.
- ✗ a 5-column BDP table whose headers hyphenate and wrap → ✓ rename headers to fit
  ("BW", "RTT", "BDP", "Regime", "Effect") and/or drop a column.
- **Verify:** on the rasterized page, read every header cell — each must occupy exactly one line.

**T3. No wasted whitespace / no over-wide columns.** Compress cells so the critical term in each cell
fits on line 1 (the whitespace-optimization rule from the Ch6 v8 pass); no column is padded far wider
than its widest real value.
- **Verify:** scan the page for columns with large empty right space, and for any cell whose key term
  wrapped to line 2.

**T4. No bad page break.** A table must not split awkwardly across a page boundary (header on one
page, body on the next; or a 6-row table straddling two pages). Keep it together, move it, or split
it deliberately.
- **Verify:** confirm the whole table sits on one page in the PDF, or breaks at an intended row with
  the header repeated.

**T5. Booktabs rules only.** Horizontal rules only (top/mid/bottom); no vertical rules, no full grid.

---

## Part E — The audit block (RUN THIS; do not eyeball)

Two halves. **A** is greppable pre-screening (catches the source-level tells fast). **B** is the
mandatory render-and-inspect that actually satisfies F1 — greps cannot see whitespace, wrapping, or
font size.

```bash
# ============ A. Source pre-screen (fast; catches obvious violations) ============
FILE=ch06_transport_v1.qmd   # or sections/*.tex for the Paper profile

# ── F2/G1: bare mermaid blocks with NO surrounding #fig- float (each hit = an unnumbered orphan) ──
grep -n '```{mermaid}' "$FILE"
#   For each hit, confirm a `#fig-` id appears within ~3 lines above (the ::: {#fig-…} opener).

# ── F6/G2: non-grayscale fills in mermaid/SVG (each hex that isn't #RRGGBB with R==G==B is suspect) ──
grep -noE 'fill:#[0-9a-fA-F]{6}|fill="#[0-9a-fA-F]{6}"' "$FILE" assets/figures/*.svg
#   Gray means the three byte pairs are equal (#e8e8e8). Anything else is color — justify or fix.

# ── F3/G5: baked-in titles ──
grep -n '^title:\|set_title\|suptitle' "$FILE" assets/figures/*.py
grep -n '<text' assets/figures/*.svg | head   # inspect the top-anchored one for a heading

# ── F4/G4: font drift inside SVGs (should all name the SAME body face at the SAME size) ──
grep -noE 'font-family="[^"]*"|font-size="[^"]*"' assets/figures/*.svg | sort | uniq -c

# ── T1: pipe tables missing a #tbl- caption (count tables vs count captions) ──
grep -cE '^\|' "$FILE"; grep -c '#tbl-' "$FILE"   # every table block should have one #tbl-

# ============ B. Render-and-inspect (MANDATORY — this is what satisfies F1) ============
cd cs176c-book
quarto render "$FILE" --to pdf         # standalone chapter render
#   Find each figure/table's page (search the PDF text or scan the outline), then for page P:
pdftoppm -png -r 150 -f P -l P ch06_transport_v1.pdf /tmp/ch06_p          # -> /tmp/ch06_p-PP.png
#   OPEN each PNG and read it. For every figure and table, confirm and REPORT:
#     F2/T1  the "Figure N.k" / "Table N.k" label is present
#     F3/G5  no title bar above the artwork
#     F4/G4  label size ≈ body size; one family throughout
#     F5/G3  boxes tight; no empty right band; float margins snug
#     F6/G2  reads correctly in grayscale
#     T2     every table header cell on ONE line
#     T3/T4  no over-wide columns; no bad page break
```

**Report format (paste into the audit summary / AUDIT_LEDGER):**

```
Figure/Table gate — <file> @ <commit>
  Source pre-screen: bare mermaids=N (all wrapped? Y/N) · color fills=N (justified/fixed) ·
                     baked titles=N · font-drift variants=N · tables=N / captions=N
  PDF inspection (render p.<pages>):
    Fig 6.1 (dependency chain), p.12 — number ✓ · no title ✓ · grayscale ✓ · boxes tight ✓ · font=body ✓
    Tbl 6.3 (pioneer diagnosis), p.13 — number ✓ · headers 1 line ✓ · no page split ✓
    ...
  Result: <clean | N items open> — every item fixed or explicitly justified, with the page shown.
```

"Clean" means every gate item is verified on a rendered page, with the page number cited — not
"audited," not "looks good."
