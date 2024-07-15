import os

import streamlit as st
import streamlit.components.v1 as components
from streamlit.components.v1.custom_component import MarshallComponentException

_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_condition_tree",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_condition_tree", path=build_dir)

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


# stole from https://github.com/andfanilo/streamlit-echarts/blob/master/streamlit_echarts/frontend/src/utils.js
# Thanks andfanilo
class JsCode:
    def __init__(self, js_code: str):
        """Wrapper around a js function to be injected on gridOptions.
        code is not checked at all.
        set allow_unsafe_jscode=True on AgGrid call to use it.
        Code is rebuilt on client using new Function Syntax (https://javascript.info/new-function)

        Args:
            js_code (str): javascript function code as str
        """
        import re
        match_js_comment_expression = r"\/\*[\s\S]*?\*\/|([^\\:]|^)\/\/.*$"
        js_code = re.sub(re.compile(match_js_comment_expression, re.MULTILINE), r"\1", js_code)

        match_js_spaces = r"\s+(?=(?:[^\'\"]*[\'\"][^\'\"]*[\'\"])*[^\'\"]*$)"
        one_line_jscode = re.sub(match_js_spaces, " ", js_code, flags=re.MULTILINE)

        js_placeholder = "::JSCODE::"
        one_line_jscode = re.sub(r"\s+|\r\s*|\n+", " ", js_code, flags=re.MULTILINE)

        self.js_code = f"{js_placeholder}{one_line_jscode}{js_placeholder}"


# Stole from https://github.com/PablocFonseca/streamlit-aggrid/blob/main/st_aggrid/shared.py
# Thanks PablocFonseca
def walk_config(config, func):
    """Recursively walk config applying func at each leaf node

    Args:
        config (dict): config dictionary
        func (callable): a function to apply at leaf nodes
    """
    from collections.abc import Mapping

    if isinstance(config, (Mapping, list)):
        for i, k in enumerate(config):

            if isinstance(config[k], Mapping):
                walk_config(config[k], func)
            elif isinstance(config[k], list):
                for j in config[k]:
                    walk_config(j, func)
            else:
                config[k] = func(config[k])


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
                   key: str = None,
                   allow_unsafe_jscode: bool = False, ):
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
    allow_unsafe_jscode: bool
        Allows jsCode to be injected in gridOptions.
        Defaults to False.

    Returns
    -------
    dict or object
        The output conditions with the selected format

    """

    if return_type == 'queryString':
        # Add backticks to fields having spaces in their name
        fields = {}
        for field_name, field_config in config['fields'].items():
            if ' ' in field_name:
                field_name = f'`{field_name}`'
            fields[field_name] = field_config

        config['fields'] = fields

    if allow_unsafe_jscode:
        walk_config(config, lambda v: v.js_code if isinstance(v, JsCode) else v)

    try:
        output_tree, component_value = _component_func(
            config=config,
            return_type=return_type,
            tree=tree,
            key='_' + key if key else None,
            min_height=min_height,
            placeholder=placeholder,
            always_show_buttons=always_show_buttons,
            default=['', ''],
            allow_unsafe_jscode=allow_unsafe_jscode,
        )

    except MarshallComponentException as e:
        # Uses a more complete error message.
        args = list(e.args)
        args[0] += ". If you're using custom JsCode objects on config, ensure that allow_unsafe_jscode is True."
        e = MarshallComponentException(*args)
        raise (e)

    if return_type == 'queryString' and not component_value:
        # Default string that applies no filter in DataFrame.query
        component_value = 'index in index'

    st.session_state[key] = output_tree

    return component_value
