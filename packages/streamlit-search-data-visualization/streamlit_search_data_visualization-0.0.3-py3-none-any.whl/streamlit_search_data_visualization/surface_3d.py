import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from copy import copy

from .base_plot import BasePlot

color_scale = px.colors.sequential.Jet


class Surface3D(BasePlot):
    def __init__(self, search_data, search_space) -> None:
        super().__init__(search_data)
        self.search_space = search_space

        if len(search_data.columns) != 3:
            error = "search_data must be 3 dimensional"
            raise Exception(error)

        self.get_data_types()

    @BasePlot.create_title("2D Scatter Plot")
    def run(
        self,
        streamlit_position,
    ):
        plotly_kwargs = {
            "search_data": self.search_data,
            "search_space": self.search_space,
        }

        self.create_plotly_chart(streamlit_position, self.plotly_surface, plotly_kwargs)

    @staticmethod
    def plotly_surface(
        search_data,
        search_space,
        title="Surface 3D plot",
        width=900,
        height=900,
        contour=False,
    ):
        col_names = list(search_data.columns)
        col_names_no_score = copy(col_names)
        col_names_no_score.remove("score")

        para1 = col_names_no_score[0]
        para2 = col_names_no_score[1]

        x_size = len(search_space[para1])
        y_size = len(search_space[para2])

        xi = np.reshape(search_data[para1].values, (x_size, y_size))
        yi = np.reshape(search_data[para2].values, (x_size, y_size))
        zi = np.reshape(search_data["score"].values, (x_size, y_size))

        fig = go.Figure(
            data=go.Surface(
                z=zi,
                x=xi,
                y=yi,
                colorscale=color_scale,
            ),
        )

        # add a countour plot
        if contour:
            fig.update_traces(
                contours_z=dict(
                    show=True,
                    usecolormap=True,
                    highlightcolor="limegreen",
                    project_z=True,
                )
            )

        # annotate the plot
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title=para1,
                yaxis_title=para2,
                zaxis_title="Metric",
            ),
            width=width,
            height=height,
        )
        return fig
