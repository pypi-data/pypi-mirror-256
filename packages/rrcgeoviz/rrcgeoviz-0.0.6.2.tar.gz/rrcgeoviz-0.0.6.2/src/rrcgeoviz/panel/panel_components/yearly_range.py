from matplotlib import pyplot as plt
import panel as pn
import plotly.express as px


def yearly_range_plot(args):
    df = args.data.copy()
    df["Year"] = df[args.options["time_column"]].dt.year
    df["Month"] = df[args.options["time_column"]].dt.month
    df["date"] = df[args.options["time_column"]].dt.date

    def update_yearly_range_plot(value):
        min_year, max_year = value
        filtered_df = df[(df["Year"] >= min_year) & (df["Year"] <= max_year)]

        fig = px.scatter_mapbox(
            filtered_df,
            lat="latitude",
            lon="longitude",
            hover_name="date",
            hover_data=["victim"],
            color="Year",
            zoom=1,
            height=400,
        )
        fig.update_layout(
            mapbox_style="open-street-map", margin={"r": 20, "t": 20, "l": 20, "b": 20}
        )

        return fig

    yearly_range_checkbox = pn.widgets.Checkbox(name="Yearly Range Plot", value=True)
    year_range_slider = pn.widgets.RangeSlider(
        name="Select Year Range",
        start=df["Year"].min(),
        end=df["Year"].max(),
        value=(df["Year"].min(), df["Year"].max()),
        step=1,
    )
    yearly_range_plot = pn.bind(update_yearly_range_plot, value=year_range_slider)

    yearly_range = pn.Column(
        yearly_range_checkbox,
        pn.Column(
            year_range_slider,
            pn.pane.Plotly(yearly_range_plot, sizing_mode="stretch_width"),
            visible=yearly_range_checkbox.param.value,
        ),
    ).servable()

    return yearly_range
