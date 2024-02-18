import numpy as np
import streamlit as st
import plotly.express as px

from .base_plot import BasePlot
from .filter import Filter

color_scale = px.colors.sequential.Jet


class ScatterMatrix(BasePlot):
    def __init__(self, search_data) -> None:
        super().__init__(search_data)

        self.filter = Filter(search_data)

        self.get_data_types()

    def select_color_para_cat(self, col1):
        # print("categorical", categorical)
        if "score" in self.col_names:
            color_index = self.col_names.index("score")
        elif len(self.cat_para_names) != 0:
            color_index = self.col_names.index(self.cat_para_names[0])
        else:
            color_index = 0

        color_para = col1.selectbox(
            "Color Parameter",
            self.col_names,
            index=color_index,
        )

        return color_para

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

    def add_parameters_num(self, _st_, key):
        para_names_f = _st_.multiselect(
            label="Parameters:",
            options=self.col_names,
            default=[n for n in self.num_para_names if n != "score"],
            key=key + " add_parameters_num",
        )
        return para_names_f

    @BasePlot.create_title("Scatter Matrix")
    def run(self):
        col1, col2 = st.columns([1, 2])

        para_names_f = self.add_parameters_num(col1, "scatter_matrix_plotly_widget")
        color_para = self.select_color_para_cat(col1)

        plotly_kwargs = {
            "search_data": self.search_data,
            "dimensions": para_names_f,
            "color": color_para,
        }
        self.create_plotly_chart(col2, self.scatter_matrix_plotly, plotly_kwargs)

    @staticmethod
    def scatter_matrix_plotly(
        search_data, dimensions, color, plotly_width=1100, plotly_height=600
    ):
        fig = px.scatter_matrix(
            search_data,
            dimensions=dimensions,
            color=color,
            color_continuous_scale=color_scale,
            # symbol="species",
        )  # remove underscore
        fig.update_traces(diagonal_visible=False, showupperhalf=False)
        fig.update_layout(autosize=False, width=plotly_width, height=plotly_height)

        return fig
