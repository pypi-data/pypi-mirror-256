# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import inspect

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

from surfaces import mathematical_functions_1d
from surfaces.visualize import plotly_surface_new

from surfaces_dashboard.page_setup import page_setup

page_setup()


test_functions_1d = {}
for mathematical_function_2d in mathematical_functions_1d:
    test_functions_1d[mathematical_function_2d.name] = mathematical_function_2d()


class TestFunction1dDetailsPage:
    def __init__(self, test_function) -> None:
        self.test_function = test_function

    def vertical_space(self, pos, n=3):
        for _ in range(n):
            pos.write("")

    def display_objective_function(self, pos, n=2):
        pos.subheader("Objective Function", divider=True)
        pos.code(inspect.getsource(self.test_function.objective_function_dict))
        self.vertical_space(pos, n=n)

    def display_search_space(self, pos, n=2):
        display_search_space = {}
        for para_name, dim_values in self.test_function.search_space().items():
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

    def display_line_plot(self, pos, n=2):
        search_data = self.test_function.load_search_data()
        fig = px.line(search_data, x="x0", y="score")
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
        self.display_formula(col1)

        col1_1, col2_1 = col1.columns([1, 0.6])

        self.display_explanation(col1_1)
        self.display_global_minimum(col2_1)

        self.display_line_plot(col2)

        self.display_objective_function(col1)
        self.display_search_space(col2)
        self.vertical_space(st)


test_function_key = st.sidebar.selectbox(
    "Select test function", list(test_functions_1d.keys())
)


TestFunction1dDetailsPage(test_functions_1d[test_function_key]).run()
