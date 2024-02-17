from __future__ import annotations

import ast
from contextlib import contextmanager
from functools import partial
from os.path import dirname
from typing import TYPE_CHECKING, Any, Literal, get_args

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats
import sklearn
from matplotlib.offsetbox import AnchoredText
from sklearn.metrics import mean_absolute_percentage_error as mape
from sklearn.metrics import r2_score


if TYPE_CHECKING:
    from collections.abc import Generator, Sequence

    from matplotlib.gridspec import GridSpec
    from matplotlib.text import Annotation
    from numpy.typing import ArrayLike

PKG_DIR = dirname(__file__)
ROOT = dirname(PKG_DIR)
TEST_FILES = f"{ROOT}/tests/files"
Backend = Literal["matplotlib", "plotly"]
VALID_BACKENDS = mpl_key, plotly_key = get_args(Backend)


df_ptable = pd.read_csv(f"{ROOT}/pymatviz/elements.csv", comment="#").set_index(
    "symbol"
)

# http://jmol.sourceforge.net/jscolors
jmol_colors = df_ptable.jmol_color.dropna().map(ast.literal_eval)

# fallback value (in nanometers) for covalent radius of an element
# see https://wikipedia.org/wiki/Atomic_radii_of_the_elements
missing_covalent_radius = 0.2
covalent_radii: pd.Series = df_ptable.covalent_radius.fillna(missing_covalent_radius)

atomic_numbers: dict[str, int] = {}
element_symbols: dict[int, str] = {}

for Z, symbol in enumerate(df_ptable.index, 1):
    atomic_numbers[symbol] = Z
    element_symbols[Z] = symbol


def with_marginal_hist(
    xs: ArrayLike,
    ys: ArrayLike,
    cell: GridSpec | None = None,
    bins: int = 100,
    fig: plt.Figure | plt.Axes | None = None,
) -> plt.Axes:
    """Call before creating a plot and use the returned `ax_main` for all
    subsequent plotting ops to create a grid of plots with the main plot in the
    lower left and narrow histograms along its x- and/or y-axes displayed above
    and near the right edge.

    Args:
        xs (array): Marginal histogram values along x-axis.
        ys (array): Marginal histogram values along y-axis.
        cell (GridSpec, optional): Cell of a plt GridSpec at which to add the
            grid of plots. Defaults to None.
        bins (int, optional): Resolution/bin count of the histograms. Defaults to 100.
        fig (Figure, optional): matplotlib Figure or Axes to add the marginal histograms
            to. Defaults to None.

    Returns:
        plt.Axes: The matplotlib Axes to be used for the main plot.
    """
    if fig is None or isinstance(fig, plt.Axes):
        ax_main = fig or plt.gca()
        fig = ax_main.figure

    gs = (cell.subgridspec if cell else fig.add_gridspec)(
        2, 2, width_ratios=(6, 1), height_ratios=(1, 5), wspace=0, hspace=0
    )

    ax_main = fig.add_subplot(gs[1, 0])
    ax_histx = fig.add_subplot(gs[0, 0], sharex=ax_main)
    ax_histy = fig.add_subplot(gs[1, 1], sharey=ax_main)

    # x_hist
    ax_histx.hist(xs, bins=bins, rwidth=0.8)
    ax_histx.axis("off")

    # y_hist
    ax_histy.hist(ys, bins=bins, rwidth=0.8, orientation="horizontal")
    ax_histy.axis("off")

    return ax_main


def annotate_bars(
    ax: plt.Axes | None = None,
    v_offset: float = 10,
    h_offset: float = 0,
    labels: Sequence[str | int | float] | None = None,
    fontsize: int = 14,
    y_max_headroom: float = 1.2,
    adjust_test_pos: bool = False,
    **kwargs: Any,
) -> None:
    """Annotate each bar in bar plot with a label.

    Args:
        ax (Axes): The matplotlib axes to annotate.
        v_offset (int): Vertical offset between the labels and the bars.
        h_offset (int): Horizontal offset between the labels and the bars.
        labels (list[str]): Labels used for annotating bars. If not provided, defaults
            to the y-value of each bar.
        fontsize (int): Annotated text size in pts. Defaults to 14.
        y_max_headroom (float): Will be multiplied with the y-value of the tallest bar
            to increase the y-max of the plot, thereby making room for text above all
            bars. Defaults to 1.2.
        adjust_test_pos (bool): If True, use adjustText to prevent overlapping labels.
            Defaults to False.
        **kwargs: Additional arguments (rotation, arrowprops, etc.) are passed to
            ax.annotate().
    """
    ax = ax or plt.gca()

    if labels is None:
        labels = [int(patch.get_height()) for patch in ax.patches]
    elif len(labels) != len(ax.patches):
        raise ValueError(
            f"Got {len(labels)} labels but {len(ax.patches)} bars to annotate"
        )

    y_max: float = 0
    texts: list[Annotation] = []
    for rect, label in zip(ax.patches, labels):
        y_pos = rect.get_height()
        x_pos = rect.get_x() + rect.get_width() / 2 + h_offset

        if ax.get_yscale() == "log":
            y_pos = y_pos + np.log(max(1, v_offset))
        else:
            y_pos = y_pos + v_offset

        y_max = max(y_max, y_pos)

        txt = f"{label:,}" if isinstance(label, (int, float)) else label
        # place label at end of the bar and center horizontally
        anno = ax.annotate(
            txt, (x_pos, y_pos), ha="center", fontsize=fontsize, **kwargs
        )
        texts.append(anno)

    # ensure enough vertical space to display label above highest bar
    ax.set(ylim=(None, y_max * y_max_headroom))
    if adjust_test_pos:
        try:
            from adjustText import adjust_text

            adjust_text(texts, ax=ax)
        except ImportError as exc:
            raise ImportError(
                "adjustText not installed, falling back to default matplotlib "
                "label placement. Use pip install adjustText."
            ) from exc


def pretty_metric_label(key: str, backend: Backend) -> str:
    """Map metric keys to their pretty labels."""
    if backend not in VALID_BACKENDS:
        raise ValueError(f"Unexpected {backend=}, must be one of {VALID_BACKENDS}")

    symbol_mapping = {
        "R2": {mpl_key: "$R^2$", plotly_key: "R<sup>2</sup>"},
        "R2_adj": {mpl_key: "$R^2_{adj}$", plotly_key: "R<sup>2</sup><sub>adj</sub>"},
    }

    return symbol_mapping.get(key, {}).get(backend, key)


def annotate_metrics(
    xs: ArrayLike,
    ys: ArrayLike,
    fig: plt.Axes | plt.Figure | go.Figure | None = None,
    metrics: dict[str, float] | Sequence[str] = ("MAE", "R2"),
    prefix: str = "",
    suffix: str = "",
    fmt: str = ".3",
    **kwargs: Any,
) -> AnchoredText:
    """Provide a set of x and y values of equal length and an optional Axes
    object on which to print the values' mean absolute error and R^2
    coefficient of determination.

    Args:
        xs (array, optional): x values.
        ys (array, optional): y values.
        metrics (dict[str, float] | list[str], optional): Metrics to show. Can be a
            subset of recognized keys MAE, R2, R2_adj, RMSE, MSE, MAPE or the names of
            sklearn.metrics.regression functions or any dict of metric names and values.
            Defaults to ("MAE", "R2").
        fig (Axes, optional): matplotlib Axes on which to add the box. Defaults to None.
        loc (str, optional): Where on the plot to place the AnchoredText object.
            Defaults to "lower right".
        fmt (str, optional): f-string float format for metrics. Defaults to '.4'.
        prefix (str, optional): Title or other string to prepend to metrics.
            Defaults to "".
        suffix (str, optional): Text to append after metrics. Defaults to "".
        **kwargs: Additional arguments (rotation, arrowprops, frameon, loc, etc.) are
            passed to matplotlib.offsetbox.AnchoredText. Sets default loc="lower right"
            and frameon=False.

    Returns:
        AnchoredText: Instance containing the metrics.
    """
    valid_ax_types = (plt.Figure, plt.Axes, go.Figure)
    if not (fig is None or isinstance(fig, valid_ax_types)):
        raise TypeError(
            f"Unexpected type for fig: {type(fig)}, must be one of None, "
            f"{', '.join(valid_ax_types)}"
        )

    if isinstance(metrics, str):
        metrics = [metrics]
    if not isinstance(metrics, (dict, list, tuple, set)):
        raise TypeError(f"metrics must be dict|list|tuple|set, not {type(metrics)}")

    backend: Backend = "plotly" if isinstance(fig, go.Figure) else "matplotlib"

    funcs = {
        "MAE": lambda x, y: np.abs(x - y).mean(),
        "RMSE": lambda x, y: (((x - y) ** 2).mean()) ** 0.5,
        "MSE": lambda x, y: ((x - y) ** 2).mean(),
        "MAPE": mape,
        "R2": r2_score,
        # TODO: check this for correctness
        "R2_adj": lambda x, y: 1 - (1 - r2_score(x, y)) * (len(x) - 1) / (len(x) - 2),
    }
    for key in set(metrics) - set(funcs):
        func = getattr(sklearn.metrics, key, None)
        if func:
            funcs[key] = func
    if bad_keys := set(metrics) - set(funcs):
        raise ValueError(f"Unrecognized metrics: {bad_keys}")

    nan_mask = np.isnan(xs) | np.isnan(ys)
    xs, ys = xs[~nan_mask], ys[~nan_mask]

    text = prefix
    newline = "\n" if backend == "matplotlib" else "<br>"

    if isinstance(metrics, dict):
        for key, val in metrics.items():
            label = pretty_metric_label(key, backend)
            text += f"{label} = {val:{fmt}}{newline}"
    else:
        for key in metrics:
            value = funcs[key](xs, ys)
            label = pretty_metric_label(key, backend)
            text += f"{label} = {value:{fmt}}{newline}"
    text += suffix

    if backend == "matplotlib":
        ax = plt.gca()
        fig = fig or ax.figure

        defaults = dict(frameon=False, loc="upper left")
        text_box = AnchoredText(text, **(defaults | kwargs))
        ax.add_artist(text_box)
    elif isinstance(fig, go.Figure):
        defaults = dict(
            xref="paper",
            yref="paper",
            x=0.02,
            y=0.96,
            showarrow=False,
            font_size=16,
            align="left",
        )

        fig.add_annotation(text=text, **(defaults | kwargs))
    else:
        raise ValueError(f"Unexpected {backend=}, must be one of {VALID_BACKENDS}")

    return fig


CrystalSystem = Literal[
    "triclinic",
    "monoclinic",
    "orthorhombic",
    "tetragonal",
    "trigonal",
    "hexagonal",
    "cubic",
]


def crystal_sys_from_spg_num(spg: int) -> CrystalSystem:
    """Get the crystal system for an international space group number."""
    # ensure integer or float with no decimal part
    if not (isinstance(spg, (int, float)) and spg == int(spg)):
        raise TypeError(f"Expect integer space group number, got {spg=}")

    if not (1 <= spg <= 230):
        raise ValueError(f"Invalid space group number {spg}, must be 1 <= num <= 230")

    if 1 <= spg <= 2:
        return "triclinic"
    if spg <= 15:
        return "monoclinic"
    if spg <= 74:
        return "orthorhombic"
    if spg <= 142:
        return "tetragonal"
    if spg <= 167:
        return "trigonal"
    if spg <= 194:
        return "hexagonal"
    return "cubic"


def add_identity_line(
    fig: go.Figure | plt.Figure | plt.Axes,
    line_kwds: dict[str, Any] | None = None,
    trace_idx: int = 0,
    **kwargs: Any,
) -> go.Figure:
    """Add a line shape to the background layer of a plotly figure spanning
    from smallest to largest x/y values in the trace specified by trace_idx.

    Args:
        fig (go.Figure | plt.Figure | plt.Axes): plotly/matplotlib figure or axes to
            add the identity line to.
        line_kwds (dict[str, Any], optional): Keyword arguments for customizing the line
            shape will be passed to fig.add_shape(line=line_kwds). Defaults to
            dict(color="gray", width=1, dash="dash").
        trace_idx (int, optional): Index of the trace to use for measuring x/y limits.
            Defaults to 0. Unused if kaleido package is installed and the figure's
            actual x/y-range can be obtained from fig.full_figure_for_development().
            Applies only to plotly figures.
        **kwargs: Additional arguments are passed to fig.add_shape().

    Raises:
        TypeError: If fig is neither a plotly nor a matplotlib figure or axes.
        ValueError: If fig is a plotly figure and kaleido is not installed and trace_idx
            is out of range.

    Returns:
        Figure: Figure with added identity line.
    """
    valid_types = (go.Figure, plt.Figure, plt.Axes)
    if not isinstance(fig, valid_types):
        type_names = " | ".join(f"{t.__module__}.{t.__qualname__}" for t in valid_types)
        raise TypeError(f"{fig=} must be instance of {type_names}")

    if isinstance(fig, (plt.Figure, plt.Axes)):  # handle matplotlib
        ax = fig if isinstance(fig, plt.Axes) else fig.gca()

        x_mid = sum(ax.get_xlim()) / 2
        ax.axline(
            (x_mid, x_mid),
            (x_mid * 1.01, x_mid * 1.01),
            **dict(alpha=0.5, zorder=0, linestyle="dashed", color="black")
            | (line_kwds or {}),
        )
        return fig

    # If kaleido is missing, try block raises ValueError: Full figure generation
    # requires the kaleido package. Install with: pip install kaleido
    # If so, we resort to manually computing the xy data ranges which are usually are
    # close to but not the same as the axes limits.
    try:
        # https://stackoverflow.com/a/62042077
        full_fig = fig.full_figure_for_development(warn=False)
        xaxis_type = full_fig.layout.xaxis.type
        yaxis_type = full_fig.layout.yaxis.type

        x_range = full_fig.layout.xaxis.range
        y_range = full_fig.layout.yaxis.range

        # Convert log range to linear if necessary
        if xaxis_type == "log":
            x_range = [10**val for val in x_range]
        if yaxis_type == "log":
            y_range = [10**val for val in y_range]

        xy_min = min(x_range[0], y_range[0])
        xy_max = max(x_range[1], y_range[1])
    except ValueError:
        trace = fig.data[trace_idx]
        df_xy = pd.DataFrame({"x": trace.x, "y": trace.y}).dropna()

        # Determine ranges based on the type of axes
        if fig.layout.xaxis.type == "log":
            x_range = [10**val for val in (min(df_xy.x), max(df_xy.x))]
        else:
            x_range = [min(df_xy.x), max(df_xy.x)]

        if fig.layout.yaxis.type == "log":
            y_range = [10**val for val in (min(df_xy.y), max(df_xy.y))]
        else:
            y_range = [min(df_xy.y), max(df_xy.y)]

        xy_min = min(x_range[0], y_range[0])
        xy_max = max(x_range[1], y_range[1])

    if fig._grid_ref is not None:  # noqa: SLF001
        kwargs.setdefault("row", "all")
        kwargs.setdefault("col", "all")

    line_defaults = dict(color="gray", width=1, dash="dash")
    fig.add_shape(
        type="line",
        **dict(x0=xy_min, y0=xy_min, x1=xy_max, y1=xy_max),
        layer="below",
        line=line_defaults | (line_kwds or {}),
        **kwargs,
    )

    return fig


def add_ecdf_line(
    fig: go.Figure,
    values: ArrayLike = (),
    trace_idx: int = 0,
    trace_kwargs: dict[str, Any] | None = None,
    **kwargs: Any,
) -> go.Figure:
    """Add an empirical cumulative distribution function (ECDF) line to a plotly figure.

    Support for matplotlib planned but not implemented. PRs welcome.

    Args:
        fig (go.Figure): plotly figure to add the ECDF line to.
        values (array, optional): Values to compute the ECDF from. Defaults to () which
            means use the x-values of trace at trace_idx in fig.
        trace_idx (int, optional): Index of the trace whose x-values to use for
            computing the ECDF. Defaults to 0. Unused if values is not empty.
        trace_kwargs (dict[str, Any], optional): Passed to trace_ecdf.update().
            Defaults to None. Use e.g. to set trace name (default "Cumulative") or
            line_color (default "gray").
        **kwargs: Passed to fig.add_trace().

    Returns:
        Figure: Figure with added ECDF line.
    """
    valid_types = (go.Figure,)
    if not isinstance(fig, valid_types):
        type_names = " | ".join(f"{t.__module__}.{t.__qualname__}" for t in valid_types)
        raise TypeError(f"{fig=} must be instance of {type_names}")

    ecdf = px.ecdf(values if len(values) else fig.data[trace_idx].x).data[0]

    # if fig has facets, add ECDF to all subplots
    add_trace_defaults = {} if fig._grid_ref is None else dict(row="all", col="all")  # noqa: SLF001

    fig.add_trace(ecdf, **add_trace_defaults | kwargs)
    # move ECDF line to secondary y-axis
    # set color to darkened version of primary y-axis color
    trace_defaults = dict(yaxis="y2", name="Cumulative", line=dict(color="gray"))
    trace_kwargs = trace_defaults | (trace_kwargs or {})
    fig.data[-1].update(**trace_kwargs)

    color = trace_kwargs.get("line_color", trace_kwargs.get("line", {}).get("color"))

    yaxis_defaults = dict(
        title=trace_kwargs["name"],
        side="right",
        overlaying="y",
        range=(0, 1),
        showgrid=False,
        color=color,
        linecolor=color,
    )
    fig.layout.yaxis2 = yaxis_defaults | getattr(fig.layout, "yaxis2", {})

    return fig


def df_to_arrays(
    df: pd.DataFrame | None,
    *args: str | Sequence[str] | ArrayLike,
    strict: bool = True,
) -> list[ArrayLike | dict[str, ArrayLike]]:
    """If df is None, this is a no-op: args are returned as-is. If df is a
    dataframe, all following args are used as column names and the column data
    returned as arrays (after dropping rows with NaNs in any column).

    Args:
        df (pd.DataFrame | None): Optional pandas DataFrame.
        *args (list[ArrayLike | str]): Arbitrary number of arrays or column names in df.
        strict (bool, optional): If True, raise TypeError if df is not pd.DataFrame
            or None. If False, return args as-is. Defaults to True.

    Raises:
        ValueError: If df is not None and any of the args is not a df column name.
        TypeError: If df is not pd.DataFrame and not None.

    Returns:
        tuple[ArrayLike, ArrayLike]: Input arrays or arrays from dataframe columns.
    """
    if df is None:
        if cols := [arg for arg in args if isinstance(arg, str)]:
            raise ValueError(f"got column names but no df to get data from: {cols}")
        return args  # type: ignore[return-value]

    if not isinstance(df, pd.DataFrame):
        if not strict:
            return args  # type: ignore[return-value]
        raise TypeError(f"df should be pandas DataFrame or None, got {type(df)}")

    if arrays := [arg for arg in args if isinstance(arg, np.ndarray)]:
        raise ValueError(
            "don't pass dataframe and arrays to df_to_arrays(), should be either or, "
            f"got {arrays}"
        )

    flat_args = []
    # tuple doesn't support item assignment
    args = list(args)  # type: ignore[assignment]

    for col_name in args:
        if isinstance(col_name, (str, int)):
            flat_args.append(col_name)
        else:
            flat_args.extend(col_name)

    df_no_nan = df.dropna(subset=flat_args)
    for idx, col_name in enumerate(args):
        if isinstance(col_name, (str, int)):
            args[idx] = df_no_nan[col_name].to_numpy()  # type: ignore[index]
        else:
            col_data = df_no_nan[[*col_name]].to_numpy().T
            args[idx] = dict(zip(col_name, col_data))  # type: ignore[index]

    return args  # type: ignore[return-value]


def bin_df_cols(
    df_in: pd.DataFrame,
    bin_by_cols: Sequence[str],
    group_by_cols: Sequence[str] = (),
    n_bins: int | Sequence[int] = 100,
    bin_counts_col: str = "bin_counts",
    kde_col: str = "",
    verbose: bool = True,
) -> pd.DataFrame:
    """Bin columns of a DataFrame.

    Args:
        df_in (pd.DataFrame): Input dataframe to bin.
        bin_by_cols (Sequence[str]): Columns to bin.
        group_by_cols (Sequence[str]): Additional columns to group by. Defaults to ().
        n_bins (int): Number of bins to use. Defaults to 100.
        bin_counts_col (str): Column name for bin counts.
            Defaults to "bin_counts".
        kde_col (str): Column name for KDE bin counts e.g. 'kde_bin_counts'. Defaults to
            "" which means no KDE to speed things up.
        verbose (bool): If True, report df length reduction. Defaults to True.

    Returns:
        pd.DataFrame: Binned DataFrame.
    """
    if isinstance(n_bins, int):
        n_bins = [n_bins] * len(bin_by_cols)

    if len(bin_by_cols) != len(n_bins):
        raise ValueError(f"{len(bin_by_cols)=} != {len(n_bins)=}")

    index_name = df_in.index.name

    for col, bins in zip(bin_by_cols, n_bins):
        df_in[f"{col}_bins"] = pd.cut(df_in[col].values, bins=bins)

    if df_in.index.name not in df_in:
        df_in = df_in.reset_index()

    group = df_in.groupby([*[f"{c}_bins" for c in bin_by_cols], *group_by_cols])

    df_bin = group.first().dropna()
    df_bin[bin_counts_col] = group.size()

    if verbose:
        print(  # noqa: T201
            f"{1 - len(df_bin) / len(df_in):.1%} row reduction from binning: from "
            f"{len(df_bin):,} to {len(df_in):,}"
        )

    if kde_col:
        # compute kernel density estimate for each bin
        values = df_in[bin_by_cols].dropna().T
        model_kde = scipy.stats.gaussian_kde(values)

        xy_binned = df_bin[bin_by_cols].T
        density = model_kde(xy_binned)
        df_bin["cnt_col"] = density / density.sum() * len(values)

    if index_name is None:
        return df_bin
    return df_bin.reset_index().set_index(index_name)


@contextmanager
def patch_dict(
    dct: dict[Any, Any], *args: Any, **kwargs: Any
) -> Generator[dict[Any, Any], None, None]:
    """Context manager to temporarily patch the specified keys in a dictionary and
    restore it to its original state on context exit.

    Useful e.g. for temporary plotly fig.layout mutations:

        with patch_dict(fig.layout, showlegend=False):
            fig.write_image("plot.pdf")

    Args:
        dct (dict): The dictionary to be patched.
        *args: Only first element is read if present. A single dictionary containing the
            key-value pairs to patch.
        **kwargs: The key-value pairs to patch, provided as keyword arguments.

    Yields:
        dict: The patched dictionary incl. temporary updates.
    """
    # if both args and kwargs are passed, kwargs will overwrite args
    updates = {**args[0], **kwargs} if args and isinstance(args[0], dict) else kwargs

    # save original values as shallow copy for speed
    # warning: in-place changes to nested dicts and objects will persist beyond context!
    patched = dct.copy()

    # apply updates
    patched.update(updates)

    yield patched


def luminance(color: tuple[float, float, float]) -> float:
    """Compute the luminance of a color as in https://stackoverflow.com/a/596243.

    Args:
        color (tuple[float, float, float]): RGB color tuple with values in [0, 1].

    Returns:
        float: Luminance of the color.
    """
    red, green, blue, *_ = color  # alpha = 1 - transparency
    return 0.299 * red + 0.587 * green + 0.114 * blue


def pick_bw_for_contrast(
    color: tuple[float, float, float], text_color_threshold: float = 0.7
) -> str:
    """Choose black or white text color for a given background color based on
    luminance.

    Args:
        color (tuple[float, float, float]): RGB color tuple with values in [0, 1].
        text_color_threshold (float, optional): Luminance threshold for choosing
            black or white text color. Defaults to 0.7.

    Returns:
        str: "black" or "white" depending on the luminance of the background color.
    """
    light_bg = luminance(color) > text_color_threshold
    return "black" if light_bg else "white"


def si_fmt(
    val: float, fmt_spec: str = ".1f", sep: str = "", binary: bool = False
) -> str:
    """Convert large numbers into human readable format using SI prefixes in binary
    (1024) or metric (1000) mode.

    https://nist.gov/pml/weights-and-measures/metric-si-prefixes

    Args:
        val (int | float): Some numerical value to format.
        binary (bool, optional): If True, scaling factor is 2^10 = 1024 else 1000.
            Defaults to False.
        fmt_spec (str): f-string format specifier. Configure precision and left/right
            padding in returned string. Defaults to ".1f". Can be used to ensure leading
            or trailing whitespace for shorter numbers. See
            https://docs.python.org/3/library/string.html#format-specification-mini-language.
        sep (str): Separator between number and postfix. Defaults to "".

    Returns:
        str: Formatted number.
    """
    factor = 1024 if binary else 1000
    _scale = ""

    if abs(val) >= 1:
        # 1, Kilo, Mega, Giga, Tera, Peta, Exa, Zetta, Yotta
        for _scale in ("", "K", "M", "G", "T", "P", "E", "Z", "Y"):
            if abs(val) < factor:
                break
            val /= factor
    elif val != 0:
        # milli, micro, nano, pico, femto, atto, zepto, yocto
        for _scale in ("", "m", "μ", "n", "p", "f", "a", "z", "y"):
            if abs(val) > 1:
                break
            val *= factor

    return f"{val:{fmt_spec}}{sep}{_scale}"


si_fmt_int = partial(si_fmt, fmt_spec=".0f")


def styled_html_tag(text: str, tag: str = "span", style: str = "") -> str:
    """Wrap text in a span with custom style. Style defaults to decreased font size
    and weight e.g. to display units in plotly labels and annotations.

    Args:
        text (str): Text to wrap in span.
        tag (str, optional): HTML tag name. Defaults to "span".
        style (str, optional): CSS style string. Defaults to
            "font-size: 0.8em; font-weight: lighter;".
    """
    style = style or "font-size: 0.8em; font-weight: lighter;"
    return f"<{tag} {style=}>{text}</{tag}>"
