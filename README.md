# data-visualization-skill

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that teaches researchers to think about data before plotting it, then produce publication-quality figures with built-in reflection.

## The Problem

Most plotting guides teach the mechanics: how to set axis labels, how to call `plt.plot()`, how to export at 300 DPI. Students learn to make figures that look professional without ever learning to make figures that *say something*. The result is evaluation sections full of beautiful, meaningless plots — bar charts of means that hide distributions, CDFs that nobody can compare because five lines overlap, figures that confirm what the author already believed without ever looking for surprise.

The root cause is that students skip the hardest part of visualization: deciding what to show and why. They go straight from "I have data" to "I need a figure," bypassing the intellectual work of understanding the data, forming expectations, and choosing a representation that honestly communicates the structure they found.

This skill fixes that by enforcing a three-phase workflow: **Brainstorm → Plan → Execute**. No code until you can articulate what you're trying to see. No execution until you've made every design decision explicit. No moving on until you've reflected on what the figure actually shows.

## Intellectual Foundations

This skill is built on ideas from three sources, combined into a workflow designed for systems and networking research.

### John W. Tukey — *Exploratory Data Analysis* (1977)

Tukey's core principle: **"It is important to understand what you CAN DO before you learn to measure how WELL you seem to have DONE it."** Exploration must precede confirmation. Before you make a paper figure, you should have made dozens of disposable plots that shaped your understanding. Tukey also gave us:

- **"The greatest value of a picture is when it forces us to notice what we never expected to see."** A figure that only confirms what you already believe is a weak figure. The best figures reveal surprise.
- **Residual analysis.** Remove the dominant pattern and examine what remains. The deviations from the expected — not the expected itself — are where discovery happens.
- **Re-expression.** Data transformations (log, square root, reciprocal) are not just axis formatting choices. They are analytical tools that make hidden structure visible. Tukey's "ladder of powers" provides a systematic way to choose.
- **The box plot.** Tukey invented it as a *comparison* tool — the point is to put many side by side and see distributional differences at a glance.

The Brainstorm mode channels Tukey: it forces you to state your expectations, name what would surprise you, and think about residuals before you write a line of code.

### Edward Tufte — The Data-Ink Ratio

Every mark on a figure should encode data. Remove chartjunk, maximize the ratio of data-ink to total ink, and let the data speak. This principle informs the execution defaults: no top/right spines, subtle grid, serif fonts, no decorative elements.

### The WALTER Principle — Narrating the Visual Story

Developed in the Gupta Research Group at UC Santa Barbara as a lab norm for presenting figures. **WALTER** is an acronym for a structured walkthrough that must accompany every figure shared in a meeting, on Slack, or in a paper:

| Letter | Question |
|--------|----------|
| **W** | **What is the hypothesis?** Why does this figure exist? |
| **A** | **Axes:** What do x and y represent? State it explicitly with units. |
| **L** | **Look here:** Where should the viewer focus? Direct their attention. |
| **T** | **Trend:** What is the dominant pattern? One sentence. |
| **E** | **Exception:** What breaks the pattern? This is where the insight lives. |
| **R** | **Result:** What is the takeaway? Does it connect back to W? |

WALTER serves two purposes. First, it is a communication protocol — it ensures the figure's message is received as intended, not left to interpretation. Second, it is a **comprehension test**: if you cannot write a WALTER paragraph for your figure, you do not yet understand what the figure shows. The Execute mode forces a WALTER reflection after every figure is generated.

## How the Skill Works

The skill has three modes, invoked as `/viz brainstorm`, `/viz plan`, and `/viz execute`. Each must complete before the next begins.

### `/viz brainstorm` — Internalize what you're trying to see

This mode is Socratic. No code is written. No plot types are suggested. The skill asks you:

1. **What is the data?** What is one observation, one batch, how many per group?
2. **What question are you trying to answer?** Not "what plot" — what question about the world.
3. **Are you exploring or confirming?**
4. **What do you expect to see?** Write a prediction before plotting.
5. **What would surprise you?** Name it — this is what you should look for.
6. **If you removed the obvious pattern, what would be left?** (Tukey's residual principle)
7. **Who is the audience?** Exploration notebook, Slack, paper, presentation?
8. **What sentence in the paper does this figure support?**

The mode ends when you can articulate the visualization intent in 3–4 sentences and the skill confirms it back to you. If you can't answer these questions, you aren't ready to plot.

### `/viz plan` — Decide how to realize it

This mode translates intent into concrete decisions:

1. **Data inspection.** The skill reads your data file, reports the schema (columns, types, row count, NaN counts), and asks which columns are x, y, and grouping variables.

2. **Plot type recommendation.** Using a built-in decision tree covering matplotlib and seaborn, the skill recommends a plot type with reasoning. It covers distributions (histogram, KDE, CDF, CCDF, box plot, violin), group comparisons (box plot, swarm plot, grouped bar), continuous relationships (scatter, line, regression), time series (with smoothing options), multi-factor displays (heatmap, faceted small multiples), and multi-variable overviews (pair plot, joint plot).

3. **Layout and formatting.** Single or double column? Golden ratio or custom aspect? Color palette, legend placement, axis scales (with justification for log vs. linear).

4. **Output: `plot_context.md`.** All decisions are synthesized into a structured markdown file — the contract between planning and execution. This file contains the intent (question, claim, prediction, surprise condition), the data specification (source, schema, filtering, variables), the plot design (type, library, sizing, colors, scales), and the output target (format, DPI, filename).

### `/viz execute` — Generate, run, and reflect

This mode reads the `plot_context.md` and:

1. **Generates a self-contained Python script** using publication-quality defaults (serif fonts, golden ratio sizing, colorblind-safe palettes, 300 DPI, no chartjunk).
2. **Runs the script** and displays the figure.
3. **Forces WALTER reflection.** You cannot move on without narrating: hypothesis, axes, where to look, trend, exception, result. If the result doesn't connect back to the hypothesis, the skill flags it and offers three paths: revise the claim, investigate the discrepancy, or adjust the visualization.
4. **Runs post-visualization checks.** Is the axis scale honest? Are you summarizing away the story? What would a skeptical reviewer challenge? Would a different plot type reveal something this one hides?
5. **Saves everything.** The WALTER narration and post-visualization notes are appended to `plot_context.md`, creating a complete record from intent through reflection.

## What's in This Repo

```
data-visualization-skill/
├── SKILL.md                              # The skill definition (install this)
├── README.md                             # You are here
├── setup.sh                              # One-command install script
├── .gitignore
└── reference/
    ├── before_you_plot.md                # 15-question pre-plotting questionnaire
    ├── plot_context_template.md          # Blank template for plot_context.md
    └── matplotlib_defaults.py            # Publication-quality rcParams + helpers
```

### `SKILL.md`

The skill itself. Contains all three modes (Brainstorm, Plan, Execute), the plot type decision tree, seaborn vs. matplotlib guidance, the WALTER reflection protocol, and the lab formatting standards. This is the file that Claude Code reads when you invoke `/viz`.

### `reference/before_you_plot.md`

A standalone 15-question questionnaire organized in five parts:

1. **What Are You Looking At?** — Confront the data before deciding how to show it.
2. **What Question Are You Asking?** — Separate exploration from confirmation. Predict, then look.
3. **Is Your Representation Honest?** — Axis scales, over-summarization, the "cover the caption" test.
4. **What Is This Figure's Job in the Paper?** — The one-sentence test, the necessity test, the skeptical-reviewer test.
5. **WALTER It** — Narrate the visual story to verify your own understanding.

This document can be used independently of the skill — print it out, pin it above your desk, or share it with students who don't use Claude Code.

### `reference/plot_context_template.md`

A blank template for the `plot_context.md` file that the Plan mode generates. You can use this directly for manual planning or as a starting point when working without the skill.

### `reference/matplotlib_defaults.py`

Drop-in Python module with publication-quality defaults:

- **`golden_ratio_figsize(width, fraction)`** — Returns dimensions using the golden ratio. `fraction=0.5` for wide time series, `1.0` for standard plots, `1.2` for squarer CDFs.
- **`set_pub_style(ax)`** — Removes top/right spines, adds subtle grid, sets outward ticks.
- **`plot_cdf(data, label)`** — CDF with proper styling.
- **`plot_ccdf(data, label, log_scale)`** — CCDF with optional log-log axes for heavy tails.
- **`plot_time_series(x, y, smooth_window)`** — Time series with optional rolling-median smoothing.
- **`COLORS`** — Colorblind-safe palette (Set1_9 from ColorBrewer).
- **`MARKERS`** / **`LINE_STYLES`** — For grayscale distinguishability.

Usage: `import matplotlib_defaults` auto-configures all rcParams. Or import individual helpers.

## Installation

### Claude Code (recommended)

```bash
git clone https://github.com/SNL-UCSB/data-visualization-skill.git
cd data-visualization-skill
./setup.sh
```

This installs the skill to `~/.claude/skills/viz/`. You can then use `/viz brainstorm`, `/viz plan`, and `/viz execute` in any Claude Code session.

### Manual

Copy `SKILL.md` to `~/.claude/skills/viz/SKILL.md`. Copy the `reference/` directory alongside it.

### Standalone (without Claude Code)

The reference materials work independently:

- Use `before_you_plot.md` as a printed questionnaire for lab meetings.
- Use `plot_context_template.md` to structure your figure planning in any markdown editor.
- Drop `matplotlib_defaults.py` into your project and `import matplotlib_defaults` to get publication-quality defaults without configuring rcParams manually.

## Adapting for Your Lab

The skill ships with formatting defaults tuned for systems and networking venues (SIGCOMM, NSDI, CoNEXT, IMC). To adapt:

1. **Figure sizing.** Edit the `Lab Standards Reference` section of `SKILL.md` to match your venue's column widths. Most CS venues use 3.5" single / 7.0" double column.
2. **Font.** Change `font.family` in `matplotlib_defaults.py`. Some venues require sans-serif (Helvetica/Arial).
3. **Color palette.** Replace `Set1_9` with your preferred colorblind-safe palette. The key constraint is that figures must also be distinguishable in grayscale (use markers + line styles, not just color).
4. **WALTER.** The acronym and protocol are general-purpose. You can rename it or adapt the letters, but keep the closed-loop structure: the last step (Result) must connect back to the first (hypothesis/Why).
5. **Brainstorm questions.** The Tukey-derived questions are domain-agnostic. You may want to add domain-specific questions for your field (e.g., "Have you checked for confounds?" in clinical research, or "Is this measurement affected by load?" in systems research).

## Design Principles

**Philosophy over mechanics.** The skill spends more tokens on *thinking about what to plot* than on *how to format it*. The formatting is handled by defaults and templates. The thinking cannot be templated — it must be practiced.

**Closed loop.** Every figure goes through: intent (brainstorm) → plan (design decisions) → execution (code) → reflection (WALTER). The reflection step is not optional. If the result doesn't connect back to the hypothesis, you aren't done.

**Exploration before confirmation.** The skill explicitly asks whether you are exploring or confirming, and adjusts its behavior. During exploration, ugly is fine and surprise is the goal. During confirmation, precision and honesty are the goals.

**Honest by default.** The skill warns against bar charts of means (which hide distributions), asks whether log scale would reveal hidden structure, and challenges you to consider what a different plot type would show. The default is to show more data, not less.

**Self-contained.** Every reference file works independently. You don't need Claude Code to use the questionnaire, the plot context template, or the matplotlib defaults. The skill enhances the workflow but doesn't gate it.

## Intellectual Lineage

| Source | Contribution | Where it appears |
|--------|-------------|------------------|
| Tukey, *Exploratory Data Analysis* (1977) | Explore before confirm; predict before plot; residual analysis; re-expression; the box plot | Brainstorm mode, questionnaire Part 2 |
| Tufte, *The Visual Display of Quantitative Information* (1983) | Data-ink ratio; chartjunk removal; small multiples | Execute mode defaults, Lab Standards |
| Gupta Lab, WALTER principle (2025) | Structured figure narration; comprehension self-test | Execute mode Step 4, questionnaire Part 5 |
| Seaborn documentation | Function taxonomy; plot type selection guidance | Plan mode decision tree |
| Matplotlib best practices | rcParams configuration; publication sizing | Execute mode code generation, `matplotlib_defaults.py` |

## Contributing

Contributions welcome. The most valuable additions would be:

- **Domain-specific plot type guidance** for fields beyond networking (ML evaluation, clinical, social science).
- **Additional re-expression examples** showing when sqrt, reciprocal, or arcsine transforms are more appropriate than log.
- **Example `plot_context.md` files** from real papers, showing the full brainstorm → plan → execute → reflect cycle.
- **Venue-specific formatting presets** (NeurIPS, ICML, CHI, USENIX Security, etc.).

## License

MIT

## Citation

If you use this skill in your research workflow, please cite:

```
@misc{data-visualization-skill,
  author = {Gupta, Arpit},
  title = {data-visualization-skill: A Claude Code skill for research visualization},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/SNL-UCSB/data-visualization-skill}
}
```
