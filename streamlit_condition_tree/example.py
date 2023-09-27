import streamlit as st
from streamlit_condition_tree import condition_tree


config = {
    'fields': {
        'name': {
            'label': 'Name',
            'type': 'text',
        },
        'qty': {
            'label': 'Age',
            'type': 'number',
            'fieldSettings': {
                'min': 0
            },
        },
        'like_tomatoes': {
            'label': 'Likes tomatoes',
            'type': 'boolean',
        }
    }
}

return_val = condition_tree(
    config,
    return_type='sql'
)

st.write(return_val)
