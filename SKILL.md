---
name: viz
description: "Research visualization assistant with six modes: /viz ingest (understand the data schema), /viz explore (disposable plots to build intuition), /viz brainstorm (internalize what to plot via Tukey-inspired questioning), /viz plan (decide how to realize it — plot types, data sources, layout — producing a plot_context.md), /viz execute (generate and run the code), and /viz analyze (first-principles feedback on the generated figure). Use when students mention plotting, figures, graphs, visualization, CDF, scatter plot, box plot, or any figure-making task for a research paper."
---

# Visualization Skill — Ingest → Explore → Brainstorm → Plan → Execute → Analyze

This skill helps you create research-quality visualizations through a six-phase workflow. The philosophy: *let the data do the talking* before you decide what to say, internalize *what* you want to show and *why* before touching any production code, and *validate what the figure actually says* against what you intended.

**Modes:**
- `/viz ingest` — Understand what you have: schema, shape, quality (structural)
- `/viz explore` — Look at the data from multiple angles with disposable plots (intuitive)
- `/viz brainstorm` — Think through what you are trying to visualize (philosophical)
- `/viz plan` — Decide how to realize it: plot type, layout, data source (mechanistic)
- `/viz execute` — Generate and run the code (operational)
- `/viz analyze` — Reflect on the figure and validate against your hypothesis (critical)

**Not every figure requires all six modes.** The early modes (Ingest, Explore, Brainstorm) are designed to build the intuition that experienced researchers already have. If you already know your data and have a clear visualization intent, you can skip straight to `/viz plan` — optionally writing your own `braindump.md` to capture your intent, which Plan and Execute will pick up automatically.

If the student invokes `/viz` without a mode, assess where they are:
- They have raw data and aren't sure what's in it → suggest `/viz ingest`
- They know their data but haven't looked at it yet → suggest `/viz explore`
- They've explored but haven't articulated what they want to show → suggest `/viz brainstorm`
- They know exactly what figure they need → suggest `/viz plan`
- They have a `plot_context.md` ready → suggest `/viz execute`
- They have a figure and want feedback → suggest `/viz analyze`

---

## Mode 0: Ingest — "What do you have?"

**Purpose:** Understand the structure, shape, and quality of the data before looking at it visually. This is the mechanical foundation — you cannot explore what you do not understand structurally.

**Start at the command line, not in Python.** Before importing anything, use basic Unix tools to look at the raw data. This builds a concrete, unmediated sense of what the file contains — how big it is, what the columns look like, whether there are obvious problems. Many students skip this step and go straight to `pd.read_csv()`, missing issues that are visible at a glance in the terminal.

### Step 1: Locate the data

Ask the student:

> Where is your data? Give me the path to the file(s) — CSV, Parquet, JSON, pickle, or a directory of results.

### Step 2: CLI first look

For CSV/TSV files, run these commands to build a raw picture of the data before opening Python. **Show the student the commands and their output** — teaching them to do this themselves is part of the skill:

```bash
# How big is it?
wc -l data.csv                    # row count (including header)
ls -lh data.csv                   # file size

# What does it look like?
head -5 data.csv                  # first 5 lines (header + 4 rows)
tail -5 data.csv                  # last 5 lines

# What are the columns?
head -1 data.csv | tr ',' '\n' | nl   # numbered column list

# How many columns?
head -1 data.csv | awk -F',' '{print NF}'

# Quick frequency table for a categorical column (e.g., column 3)
cut -d, -f3 data.csv | tail -n+2 | sort | uniq -c | sort -rn | head -10

# Quick min/max for a numeric column (e.g., column 4)
cut -d, -f4 data.csv | tail -n+2 | sort -n | head -1    # min
cut -d, -f4 data.csv | tail -n+2 | sort -n | tail -1    # max

# Check for empty fields
grep -c ',,' data.csv

# Check for duplicate rows
sort data.csv | uniq -d | wc -l
```

A full CLI cheat sheet is available at `reference/cli_data_inspection.md` with one-liners for statistics, data quality checks, filtering, and sampling.

For binary formats (Parquet, pickle), skip the CLI step and go directly to Step 3.

### Step 3: Read and report the schema

After the CLI first look, load the data in Python for a structured summary:

1. **Read the file** (or a sample: first 20 rows + dtypes + shape).
2. **Report the schema** back to the student: column names, data types, number of rows, any obvious issues (NaN counts, mixed types, suspicious min/max values).
3. **Ask clarifying questions** about the schema:
   - "What does each column represent? Are there columns I should ignore?"
   - "What are the units for the numeric columns?"
   - "What generated this data? (experiment, simulation, measurement, survey)"
   - "Are there multiple experimental conditions, configurations, or runs? Which columns encode them?"
   - "Is there any filtering needed? (e.g., exclude warm-up, specific configs only)"

### Step 4: Flag data quality issues

Report anything that could affect downstream analysis:

- **Missing data:** Which columns have NaNs? What fraction? Is missingness random or systematic?
- **Scale issues:** Are there columns spanning many orders of magnitude (suggesting log scale later)?
- **Duplicates or near-duplicates:** Repeated rows that might indicate measurement artifacts.
- **Type mismatches:** Numeric columns stored as strings, timestamps as integers, etc.
- **Suspicious values:** Min/max outliers, negative values in columns that should be positive, etc.

### Step 5: Save data_summary.md

Save a structured summary of the data for use in later modes:

```markdown
# Data Summary

## Source
- **Path:** [path to data file(s)]
- **Format:** [CSV / Parquet / JSON / etc.]
- **Generated by:** [experiment / simulation / measurement / etc.]

## Schema
| Column | Type | Unit | Description | Issues |
|--------|------|------|-------------|--------|
| [name] | [dtype] | [unit] | [what it represents] | [NaN count, suspicious values, etc.] |

## Shape
- **Rows:** [count]
- **Columns:** [count]
- **Experimental conditions:** [list of conditions/configs and how they are encoded]

## Quality Notes
- [Any issues flagged in Step 3]
- [Filtering applied or recommended]
```

Tell the student: "Your data summary is saved at [path]. Run `/viz explore` to start looking at this data visually."

**Output of ingest mode:** A `data_summary.md` file containing the structural understanding of the data.

---

## Mode 1: Explore — "Let the data do the talking"

**Purpose:** Build intuition about the data through quick, disposable visualizations before forming any hypotheses or committing to a plot type. This is Tukey's core principle: *look at the data from multiple angles and let it tell you what's interesting.* The plots generated here are throwaway — speed and coverage matter, not aesthetics.

**This mode generates code and plots, but they are explicitly disposable.** Do not apply publication formatting. Use seaborn defaults for speed. The goal is to *see*, not to *present*.

**CRITICAL: Explore-mode code must NOT be carried into production figures.** The most common source of style violations in paper figures is copying exploration code (which uses `sns.set_theme()` and seaborn defaults) into the final plotting script. `sns.set_theme()` overrides all matplotlib rcParams — it resets fonts to sans-serif, changes gridline colors, and overrides spine settings. Explore-mode code is disposable by design. When you move to Execute mode, write the production script from scratch using the lab's rcParams setup, not by modifying explore-mode code.

**Seaborn is the primary tool for this mode.** It provides high-level functions that generate informative plots with minimal code — exactly what you need for fast exploration. The [seaborn tutorial](https://seaborn.pydata.org/tutorial.html) is an excellent reference for understanding what each function does and when to use it.

**First:** Look for a `data_summary.md` in the working directory. If one exists, read it to understand the schema. If not, do a quick schema read (as in Ingest Step 3) before proceeding.

### Step 1: Univariate overview — "What does each variable look like?"

For each numeric column (or the most important ones if there are many), generate quick views of the distribution. **Show the student the code** — learning these one-liners is part of the skill:

```python
import seaborn as sns; sns.set_theme()
import pandas as pd

df = pd.read_csv("data.csv")

# Histogram with KDE overlay — most intuitive first look
sns.histplot(df, x="column_name", kde=True)

# ECDF — zero tuning parameters, shows every data point directly
sns.displot(df, x="column_name", kind="ecdf")

# KDE — smooth density, easy to compare groups
sns.kdeplot(df, x="column_name", hue="group_column")

# Compare distributions across groups — faceted histograms
sns.displot(df, x="column_name", col="group_column", kde=True)
```

**Which distribution plot to use:**

| Function | Best for | Watch out for |
|----------|----------|---------------|
| `histplot` | First look, seeing actual counts | Sensitive to bin size — try different values |
| `kdeplot` | Smooth comparison across groups | Misleading on discrete data; assumes continuous unbounded |
| `ecdfplot` | Safest "just show me the data" option | Less intuitive shape; bimodality shows as slope changes |

Also check:
- **Summary statistics** — Mean, median, std, min, max, and the ratio of mean to median (a quick skewness indicator).
- **Log-scale check** — If the data spans more than 2 orders of magnitude, also plot on log scale. Does structure appear that was hidden on linear scale?
- For categorical columns: `sns.countplot(df, x="category_column")` for frequency counts.

### Step 2: Bivariate relationships — "How do variables relate?"

Generate quick views of how variables relate to each other:

```python
# The single most powerful EDA one-liner — all pairwise relationships
sns.pairplot(df, hue="group_column")

# Scatter plot with grouping
sns.scatterplot(df, x="col_x", y="col_y", hue="group_column")

# Joint plot — scatter with marginal distributions
sns.jointplot(df, x="col_x", y="col_y", hue="group_column")

# Scatter with regression line and confidence interval
sns.lmplot(df, x="col_x", y="col_y", hue="group_column")

# Correlation heatmap — for many numeric columns
sns.heatmap(df.select_dtypes("number").corr(), annot=True)

# Group comparisons — box plots split by category
sns.boxplot(df, x="group_column", y="value_column")

# See every point — swarm plot (small datasets only)
sns.swarmplot(df, x="group_column", y="value_column")

# Full distribution shape per group
sns.violinplot(df, x="group_column", y="value_column")
```

**Choosing the right categorical comparison:**

| Function | Best for | Avoid when |
|----------|----------|------------|
| `boxplot` | Quick summary — median, quartiles, outliers | You need to see the full distribution shape |
| `violinplot` | Seeing the full distribution shape | Very small N per group (shape is meaningless) |
| `swarmplot`/`stripplot` | Seeing every individual data point | Large N (too many points overlap) |
| `barplot` | Comparing means across categories | **CAUTION: hides distribution — prefer box/violin** |

### Step 3: Temporal or sequential structure

If the data has a time or sequence dimension:

```python
# Line plot — auto-aggregates repeated observations with CI band
sns.relplot(df, x="time_column", y="value_column", kind="line")

# Multiple series with grouping
sns.relplot(df, x="time_column", y="value_column", kind="line", hue="group_column")

# Faceted by condition
sns.relplot(df, x="time_column", y="value_column", kind="line",
            hue="group_column", col="condition_column")
```

Also check:
1. **Stationarity** — Does the distribution change across the time range? (Plot rolling mean/std.)
2. **Different time scales** — Zoom in and zoom out. Patterns visible at one granularity may vanish at another.
3. **Noisy data** — Try smoothed line (rolling median) with raw data in the background.

### Step 4: Ask the student what they notice

After generating the exploratory plots, ask:

> Look at these plots. Before I say anything:
> 1. **What jumps out at you?** What patterns do you see?
> 2. **What surprises you?** Is anything different from what you expected?
> 3. **What's missing?** Is there a view of the data you want to see that we haven't generated?
> 4. **Does the data look right?** Are there artifacts, outliers, or issues that suggest a problem with the experiment itself?

**Critical:** If the student's answers to question 4 suggest the data is flawed — wrong variables measured, insufficient coverage, confounds, measurement artifacts — flag this explicitly:

> "Based on what we're seeing, it might be worth revisiting the experiment before making figures. Specifically: [describe the issue]. Would you like to discuss what additional data you'd need, or do you want to proceed with what you have?"

Going back to collect better data is a valid and valuable outcome of exploration. It is better to discover this now than after producing a polished figure from flawed data.

### Step 5: Save exploration_log.md

Save a record of what was observed:

```markdown
# Exploration Log

## Data
- **Source:** [path, or reference to data_summary.md]
- **Date explored:** [date]

## Key Observations
- [What patterns were visible in the univariate distributions]
- [Notable bivariate relationships or group differences]
- [Temporal structure, if applicable]

## Surprises
- [Anything unexpected — this is the most valuable section]

## Data Quality Concerns
- [Any issues discovered during exploration]
- [Whether the data is sufficient or the experiment needs revisiting]

## Questions Raised
- [New questions that emerged from looking at the data]
- [Specific views the student wants to investigate further]
```

Tell the student: "Your exploration log is saved at [path]. When you're ready to articulate what you want to show, run `/viz brainstorm`. Or if you already know, you can write your own `braindump.md` and go straight to `/viz plan`."

**Output of explore mode:** An `exploration_log.md` and a set of disposable plots. The log captures observations and surprises that feed forward into brainstorming.

---

## Mode 2: Brainstorm — "What are you trying to see?"

**Purpose:** Help the student internalize the visualization goal before any code is written. This mode is interactive and Socratic — you ask questions, the student answers, and together you refine until the visualization intent is crystal clear.

**Do NOT write any code in this mode. Do NOT suggest plot types yet. The goal is purely intellectual clarity.**

**If the student has completed Explore mode**, the `exploration_log.md` will contain observations and surprises that can seed this conversation. Read it if available — the student's answers to the Tukey questions will be richer if grounded in what they actually saw in the data.

### Step 1: Open with the Tukey question

Ask the student:

> Before we talk about plots, I need to understand what you are looking at. Tell me:
> 1. **What is the data?** What is one observation? What is one batch/group? How many observations per group?
> 2. **What question are you trying to answer?** Not "what plot do you want to make" — what *question about the world* does this figure address?
> 3. **Are you exploring or confirming?** Are you still trying to understand what the data shows, or do you already know the claim and need a figure to support it?

Listen carefully to the answers. Most students will try to skip to "I want a CDF." Redirect them: "Before we decide on a CDF — what question would the CDF answer? What do you expect it to show?"

### Step 2: Prediction and surprise

Once you understand the data and question, ask:

> 4. **What do you expect to see?** Write down your prediction. "I expect X to increase with Y, because Z."
> 5. **What would surprise you?** Name one result that would make you say "wait, that's not right." This is the most important question — it tells you what to look for.
> 6. **If you removed the obvious pattern, what would be left?** If your system is 2x faster overall, what happens when you subtract that factor? Which conditions show 3x? Which show 1.1x?

### Step 3: Audience and argument

> 7. **Who is the audience for this figure?** Is this for your own exploration notebook, a Slack message to your advisor, a paper draft, or a presentation? The standards are different for each.
> 8. **If this is for a paper: what is the one sentence this figure supports?** Can you point to the exact claim in the text? If not, the figure may be premature.

### Step 4: Synthesize, confirm, and save braindump

Summarize what you have learned back to the student in 3–4 sentences:

> "So you have [data description], and you want to answer [question]. You expect to see [prediction], and it would surprise you if [surprise]. This figure's job is to [support claim / explore pattern / motivate problem]."

Ask: "Does that capture it? Anything missing or wrong?"

If the student confirms, save the synthesis as a `braindump.md` file in the working directory, then tell them they are ready for `/viz plan`. If there are gaps, ask follow-up questions until the intent is clear.

**Output of brainstorm mode:** A `braindump.md` file that captures the full brainstorm synthesis. This file serves as durable context that carries forward into plan and execute modes — the student (or a new conversation) can pick up from here without losing any of the thinking. Experienced students who know what they want can also write their own `braindump.md` directly and skip to `/viz plan`.

```markdown
# Visualization Braindump

## Data
- **What is the data?** [description of observations, batches/groups, scale]

## Question
- **Core question:** [the question about the world this figure addresses]
- **Exploring or confirming?** [exploration vs. supporting a known claim]

## Predictions
- **Expected pattern:** [what the student expects to see and why]
- **Surprise condition:** [what would be unexpected — the most important diagnostic]
- **Residual structure:** [what remains after removing the obvious pattern]

## Audience & Argument
- **Audience:** [exploration notebook / advisor update / paper figure / talk slide]
- **Paper claim (if applicable):** [the exact sentence this figure supports]

## Synthesis
[3–4 sentence summary of the visualization intent, written in plain language]
```

---

## Mode 3: Plan — "How should we realize it?"

**Purpose:** Translate the intellectual intent from brainstorm mode into concrete technical decisions: plot type, layout, data source, and visual encoding. This mode produces a `plot_context.md` file that contains everything needed for execution.

**First:** Look for prior artifacts in the working directory:
- **`braindump.md`** — If it exists, read it to load the brainstorm context (intent, predictions, audience).
- **`data_summary.md`** — If it exists, read it to load the data schema and quality notes.
- **`exploration_log.md`** — If it exists, read it to understand what the student has already observed.

If none of these exist and the student hasn't completed earlier modes, suggest they start with `/viz brainstorm` at minimum. If the student wants to skip ahead, proceed — experienced students may carry all this context in their head.

### Step 1: Confirm the data and variable mappings

If `data_summary.md` exists, reference it and ask the student to confirm the variable mappings for this specific figure:

> Based on your data summary, let's decide what goes where:
> - "Which column is the independent variable (x-axis)?"
> - "Which column is the dependent variable (y-axis)?"
> - "Which column(s) define the groups you want to compare?"
> - "Any additional filtering beyond what's already noted?"

If `data_summary.md` does not exist, locate and inspect the data directly: ask for the path, read a sample (first 20 rows + dtypes + shape), report the schema, and ask the clarifying questions above.

### Step 2: Recommend a plot type

Based on the brainstorm intent AND the data schema, recommend a plot type using this decision framework:

**What kind of relationship are you showing?**

| Question | Best plot types | When to choose |
|----------|----------------|----------------|
| How is Y distributed? | Histogram, KDE, ECDF/CDF, box plot, violin plot | Single variable, understanding shape/spread |
| How does Y differ across groups? | Box plot, violin plot, strip/swarm plot, grouped bar | Categorical x, continuous y |
| How does Y change with X? | Line plot, scatter plot | Continuous x, continuous y |
| How does Y change over time? | Line plot (with optional smoothing) | Time series |
| How do two distributions compare? | Overlaid CDF/CCDF, side-by-side box plots, KDE overlay | Comparing systems/configs |
| What is the tail behavior? | CCDF on log-log scale | Heavy-tailed distributions (flow sizes, RTTs) |
| How do multiple factors interact? | Heatmap, faceted small multiples, grouped box plots | Two+ categorical dimensions |

**Seaborn vs. Matplotlib guidance:**

- **Use seaborn when:** You need to compare distributions across groups (catplot, displot), show relationships with automatic grouping (relplot), or want quick exploratory faceted plots (FacetGrid). Seaborn excels at: violin plots (`violinplot`), swarm plots (`swarmplot`), pair plots (`pairplot`), heatmaps (`heatmap`), joint distributions (`jointplot`), and KDE overlays (`kdeplot`).
- **Use matplotlib when:** You need pixel-level control for camera-ready figures, custom CDF/CCDF functions, dual y-axes, or specific SIGCOMM/NSDI formatting. Matplotlib is better for: final paper figures with precise sizing, custom annotation placement, and reproducible style via rcParams.
- **Use both when:** Explore with seaborn first (fast iteration, automatic semantics), then port to matplotlib for the final paper figure (precise control, golden ratio, conference formatting). **Warning:** If you use seaborn in the final figure, do NOT call `sns.set_theme()` — it overrides all rcParams (fonts, gridlines, spines). Instead, import seaborn and use its plotting functions (e.g., `sns.heatmap()`) while relying on matplotlib rcParams for styling. See Execute mode for the correct setup.

Present your recommendation with reasoning:

> "Given that you want to compare RTT distributions across 5 congestion control algorithms, I recommend **side-by-side box plots** (seaborn `boxplot` or `violinplot` for exploration, matplotlib for the final paper figure). Box plots let you see the median, spread, and outliers for all 5 algorithms at a glance — which directly answers your question of 'which algorithm has the most consistent performance.' A CDF overlay would work too, but with 5 lines it gets hard to compare. If you want both, we can do box plots as the main figure and a CDF in the appendix."

Ask: "Does this match what you had in mind? Want to explore a different plot type?"

### Step 3: Layout and sizing decisions

Ask or determine:

> - **Single column or double column?** (3.5" vs 7.0" width for SIGCOMM/NSDI)
> - **Aspect ratio:** Golden ratio (default), wider for time series (fraction=0.5), squarer for CDFs (fraction=1.2)?
> - **How many subplots?** Single figure, or a grid of related panels?
> - **Color scheme:** Colorblind-safe palette (Set1_9 default)? Need grayscale distinguishability?
> - **Legend placement:** Inside plot, outside right, above?

### Step 4: Generate plot_context.md

Synthesize all decisions into a `plot_context.md` file saved alongside the student's data or in their working directory. This file is the contract between planning and execution.

```markdown
# Plot Context

## Intent
- **Question:** [the question this figure answers]
- **Claim:** [the paper sentence it supports, or "exploration" if exploratory]
- **Prediction:** [what the student expects to see]
- **Surprise condition:** [what would be unexpected]

## Data
- **Source:** [path to data file(s)]
- **Schema:** [key columns, types, units]
- **Rows:** [count]
- **Filtering:** [any exclusions applied]
- **X variable:** [column name] — [description with units]
- **Y variable:** [column name] — [description with units]
- **Group variable(s):** [column name(s)] — [what each group represents]

## Plot Design
- **Plot type:** [e.g., side-by-side box plot]
- **Library:** [matplotlib / seaborn / both]
- **Sizing:** [single/double column, aspect ratio]
- **Dimensions:** [width x height in inches]
- **Color palette:** [e.g., Set1_9 colorblind-safe]
- **Markers/lines:** [if applicable]
- **Legend:** [placement]
- **Axis scales:** [linear/log for each axis, with justification]
- **Grid:** [on/off, style]
- **Font:** [serif/sans-serif, sizes]

## Annotations
- [Any specific annotations, reference lines, or highlights planned]

## Output
- **Format:** [PDF/PNG/SVG]
- **DPI:** [300 for paper, 150 for exploration]
- **Filename:** [target filename]
- **Save path:** [directory]
```

Save this file and tell the student: "Your plot context is saved at [path]. Review it — once you're happy, run `/viz execute` to generate the figure."

**Output of plan mode:** A `plot_context.md` file containing every decision needed for execution.

---

## Mode 4: Execute — "Generate and run the code"

**Purpose:** Generate the plotting code based on `plot_context.md` and execute it. This mode is purely operational — code generation, debugging, and producing the figure. All reflection and analysis happen in the next mode.

### Step 1: Locate the plot context

Ask the student for the path to their `plot_context.md`, or look for one in the current directory. Read it. If it does not exist, tell the student to run `/viz plan` first.

### Step 2: Generate the code

Write a self-contained Python script that:

1. **Imports and setup** — Use the lab's standard configuration. **CRITICAL: Do NOT call `sns.set_theme()` in production code.** `sns.set_theme()` overrides all rcParams — it resets fonts to sans-serif, changes gridline colors to seaborn's pink/salmon tint, and overrides spine settings. This is the #1 source of style violations in paper figures. If you need seaborn plotting functions (e.g., `sns.heatmap`, `sns.kdeplot`), import seaborn but configure it through matplotlib's rcParams, which seaborn respects when `set_theme()` is not called.

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import seaborn as sns  # DO NOT call sns.set_theme() — it overrides rcParams
from palettable.colorbrewer.qualitative import Set1_9, Paired_12
from cycler import cycler

# Lab-standard defaults (SIGCOMM/NSDI quality)
# These MUST be set AFTER imports and WITHOUT calling sns.set_theme()
plt.rcParams.update({
    'figure.figsize': (3.5, 2.6),       # Adjust per plot_context.md
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'],
    'font.size': 9,
    'axes.labelsize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'axes.linewidth': 0.5,
    'lines.linewidth': 1.0,
    'lines.markersize': 3,
    'figure.constrained_layout.use': True,
    'axes.spines.top': False,            # Remove top spine
    'axes.spines.right': False,          # Remove right spine
    'axes.grid': True,                   # Enable grid
    'grid.linestyle': ':',               # Dotted gridlines
    'grid.linewidth': 0.5,
    'grid.alpha': 0.5,
    'grid.color': '#cccccc',             # Light gray, NOT seaborn's pink
    'axes.prop_cycle': cycler(color=Set1_9.mpl_colors),
})
```

**Why `rcParams.update()` instead of individual assignments:** A single `update()` call is atomic — it applies all settings at once, reducing the chance of partial application if an error occurs partway through. It also makes the configuration block easy to copy as a unit.

**If you must use seaborn's theming** (e.g., for heatmaps where seaborn controls the colorbar), configure it explicitly without calling the bare `set_theme()`:
```python
# ONLY if you need seaborn theme functions — set AFTER rcParams
sns.set_theme(style="ticks", font="serif", rc={
    'font.family': 'serif',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'grid.color': '#cccccc',
    'grid.alpha': 0.5,
    'grid.linestyle': ':',
})
```
This passes lab-standard overrides through seaborn's own API, preventing the defaults from stomping your configuration.

2. **Load and filter data** — Read from the path in plot_context.md, apply any filtering.

3. **Create the figure** — Using the plot type, sizing, and parameters from plot_context.md. Apply:
   - Golden ratio sizing via `golden_ratio_figsize()` helper
   - SIGCOMM style: no top/right spines, subtle grid, outward ticks
   - Proper axis labels with units
   - Colorblind-safe markers AND line styles for grayscale distinguishability
   - Legend placement per plan

4. **Save the figure** — To the path specified in plot_context.md, in the requested format.

5. **Also display it** — So the student can see it immediately.

### Step 3: Run the code

Execute the script. If it fails, diagnose and fix. If the data path is wrong or the schema doesn't match, tell the student what went wrong and how to fix it.

Once the figure is generated, tell the student: "Your figure is saved at [path]. Run `/viz analyze` to reflect on what it shows and validate it against your hypothesis."

**Output of execute mode:** A saved figure and the Python script that generated it.

---

## Mode 5: Analyze — "What is this figure really telling you?"

**Purpose:** Close the loop between intent and outcome. This mode has two phases: first the student articulates what they see (so the skill doesn't anchor their thinking), then the skill provides substantive feedback by cross-referencing the figure against all accumulated context — the predictions from brainstorm, the design rationale from plan, and the first principles (Tukey, Tufte, WALTER) encoded throughout the skill.

This is the mode that turns a plotting exercise into a learning experience. Without it, students produce figures and move on. With it, they are forced to confront whether the figure actually says what they think it says.

**First:** Load all prior artifacts:
- **`braindump.md`** — The student's predictions, surprise conditions, and intended claim.
- **`plot_context.md`** — The design rationale, variable mappings, and intended question.
- **`exploration_log.md`** — What the student observed during exploration (if available).
- **The generated figure** — Read the image to analyze what it actually shows.

### Step 1: Student interpretation first

**Do not offer any analysis yet.** Ask the student to look at the figure and share their reading of it:

> The figure is generated. Before I share my analysis, I want to hear yours. Look at the plot and tell me:
> 1. **What do you see?** Describe the main pattern in your own words.
> 2. **Does it match what you predicted?** Go back to your prediction — were you right?
> 3. **What surprises you?** Is there anything you didn't expect?
> 4. **What is the one-sentence takeaway?** If you had to caption this figure right now, what would you write?

Listen carefully. The student's answers reveal how well they understand what the figure shows — and where the gaps are.

### Step 2: WALTER narration

Now walk through the structured WALTER narration together. Draft answers based on the accumulated context and ask the student to confirm or correct:

> Let's WALTER this figure to make sure we have a complete understanding:
>
> **W — What is the hypothesis?**
> [Draft from braindump.md — the question and prediction the student articulated]
>
> **A — Axes: what do x and y represent?**
> [State from plot_context.md — column names, units, and what they measure]
>
> **L — Look here: where should the viewer focus?**
> [Suggest based on what the plot actually shows — the region that carries the most information]
>
> **T — Trend: what is the dominant pattern?**
> [Describe what the figure shows — incorporate the student's answer from Step 1]
>
> **E — Exception: what breaks the pattern, and why?**
> [Flag anything that deviates from the trend — outliers, crossover points, unexpected groups]
>
> **R — Result: what is the takeaway? Does it connect back to W?**
> [Close the loop — does the result answer the original hypothesis?]

### Step 3: First-principles feedback

Now provide substantive analysis by applying the principles encoded in this skill. This is where the skill adds value beyond what the student can do alone — it systematically checks the figure against multiple lenses:

**Tukey lens — Exploration and surprise:**
- **Prediction vs. reality.** Compare what the student predicted in `braindump.md` against what the figure actually shows. If the prediction was correct, acknowledge it but ask: "Is there anything *beyond* the expected pattern worth noting?" If the prediction was wrong, flag it explicitly: "You predicted [X], but the figure shows [Y]. This discrepancy is worth investigating — it may be more interesting than the original hypothesis."
- **Residual thinking.** "If you removed the dominant pattern from this figure, what would be left? Are there subgroups where the effect is much stronger or weaker than average? The overall trend may be masking important variation."
- **Re-expression.** Would the same data on a different scale (log, sqrt, reciprocal) reveal structure that is hidden here? If the data spans orders of magnitude, suggest trying log scale. If it's a proportion, suggest logit.

**Tufte lens — Compliance with visualization principles:**

Audit the generated figure against Tufte's principles and report specific findings:

- **Data-ink ratio.** Examine the figure for non-data ink. Are there decorative elements (background fills, 3D effects, heavy borders, ornamental gridlines) that could be removed without losing information? Every mark should encode data. If the figure has a low data-ink ratio, identify what should be removed.
- **Chartjunk check.** Flag specific violations: unnecessary legends (if there's only one series), redundant axis labels, overly prominent gridlines, drop shadows, gradient fills, or any element that distracts from the data itself.
- **Scale integrity.** Does the axis scale faithfully show the data? Is the baseline appropriate (does it start at zero for bar charts)? Would a truncated axis exaggerate small differences? Does the lie factor — the ratio of visual effect size to data effect size — stay close to 1.0? Would log scale reveal patterns hidden on linear scale?
- **Over-summarization.** If the plot shows means or medians: "Are you summarizing away the story? The distribution might be bimodal, or the variance across groups might be the most interesting finding. Consider showing the full distribution (box plot, violin, or CDF) instead of just the central tendency." A bar chart of means is almost always the wrong choice — flag it explicitly.
- **Small multiples.** If the figure crams too many series into one panel (multiple hues, sizes, and styles that become hard to read), recommend faceted small multiples instead. Several simple, consistent panels that the eye can compare at a glance are almost always more effective than one complex, overloaded plot.
- **Alternative representations.** "Would a different plot type reveal something this one hides?" Suggest at least one concrete alternative and explain what it would show differently. If the student used a bar chart, suggest a box plot. If they used overlaid CDFs with many lines, suggest faceted panels. If they used a scatter plot with thousands of points, suggest a 2D KDE or hexbin.
- **Typography and labeling.** Are axis labels present with units? Are font sizes readable at the intended print size? Is the legend necessary, and if so, is it placed where it doesn't occlude data? Are tick labels uncluttered (no overlapping, no unnecessary decimal places)?

**Hypothesis validation:**
- Cross-reference the figure against the specific claim from `braindump.md` (the "paper sentence" the figure is supposed to support). Does the figure actually support it? Be honest: "The claim says [X], but the figure shows [Y]. You may need to revise the claim, or produce a different figure that directly tests it."
- If the figure supports the claim, stress-test it: "A skeptical reviewer would focus on [aspect]. Can you defend it? Is there a confound that could explain the pattern?"

**Completeness check:**
- Are there conditions, groups, or variables from `data_summary.md` that are *not* shown in this figure but could change the interpretation?
- Would a companion figure (e.g., same data, different plot type; same plot type, different grouping) strengthen or undermine the current figure's message?

### Step 4: Suggest next steps

Based on the analysis, recommend one of:

> **a) The figure validates the hypothesis.** "The result connects back to the prediction. This figure is ready for the paper. Here's a draft caption: [interpretive caption that states the takeaway, not just the axes]."
>
> **b) The figure tells a different story.** "The data doesn't match the prediction — but the actual pattern is [describe]. This might be more interesting than the original hypothesis. Consider revising the claim to match what the data actually shows."
>
> **c) The figure is inconclusive.** "The pattern is ambiguous — it could support the claim or not, depending on [factor]. You may need additional data, a different grouping, or a follow-up figure to resolve this."
>
> **d) The representation needs revision.** "The figure makes a point, but the current plot type / scale / grouping doesn't show it as clearly as it could. Consider [specific change] and re-run `/viz execute`."
>
> **e) Go back to exploration.** "What we're seeing suggests a different question than the one you started with. Consider going back to `/viz explore` to investigate [specific observation] before committing to a paper figure."

### Step 5: Save the analysis

Append the full analysis to `plot_context.md` under new sections:

```markdown
## WALTER Narration
- **W (Hypothesis):** [...]
- **A (Axes):** [...]
- **L (Look here):** [...]
- **T (Trend):** [...]
- **E (Exception):** [...]
- **R (Result):** [...]

## First-Principles Feedback
- **Prediction vs. reality:** [match/mismatch and implications]
- **Residual analysis:** [what remains after removing the dominant pattern]
- **Representation honesty:** [scale, over-summarization, alternative plot types]
- **Hypothesis validation:** [does the figure support the claim? reviewer stress-test]

## Next Steps
- [Recommended action: finalize / revise claim / iterate on figure / go back to explore]

## Post-Analysis Notes
- [Any additional observations, surprises, or follow-up questions]
- [Iteration history if multiple versions were generated]
```

This creates a complete record: intent → plan → execution → analysis → next steps.

---

## Quick Reference: Plot Type Decision Tree

Use this during Plan mode to recommend plot types:

```
What are you showing?
│
├── Distribution of one variable
│   ├── Quick exploration → histogram (sns.histplot) or KDE (sns.kdeplot)
│   ├── Formal comparison → CDF/ECDF (sns.ecdfplot or custom matplotlib)
│   ├── Heavy tail behavior → CCDF on log-log (custom matplotlib)
│   └── Show individual points → rug plot or strip plot (sns.stripplot)
│
├── Comparing distributions across groups
│   ├── Few groups (2-5) → overlaid CDFs or KDE
│   ├── Many groups (5-20) → side-by-side box plots (sns.boxplot)
│   ├── Need distribution shape → violin plots (sns.violinplot)
│   ├── Small N per group → swarm/strip plot (sns.swarmplot)
│   └── Summary only → grouped bar with CI (sns.barplot) [CAUTION: hides distribution]
│
├── Relationship between two continuous variables
│   ├── General relationship → scatter plot (sns.scatterplot)
│   ├── With regression → lmplot (sns.lmplot)
│   ├── Dense data → 2D KDE or hexbin (sns.kdeplot with fill=True)
│   └── Time-ordered → line plot (matplotlib plt.plot or sns.lineplot)
│
├── Change over time
│   ├── Single series → line plot
│   ├── Multiple series → line plot with hue (sns.lineplot)
│   ├── With uncertainty → line plot with CI band (sns.lineplot default)
│   ├── Noisy data → smoothed line (rolling median) + raw data background
│   └── Multiple panels → faceted line plots (sns.relplot with col=)
│
├── Two categorical dimensions + continuous value
│   ├── Dense grid → heatmap (sns.heatmap)
│   ├── Row/column effects → heatmap of residuals (Tukey two-way decomposition)
│   └── Sparse → grouped bar or point plot (sns.pointplot)
│
└── Multi-variable overview
    ├── All pairwise → pair plot (sns.pairplot)
    ├── Two variables + marginals → joint plot (sns.jointplot)
    └── Faceted by condition → FacetGrid or relplot with col/row
```

---

## Lab Standards Reference

These are non-negotiable for any paper figure produced by this skill:

- **Font:** Serif (Times New Roman), size 9pt body, 8pt ticks/legend
- **Sizing:** Golden ratio default; 3.5" single column, 7.0" double column
- **Colors:** Set1_9 from palettable (colorblind-safe); also use distinct markers + line styles for grayscale
- **Spines:** Remove top and right; left and bottom at 0.5pt
- **Grid:** Dotted, 0.5pt, light gray, alpha 0.5
- **DPI:** 300 for paper, 150 for exploration
- **Format:** PDF for paper figures (vector), PNG for Slack/exploration
- **Axis labels:** Always include units; use LaTeX math mode for symbols
- **Legend:** Inside plot when space allows; outside right otherwise; multi-column above for many entries
- **Booktabs:** Tables use \toprule/\midrule/\bottomrule only
- **Captions:** Interpretive, not descriptive. State the takeaway, not just the axes.
- **Seaborn hazard:** NEVER call `sns.set_theme()` in production code. It overrides all rcParams (fonts → sans-serif, grid → pink/salmon, spines → all visible). This is the single most common source of style violations. Import seaborn for its plotting functions; control styling through matplotlib rcParams only.
