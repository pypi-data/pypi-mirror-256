from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Union, no_type_check

import plotly.express as px
import plotly.graph_objects as go
import scipy.constants as const
from plotly.subplots import make_subplots
from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine
from pymatgen.phonon.bandstructure import PhononBandStructureSymmLine as PhononBands
from pymatgen.phonon.dos import PhononDos
from pymatgen.util.string import htmlify


if TYPE_CHECKING:
    import numpy as np


AnyBandStructure = Union[BandStructureSymmLine, PhononBands]


def pretty_sym_point(symbol: str) -> str:
    """Convert a symbol to a pretty-printed version."""
    # htmlify maps S0 -> S<sub>0</sub> but leaves S_0 as is so we remove underscores
    return (
        htmlify(symbol.replace("_", ""))
        .replace("GAMMA", "Γ")
        .replace("DELTA", "Δ")
        .replace("SIGMA", "Σ")
    )


def get_band_xaxis_ticks(bs: PhononBands) -> tuple[list[float], list[str]]:
    """Get all ticks and labels for a band structure plot.

    Returns:
        tuple[list[float], list[str]]: Ticks and labels for the x-axis of a band
            structure plot.
    """
    ticks_x_pos = []
    tick_labels: list[str] = []
    prev_label = bs.qpoints[0].label
    prev_branch = bs.branches[0]["name"]

    for idx, point in enumerate(bs.qpoints):
        if point.label is None:
            continue
        ticks_x_pos += [bs.distance[idx]]

        branches = (
            branch["name"]
            for branch in bs.branches
            if branch["start_index"] <= idx <= branch["end_index"]
        )
        this_branch = next(branches, None)

        if point.label != prev_label and prev_branch != this_branch:
            tick_labels.pop()
            ticks_x_pos.pop()
            tick_labels += [f"{prev_label or ''}|{point.label}"]
        else:
            tick_labels += [point.label]

        prev_label = point.label
        prev_branch = this_branch

    tick_labels = list(map(pretty_sym_point, tick_labels))
    return ticks_x_pos, tick_labels


YMin = Union[float, Literal["y_min"]]
YMax = Union[float, Literal["y_max"]]


@no_type_check
def _shaded_range(
    fig: go.Figure, shaded_ys: dict[tuple[YMin, YMax], dict[str, Any]] | bool | None
) -> go.Figure:
    if shaded_ys is False:
        return fig

    shade_defaults = dict(layer="below", row="all", col="all")
    y_lim = dict(zip(("y_min", "y_max"), fig.layout.yaxis.range))

    shaded_ys = shaded_ys or {(0, "y_min"): dict(fillcolor="gray", opacity=0.07)}
    for (y0, y1), kwds in shaded_ys.items():
        for y_val in (y0, y1):
            if isinstance(y_val, str) and y_val not in y_lim:
                raise ValueError(f"Invalid {y_val=}, must be one of {[*y_lim]}")
        fig.add_hrect(
            y0=y_lim.get(y0, y0), y1=y_lim.get(y1, y1), **shade_defaults | kwds
        )

    return fig


def plot_phonon_bands(
    band_structs: PhononBands | dict[str, PhononBands],
    line_kwds: dict[str, Any] | None = None,
    shaded_ys: dict[tuple[YMin, YMax], dict[str, Any]] | bool | None = None,
    **kwargs: Any,
) -> go.Figure:
    """Plot single or multiple pymatgen band structures using Plotly, focusing on the
    minimum set of overlapping branches.

    Warning: Only tested with phonon band structures so far but plan is to extend to
    electronic band structures.

    Args:
        band_structs (PhononBandStructureSymmLine | dict[str, PhononBandStructure]):
            Single BandStructureSymmLine or PhononBandStructureSymmLine object or a dict
            with labels mapped to multiple such objects.
        line_kwds (dict[str, Any]): Passed to Plotly's Figure.add_scatter method.
        shaded_ys (dict[tuple[float | str, float | str], dict]): Keys are y-ranges
            (min, max) tuple and values are kwargs for shaded regions created by
            fig.add_hrect(). Defaults to single entry (0, "y_min"):
            dict(fillcolor="gray", opacity=0.07). "y_min" and "y_max" will be replaced
            with the figure's y-axis range. dict(layer="below", row="all", col="all") is
            always passed to add_hrect but can be overridden by the user. Set to False
            to disable.
        **kwargs: Passed to Plotly's Figure.add_scatter method.

    Returns:
        go.Figure: Plotly figure object.
    """
    fig = go.Figure()
    line_kwds = line_kwds or {}

    if not isinstance(band_structs, dict):  # normalize input to dictionary
        band_structs = {"": band_structs}

    # find common branches by normalized branch names
    common_branches: set[str] = set()
    for bs in band_structs.values():
        if not isinstance(bs, PhononBands):
            type_name = type(bs).__name__
            raise TypeError(
                f"Only {PhononBands.__name__} objects supported, got {type_name}"
            )
        branches = {pretty_sym_point(branch["name"]) for branch in bs.branches}
        common_branches = common_branches & branches if common_branches else branches

    if not common_branches:
        raise ValueError("No common branches found among the band structures.")

    # plotting only the common branches for each band structure
    first_bs = None
    colors = px.colors.qualitative.Plotly
    line_styles = ("solid", "dot", "dash", "longdash", "dashdot", "longdashdot")

    for bs_idx, (label, bs) in enumerate(band_structs.items()):
        color = colors[bs_idx % len(colors)]
        line_style = line_styles[bs_idx % len(line_styles)]
        line_defaults = dict(color=color, width=1.5, dash=line_style)
        # 1st bands determine x-axis scale (there are usually slight scale differences
        # between bands)
        first_bs = first_bs or bs
        for branch_idx, branch in enumerate(bs.branches):
            start_idx = branch["start_index"]
            end_idx = branch["end_index"] + 1  # Include the end point
            # using the same first_bs x-axis for all band structures to avoid band
            # shifting
            distances = first_bs.distance[start_idx:end_idx]
            for band in range(bs.nb_bands):
                frequencies = bs.bands[band][start_idx:end_idx]
                # group traces for toggling and set legend name only for 1st band
                fig.add_scatter(
                    x=distances,
                    y=frequencies,
                    mode="lines",
                    line=line_defaults | line_kwds,
                    legendgroup=label,
                    name=label,
                    showlegend=branch_idx == band == 0,
                    **kwargs,
                )

    # add x-axis labels and vertical lines for common high-symmetry points
    first_bs = next(iter(band_structs.values()))
    x_ticks, x_labels = get_band_xaxis_ticks(first_bs)
    fig.layout.xaxis.update(tickvals=x_ticks, ticktext=x_labels, tickangle=0)

    # remove 0 and the last line to avoid duplicate vertical line, looks like
    # graphical artifact
    for x_pos in {*x_ticks} - {0, x_ticks[-1]}:
        fig.add_vline(x=x_pos, line=dict(color="black", width=1))

    fig.layout.xaxis.title = "Wave Vector"
    fig.layout.yaxis.title = "Frequency (THz)"
    fig.layout.margin = dict(t=5, b=5, l=5, r=5)

    # get y-axis range from all band structures
    y_min = min(min(bs.bands.ravel()) for bs in band_structs.values())
    y_max = max(max(bs.bands.ravel()) for bs in band_structs.values())

    if y_min < -0.1:  # no need for y=0 line if y_min = 0
        fig.add_hline(y=0, line=dict(color="black", width=1))
    if y_min >= -0.01:  # set y_min=0 if below tolerance for imaginary frequencies
        y_min = 0
    fig.layout.yaxis.range = (1.05 * y_min, 1.05 * y_max)

    axes_kwds = dict(linecolor="black", gridcolor="lightgray")
    fig.layout.xaxis.update(**axes_kwds)
    fig.layout.yaxis.update(**axes_kwds)

    # move legend to top left corner
    fig.layout.legend.update(
        x=0.005,
        y=0.99,
        orientation="h",
        yanchor="top",
        bgcolor="rgba(255, 255, 255, 0.6)",
        tracegroupgap=0,
    )

    # scale font size with figure size
    fig.layout.font.size = 16 * (fig.layout.width or 800) / 800

    _shaded_range(fig, shaded_ys)

    return fig


def plot_phonon_dos(
    doses: PhononDos | dict[str, PhononDos],
    stack: bool = False,
    sigma: float = 0,
    units: Literal["THz", "eV", "meV", "Ha", "cm-1"] = "THz",
    normalize: Literal["max", "sum", "integral"] | None = None,
    last_peak_anno: str | None = None,
    **kwargs: Any,
) -> go.Figure:
    """Plot phonon DOS using Plotly.

    Args:
        doses (PhononDos | dict[str, PhononDos]): PhononDos or dict of multiple.
        stack (bool): Whether to plot the DOS as a stacked area graph. Defaults to
            False.
        sigma (float): Standard deviation for Gaussian smearing. Defaults to None.
        units (str): Units for the frequencies. Defaults to "THz".
        legend (dict): Legend configuration.
        normalize (bool): Whether to normalize the DOS. Defaults to False.
        last_peak_anno (str): Annotation for last DOS peak with f-string placeholders
            for key (of dict containing multiple DOSes), last_peak frequency and units.
            Defaults to None, meaning last peak annotation is disabled. Set to "" to
            enable with a sensible default string.
        **kwargs: Passed to Plotly's Figure.add_scatter method.

    Returns:
        go.Figure: Plotly figure object.
    """
    valid_normalize = (None, "max", "sum", "integral")
    if normalize not in valid_normalize:
        raise ValueError(f"Invalid {normalize=}, must be one of {valid_normalize}.")
    if last_peak_anno == "":
        last_peak_anno = "ω<sub>{key}</sub></span>={last_peak:.1f} {units}"

    fig = go.Figure()
    doses = {"": doses} if isinstance(doses, PhononDos) else doses

    for key, dos in doses.items():
        if not isinstance(dos, PhononDos):
            raise TypeError(
                f"Only PhononDos objects supported, got {type(dos).__name__}"
            )
        frequencies = dos.frequencies
        densities = dos.get_smeared_densities(sigma)

        # convert frequencies to specified units
        frequencies = convert_frequencies(frequencies, units)

        # normalize DOS
        if normalize == "max":
            densities = densities / densities.max()
        elif normalize == "sum":
            densities = densities / densities.sum()
        elif normalize == "integral":
            bin_width = frequencies[1] - frequencies[0]
            densities = densities / densities.sum() / bin_width

        defaults = dict(mode="lines")
        if stack:
            if fig.data:  # for stacked plots, accumulate densities
                densities = densities + fig.data[-1].y
            defaults.setdefault("fill", "tonexty")

        fig.add_scatter(x=frequencies, y=densities, name=key, **(defaults | kwargs))

    fig.layout.xaxis.update(title=f"Frequency ({units})")
    fig.layout.yaxis.update(title="Density of States")
    fig.layout.margin = dict(t=5, b=5, l=5, r=5)
    fig.layout.font.size = 16 * (fig.layout.width or 800) / 800
    fig.layout.legend.update(x=0.005, y=0.99, orientation="h", yanchor="top")

    qual_colors = px.colors.qualitative.Plotly
    if last_peak_anno:
        for idx, (key, dos) in enumerate(doses.items()):
            last_peak = dos.get_last_peak()
            color = (
                fig.data[idx].line.color
                or fig.data[idx].marker.color
                or qual_colors[idx % len(qual_colors)]
            )

            anno = dict(
                text=last_peak_anno.format(key=key, last_peak=last_peak, units=units),
                font=dict(color=color),
                xanchor="right",
                yshift=idx * -30,  # shift downward with increasing index
            )
            fig.add_vline(
                x=last_peak,
                line=dict(color=color, dash="dot"),
                name=f"last phDOS peak {key}",
                annotation=anno,
            )

    return fig


def convert_frequencies(
    frequencies: np.ndarray,
    unit: Literal["THz", "eV", "meV", "Ha", "cm-1"] = "THz",
) -> np.ndarray:
    """Convert frequencies from THz to specified units.

    Args:
        frequencies (np.ndarray): Frequencies in THz.
        unit (str): Target units. One of 'THz', 'eV', 'meV', 'Ha', 'cm-1'.

    Returns:
        np.ndarray: Converted frequencies.
    """
    conversion_factors = {
        "THz": 1,
        "eV": const.value("hertz-electron volt relationship") * const.tera,
        "meV": const.value("hertz-electron volt relationship")
        * const.tera
        / const.milli,
        "Ha": const.value("hertz-hartree relationship") * const.tera,
        "cm-1": const.value("hertz-inverse meter relationship")
        * const.tera
        * const.centi,
    }

    factor = conversion_factors.get(unit)
    if factor is None:
        raise ValueError(f"Invalid {unit=}, must be one of {list(conversion_factors)}")
    return frequencies * factor


def plot_phonon_bands_and_dos(
    band_structs: PhononBands | dict[str, PhononBands],
    doses: PhononDos | dict[str, PhononDos],
    bands_kwargs: dict[str, Any] | None = None,
    dos_kwargs: dict[str, Any] | None = None,
    subplot_kwargs: dict[str, Any] | None = None,
    **kwargs: Any,
) -> go.Figure:
    """Plot phonon DOS and band structure using Plotly.

    Args:
        doses (PhononDos | dict[str, PhononDos]): PhononDos or dict of multiple.
        band_structs (PhononBandStructureSymmLine | dict[str, PhononBandStructure]):
            Single BandStructureSymmLine or PhononBandStructureSymmLine object or a dict
            with labels mapped to multiple such objects.
        bands_kwargs (dict[str, Any]): Passed to Plotly's Figure.add_scatter method.
        dos_kwargs (dict[str, Any]): Passed to Plotly's Figure.add_scatter method.
        subplot_kwargs (dict[str, Any]): Passed to Plotly's make_subplots method.
            Defaults to dict(shared_yaxes=True, column_widths=(0.8, 0.2),
            horizontal_spacing=0.01).
        **kwargs: Passed to Plotly's Figure.add_scatter method.

    Returns:
        go.Figure: Plotly figure object.
    """
    if not isinstance(band_structs, dict):  # normalize input to dictionary
        band_structs = {"": band_structs}
    if not isinstance(doses, dict):  # normalize input to dictionary
        doses = {"": doses}
    if (band_keys := set(band_structs)) != (dos_keys := set(doses)):
        raise ValueError(f"{band_keys=} and {dos_keys=} must be identical")

    subplot_defaults = dict(
        shared_yaxes=True, column_widths=(0.8, 0.2), horizontal_spacing=0.03
    )
    fig = make_subplots(rows=1, cols=2, **subplot_defaults | (subplot_kwargs or {}))

    # plot band structure
    bands_kwargs = bands_kwargs or {}
    shaded_ys = bands_kwargs.pop("shaded_ys", None)
    # disable shaded_ys for bands, would cause double shading due to _shaded_range below
    bands_kwargs["shaded_ys"] = False
    bands_fig = plot_phonon_bands(band_structs, **kwargs | bands_kwargs)
    # import band structure layout to main figure
    fig.update_layout(bands_fig.layout)

    fig.add_traces(bands_fig.data, rows=1, cols=1)

    # plot density of states
    dos_fig = plot_phonon_dos(doses, **kwargs | (dos_kwargs or {}))
    # swap DOS x and y axes (for 90 degrees rotation)
    for trace in dos_fig.data:
        trace.x, trace.y = trace.y, trace.x

    fig.add_traces(dos_fig.data, rows=1, cols=2)
    # transfer zero line from DOS to band structure
    if fig.layout.yaxis.range[0] < -0.1:
        fig.add_hline(y=0, line=dict(color="black", width=1), row=1, col=2)

    # put traces with same labels into the same legend group and hide the legend for
    # the 2nd subplot, give them the same color as the corresponding band structure
    line_map: dict[str, dict[str, Any]] = {}
    for trace in fig.data:
        trace.legendgroup = trace.name
        trace.showlegend = trace.showlegend and trace.xaxis == "x2"
        trace.line = line_map.setdefault(trace.name, trace.line)

    fig.layout.xaxis2.update(title="DOS")
    # transfer x-axis label from DOS fig to parent fig (since DOS may have custom units)
    fig.layout.yaxis.update(title=dos_fig.layout.xaxis.title.text)

    # set y-axis range to match band structure
    fig.layout.yaxis.update(range=bands_fig.layout.yaxis.range)

    _shaded_range(fig, shaded_ys)

    return fig
