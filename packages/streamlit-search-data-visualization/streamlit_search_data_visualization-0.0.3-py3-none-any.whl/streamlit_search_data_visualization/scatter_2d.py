import numpy as np
import streamlit as st
import plotly.express as px

from .base_plot import BasePlot
from .filter import Filter

color_scale = px.colors.sequential.Jet


class Scatter2D(BasePlot):
    def __init__(self, search_data) -> None:
        super().__init__(search_data)

        self.filter = Filter(search_data)

        self.get_data_types()

    @BasePlot.create_title("2D Scatter Plot")
    def run(self):
        col1, col2 = st.columns([1, 2])

        idx_1st_para, idx_2nd_para = self.get_n_idx_default_para(2)

        select_para_d_1 = {
            "parameter_l": self.col_names,
            "name": "First parameter",
            "_st_": col1,
            "index": idx_1st_para,
        }
        select_para_d_2 = {
            "parameter_l": self.col_names,
            "name": "Second parameter",
            "_st_": col1,
            "index": idx_2nd_para,
        }
        select_para_d_3 = {
            "parameter_l": self.col_names,
            "name": "Color Parameter",
            "_st_": col1,
            "index": self.score_idx,
        }

        scatter2_para1 = self.select_parameter(**select_para_d_1)
        scatter2_para2 = self.select_parameter(**select_para_d_2)
        color_para = self.select_parameter(**select_para_d_3)

        col1.divider()

        search_data_f = self.filter.filter_parameter(col1, self.search_data)
        plotly_kwargs = {
            "data_frame": search_data_f,
            "x": scatter2_para1,
            "y": scatter2_para2,
            "color": color_para,
        }

        self.create_plotly_chart(col2, self.plotly_scatter, plotly_kwargs)

    @staticmethod
    def plotly_scatter(data_frame, x, y, color, plotly_width=1200, plotly_height=600):
        fig = px.scatter(data_frame, x, y, color, color_continuous_scale=color_scale)
        fig.update_layout(autosize=False, width=plotly_width, height=plotly_height)

        return fig
