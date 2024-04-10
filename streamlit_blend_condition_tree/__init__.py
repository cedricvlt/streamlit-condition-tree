import os
import streamlit.components.v1 as components
import streamlit as st

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_blend_condition_tree",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_blend_condition_tree", path=build_dir)


type_mapper = {
    'b': 'boolean',
    'i': 'number',
    'u': 'number',
    'f': 'number',
    'c': '',
    'm': '',
    'M': 'datetime',
    'O': 'text',
    'S': 'text',
    'U': 'text',
    'V': ''
}


def config_from_dataframe(dataframe):
    """Return a basic configuration from dataframe columns"""

    fields = {}
    for col_name, col_dtype in zip(dataframe.columns, dataframe.dtypes):
        col_type = 'select' if col_dtype == 'category' else type_mapper[col_dtype.kind]

        if col_type:
            col_config = {
                'label': col_name,
                'type': col_type
            }
            if col_type == 'select':
                categories = dataframe[col_name].cat.categories
                col_config['fieldSettings'] = {
                    'listValues': [{'value': c, 'title': c} for c in categories]
                }
            fields[f'{col_name}'] = col_config

    return {'fields': fields}


def condition_tree(config: dict,
                   return_type: str = 'queryString',
                   tree: dict = None,
                   min_height: int = 400,
                   placeholder: str = '',
                   always_show_buttons: bool = False,
                   key: str = None):
    """Create a new instance of condition_tree.

    Parameters
    ----------
    config: dict
        Configuration defining the value types, supported operators and how
        they are rendered, imported and exported.
    return_type: str or None
        Format in which output should be returned to streamlit.
        Possible values : queryString | mongodb | sql | spel |
        elasticSearch | jsonLogic.
        Default : queryString (compatible with DataFrame.query)
    tree: dict or None
        Input condition tree
        Default: None
    min_height: int
        Minimum height of the component frame
        Default: 400
    placeholder: str
        Text displayed when the condition tree is empty
        Default: empty
    always_show_buttons: false
        If false, buttons (add rule, etc.) will be shown only on hover
        Default: true
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
        Can also be used to access the condition tree through st.session_state.

    Returns
    -------
    dict or object
        The output conditions with the selected format

    """

    if return_type == 'queryString':
        # Add backticks to fields with space in their name
        fields = {}
        for field_name, field_config in config['fields'].items():
            if ' ' in field_name:
                field_name = f'`{field_name}`'
            fields[field_name] = field_config

        config['fields'] = fields

    output_tree, component_value = _component_func(
        config=config,
        return_type=return_type,
        tree=tree,
        key='_' + key if key else None,
        min_height=min_height,
        placeholder=placeholder,
        always_show_buttons=always_show_buttons,
        default=['', '']
    )

    if return_type == 'queryString' and not component_value:
        # Default string that returns all the values in DataFrame.query
        component_value = 'index in index'

    st.session_state[key] = output_tree

    return component_value
