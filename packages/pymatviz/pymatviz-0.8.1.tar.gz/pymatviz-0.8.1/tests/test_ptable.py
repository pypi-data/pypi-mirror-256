from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pytest
from plotly.exceptions import PlotlyError

from pymatviz import (
    count_elements,
    ptable_heatmap,
    ptable_heatmap_plotly,
    ptable_heatmap_ratio,
    ptable_hists,
    ptable_scatters,
)
from pymatviz.utils import df_ptable, si_fmt, si_fmt_int


if TYPE_CHECKING:
    from collections.abc import Sequence

    from pymatgen.core import Composition

    from pymatviz.ptable import CountMode


@pytest.fixture()
def glass_elem_counts(glass_formulas: pd.Series[Composition]) -> pd.Series[int]:
    return count_elements(glass_formulas)


@pytest.fixture()
def steel_formulas() -> list[str]:
    """Unusually fractional compositions, good for testing edge cases.

    Output of:
    from matminer.datasets import load_dataset

    load_dataset("matbench_steels").composition.head(2)
    """
    return [
        "Fe0.620C0.000953Mn0.000521Si0.00102Cr0.000110Ni0.192Mo0.0176V0.000112"
        "Nb0.0000616Co0.146Al0.00318Ti0.0185",
        "Fe0.623C0.00854Mn0.000104Si0.000203Cr0.147Ni0.0000971Mo0.0179V0.00515"
        "N0.00163Nb0.0000614Co0.188W0.00729Al0.000845",
    ]


@pytest.fixture()
def steel_elem_counts(steel_formulas: pd.Series[Composition]) -> pd.Series[int]:
    return count_elements(steel_formulas)


@pytest.mark.parametrize(
    "count_mode, counts",
    [
        ("composition", {"Fe": 22, "O": 63, "P": 12}),
        ("fractional_composition", {"Fe": 2.5, "O": 5, "P": 0.5}),
        ("reduced_composition", {"Fe": 13, "O": 27, "P": 3}),
        ("occurrence", {"Fe": 8, "O": 8, "P": 3}),
    ],
)
def test_count_elements(count_mode: CountMode, counts: dict[str, float]) -> None:
    series = count_elements(["Fe2 O3"] * 5 + ["Fe4 P4 O16"] * 3, count_mode=count_mode)
    expected = pd.Series(counts, index=df_ptable.index, name="count").fillna(0)
    pd.testing.assert_series_equal(series, expected, check_dtype=False)


def test_count_elements_by_atomic_nums() -> None:
    series_in = pd.Series(1, index=range(1, 119))
    el_cts = count_elements(series_in)
    expected = pd.Series(1, index=df_ptable.index, name="count")

    pd.testing.assert_series_equal(expected, el_cts)


@pytest.mark.parametrize("range_limits", [(-1, 10), (100, 200)])
def test_count_elements_bad_atomic_nums(range_limits: tuple[int, int]) -> None:
    with pytest.raises(ValueError, match="assumed to represent atomic numbers"):
        count_elements(dict.fromkeys(range(*range_limits), 0))

    with pytest.raises(ValueError, match="assumed to represent atomic numbers"):
        # string and integer keys for atomic numbers should be handled equally
        count_elements({str(idx): 0 for idx in range(*range_limits)})


def test_ptable_heatmap(
    glass_formulas: list[str], glass_elem_counts: pd.Series[int]
) -> None:
    ax = ptable_heatmap(glass_formulas)
    assert isinstance(ax, plt.Axes)

    ptable_heatmap(glass_formulas, log=True)

    # custom colormap
    ptable_heatmap(glass_formulas, log=True, colorscale="summer")

    # heat_mode normalized to total count
    ptable_heatmap(glass_formulas, heat_mode="fraction")
    ptable_heatmap(glass_formulas, heat_mode="percent")

    # without heatmap values
    ptable_heatmap(glass_formulas, heat_mode=None)
    ptable_heatmap(glass_formulas, log=True, heat_mode=None)

    # element properties as heatmap values
    ptable_heatmap(df_ptable.atomic_mass)

    # element properties as heatmap values
    ptable_heatmap(df_ptable.atomic_mass, text_color=("red", "blue"))

    # custom cbar_range
    ptable_heatmap(glass_formulas, cbar_range=(0, 100))
    ptable_heatmap(glass_formulas, log=True, cbar_range=(None, 100))
    ptable_heatmap(glass_formulas, log=True, cbar_range=(1, None))

    with pytest.raises(ValueError, match="Invalid vmin or vmax"):
        # can't use cbar_min=0 with log=True
        ptable_heatmap(glass_formulas, log=True, cbar_range=(0, None))

    # cbar_kwargs
    ax = ptable_heatmap(glass_formulas, cbar_kwargs=dict(orientation="horizontal"))
    cax = ax.inset_axes([0.1, 0.9, 0.8, 0.05])
    ptable_heatmap(glass_formulas, cbar_kwargs={"cax": cax, "format": "%.3f"})

    # element counts
    ptable_heatmap(glass_elem_counts)

    with pytest.raises(ValueError, match="Combining log color scale and"):
        ptable_heatmap(glass_formulas, log=True, heat_mode="percent")

    ptable_heatmap(glass_elem_counts, exclude_elements=["O", "P"])

    with pytest.raises(ValueError, match=r"Unexpected symbol\(s\) foobar"):
        ptable_heatmap(glass_elem_counts, exclude_elements=["foobar"])

    # cbar_fmt as string
    ax = ptable_heatmap(glass_elem_counts, cbar_fmt=".3f")
    cbar_labels = [label.get_text() for label in ax.child_axes[0].get_xticklabels()]
    assert cbar_labels[:2] == ["0.000", "50.000"]

    # cbar_fmt as function
    ax = ptable_heatmap(glass_elem_counts, fmt=si_fmt)
    ax = ptable_heatmap(
        glass_elem_counts, fmt=lambda x, _: f"{x:.0f}", cbar_fmt=si_fmt_int
    )
    ax = ptable_heatmap(glass_elem_counts, cbar_fmt=lambda x, _: f"{x:.3f} kg")

    ax = ptable_heatmap(glass_elem_counts, heat_mode="percent", cbar_fmt=".3%")
    cbar_1st_label = ax.child_axes[0].get_xticklabels()[0].get_text()
    assert cbar_1st_label == "0.000%"

    # tile_size
    ptable_heatmap(df_ptable.atomic_mass, tile_size=1)
    ptable_heatmap(df_ptable.atomic_mass, tile_size=(0.9, 1))

    # bad colorscale should raise ValueError
    bad_name = "bad color scale"
    with pytest.raises(
        ValueError,
        match=f"{bad_name!r} is not a valid value for name; supported values are "
        "'Accent', 'Accent_r'",
    ):
        ptable_heatmap(glass_formulas, colorscale=bad_name)

    # test text_style
    ptable_heatmap(glass_formulas, text_style=dict(color="red", fontsize=12))

    # test show_scale (with heat_mode)
    ptable_heatmap(glass_formulas, heat_mode="percent", show_scale=False)


def test_ptable_heatmap_ratio(
    steel_formulas: list[str],
    glass_formulas: list[str],
    steel_elem_counts: pd.Series[int],
    glass_elem_counts: pd.Series[int],
) -> None:
    # composition strings
    ax = ptable_heatmap_ratio(glass_formulas, steel_formulas)
    assert isinstance(ax, plt.Axes)

    # element counts
    ptable_heatmap_ratio(glass_elem_counts, steel_elem_counts, normalize=True)

    # mixed element counts and composition
    ptable_heatmap_ratio(glass_formulas, steel_elem_counts, exclude_elements=("O", "P"))
    ptable_heatmap_ratio(glass_elem_counts, steel_formulas, not_in_numerator=None)


def test_ptable_heatmap_plotly(glass_formulas: list[str]) -> None:
    fig = ptable_heatmap_plotly(glass_formulas)
    assert isinstance(fig, go.Figure)
    assert (
        len(fig.layout.annotations) == 18 * 10
    ), "not all periodic table tiles have annotations"
    assert (
        sum(anno.text != "" for anno in fig.layout.annotations) == 118
    ), "no annotations should be empty"

    # test hover_props and show_values=False
    ptable_heatmap_plotly(
        glass_formulas,
        hover_props=("atomic_mass", "atomic_number", "density"),
        show_values=False,
    )
    ptable_heatmap_plotly(
        glass_formulas,
        hover_data="density = " + df_ptable.density.astype(str) + " g/cm^3",
    )
    # test label_map as dict
    fig = ptable_heatmap_plotly(df_ptable.density, fmt=".1f", label_map={"0": "zero"})
    # test label_map as callable
    ptable_heatmap_plotly(
        df_ptable.density,
        fmt=".1f",
        label_map=lambda x: "meaning of life" if x == 42 else x,
    )

    ptable_heatmap_plotly(glass_formulas, heat_mode="percent")

    # test log color scale with -1, 0, 1 and random negative value
    for val in (-9.72, -1, 0, 1):
        ptable_heatmap_plotly([f"H{val}", "O2"], log=True)
        df_ptable["tmp"] = val
        fig = ptable_heatmap_plotly(df_ptable["tmp"], log=True)
        assert isinstance(fig, go.Figure)
        heatmap = next(
            trace
            for trace in fig.data
            if isinstance(trace, go.Heatmap) and "colorbar" in trace
        )
        assert heatmap.colorbar.title.text == "tmp"
        c_scale = heatmap.colorscale
        assert isinstance(c_scale, tuple)
        assert isinstance(c_scale[0], tuple)
        assert isinstance(c_scale[0][0], float)
        assert isinstance(c_scale[0][1], str)
        assert val <= max(c[0] for c in c_scale)

    with pytest.raises(TypeError, match="should be string, list of strings or list"):
        # test that bad colorscale raises ValueError
        ptable_heatmap_plotly(glass_formulas, colorscale=lambda: "bad scale")  # type: ignore[arg-type]

    # test that unknown builtin colorscale raises ValueError
    with pytest.raises(PlotlyError, match="Colorscale foobar is not a built-in scale"):
        ptable_heatmap_plotly(glass_formulas, colorscale="foobar")

    with pytest.raises(ValueError, match="Combining log color scale and"):
        ptable_heatmap_plotly(glass_formulas, log=True, heat_mode="percent")


@pytest.mark.parametrize("exclude_elements", [(), [], ["O", "P"]])
@pytest.mark.parametrize(
    "heat_mode, log", [(None, True), ("fraction", False), ("percent", False)]
)
@pytest.mark.parametrize("show_scale", [False, True])
@pytest.mark.parametrize("font_size", [None, 14])
@pytest.mark.parametrize("font_colors", [["red"], ("black", "white")])
def test_ptable_heatmap_plotly_kwarg_combos(
    glass_formulas: list[str],
    exclude_elements: Sequence[str],
    heat_mode: Literal["value", "fraction", "percent"] | None,
    show_scale: bool,
    font_size: int,
    font_colors: tuple[str] | tuple[str, str],
    log: bool,
) -> None:
    fig = ptable_heatmap_plotly(
        glass_formulas,
        exclude_elements=exclude_elements,
        heat_mode=heat_mode,
        show_scale=show_scale,
        font_size=font_size,
        font_colors=font_colors,
        log=log,
    )
    assert isinstance(fig, go.Figure)


@pytest.mark.parametrize(
    "colorscale", ["YlGn", ["blue", "red"], [(0, "blue"), (1, "red")]]
)
def test_ptable_heatmap_plotly_colorscale(
    glass_formulas: list[str], colorscale: str | list[tuple[float, str]] | list[str]
) -> None:
    fig = ptable_heatmap_plotly(glass_formulas, colorscale=colorscale)
    assert isinstance(fig, go.Figure)


@pytest.mark.parametrize(
    "color_bar", [{}, dict(orientation="v", len=0.8), dict(orientation="h", len=0.3)]
)
def test_ptable_heatmap_plotly_color_bar(
    glass_formulas: list[str], color_bar: dict[str, Any]
) -> None:
    fig = ptable_heatmap_plotly(glass_formulas, color_bar=color_bar)
    # check color bar has expected length
    assert fig.data[0].colorbar.len == color_bar.get("len", 0.4)
    # check color bar has expected title side
    assert (
        fig.data[0].colorbar.title.side == "right"
        if color_bar.get("orientation") == "v"
        else "top"
    )


@pytest.mark.parametrize(
    "cscale_range", [(None, None), (None, 10), (2, None), (2, 87123)]
)
def test_ptable_heatmap_plotly_cscale_range(
    cscale_range: tuple[float | None, float | None],
) -> None:
    fig = ptable_heatmap_plotly(df_ptable.density, cscale_range=cscale_range)
    trace = fig.data[0]
    assert "colorbar" in trace
    # check for correct color bar range
    if cscale_range == (None, None):
        # if both None, range is dynamic based on plotted data
        assert trace["zmin"] == pytest.approx(df_ptable.density.min())
        assert trace["zmax"] == pytest.approx(df_ptable.density.max())
    else:
        assert cscale_range == (trace["zmin"], trace["zmax"])


def test_ptable_heatmap_plotly_cscale_range_raises() -> None:
    cscale_range = (0, 10, 20)
    with pytest.raises(ValueError) as exc:
        ptable_heatmap_plotly(df_ptable.density, cscale_range=cscale_range)  # type: ignore[arg-type]
    assert f"{cscale_range=} should have length 2" in str(exc.value)


@pytest.mark.parametrize(
    "label_map",
    [None, False, {"1.0": "one", "2.0": "two", "3.0": "three", np.nan: "N/A"}],
)
def test_ptable_heatmap_plotly_label_map(
    label_map: dict[str, str] | Literal[False] | None,
) -> None:
    elem_vals = dict(Al=1.0, Cr=2.0, Fe=3.0, Ni=np.nan)
    fig = ptable_heatmap_plotly(elem_vals, label_map=label_map)
    assert isinstance(fig, go.Figure)

    # if label_map is not False, ensure mapped labels appear in figure annotations
    if label_map is not False:
        if label_map is None:
            # use default map
            label_map = dict.fromkeys([np.nan, None, "nan"], " ")  # type: ignore[list-item]
        # check for non-empty intersection between label_map values and annotations
        # we use `val in anno.text` cause the labels are wrapped in non-matching
        # HTML <span> tags
        assert sum(
            any(val in anno.text for val in label_map.values())
            for anno in fig.layout.annotations
        )


@pytest.mark.parametrize(
    "data, symbol_pos, anno_kwds, hist_kwds",
    [
        (pd.DataFrame({"H": [1, 2, 3], "He": [4, 5, 6]}), (0, 0), {}, None),
        (
            dict(H=[1, 2, 3], He=[4, 5, 6]),
            (1, 1),
            dict(text=lambda x: f"{len(x):,}"),
            {},
        ),
        (
            dict(H=np.array([1, 2, 3]), He=np.array([4, 5, 6])),
            (1, 1),
            dict(text=lambda x: f"{len(x):,}"),
            {},
        ),
        (
            pd.Series([[1, 2, 3], [4, 5, 6]], index=["H", "He"]),
            (1, 1),
            dict(xy=(0, 0)),
            lambda _hist_vals: dict(color="red"),
        ),
    ],
)
def test_ptable_hists(
    data: pd.DataFrame | pd.Series | dict[str, list[int]],
    symbol_pos: tuple[int, int],
    anno_kwds: dict[str, Any],
    hist_kwds: dict[str, Any],
) -> None:
    fig = ptable_hists(
        data, symbol_pos=symbol_pos, anno_kwds=anno_kwds, hist_kwds=hist_kwds
    )
    assert isinstance(fig, plt.Figure)


def test_ptable_scatters() -> None:
    """Test ptable_scatters with 3rd color dimension."""
    fig = ptable_scatters(
        data={
            "Fe": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            "O": [[10, 11], [12, 13], [14, 15]],
        },
        colormap="coolwarm",
        cbar_title="Test ptable_scatters",
    )
    assert isinstance(fig, plt.Figure)


@pytest.mark.parametrize(
    "data",
    [
        {"Fe": [[1, 2, 3], [4, 5, 6]], "O": [[7, 8], [9, 10]]},
        {"Fe": np.array([[1, 2, 3], [4, 5, 6]]), "O": np.array([[7, 8], [9, 10]])},
        pd.DataFrame({"Fe": [[1, 2, 3], [4, 5, 6]], "O": [[7, 8], [9, 10]]}),
        pd.Series([[[1, 2, 3], [4, 5, 6]], [[7, 8], [9, 10]]], index=["Fe", "O"]),
    ],
)
def test_ptable_scatters_datatypes(
    data: pd.DataFrame | pd.Series | dict[str, list[int]],
) -> None:
    """Test ptable_scatters with various input data types."""
    fig = ptable_scatters(data)
    assert isinstance(fig, plt.Figure)
    assert len(fig.axes) == 180
