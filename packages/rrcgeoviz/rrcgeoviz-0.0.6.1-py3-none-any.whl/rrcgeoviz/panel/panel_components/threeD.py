from matplotlib import pyplot as plt
import panel as pn
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.cluster import DBSCAN


def threeD_plot(args):
    df = args.data.copy()
    first_datetime = df["date"].min()
    df["days_int"] = (df["date"] - first_datetime).dt.days
    lat_min, lat_max = df["latitude"].min(), df["latitude"].max()
    long_min, long_max = df["longitude"].min(), df["longitude"].max()
    date_min, date_max = df["days_int"].min(), df["days_int"].max()
    df["Normalized_Longitude"] = (df["longitude"] - long_min) / (long_max - long_min)
    df["Normalized_Latitude"] = (df["latitude"] - lat_min) / (lat_max - lat_min)
    df["Time"] = (df["days_int"] - date_min) / (date_max - date_min)
    X = df[["Normalized_Longitude", "Normalized_Latitude", "Time"]]
    db = DBSCAN(eps=0.05, min_samples=5)
    df["cluster"] = db.fit_predict(X)
    num_colors = len(df)
    colors = np.random.randint(0, 256, size=(num_colors, 3))
    plotly_df = pd.concat([df, pd.DataFrame(colors, columns=["r", "g", "b"])], axis=1)
    fig = px.scatter_3d(
        plotly_df,
        x="Normalized_Longitude",
        y="Normalized_Latitude",
        z="Time",
        color="cluster",
        color_continuous_scale="solar",
        size_max=10,
    )
    fig.update_layout(scene_aspectmode="auto")
    fig.update_layout(width=800, height=800)

    threeD_checkbox = pn.widgets.Checkbox(name="3d Plot", value=True)

    three_D = pn.Column(
        threeD_checkbox,
        pn.Column(fig, visible=threeD_checkbox.param.value),
    ).servable()

    return three_D
