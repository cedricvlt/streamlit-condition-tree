
Based on [react-awesome-query-builder](https://github.com/ukrbublik/react-awesome-query-builder)

Check out [live demo](https://app-condition-tree-demo-dkclrsnqxpcgzkjzlv3mqu.streamlit.app/) !

<img src="preview.jpg" width="500" alt="preview">


## Install

`pip install streamlit-condition-tree`


## Features
- Highly configurable
- Fields can be of type:
  - simple (string, number, bool, date/time/datetime, list)
  - structs (will be displayed in selectbox as tree)
- Comparison operators can be:
  - binary (== != < > ..)
  - unary (is empty, is null)
  - 'between' (for numbers, dates, times)
  - complex operators like 'proximity'
- RHS can be:
  - values
  - another fields (of same type)
  - functions (arguments also can be values/fields/funcs)
- LHS can be field or function
- Reordering (drag-n-drop) support for rules and groups of rules
- Export to MongoDb, SQL, JsonLogic, SpEL or ElasticSearch

## Basic usage

```python
import streamlit as st
from streamlit_condition_tree import condition_tree


config = {
    'fields': {
        'name': {
            'label': 'Name',
            'type': 'text',
        },
        'qty': {
            'label': "Age",
            'type': "number",
            'fieldSettings': {
                'min': 0
            },
            'preferWidgets': ['number']
        },
        'like_tomatoes': {
            'label': 'Likes tomatoes',
            'type': "boolean",
            'operators': ["equal"],
        }
    }
}

return_val = condition_tree(
    config,
    return_type='sql'
)

st.write(return_val)
```

## API

### Parameters

```python
def condition_tree(
    config: Dict
    return_type: str
    tree: Dict
    min_height: int
    placeholder: str
    key: str
)
```

- **config**: Python dictionary that resembles the JSON counterpart of
  the React component [config](https://github.com/ukrbublik/react-awesome-query-builder/blob/master/CONFIG.adoc).  
*Note*: Javascript functions (ex: validators) are not yet supported.


- **return_type**: Format of the returned value :
  - queryString
  - mongodb
  - sql
  - spel
  - elasticSearch
  - jsonLogic


- **tree**: Input condition tree (see section below)


- **min_height**: Minimum height of the component frame


- **placeholder**: Text displayed when the condition tree is empty


- **key**: Fixed identity if you want to change its arguments over time and not have it be re-created.  
Can also be used to access the generated condition tree (see section below).


### Export & import a condition tree

When a key is defined for the component, the condition tree generated is accessible through `st.session_state[key]` as a dictionary.  
It can be loaded as an input tree through the `tree` parameter.
