import numpy as np
import streamlit as st
import plotly.express as px

from .base_plot import BasePlot
from .filter import Filter

color_scale = px.colors.sequential.Jet


class ParallelCoordinates(BasePlot):
    def __init__(self, search_data) -> None:
        super().__init__(search_data)

        self.filter = Filter(search_data)

        self.get_data_types()

    def add_parameters_num(self, _st_, key):
        para_names_f = _st_.multiselect(
            label="Parameters:",
            options=self.col_names,
            default=[n for n in self.num_para_names if n != "score"],
            key=key + " add_parameters_num",
        )
        return para_names_f

    def select_color_para_num(self, col1, key):
        if "score" in self.col_names:
            color_index = self.col_names.index("score")
        elif len(self.num_para_names) != 0:
            color_index = self.col_names.index(self.num_para_names[0])
        else:
            color_index = 0

        color_para = col1.selectbox(
            "Color Parameter",
            self.col_names,
            index=color_index,
            key=key + " select_color_para_num",
        )

        return color_para

    @BasePlot.create_title("Parallel Coordinates")
    def run(self):
        col1, col2 = st.columns([1, 2])

        para_names_f = self.add_parameters_num(
            col1, "parallel_coordinates_plotly_widget"
        )

        if "score" not in para_names_f:
            para_names_f_s = para_names_f + ["score"]
        else:
            para_names_f_s = para_names_f

        search_data_f = self.filter.filter_parameter(
            col1, self.search_data, para_names=para_names_f_s
        )
        color_para = self.select_color_para_num(
            col1, "parallel_coordinates_plotly_widget"
        )

        plotly_kwargs = {
            "data_frame": search_data_f,
            "dimensions": para_names_f,
            "color": color_para,
        }

        self.create_plotly_chart(col2, self.parallel_coordinates_plotly, plotly_kwargs)

    @staticmethod
    def parallel_coordinates_plotly(
        data_frame, dimensions, color, plotly_width=1200, plotly_height=600
    ):
        fig = px.parallel_coordinates(
            data_frame, dimensions, color, color_continuous_scale=color_scale
        )
        fig.update_layout(autosize=False, width=plotly_width, height=plotly_height)

        return fig
