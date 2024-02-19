import panel as pn
from io import BytesIO
from ydata_profiling import ProfileReport


def gen_profile_report(args):
    df = args.data

    def generate_profile_report():
        loading_spinner.value = True
        loading_spinner.visible = True
        # Generate a Pandas Profiling report
        profile_report = ProfileReport(df)
        html_content = profile_report.to_html().encode()
        html_bytesio = BytesIO(html_content)
        loading_spinner.visible = False
        loading_spinner.value = False
        return html_bytesio

    download_button = pn.widgets.FileDownload(
        label="Download Report",
        callback=generate_profile_report,
        filename="Pandas_Profiling.html",
    )
    loading_spinner = pn.indicators.LoadingSpinner(
        value=False, visible=False, size=50, color="primary", bgcolor="dark"
    )

    return pn.Column(download_button, loading_spinner)
