import numpy as np
import pandas as pd
import streamlit as st
from streamlit_condition_tree import condition_tree, config_from_dataframe

df = pd.read_csv(
    'https://media.githubusercontent.com/media/datablist/sample-csv-files/main/files/people/people-100.csv',
    index_col=0,
    parse_dates=['Date of birth'],
    date_format='%Y-%m-%d')
df['Age'] = ((pd.Timestamp.today() - df['Date of birth']).dt.days / 365).astype(int)
df['Sex'] = pd.Categorical(df['Sex'])
df['Likes tomatoes'] = np.random.randint(2, size=df.shape[0]).astype(bool)

st.dataframe(df)

config = config_from_dataframe(df)

return_val = condition_tree(
    config,
)

st.code(return_val)

df = df.query(return_val)
st.dataframe(df)
