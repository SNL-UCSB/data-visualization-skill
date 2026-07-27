# TikZ Pipeline & Schematic Figures (HotNets / SIGCOMM convention)

The viz skill is data-plot-first (matplotlib / seaborn). Networking papers
also need *schematic* figures — pipelines, system architectures, decision
flows — which are drawn in TikZ inside LaTeX, not Python. This reference
captures the conventions accepted HotNets / SIGCOMM papers follow for
those figures.

Survey basis: ArachNet (HotNets'25), Confucius (SIGCOMM'25), netUnicorn
(CCS'23), Democratize NetAI (HotNets'19), Mani et al. (HotNets'23),
CCAnalyzer (HotNets'25). All linked at the bottom.

## When to use this reference

A figure belongs in TikZ (not matplotlib) when it has no underlying data —
it shows *structure* a reader has to read in order: a pipeline, a system
architecture, a decision flow, an interface diagram. The Brainstorm and
Plan modes still apply (what is the figure showing? what should a reader
take away in 5 seconds?), but Execute mode is TikZ, not Python.

## Layout conventions

| Property | Convention |
|---|---|
| Orientation | **Horizontal**, left-to-right. Pipelines with 4+ stages almost always go horizontal in this corpus. Vertical is acceptable only for ≤3-stage flows in single-column figures. |
| Width | **Full text-width** for ≥5-stage pipelines (`figure*` in `acmart sigconf`). Single-column only when the pipeline is short and tall (e.g., 3 stages with example screenshots beside each). |
| Aspect ratio | ~3.5:1 to 4:1 wide:tall for a 5-stage horizontal pipeline. |
| Uniformity | Stages get **uniform widths**; variable widths read as "architecture," uniform widths read as "pipeline." |
| Spacing | Tight (~3 mm between adjacent stages). Wasted whitespace is the most common reviewer complaint on schematic figures. |

## Box and node conventions

- **Rounded rectangles only.** `rounded corners=2.5pt` is the standard radius.
- **Thin uniform stroke** (`line width=0.5pt`, `draw=gray!55`).
- **Light pastel fills.** Saturated colors fail HotNets's grayscale-legibility
  requirement. Use `fill=color!12` to `fill=color!22`. Pick pastels that
  differ in *lightness*, not just hue.
- **NO DIAMONDS for decision nodes.** Diamonds read as dated flowchart and
  are absent from recent accepted papers. A decision is a normal rounded
  rectangle whose label is phrased as a question ("Capability match?"),
  with two labeled outgoing arrows ("yes / in scope", "no / unsupported").
- **Semantic color palette** (the most common scheme):

| Color | Meaning | Example |
|---|---|---|
| grey | external data (input or output of pipeline) | "Paper (PDF)" |
| pastel blue | pipeline stage | "Classify paragraphs" |
| pastel yellow | decision point | "Capability match?" |
| pastel green | success terminal | "vs. published" |
| pastel red / grey | failure terminal | "out of scope" |

## Arrow conventions

- **Orthogonal/elbow only.** Diagonal arrows look wonky in print and are
  rejected on first read. Every arrow is purely horizontal or purely
  vertical. Use right-angle routing (`-|` or `|-`) when two boxes are not
  aligned.
- **Single-headed**, **uniform thin black** (`-{Stealth[length=4pt]}, thin`).
- **No double-headed arrows** — they obscure direction of flow.
- **Curved arrows only for feedback loops** (e.g., closed-loop training).
- **Labels above the arrow**, scriptsize, italic, grey-text — never inline
  in the arrow's path.

## Sidecar and branch idioms

Two patterns appear across the corpus:

1. **Backplane sidecar (ArachNet, Confucius).** A wide grey bar sits
   *underneath* the entire pipeline, with thin vertical lines feeding
   upward into multiple stages. Use when the sidecar is shared by many
   stages (registry, memory, knowledge base).
2. **Single sidecar enters from above (Mani et al., Democratize NetAI).**
   A small auxiliary box sits *above* the one stage it feeds, with a
   short vertical arrow down. Use when the sidecar feeds exactly one
   stage (capability spec, prompt template, schema).
3. **Branch exits downward.** A short vertical arrow from the decision
   stage down to a small, *visually subordinate* (smaller, desaturated)
   terminal box. Never let the branch terminal compete with the main
   pipeline's success terminal.

The combination *single sidecar above + branch terminal below* is the
cleanest layout when one decision stage has one auxiliary input and one
failure exit (the common "capability-match" pattern).

## Reference TikZ template

```latex
% NOTE: pt* colors are Paul Tol bright palette, defined once in the
% preamble. Replace with any palette as long as the semantic mapping
% above is preserved.
\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[
    node distance=3mm,
    stage/.style={rectangle, draw=gray!55, rounded corners=2.5pt,
        line width=0.5pt, minimum width=2.25cm, minimum height=1.05cm,
        align=center, font=\footnotesize\sffamily, fill=ptblue!12},
    decision/.style={rectangle, draw=ptyellow!55!black, rounded corners=2.5pt,
        line width=0.6pt, minimum width=2.25cm, minimum height=1.05cm,
        align=center, font=\footnotesize\sffamily, fill=ptyellow!22},
    io/.style={rectangle, draw=gray!55, rounded corners=2.5pt,
        line width=0.5pt, minimum width=1.55cm, minimum height=1.05cm,
        align=center, font=\footnotesize\sffamily, fill=ptgrey!22},
    winbox/.style={rectangle, draw=ptgreen!55!black, rounded corners=2.5pt,
        line width=0.5pt, minimum width=1.75cm, minimum height=1.05cm,
        align=center, font=\footnotesize\sffamily, fill=ptgreen!16},
    aux/.style={rectangle, draw=gray!55, rounded corners=2.5pt,
        line width=0.5pt, minimum width=2.6cm, minimum height=0.65cm,
        align=center, font=\scriptsize\sffamily, fill=ptblue!22},
    oosbox/.style={rectangle, draw=ptred!55!black, rounded corners=2.5pt,
        line width=0.5pt, minimum width=1.8cm, minimum height=0.55cm,
        align=center, font=\scriptsize\sffamily, fill=ptred!10},
    arrow/.style={-{Stealth[length=4pt]}, thin},
    lbl/.style={font=\scriptsize\sffamily, text=gray!50!black},
]
\node[io]                          (in)  at (0, 0) {Input};
\node[stage,    right=3mm of in]   (s1)  {1.\,Stage A};
\node[stage,    right=3mm of s1]   (s2)  {2.\,Stage B};
\node[decision, right=3mm of s2]   (s3)  {3.\,Decision?};
\node[stage,    right=3mm of s3]   (s4)  {4.\,Stage C};
\node[winbox,   right=3mm of s4]   (out) {Output};

\node[aux,    above=7mm of s3]     (cap) {Auxiliary input};
\node[oosbox, below=7mm of s3]     (rej) {rejected};

\draw[arrow] (in) -- (s1);
\draw[arrow] (s1) -- (s2);
\draw[arrow] (s2) -- (s3);
\draw[arrow] (s3) -- node[lbl, above]{yes} (s4);
\draw[arrow] (s4) -- (out);
\draw[arrow] (cap.south) -- (s3.north);
\draw[arrow] (s3.south)  -- node[lbl, right, inner sep=1pt]{no} (rej.north);
\end{tikzpicture}}
```

## Anti-patterns (do not do)

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| TikZ `diamond` shape for decisions | Reads as dated flowchart; absent from recent accepted papers | Use a rounded rectangle whose text is a question |
| Diagonal arrows | Visually wonky; reviewers comment | Right-angle routing (`-|` or `|-`) or place nodes so the arrow is horizontal/vertical |
| Em-dash-style "configure, execute, capture" arrow labels | AI-rhetoric tell; clutters the arrow | Either delete the label (the diagram is self-evident) or move it to the caption |
| Style keys named `cap`, `out`, `in`, `to`, `from` | Collide with TikZ reserved keywords (`cap` = line cap, `out=` = `to`-path angle) | Suffix the role: `capbox`, `oosbox`, `inputbox` |
| Saturated colors | Fails grayscale-legibility check | Stick to `color!12` to `color!22` pastels |
| Variable box widths in a pipeline | Reads as architecture, not pipeline | Force `minimum width=...` to one value |
| Diamond aspect ratios that crush text | Two-line text becomes illegible | Use rounded rectangle (see #1) |
| Floating sidecar with a long diagonal arrow into the middle of the pipeline | The diagonal is the wonkiness the user is reacting to | Put the sidecar directly above or below the stage it feeds; vertical arrow only |

## Sources

- ArachNet (HotNets'25): https://conferences.sigcomm.org/hotnets/2025/papers/hotnets25-final235.pdf
- Confucius (SIGCOMM'25): https://minlanyu.seas.harvard.edu/writeup/sigcomm25.pdf
- netUnicorn (CCS'23): https://arxiv.org/pdf/2306.08853
- Democratize NetAI (HotNets'19): https://sites.cs.ucsb.edu/~arpitgupta/pdfs/democratize_netai.pdf
- Mani et al. (HotNets'23): https://conferences.sigcomm.org/hotnets/2023/papers/hotnets23_mani_zhou.pdf
- CCAnalyzer (HotNets'25): https://conferences.sigcomm.org/hotnets/2025/papers/hotnets25-final681.pdf
