# data-visualization-skill

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that teaches researchers to think about data before plotting it, then produce publication-quality figures with built-in reflection.

## The Problem

Most plotting guides teach the mechanics: how to set axis labels, how to call `plt.plot()`, how to export at 300 DPI. Students learn to make figures that look professional without ever learning to make figures that *say something*. The result is evaluation sections full of beautiful, meaningless plots — bar charts of means that hide distributions, CDFs that nobody can compare because five lines overlap, figures that confirm what the author already believed without ever looking for surprise.

The root cause is that students skip the hardest part of visualization: deciding what to show and why. They go straight from "I have data" to "I need a figure," bypassing the intellectual work of understanding the data, forming expectations, and choosing a representation that honestly communicates the structure they found.

This skill fixes that by enforcing a six-phase workflow: **Ingest → Explore → Brainstorm → Plan → Execute → Analyze**. Look at the raw data before forming hypotheses. Explore visually before committing to a plot type. No production code until you can articulate what you're trying to see. No execution until you've made every design decision explicit. And after the figure is generated, validate what it actually says against what you intended — closing the loop between hypothesis and evidence.

Not every figure requires all six phases. Experienced researchers who already know their data and have a clear intent can skip straight to Plan. The early phases (Ingest, Explore, Brainstorm) are designed to build the intuition that experts already carry — they meet students where they are.

## Intellectual Foundations

This skill is built on ideas from several sources, combined into a workflow designed for systems and networking research.

### John W. Tukey — *Exploratory Data Analysis* (1977)

Tukey's core principle: **"It is important to understand what you CAN DO before you learn to measure how WELL you seem to have DONE it."** Exploration must precede confirmation. Before you make a paper figure, you should have made dozens of disposable plots that shaped your understanding. Tukey also gave us:

- **"The greatest value of a picture is when it forces us to notice what we never expected to see."** A figure that only confirms what you already believe is a weak figure. The best figures reveal surprise.
- **Residual analysis.** Remove the dominant pattern and examine what remains. The deviations from the expected — not the expected itself — are where discovery happens.
- **Re-expression.** Data transformations (log, square root, reciprocal) are not just axis formatting choices. They are analytical tools that make hidden structure visible. Tukey's "ladder of powers" provides a systematic way to choose.
- **The box plot.** Tukey invented it as a *comparison* tool — the point is to put many side by side and see distributional differences at a glance.

The Brainstorm mode channels Tukey: it forces you to state your expectations, name what would surprise you, and think about residuals before you write a line of code.

### Philipp Winter — *Research Power Tools* (2023)

Winter's [*Research Power Tools*](https://research-power-tools.com/) is a practical guide to productive systems research, covering everything from version control to academic programming. A key theme relevant to this skill: **use command-line tools to inspect your data before writing any code.** Basic Unix commands — `head`, `wc`, `cut`, `sort | uniq -c`, `awk` — give you an unmediated view of what is actually in the file: how big it is, what the columns look like, what the distinct values are, where the data is missing or broken. Many students skip this step entirely, jumping straight to `pd.read_csv()` and missing issues that are visible at a glance in the terminal.

The Ingest mode channels Winter: before you open Python, look at the raw data with CLI tools. The `reference/cli_data_inspection.md` cheat sheet provides copy-paste one-liners for this purpose.

### Edward Tufte — Visual Integrity and the Data-Ink Ratio

Tufte's *The Visual Display of Quantitative Information* (1983) provides the aesthetic and ethical framework for this skill's execution defaults. Several of his principles directly inform how the skill generates figures:

- **Data-ink ratio.** Every mark on a figure should encode data. Maximize the ratio of data-ink to total ink by removing anything that does not carry information. This is why the skill's defaults strip top and right spines (they add visual weight without encoding anything), use subtle dotted gridlines at low opacity (present if you look for them, invisible if you don't), and avoid decorative elements like background fills or 3D effects.
- **Chartjunk.** Tufte's term for visual elements that distract from the data: heavy borders, gradient fills, unnecessary legends, ornamental gridlines. The lab standards enforce a minimal style — 0.5pt axis lines, 1.0pt data lines, serif fonts — so the data is always the most prominent element in the figure.
- **Small multiples.** Rather than overloading a single plot with too many variables (multiple hues, sizes, and styles that become unreadable), show a grid of simple, consistent panels that the eye can compare at a glance. This is why the Plan mode recommends faceted plots (`sns.relplot` with `col=`/`row=`) over cramming everything into one panel, and why the skill's design principle is "several simple plots are usually more effective than one complex plot."
- **Graphical integrity.** The representation should not distort the data. The skill's post-visualization checks explicitly ask: "Does the axis scale faithfully show the data, or is it hiding structure?" and "Are you summarizing away important information?" — prompting students to consider whether log scale would reveal hidden patterns, whether showing means hides the distribution, and whether a different plot type would tell a different story.
- **The lie factor.** The visual impact of a graphic should be proportional to the quantity represented. This is why the skill defaults to starting axes at zero for bar charts, warns against truncated axes that exaggerate small differences, and recommends colorblind-safe palettes that don't create false visual hierarchies.

### Seaborn — Fast Exploratory Visualization

The [seaborn library](https://seaborn.pydata.org/tutorial.html) provides high-level statistical visualization functions that generate informative plots with minimal code. Where matplotlib gives you pixel-level control for publication figures, seaborn gives you speed and semantic clarity for exploration. One-liners like `sns.pairplot(df, hue="group")` or `sns.displot(df, x="col", kind="ecdf")` let you see the structure of a new dataset in seconds, without committing to any design decisions.

The Explore mode uses seaborn as its primary tool, with concrete recipes organized by question: "What does this distribution look like?" → `histplot`. "How do groups compare?" → `boxplot` or `violinplot`. "Show me everything at once" → `pairplot`. Students learn these one-liners as part of the skill, building a toolkit for the exploratory "fishing expeditions" that precede any paper figure.

### The WALTER Principle — Narrating the Visual Story

WALTER is a structured figure narration framework that has been a common practice in systems and networking research for years. The acronym provides a walkthrough that should accompany every figure shared in a meeting, on Slack, or in a paper:

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

The skill has six modes, invoked as `/viz ingest`, `/viz explore`, `/viz brainstorm`, `/viz plan`, `/viz execute`, and `/viz analyze`. Not every figure requires all six — experienced researchers can skip directly to `/viz plan` or `/viz execute`.

### `/viz ingest` — Understand what you have

Start at the command line, not in Python. Use basic Unix tools (`head`, `wc`, `cut`, `sort | uniq -c`) to get a raw, unmediated sense of the data — how big it is, what the columns look like, where it's broken. Then load it in Python for a structured schema report. Saves a `data_summary.md`.

### `/viz explore` — Let the data do the talking

Generate quick, disposable plots using seaborn to look at the data from multiple angles before forming any hypotheses. Univariate distributions (`histplot`, `ecdfplot`), bivariate relationships (`pairplot`, `scatterplot`, `jointplot`), group comparisons (`boxplot`, `violinplot`), temporal structure (`lineplot`). The plots are throwaway — speed and coverage matter, not aesthetics. Saves an `exploration_log.md`.

**A valid outcome of exploration is discovering that the data is flawed and the experiment needs revisiting.** It is better to discover this now than after producing a polished figure from broken data.

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

The mode ends when you can articulate the visualization intent in 3–4 sentences and the skill confirms it back to you. Saves a `braindump.md`. If you can't answer these questions, you aren't ready to plot. Experienced students can also write their own `braindump.md` and skip directly to Plan.

### `/viz plan` — Decide how to realize it

This mode translates intent into concrete decisions. It loads prior artifacts (`braindump.md`, `data_summary.md`, `exploration_log.md`) if they exist:

1. **Variable mappings.** Confirm which columns are x, y, and grouping variables for this specific figure.

2. **Plot type recommendation.** Using a built-in decision tree covering matplotlib and seaborn, the skill recommends a plot type with reasoning. It covers distributions (histogram, KDE, CDF, CCDF, box plot, violin), group comparisons (box plot, swarm plot, grouped bar), continuous relationships (scatter, line, regression), time series (with smoothing options), multi-factor displays (heatmap, faceted small multiples), and multi-variable overviews (pair plot, joint plot).

3. **Layout and formatting.** Single or double column? Golden ratio or custom aspect? Color palette, legend placement, axis scales (with justification for log vs. linear).

4. **Output: `plot_context.md`.** All decisions are synthesized into a structured markdown file — the contract between planning and execution.

### `/viz execute` — Generate and run the code

This mode is purely operational. It reads the `plot_context.md` and:

1. **Generates a self-contained Python script** using publication-quality defaults (serif fonts, golden ratio sizing, colorblind-safe palettes, 300 DPI, no chartjunk).
2. **Runs the script** and displays the figure.
3. **Diagnoses and fixes** any errors — wrong data paths, schema mismatches, missing dependencies.

No reflection happens here. The figure is produced and saved. All analysis happens in the next mode.

### `/viz analyze` — What is this figure really telling you?

This is the mode that turns a plotting exercise into a learning experience. It has two phases: the student interprets first (so the skill doesn't anchor their thinking), then the skill provides substantive feedback.

1. **Student interpretation first.** The student describes what they see, whether it matches their prediction, and what surprises them — before the skill offers any analysis.
2. **WALTER narration.** The structured walkthrough: hypothesis, axes, look here, trend, exception, result. Drafted from accumulated context and confirmed with the student.
3. **First-principles feedback.** The skill cross-references the figure against all prior artifacts and applies three analytical lenses:
   - *Tukey lens* — Does the figure match the prediction from `braindump.md`? If not, the discrepancy may be more interesting than the original hypothesis. What would residual analysis reveal? Would a different scale (log, sqrt) expose hidden structure?
   - *Tufte lens* — Is every visual element earning its place? Is the axis scale honest? Are you summarizing away the distribution? Would a different plot type reveal something this one hides?
   - *Hypothesis validation* — Does the figure actually support the specific claim from `braindump.md`? What would a skeptical reviewer focus on? Are there confounds?
4. **Next steps.** The skill recommends one of: finalize for the paper, revise the claim to match the data, iterate on the figure design, or go back to `/viz explore` to investigate something unexpected.
5. **Saves everything.** The WALTER narration, first-principles feedback, and next steps are appended to `plot_context.md`, creating a complete record from intent through analysis.

## What's in This Repo

```
data-visualization-skill/
├── SKILL.md                              # The skill definition (install this)
├── README.md                             # You are here
├── setup.sh                              # One-command install script
├── .gitignore
└── reference/
    ├── before_you_plot.md                # 15-question pre-plotting questionnaire
    ├── cli_data_inspection.md            # CLI one-liners for raw data inspection
    ├── plot_context_template.md          # Blank template for plot_context.md
    ├── matplotlib_defaults.py            # Publication-quality rcParams + helpers
    └── figure_presentation_gate.md       # Numbered, output-verified figure/table gate
```

### `SKILL.md`

The skill itself. Contains all six modes (Ingest, Explore, Brainstorm, Plan, Execute, Analyze), CLI inspection recipes, seaborn exploration one-liners, the plot type decision tree, seaborn vs. matplotlib guidance, the WALTER reflection protocol, first-principles feedback framework, and the lab formatting standards. This is the file that Claude Code reads when you invoke `/viz`.

### `reference/before_you_plot.md`

A standalone 15-question questionnaire organized in five parts:

1. **What Are You Looking At?** — Confront the data before deciding how to show it.
2. **What Question Are You Asking?** — Separate exploration from confirmation. Predict, then look.
3. **Is Your Representation Honest?** — Axis scales, over-summarization, the "cover the caption" test.
4. **What Is This Figure's Job in the Paper?** — The one-sentence test, the necessity test, the skeptical-reviewer test.
5. **WALTER It** — Narrate the visual story to verify your own understanding.

This document can be used independently of the skill — print it out, pin it above your desk, or share it with students who don't use Claude Code.

### `reference/cli_data_inspection.md`

A copy-paste cheat sheet of Unix command-line one-liners for inspecting CSV/TSV files before opening Python. Organized by task: first look (`wc`, `head`, `tail`), column inspection (`cut`, `sort`, `uniq`), quick statistics (`awk`, `datamash`), data quality checks (`grep`, duplicate detection), and filtering/sampling (`awk`, `shuf`). Inspired by the practical tooling philosophy in Philipp Winter's [*Research Power Tools*](https://research-power-tools.com/).

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

### `reference/figure_presentation_gate.md`

The enforceable, numbered figure- and table-presentation gate — to figures what a mechanical style
gate is to prose. Where the Lab Standards in `SKILL.md` are a prose mnemonic, this file is the
checklist that actually gates a figure in Execute mode: numbered rules (**F** universal, **D** data
figures, **G** mermaid/SVG diagrams, **T** tables) each with a wrong→right example and a verification
method, plus a runnable audit block. Its core discipline: **verify in the compiled PDF, not the
source and not a browser preview** — render, rasterize the page (`pdftoppm`), open it, and report
what you saw on which page. Covers a `target-medium` selector (book/PDF grayscale + body font vs.
conference-paper color + serif) so the same gate serves both. This is what closes the "prose
standards nobody enforced" gap.
- **`MARKERS`** / **`LINE_STYLES`** — For grayscale distinguishability.

Usage: `import matplotlib_defaults` auto-configures all rcParams. Or import individual helpers.

## Installation

### Claude Code (recommended)

```bash
git clone https://github.com/SNL-UCSB/data-visualization-skill.git
cd data-visualization-skill
./setup.sh
```

This installs the skill to `~/.claude/skills/viz/`. You can then use `/viz ingest`, `/viz explore`, `/viz brainstorm`, `/viz plan`, `/viz execute`, and `/viz analyze` in any Claude Code session.

### Manual

Copy `SKILL.md` to `~/.claude/skills/viz/SKILL.md`. Copy the `reference/` directory alongside it.

### Standalone (without Claude Code)

The reference materials work independently:

- Use `cli_data_inspection.md` as a cheat sheet for inspecting data files at the command line.
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

## Part of a Research Skills Family

This skill belongs to a family of three Claude Code skills built by the [Systems and Networking Lab (SNL)](https://github.com/SNL-UCSB) at UC Santa Barbara. Together they cover the core research pipeline — reading the literature, visualizing data, and writing the paper. The design philosophy behind the family is described in [*Systems for Agents, Agents for Systems*](https://sites.cs.ucsb.edu/~arpitgupta/blog/systems-for-agents-agents-for-systems.html).

| Skill | What it compresses | What it protects |
|-------|-------------------|-----------------|
| [**literature-survey-skill**](https://github.com/SNL-UCSB/literature-survey-skill) | Paper ingestion, claim extraction, cross-referencing | Hypothesis formation, gap recognition, critical reading |
| **data-visualization-skill** (this repo) | Plot formatting, code generation, layout mechanics | Deciding what to show, whether representations are honest, what the figure means |
| [**paper-writing-skill**](https://github.com/SNL-UCSB/paper-writing-skill) | Section structure, voice consistency, page compression | Argument construction, positioning, intellectual contribution |

### Shared intellectual spine

All three skills operate under one principle: **bridge the gap between ideation and execution — compress the operational middle, protect the thinking.** The machine handles logistics (formatting, boilerplate, cross-referencing); the human retains judgment (what to claim, what to show, what matters). Three design commitments are shared across the family:

1. **Empirical foundations.** Each skill's workflow was extracted from forensic analysis of actual research practice — tracked edits, real figure iterations, observed survey strategies — not invented from first principles. The writing skill's editorial principles, for example, were distilled from 7,600+ tracked edits across six papers (see [*The Paper Behind the Paper*](https://sites.cs.ucsb.edu/~arpitgupta/blog/the-paper-behind-the-paper.html)).
2. **Structured externalization.** Vague intuitions become concrete, inspectable statements before any execution begins. In this skill, that is the `braindump.md`; in the survey skill, it is the intent document; in the writing skill, it is the 34-question brainstorm.
3. **Clean human–machine division.** Each skill draws an explicit line: judgment stays with the researcher, mechanics go to the tool. The line is different in each skill, but the principle is the same.

### How the skills reinforce each other

The skills are independent — use any one alone — but they form a closed loop when used together:

- The **survey skill's** landscape maps and competitive positioning feed directly into the paper's related work and introduction. Its claim extraction — built on the invariant questions from [*A First-Principles Approach to Networked Systems*](https://sites.cs.ucsb.edu/~arpitgupta/first-principles-networking/) — identifies gaps that motivate new contributions.
- The **visualization skill's** exploration phase can reshape what claims are defensible — a figure that contradicts your hypothesis changes the paper's argument, not just the evaluation section. The WALTER narration from `/viz analyze` provides ready-made figure descriptions for the paper.
- The **writing skill** sharpens reading and vice versa: writing a precise claim reveals what evidence is missing; reading with the six-move introduction formula in mind reveals how other authors positioned their work.

All three skills also share the **WALTER principle** as a common thread — the survey skill uses it during deep reading to analyze figures in papers you're reviewing, this skill uses it to narrate your own figures, and the writing skill uses it to ensure figure references in the text faithfully represent what the figure shows.

## Intellectual Lineage

| Source | Contribution | Where it appears |
|--------|-------------|------------------|
| Tukey, *Exploratory Data Analysis* (1977) | Explore before confirm; predict before plot; residual analysis; re-expression; the box plot | Explore mode, Brainstorm mode, questionnaire Part 2 |
| Winter, *Research Power Tools* (2023) | CLI-first data inspection; practical research tooling | Ingest mode, `cli_data_inspection.md` |
| Tufte, *The Visual Display of Quantitative Information* (1983) | Data-ink ratio; chartjunk removal; small multiples | Execute mode defaults, Lab Standards |
| WALTER principle (common practice in systems/networking research) | Structured figure narration; comprehension self-test | Execute mode Step 4, questionnaire Part 5 |
| [Seaborn tutorial & API](https://seaborn.pydata.org/tutorial.html) | Exploratory visualization recipes; plot type selection guidance | Explore mode, Plan mode decision tree |
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
