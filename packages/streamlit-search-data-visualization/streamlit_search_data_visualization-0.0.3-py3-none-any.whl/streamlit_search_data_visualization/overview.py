import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from .base_plot import BasePlot
from .filter import Filter

color_scale = px.colors.sequential.Jet


def to_int(number):
    if number.is_integer():
        return int(number)
    else:
        return number


class Overview(BasePlot):
    def __init__(self, search_data) -> None:
        super().__init__(search_data)

        self.filter = Filter(search_data)

        self.get_data_types()

    @staticmethod
    def statistics(search_data):
        search_data_rel = search_data.drop(
            ["eval_time", "iter_time"], axis=1, errors="ignore"
        )

        search_data_num = search_data_rel.select_dtypes(include=[np.number])

        statistics_d = {}

        for col in search_data_num.columns:
            col_np = search_data_num[col].values
            counts_ = np.unique(col_np).shape[0]
            min_ = float(np.min(col_np))
            max_ = float(np.max(col_np))
            mean_ = float(col_np.mean())
            median_ = float(np.median(col_np))

            statistics_d[col] = [
                counts_,
                to_int(min_),
                to_int(max_),
                to_int(mean_),
                to_int(median_),
            ]

        columns = ["uniques", "min", "max", "mean", "median"]

        statistics_df = pd.DataFrame.from_dict(
            statistics_d, orient="index", columns=columns
        )
        return statistics_df

    @BasePlot.create_title("Overview")
    def run(self):
        st.subheader("Search data samples")
        sd_sample = self.search_data.sample(n=10, random_state=1)

        st.table(sd_sample)

        col1, col2 = st.columns([1, 1])

        statistics_df = self.statistics(self.search_data)

        col1.subheader("Search data statistics")
        col1.table(statistics_df)

        plotly_kwargs = {
            "data_frame": self.search_data,
            "x": "score",
            "hover_data": self.col_names,
        }
        self.create_plotly_chart(col2, self.plot_hist, plotly_kwargs)

    @staticmethod
    def plot_hist(data_frame, x, hover_data, plotly_width=1100, plotly_height=600):
        return px.histogram(data_frame, x, hover_data)
