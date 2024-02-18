import os
from matplotlib import pyplot as plt
import panel as pn
import geopandas as gpd
import os.path
import geopandas


def worldmap():
    return gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    fp = os.path.dirname(__file__) + "/../../static_data/world/world.shp"
    return gpd.read_file(fp)


def one_year_plot(args):
    df = args.data.copy()
    df["Year"] = df[args.options["time_column"]].dt.year
    df["Month"] = df[args.options["time_column"]].dt.month
    world_tiles = worldmap()

    def update_one_year_plot(event):
        desired_year = desired_year_num.value
        # fig, ax = plt.subplots(figsize=(6, 4))
        # ax.set_axis_off()
        filtered_df = df[df["Year"] == desired_year]
        # world_tiles.plot(color="lightgrey", ax=ax)
        # ax.set_title("Incidents by Month (Number Input)")
        gdf = geopandas.GeoDataFrame(
            filtered_df,
            geometry=geopandas.points_from_xy(
                filtered_df[args.options["longitude_column"]],
                filtered_df[args.options["latitude_column"]],
            ),
            crs="EPSG:4326",  # TODO: Make the projection an option
        )

        out = world_tiles.hvplot(
            geo=True,
        ) * gdf.hvplot.points(
            "Longitude", "Latitude", geo=True, color="red", alpha=0.2, frame_width=600
        )
        return out

    one_year_checkbox = pn.widgets.Checkbox(name="One Year Plot", value=True)
    desired_year_num = pn.widgets.IntInput(
        name="Enter Year",
        start=df["Year"].min(),
        end=df["Year"].max(),
        value=df["Year"].median().astype("int32"),
        step=1,
    )

    refresh_button = pn.widgets.Button(name="Refresh Plot", button_type="primary")
    one_year_plot = pn.panel(pn.bind(update_one_year_plot, refresh_button))

    one_year = pn.Column(
        one_year_checkbox,
        pn.Column(
            pn.Row(desired_year_num, refresh_button),
            pn.panel(one_year_plot),
            visible=one_year_checkbox.param.value,
        ),
    ).servable()

    return one_year
