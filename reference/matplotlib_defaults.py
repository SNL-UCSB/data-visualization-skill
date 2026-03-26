"""
Publication-quality Matplotlib defaults for systems/networking research papers.

Usage:
    import matplotlib_defaults  # auto-configures rcParams
    # ... then use plt.plot(), plt.savefig(), etc. as normal

Or selectively:
    from matplotlib_defaults import golden_ratio_figsize, set_pub_style, plot_cdf, plot_ccdf

These defaults target single-column (3.5") and double-column (7.0") layouts
typical of SIGCOMM, NSDI, CoNEXT, IMC, and similar venues.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

try:
    from palettable.colorbrewer.qualitative import Set1_9, Paired_12
    from cycler import cycler
    COLORS = Set1_9.mpl_colors
except ImportError:
    # Fallback colorblind-safe palette if palettable not installed
    COLORS = [
        '#e41a1c', '#377eb8', '#4daf4a', '#984ea3',
        '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#999999'
    ]
    from cycler import cycler

# --- Global rcParams ---
plt.rcParams['figure.figsize'] = (3.5, 2.6)       # single column default
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['font.size'] = 9
plt.rcParams['axes.labelsize'] = 9
plt.rcParams['axes.titlesize'] = 9
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['figure.titlesize'] = 10
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['axes.linewidth'] = 0.5
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams['lines.linewidth'] = 1.0
plt.rcParams['lines.markersize'] = 3
plt.rcParams['figure.constrained_layout.use'] = True
plt.rcParams['axes.prop_cycle'] = cycler(color=COLORS)

# Marker and line styles for grayscale distinguishability
MARKERS = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h']
LINE_STYLES = ['-', '--', '-.', ':']


def golden_ratio_figsize(width=3.5, fraction=1.0):
    """Return figure dimensions based on the golden ratio.

    Args:
        width: Figure width in inches (3.5 for single column, 7.0 for double)
        fraction: Multiplier for height. Use 0.5 for wide time series,
                  1.0 for standard plots, 1.2 for squarer CDFs.
    """
    golden_ratio = (1 + 5**0.5) / 2
    height = width / golden_ratio * fraction
    return (width, height)


def set_pub_style(ax=None):
    """Apply publication style to an axes: remove top/right spines, add subtle grid."""
    if ax is None:
        ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.tick_params(direction='out', length=3, width=0.5)
    ax.grid(True, linestyle=':', linewidth=0.5, color='#CCCCCC', alpha=0.5)
    return ax


def plot_cdf(data, label=None, ax=None, **kwargs):
    """Plot a CDF with publication styling.

    Args:
        data: 1D array-like of values
        label: Legend label
        ax: Axes to plot on (default: current axes)
    """
    if ax is None:
        ax = plt.gca()
    sorted_data = np.sort(data)
    cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    ax.plot(sorted_data, cdf, label=label, **kwargs)
    ax.set_ylabel('CDF')
    set_pub_style(ax)
    return ax


def plot_ccdf(data, label=None, log_scale=True, ax=None, **kwargs):
    """Plot a CCDF (1-CDF), optionally on log-log scale.

    Useful for heavy-tailed distributions common in networking:
    flow sizes, RTTs, inter-arrival times, connection durations.

    Args:
        data: 1D array-like of values
        label: Legend label
        log_scale: Whether to use log-log axes (default True)
        ax: Axes to plot on (default: current axes)
    """
    if ax is None:
        ax = plt.gca()
    sorted_data = np.sort(data)
    ccdf = 1 - (np.arange(1, len(sorted_data) + 1) / len(sorted_data))
    ax.plot(sorted_data, ccdf, label=label, **kwargs)
    if log_scale:
        ax.set_xscale('log')
        ax.set_yscale('log')
    ax.set_ylabel('CCDF: Pr(X > x)')
    set_pub_style(ax)
    return ax


def plot_time_series(x, y, label=None, width=7.0, smooth_window=None, ax=None, **kwargs):
    """Plot a time series with optional rolling-median smoothing.

    Args:
        x: Time values
        y: Metric values
        label: Legend label
        width: Figure width (default 7.0 for double column)
        smooth_window: If set, overlay a rolling median with this window size
        ax: Axes to plot on
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=golden_ratio_figsize(width, fraction=0.5))
    ax.plot(x, y, label=label, alpha=0.4 if smooth_window else 1.0, **kwargs)
    if smooth_window:
        import pandas as pd
        smoothed = pd.Series(y).rolling(smooth_window, center=True).median()
        ax.plot(x, smoothed, label=f'{label} (smoothed)', linewidth=1.5)
    set_pub_style(ax)
    return ax
