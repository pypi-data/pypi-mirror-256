from matplotlib import pyplot as plt
import panel as pn
import seaborn as sns


def all_months_plot(args):
    df = args.data.copy()
    df["Month"] = df[args.options["time_column"]].dt.month
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.set(style="whitegrid")
    sns.countplot(data=df, x="Month", palette="colorblind")
    plt.xlabel("Month")
    plt.ylabel("Frequency")
    plt.title("All Incidents by Month")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    sns.set_theme(font_scale=0.4)
    sns.countplot(data=df, x="Month", palette="colorblind")
    plt.title("All Incidents by Month", fontsize=12)

    months_app = pn.pane.Matplotlib(plt.gcf())
    months_checkbox = pn.widgets.Checkbox(name="All Months Plot", value=True)
    all_months = pn.Column(
        months_checkbox,
        pn.Column(
            months_app,
            visible=months_checkbox.param.value,
        ),
    )
    # Show the Panel app
    return all_months.servable()
