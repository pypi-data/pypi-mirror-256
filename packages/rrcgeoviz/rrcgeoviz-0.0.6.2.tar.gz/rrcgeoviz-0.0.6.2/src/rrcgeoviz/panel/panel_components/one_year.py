import panel as pn
import plotly.express as px
import plotly.graph_objects as go


def one_year_plot(args):
    df = args.data.copy()
    df["Year"] = df[args.options["time_column"]].dt.year
    df["Month"] = df[args.options["time_column"]].dt.month
    df["Month"] = df["Month"].astype("category")
    df["date"] = df[args.options["time_column"]].dt.date

    def emptyScattermap():
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 20, "t": 20, "l": 20, "b": 20},
            annotations=[
                {
                    "text": "No Points Found",
                    "x": 0.5,
                    "y": 0.5,
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 18},
                }
            ],
        )
        return fig

    def update_one_year_plot(new_df, year_value, victim_value):
        filtered_df = new_df[new_df["Year"] == year_value]
        if victim_value != "All":
            filtered_df = filtered_df[filtered_df["victim"] == victim_value]
        if filtered_df.empty:
            return emptyScattermap()

        fig = px.scatter_mapbox(
            filtered_df,
            lat="latitude",
            lon="longitude",
            hover_name="date",
            hover_data=["victim", "Month"],
            color="Month",
            color_discrete_sequence=px.colors.qualitative.Light24,
            zoom=1,
            height=400,
        )
        fig.update_layout(
            mapbox_style="open-street-map", margin={"r": 20, "t": 20, "l": 20, "b": 20}
        )

        return fig

    unique_victims = df["victim"].value_counts().index.tolist()
    unique_victims = ["All"] + unique_victims
    # Create a dropdown widget with unique victim values
    victim_dropdown = pn.widgets.Select(value=unique_victims[0], options=unique_victims)

    # Define callbacks to update the plot based on selected year and selected victim
    desired_year_num = pn.widgets.IntInput(
        name="Enter Year",
        start=df["Year"].min(),
        end=df["Year"].max(),
        value=df["Year"].median().astype("int32"),
        step=1,
    )

    one_year_plot = pn.bind(
        update_one_year_plot,
        new_df=df,
        year_value=desired_year_num,
        victim_value=victim_dropdown,
    )

    one_year_checkbox = pn.widgets.Checkbox(name="One Year Plot", value=True)

    # Display the dropdowns and initial plot
    one_year = pn.Column(
        one_year_checkbox,
        pn.Column(
            desired_year_num,
            victim_dropdown,
            pn.pane.Plotly(one_year_plot, sizing_mode="stretch_width"),
            visible=one_year_checkbox.param.value,
        ),
    ).servable()

    return one_year
