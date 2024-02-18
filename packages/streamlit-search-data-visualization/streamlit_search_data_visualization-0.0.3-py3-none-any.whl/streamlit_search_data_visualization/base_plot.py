import numpy as np
import pandas as pd
import streamlit as st


class BasePlot:
    def __init__(self, search_data) -> None:
        self.search_data = search_data

        self.col_names = list(search_data.columns)
        self.para_names = [n for n in self.col_names if n != "score"]

    @staticmethod
    def select_parameter(parameter_l, name, _st_, index=0):
        _name_ = "select_parameter"
        return _st_.selectbox(
            name,
            parameter_l,
            index=index,
            # key=random_key(_name_),
        )

    @staticmethod
    def select_column(search_data, _st_):
        _name_ = "select_column"

        para_names = list(search_data.columns)
        para_names_f = _st_.multiselect(
            label="Parameters:",
            options=para_names,
            # key=random_key(_name_),
        )
        return para_names_f

    @staticmethod
    def create_plotly_chart(_st_, plot_func, plot_kwargs):
        fig = plot_func(**plot_kwargs)
        _st_.plotly_chart(fig)

    def get_data_types(self):
        data_types = {}
        cat_para_names = []
        num_para_names = []

        for para_name in self.col_names:
            values = self.search_data[para_name].values

            try:
                values * values
                values - values
            except:
                data_types[para_name] = "categorical"
                cat_para_names.append(para_name)

            else:
                data_types[para_name] = "numeric"
                num_para_names.append(para_name)

        self.data_types = data_types
        self.cat_para_names = cat_para_names
        self.num_para_names = num_para_names

    def _n_uniques_d(self):
        n_uniques_d = {}
        for para_name in self.col_names:
            n_uniques_d[para_name] = np.unique(
                self.search_data[para_name].values
            ).shape[0]
        return n_uniques_d

    def _get_n_default_para(self):
        n_uniques_d = self._n_uniques_d()
        n_uniques_d_sorted = dict(sorted(n_uniques_d.items(), key=lambda item: item[1]))
        return list(n_uniques_d_sorted.keys())

    def get_n_idx_default_para(self, n, score=False):
        n_uniques_para_names_sorted = self._get_n_default_para()
        n_idx_default_para = [
            self.col_names.index(para_name) for para_name in n_uniques_para_names_sorted
        ]
        if not score:
            n_idx_default_para.remove(self.score_idx)
        return n_idx_default_para[-n:]

    @property
    def score_idx(self):
        return self.col_names.index("score")

    @staticmethod
    def create_title(title):
        def decorator(widget):
            def wrapper(*args, **kwargs):
                st.title(title)
                st.divider()
                st.text("")
                result = widget(*args, **kwargs)
                return result

            wrapper.__name__ = widget.__name__

            return wrapper

        return decorator
