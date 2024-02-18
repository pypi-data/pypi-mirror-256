import os
from matplotlib import pyplot as plt
import numpy as np
import panel as pn
import seaborn as sns
from bokeh.models import Div
import geopandas as gpd
import hvplot.pandas
import geopandas
import contextily as ctx
import time

import importlib.resources
import os.path

"""
Optimizations:
- putting the map drawing in the yearly_range_plot scope so it only is created once
"""


def worldmap():
    return gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    fp = os.path.dirname(__file__) + "/../../static_data/world/world.shp"
    return gpd.read_file(fp)
    # file_path = str(importlib.resources.path("rrcgeoviz.static_data", "world.shp"))
    # return gpd.read_file(file_path)


def yearly_range_plot(args):
    # given args (an Arguments object with data and options), return a servable panel component
    silence(EMPTY_LAYOUT, True)
    silence(MISSING_RENDERERS, True)
    df = args.data.copy()
    df["Year"] = df[args.options["time_column"]].dt.year
    df["Month"] = df[args.options["time_column"]].dt.month
    world_tiles = worldmap()
    map_plot = world_tiles.hvplot(geo=True)

    def update_yearly_range_plot(event):
        silence(EMPTY_LAYOUT, True)
        silence(MISSING_RENDERERS, True)
        min_year, max_year = year_range_slider.value

        filtered_df = df[(df["Year"] >= min_year) & (df["Year"] <= max_year)]

        gdf = geopandas.GeoDataFrame(
            filtered_df,
            geometry=geopandas.points_from_xy(
                filtered_df[args.options["longitude_column"]],
                filtered_df[args.options["latitude_column"]],
            ),
            crs="EPSG:4326",  # TODO: Make the projection an option
        )

        out = map_plot * gdf.hvplot.points(
            "Longitude",
            "Latitude",
            geo=True,
            color="red",
            alpha=0.2,
            frame_width=600,
        )

        return out

    yearly_range_checkbox = pn.widgets.Checkbox(name="Yearly Range Plot", value=True)
    year_range_slider = pn.widgets.RangeSlider(
        name="Select Year Range",
        start=df["Year"].min(),
        end=df["Year"].max(),
        value=(df["Year"].min(), df["Year"].max()),
        step=1,
    )
    refresh_button = pn.widgets.Button(name="Refresh Plot", button_type="primary")
    yearly_range_plot = pn.panel(pn.bind(update_yearly_range_plot, refresh_button))

    yearly_range = pn.Column(
        yearly_range_checkbox,
        pn.Column(
            pn.Row(year_range_slider, refresh_button),
            yearly_range_plot,
            visible=yearly_range_checkbox.param.value,
        ),
    ).servable()

    return yearly_range
