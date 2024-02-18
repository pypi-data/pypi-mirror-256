import plotly.express as px

from surfaces_dashboard.page_setup import page_setup

page_setup()


color_scale = px.colors.sequential.Jet


def overview_1d(df):
    return px.line(df, x="x0", y="score")


def overview_2d(df):
    return px.scatter(
        df,
        x="x0",
        y="x1",
        color="score",
        color_continuous_scale=color_scale,
    )


def overview_3d(df):
    return px.scatter_3d(
        df,
        x="x0",
        y="x1",
        z="x2",
        color="score",
        color_continuous_scale=color_scale,
    )


def overview_ml(df):
    dimensions = list(df.columns)
    dimensions.remove("score")

    return px.parallel_coordinates(
        df,
        dimensions=dimensions,
        color="score",
        color_continuous_scale=color_scale,
    )
