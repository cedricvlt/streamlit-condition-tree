import streamlit as st
import pandas as pd

from streamlit_blend_condition_tree import condition_tree, config_from_dataframe

# Initial dataframe
df = pd.DataFrame({
    'First Name': ['Georges', 'Alfred'],
    'Age': [45, 98],
    'Favorite Color': ['Green', 'Red'],
    'Like Tomatoes': [True, False]
})

# Basic field configuration from dataframe
config = config_from_dataframe(df)

# Condition tree
query_string = condition_tree(
    config,
    always_show_buttons=True
)

# Filtered dataframe
df = df.query(query_string)