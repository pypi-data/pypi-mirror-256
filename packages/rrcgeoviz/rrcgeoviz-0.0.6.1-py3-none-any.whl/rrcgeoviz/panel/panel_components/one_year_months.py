from matplotlib import pyplot as plt
import panel as pn
import seaborn as sns


def one_year_months_plot(args):
    df = args.data.copy()
    df["Year"] = df[args.options["time_column"]].dt.year
    df["Month"] = df[args.options["time_column"]].dt.month

    def update_year_months_plot(value):
        desired_year = value
        filtered_df = df[df["Year"] == desired_year]
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.set_theme(style="whitegrid")
        month_order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        sns.countplot(
            data=filtered_df, x="Month", order=month_order, palette="colorblind"
        )
        plt.xlabel("Month")
        plt.ylabel("Frequency")
        plt.title(f"Incidents by Month for Year {desired_year}")

        return plt.gcf()

    one_year_months_checkbox = pn.widgets.Checkbox(name="One Month Plot", value=True)
    desired_year = pn.widgets.IntInput(
        name="Enter Year",
        start=df["Year"].min(),
        end=df["Year"].max(),
        value=int(df["Year"].median()),
        step=1,
    )
    year_months_plot = pn.bind(update_year_months_plot, value=desired_year)

    one_year_months = pn.Column(
        one_year_months_checkbox,
        pn.Column(
            desired_year,
            pn.panel(year_months_plot),
            visible=one_year_months_checkbox.param.value,
        ),
    ).servable()

    return one_year_months
