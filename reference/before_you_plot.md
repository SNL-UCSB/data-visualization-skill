# Before You Plot: A Questionnaire

*Adapted from John W. Tukey's Exploratory Data Analysis (1977) and the WALTER principle (a common practice in systems and networking research) for research visualization. Answer these questions before you write any plotting code — and after you finish.*

---

## Part 1: What Are You Looking At?

These questions force you to confront what you actually have before deciding how to show it.

**1. What is one batch, and what is one observation?**

Write it down. "I have 500 RTT measurements per flow, across 12 flows, under 3 congestion control algorithms." Until you can state the unit of observation and how observations are grouped, you do not understand your data well enough to plot it.

**2. How many observations do you have, and is that enough to see what you want to see?**

A CDF with 15 data points is lying to you. A box plot with 3 observations per group is meaningless. State the count per group and ask yourself: if the pattern I expect is real, would I be able to see it with this many observations? If the answer is "maybe not," you have an experimental design problem, not a visualization problem.

**3. Have you looked at the raw numbers?**

Not a plot — the actual numbers. Tukey's stem-and-leaf display was built on the principle that you should *see the data* before you summarize it. Open a terminal, print the first 50 values, sort them, look at the min and max. Can you spot anything already? Are there impossible values (negative RTTs, throughputs exceeding link capacity, timestamps from 1970)? This step catches data bugs that no plot will reveal because plots smooth over individual values.

**4. What did the data look like *before* you cleaned it?**

If you removed outliers, filtered incomplete runs, or excluded warm-up periods — what did the unfiltered data look like? Can you justify every exclusion with a sentence? If you cannot, you may be hiding something important rather than removing noise.

---

## Part 2: What Question Are You Asking?

Tukey's foundational distinction: are you *exploring* or *confirming*? Most students skip exploration entirely and go straight to making "paper figures" that confirm what they already believe. This section forces you to separate the two.

**5. Are you exploring or confirming?**

Be honest. If you already know the claim this figure is supposed to support ("our system achieves 2x higher throughput"), you are confirming. That is fine for the paper — but it means you have already done the exploration phase (or you skipped it, which is the problem). If you are still trying to understand *what* the data shows, you are exploring, and the rules are different: ugly plots are fine, disposable notebooks are fine, and your goal is surprise, not polish.

**6. What do you expect to see — and why?**

Write down your prediction before you plot. "I expect throughput to increase roughly linearly with the number of cores, plateauing around 8 cores due to lock contention." This is the single most important habit in data analysis. If the plot matches your expectation, you have confirmed something (good, but not exciting). If it *doesn't* match, you have found something — and that is where the real work begins. Tukey: *"The greatest value of a picture is when it forces us to notice what we never expected to see."*

**7. What would *surprise* you?**

Name it. "It would surprise me if Algorithm B beats Algorithm A in any workload, because Algorithm A was designed specifically for this case." "It would surprise me if the variance doesn't decrease with more samples." Writing down what would surprise you makes you actually *look for it* in the plot. Most students glance at a figure, see what they expected, and move on — missing the anomaly in the third quartile or the one workload where the baseline wins.

**8. If you removed the expected pattern, what would be left?**

This is Tukey's residual principle: *"Regard every description (always incomplete!) as something to be lifted off and looked under."* If your system is 2x faster on average, subtract that factor and look at what remains. Which workloads show 3x? Which show 1.1x? The residuals — the deviations from the overall pattern — are often more interesting than the pattern itself. You do not have to literally compute residuals for every plot. But you should be able to answer: what is the dominant pattern, and what might be hiding underneath it?

---

## Part 3: Is Your Representation Honest?

These questions address whether your choice of plot type, axis scale, and summary statistic faithfully represents the data rather than flattering your system.

**9. Is the shape of your distribution hiding in your axis scale?**

If you are plotting a heavy-tailed distribution (flow sizes, RTTs, inter-arrival times) on a linear scale, you are compressing 95% of the interesting structure into a tiny sliver on the right. Tukey's re-expression principle: try log scale, try square root, try reciprocal. Which transformation makes the pattern *most visible*? This is not about aesthetics — it is about whether a reader can see the structure you are trying to communicate. If you cannot articulate why you chose linear vs. log, you have not thought about it enough.

**10. Are you summarizing away the story?**

A bar chart of means is the most information-destroying visualization in systems research. It tells you nothing about variance, nothing about the shape of the distribution, nothing about outliers. Before you use a mean (or median), ask: does the spread matter for my claim? Almost always the answer is yes. Show the distribution, not just a point estimate. Use box plots, violin plots, or strip plots. Overlay individual data points when you have fewer than a few hundred. Tukey's philosophy: the reader should be able to see the *data*, not just your summary of it.

**11. If you showed this plot to someone with no context, what would they conclude?**

This is the intellectual honesty test. Cover the caption, cover the title. What message does the figure *force* upon you? If the honest answer is "Algorithm A and Algorithm B look about the same," but your caption says "Algorithm A significantly outperforms Algorithm B," you have a problem — either with the visualization or with the claim. Tukey: *"Demand impact from our pictures."* If the picture doesn't deliver impact by itself, the picture is wrong or the result is weaker than you think.

**12. Would a different plot type reveal something this one hides?**

The same data plotted as a CDF, a box plot, a time series, and a scatter plot will tell you four different things. The CDF shows the full distribution but hides temporal patterns. The box plot enables comparison across conditions but hides within-group structure. The time series shows trends but hides the distribution. During exploration, you should make at least two different plots of the same data. If they tell the same story, good — you understand your result. If they contradict each other, you have found something important.

---

## Part 4: What Is This Figure's Job in the Paper?

These questions bridge from exploration to presentation. Once you understand your data, you need to decide what role this figure plays in your argument.

**13. What is the one sentence this figure supports?**

Not a paragraph — one sentence. Every figure in a paper exists to support a specific claim in the text. If you cannot write that sentence, the figure is orphaned. If the sentence requires the reader to squint at the figure and take your word for it, the figure is not doing its job.

**14. Is this figure *necessary*, or just *nice to have*?**

Conference papers have strict page limits. Every figure costs roughly a quarter of a page (single column) or half a page (full width). Ask: if I removed this figure, would the paper's argument collapse? If the answer is no, consider whether the space is better spent on a different figure, a table, or more text. The bar for inclusion is "this figure is *essential* to the argument," not "this figure exists and I spent time making it."

**15. What would the skeptical reviewer focus on?**

Look at your figure and imagine the most adversarial reader. What would they challenge? "Why did you only show the median?" "Why does the x-axis start at 50 instead of 0?" "Why are there only 4 data points for this condition?" Anticipating these questions is how you decide whether to add error bars, adjust axis limits, include a secondary plot, or preemptively address the limitation in the caption.

---

## Part 5: WALTER It — Narrate the Visual Story

Parts 1–4 are about *making* the figure. This part is about *presenting* it — to your advisor, on Slack, in a meeting, or in a paper caption. Every time you share a figure, accompany it with a WALTER narration. The acronym stands for:

**W — What is the hypothesis?**

Why does this figure exist? What question motivated it? This is the "why are we looking at this" that grounds everything. If you cannot state the hypothesis in one sentence, you are sharing a figure without a purpose. The hypothesis connects back to questions 6 and 13 above — what you expected and what claim the figure supports. State it first, before anyone looks at the plot.

**A — Axes: what do x and y represent?**

Say it explicitly. "The x-axis is the number of concurrent flows, ranging from 1 to 128. The y-axis is median completion time in milliseconds." This sounds obvious, but students routinely share plots on Slack where the axis labels are truncated, use internal variable names (`feat_idx_3`), or lack units entirely. If you cannot narrate the axes in plain language, the figure is not ready to share.

**L — Look here: where should the viewer focus?**

Direct attention. "Look at the crossover point near 32 flows." "Focus on the gap between the red and blue lines in the right half of the plot." A figure without guidance forces the viewer to wander — and different viewers will focus on different things, drawing different (possibly wrong) conclusions. You made this figure because you saw something in it. Tell the viewer where to look.

**T — Trend: what is the dominant pattern?**

State the main story. "Throughput scales linearly up to 16 cores, then plateaus." "Our system consistently outperforms the baseline across all RTT buckets." The trend is what the figure would say if it could talk. If you cannot state the trend in one sentence, either the figure is showing too many things at once, or you have not yet understood what it shows.

**E — Exception: what breaks the pattern, and why?**

This is where the real insight lives. "The exception is the 200ms RTT bucket, where the baseline actually wins by 5%. We believe this is because our prefetch heuristic becomes counterproductive at very high latencies." Exceptions are not embarrassments to hide — they are the most informative part of any figure. A result with no exceptions is either too simple to be interesting or too aggregated to be honest. Tukey's entire philosophy is that the exceptions, the residuals, the things that break the pattern are where discovery happens.

**R — Result: what is the takeaway?**

Close the loop back to **W**. "The result is that our hypothesis holds — linear scaling up to the memory bandwidth limit — with one exception at high latencies that we need to investigate." The takeaway must connect the observed pattern (T + E) back to the original question (W). If the result doesn't answer the hypothesis, either the hypothesis was wrong (interesting!) or the figure doesn't actually test what you thought it tested (go back to Part 2).

### Why WALTER matters

The WALTER narration is not just a presentation trick. It is a *comprehension test*. If you cannot write a WALTER paragraph for your figure, you do not yet understand what the figure shows. The act of writing it will expose gaps in your understanding — you will discover that you cannot state the trend clearly, or that you have not noticed the exception, or that the result does not actually connect back to the hypothesis. These are exactly the gaps that your advisor or a reviewer will find. Better to find them yourself.

**When you share a figure on Slack, in a meeting, or in a draft, always WALTER it.** The WALTER text controls where the viewer focuses attention and ensures that the figure's message is received as intended, not left to interpretation.

---

## How to Use This Questionnaire

**During exploration (before you have paper figures):** Answer questions 1–8. Do this in a Jupyter notebook or a scratch script. Keep the notebook — it is your exploration log. Many of these plots will never appear in the paper, and that is correct.

**During figure design (when you are making paper figures):** Answer questions 9–15. Do this *after* you have explored and *before* you start polishing. If you find yourself unable to answer question 13, you are making the figure too early — go back to exploration.

**When presenting any figure (Slack, meetings, drafts):** WALTER it (Part 5). Write the W-A-L-T-E-R paragraph before you hit send. If you cannot complete it, the figure is not ready to share.

**During revision (advisor or reviewer feedback):** Re-answer questions 11, 15, and the WALTER narration. Your understanding of the data has deepened since you first made the figure. Does the narration still hold up? Has the exception changed? Does the result still connect to the hypothesis?

The goal is not to fill out this questionnaire like a checklist. The goal is to internalize these questions — and the WALTER habit — until you ask them automatically. Parts 1–4 teach you to *think* before you plot. Part 5 teaches you to *verify your own understanding* after you plot. Together, they form a closed loop: hypothesis → exploration → design → narration → verification. Once this loop is instinctive, the plotting itself — the matplotlib code, the axis formatting, the color choices — is the easy part. The hard part was always figuring out what to show and why, and then confirming that you actually showed it.

---

*"It is important to understand what you CAN DO before you learn to measure how WELL you seem to have DONE it." — John W. Tukey, 1977*

*"Always WALTER it to control where you'd like the viewer focus attention."*
