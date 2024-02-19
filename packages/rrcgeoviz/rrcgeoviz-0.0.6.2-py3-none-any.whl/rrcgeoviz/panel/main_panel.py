import os
import threading
from time import sleep
import time
import pandas as pd
import panel as pn
from bokeh.models import Div

from .panel_components.yearly_range import yearly_range_plot
from .panel_components.heatmap import heatmap_plot
from .panel_components.one_year import one_year_plot
from .panel_components.all_months import all_months_plot
from .panel_components.one_year_months import one_year_months_plot
from .panel_components.threeD import threeD_plot
from .panel_components.pandas_profile import gen_profile_report
from panel.widgets.indicators import BooleanIndicator
from dateutil.parser import parse
from panel.io import server

import importlib.resources


def render_panel(args, test=False):
    # get favicon
    # favicon_path = str(importlib.resources.path("static_data", "favicon.ico"))
    # logo_path = str(importlib.resources.path("static_data", "geoviz.jpg"))
    logo_path = "https://i.imgur.com/Loud9RB.jpeg"

    template = pn.template.BootstrapTemplate(
        title="GeoViz - " + str(args.data_file_name),
        collapsed_sidebar=True,
        logo=logo_path,
        # favicon=favicon_path,
    )

    if "time_column" in args.options:
        args.data[args.options["time_column"]] = pd.to_datetime(
            args.data[args.options["time_column"]]
        )

    # add components here
    mainColumn = addCorrectElements(args)

    template.main.append(
        pn.Tabs(
            ("Visualizations", mainColumn),
            ("Pandas Profiling", pn.Column(gen_profile_report(args))),
        )
    )

    if not test:
        server = pn.serve(template)

    return template


def addCorrectElements(arguments):
    """Actually add the right elements to the display.
    A dictionary of generated data and the arguments are available for purchase at the gift store.
    """
    mainColumn = pn.Column()

    # TODO:POI (data gen), NLP (data gen)
    # month/year heatmap
    if (
        "month_year_heatmap" in arguments.options
        and arguments.options["month_year_heatmap"]
        and "time_column" in arguments.options
    ):
        heatmap_element = heatmap_plot(arguments)
        mainColumn.append(pn.pane.HTML("<h2>Year/Month Heatmap</h2>"))
        mainColumn.append(heatmap_element)

    if (
        "yearly_range" in arguments.options
        and arguments.options["yearly_range"]
        and "latitude_column" in arguments.options
        and "longitude_column" in arguments.options
    ):
        yearly_range_element = yearly_range_plot(arguments)
        mainColumn.append(pn.pane.HTML("<hr><h2>Year Range Map</h2>"))
        mainColumn.append(yearly_range_element)

    if (
        "one_year" in arguments.options
        and arguments.options["one_year"]
        and "latitude_column" in arguments.options
        and "longitude_column" in arguments.options
    ):
        one_year_element = one_year_plot(arguments)
        mainColumn.append(pn.pane.HTML("<hr><h2>One Year Map</h2>"))
        mainColumn.append(one_year_element)

    if "all_months" in arguments.options and arguments.options["all_months"]:
        all_months_element = all_months_plot(arguments)
        mainColumn.append(pn.pane.HTML("<hr><h2>Month-to-Month Frequency</h2>"))
        mainColumn.append(all_months_element)

    if "one_year_months" in arguments.options and arguments.options["one_year_months"]:
        one_year_months_element = one_year_months_plot(arguments)
        mainColumn.append(
            pn.pane.HTML("<hr><h2>Month-to-Month Frequency for One Year</h2>")
        )
        mainColumn.append(one_year_months_element)

    if "threeD" in arguments.options and arguments.options["threeD"]:
        threeD_element = threeD_plot(arguments)
        mainColumn.append(
            pn.pane.HTML("<hr><h2>Latitude/Longitude/Time 3D Visualization</h2>")
        )
        mainColumn.append(threeD_element)

    return mainColumn
