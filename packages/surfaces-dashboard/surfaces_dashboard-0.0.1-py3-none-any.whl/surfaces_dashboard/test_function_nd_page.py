# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import inspect

import streamlit as st
import numpy as np
import pandas as pd

from surfaces import mathematical_functions_nd

from surfaces.visualize import plotly_surface_new
from streamlit_search_data_visualization import (
    Scatter2D,
    ParallelCoordinates,
)

from surfaces_dashboard.overview_plots import (
    overview_1d,
    overview_2d,
    overview_3d,
    overview_ml,
)

from surfaces_dashboard.page_setup import page_setup

page_setup()


widgets_d = {
    "2D Scatter plot": Scatter2D,
    "Parallel Coordinates": ParallelCoordinates,
}

test_functions_nd = {}
for mathematical_function_nd in mathematical_functions_nd:
    test_functions_nd[mathematical_function_nd.name] = mathematical_function_nd


class TestFunctionNdDetailsPage:
    def __init__(self, test_function) -> None:
        self.n_dim = st.sidebar.selectbox(
            "N dimensions:", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        )
        self.test_function = test_function(self.n_dim)
        self.search_data = self.test_function.search_data()

    def vertical_space(self, pos, n=3):
        for _ in range(n):
            pos.write("")

    def display_objective_function(self, pos, n=2):
        pos.subheader("Objective Function", divider=True)
        pos.code(inspect.getsource(self.test_function.objective_function_dict))
        self.vertical_space(pos, n=n)

    def display_search_space(self, pos, n=2):
        display_search_space = {}
        for para_name, dim_values in self.test_function.search_space.items():
            min_ = float(np.min(dim_values))
            max_ = float(np.max(dim_values))

            para_type = "Numeric"

            display_search_space[para_name] = [para_type, min_, max_]

        display_search_space_pd = pd.DataFrame.from_dict(
            display_search_space, orient="index", columns=["Type", "Minimum", "Maximum"]
        ).transpose()
        pos.subheader("Search Space", divider=True)
        pos.table(display_search_space_pd)
        self.vertical_space(pos, n=n)

    def display_overview_plot(self, pos, n=2):
        if self.n_dim == 1:
            fig = overview_1d(self.search_data)
        elif self.n_dim == 2:
            fig = overview_2d(self.search_data)
        elif self.n_dim == 3:
            fig = overview_3d(self.search_data)
        else:
            fig = overview_ml(self.search_data)

        pos.plotly_chart(fig, use_container_width=True)
        self.vertical_space(pos, n=n)

    def display_explanation(self, pos, n=2):
        explanation = self.test_function.explanation
        pos.write(explanation)
        self.vertical_space(pos, n=n)

    def display_formula(self, pos, n=2):
        pos.subheader("Formula", divider=True)
        pos.latex(self.test_function.formula)
        self.vertical_space(pos, n=n)

    def display_global_minimum(self, pos, n=2):
        pos.subheader("Global minimum", divider=True)
        pos.latex(self.test_function.global_minimum)
        self.vertical_space(pos, n=n)

    def run(self):
        st.title(self.test_function.name)
        st.divider()
        self.vertical_space(st.sidebar)

        col1, col2 = st.columns([1, 1])

        self.vertical_space(col1)

        widget_slct = st.sidebar.selectbox(
            label="Select Widget", options=list(widgets_d.keys())
        )

        self.display_formula(col1)

        col1_1, col2_1 = col1.columns([1, 0.6])

        self.display_explanation(col1_1)
        self.display_global_minimum(col2_1)

        self.display_overview_plot(col2)

        self.display_objective_function(col1)
        self.display_search_space(st)
        self.vertical_space(st)

        # widgets_d[widget_slct](self.search_data).run()


test_function_key = st.sidebar.selectbox(
    "Select test function", list(test_functions_nd.keys())
)


TestFunctionNdDetailsPage(test_functions_nd[test_function_key]).run()
