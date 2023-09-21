import os
import streamlit.components.v1 as components
import streamlit as st

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


def condition_tree(config: dict,
                   return_type: str = 'queryString',
                   tree: dict = None,
                   min_height: int = 400,
                   placeholder: str = '',
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
    tree: dict or None
        Input condition tree
    min_height: int
        Minimum height of the component frame
    placeholder: str
        Text displayed when the condition tree is empty
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

    output_tree, component_value = _component_func(
        config=config,
        return_type=return_type,
        tree=tree,
        key='_' + key if key else None,
        min_height=min_height,
        placeholder=placeholder,
        default=['', '']
    )
    st.session_state[key] = output_tree

    return component_value
