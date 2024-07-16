import pandas as pd
import streamlit as st

from streamlit_condition_tree import condition_tree, JsCode

# Initial dataframe
df = pd.DataFrame({
    'First Name': ['Georges', 'Alfred'],
    'Age': [45, 98],
    'Favorite Color': ['Green', 'Red'],
    'Like Tomatoes': [True, False]
})
df = st.data_editor(df)

# Component settings
settings = {
    "defaultSliderWidth": "200px",
    "defaultSelectWidth": "200px",
    "defaultSearchWidth": "100px",
    "defaultMaxRows": 5,
    "valueSourcesInfo": {
        "value": {
            "label": "Value"
        },
        "field": {
            "label": "Field",
            "widget": "field"
        },
        "func": {
            "label": "Function",
            "widget": "func"
        }
    },
    "fieldSources": ["field", "func"],
    "keepInputOnChangeFieldSrc": True,
    "reverseOperatorsForNot": False,
    "canShortMongoQuery": True,
    "maxNesting": 5,
    "canLeaveEmptyGroup": True,
    "shouldCreateEmptyGroup": False,
    "showErrorMessage": True,
    "removeEmptyGroupsOnLoad": False,
    "removeEmptyRulesOnLoad": False,
    "removeIncompleteRulesOnLoad": False,
    "customFieldSelectProps": {
        "showSearch": True
    }
}

# Custom functions definitions
funcs = {
    "lower": {
        "label": "Lowercase",
        "mongoFunc": "$toLower",
        "jsonLogic": "toLowerCase",
        "spelFunc": "${str}.toLowerCase()",
        "jsonLogicCustomOps": {
            "toLowerCase": {}
        },
        "returnType": "text",
        "args": {
            "str": {
                "label": "String",
                "type": "text",
                "valueSources": ["value", "field", "func"]
            }
        }
    },
    "upper": {
        "label": "Uppercase",
        "mongoFunc": "$toUpper",
        "jsonLogic": "toUpperCase",
        "spelFunc": "${str}.toUpperCase()",
        "jsonLogicCustomOps": {
            "toUpperCase": {}
        },
        "returnType": "text",
        "args": {
            "str": {
                "label": "String",
                "type": "text",
                "valueSources": ["value", "field", "func"]
            }
        }
    },
    "linear_regression": {
        "label": "Linear regression",
        "returnType": "number",
        "formatFunc": JsCode("function ({coef, bias, val}, _) { return `(${coef} * ${val} + ${bias})`; }"),
        "sqlFormatFunc": JsCode("function ({coef, bias, val}) { return `(${coef} * ${val} + ${bias})`; }"),
        "spelFormatFunc": JsCode("function ({coef, bias, val}) { return `(${coef} * ${val} + ${bias})`; }"),
        "spelImport": JsCode("""
        function (spel) {
            let coef, val, bias, a;
            if (spel.type === "op-plus") {
                [a, bias] = spel.children;
                if (a.type === "op-multiply") {
                    [coef, val] = a.children;
                    return {coef, val, bias};
                }
            }
        }"""),
        "mongoFormatFunc": JsCode(
            "function ({coef, bias, val}) { return { '$sum': [{ '$multiply': [coef, val] }, bias] }; }"),
        "jsonLogic": JsCode("function ({coef, bias, val}) { return { '+': [{ '*': [coef, val] }, bias] }; }"),
        "jsonLogicImport": JsCode("""
        function (v) {
            const coef = v['+'][0]['*'][0];
            const val = v['+'][0]['*'][1];
            const bias = v['+'][1];
            return [coef, val, bias];
        }"""),
        "renderBrackets": ["", ""],
        "renderSeps": [" * ", " + "],
        "args": {
            "coef": {
                "label": "Coef",
                "type": "number",
                "defaultValue": 1,
                "valueSources": ["value"]
            },
            "val": {
                "label": "Value",
                "type": "number",
                "valueSources": ["value", "field"]
            },
            "bias": {
                "label": "Bias",
                "type": "number",
                "defaultValue": 0,
                "valueSources": ["value"]
            }
        }
    }
}

# Fields configuration
fields = {
    "user": {
        "label": "User",
        "tooltip": "Group of fields",
        "type": "!struct",
        "subfields": {
            "firstName": {
                "label2": "Username",
                "type": "text",
                "fieldSettings": {
                    "validateValue": JsCode("function (val, fieldSettings) { return val.length < 10; }")
                },
                "mainWidgetProps": {
                    "valueLabel": "Name",
                    "valuePlaceholder": "Enter name"
                }
            },
            "login": {
                "type": "text",
                "fieldSettings": {
                    "validateValue": JsCode("""
                    function (val, fieldSettings) {
                        return val.length < 10 && (val === '' || val.match(/^[A-Za-z0-9_-]+$/) !== null);
                    }
                    """)
                },
                "mainWidgetProps": {
                    "valueLabel": "Login",
                    "valuePlaceholder": "Enter login"
                }
            }
        }
    },
    "bio": {
        "label": "Bio",
        "type": "text",
        "preferWidgets": ["textarea"],
        "fieldSettings": {
            "maxLength": 1000
        }
    },
    "results": {
        "label": "Results",
        "type": "!group",
        "subfields": {
            "product": {
                "type": "select",
                "fieldSettings": {
                    "listValues": ["abc", "def", "xyz"]
                },
                "valueSources": ["value"]
            },
            "score": {
                "type": "number",
                "fieldSettings": {
                    "min": 0,
                    "max": 100
                },
                "valueSources": ["value"]
            }
        }
    },
    "cars": {
        "label": "Cars",
        "type": "!group",
        "mode": "array",
        "conjunctions": ["AND", "OR"],
        "showNot": True,
        "operators": [
            "equal", "not_equal", "less", "less_or_equal",
            "greater", "greater_or_equal", "between",
            "not_between",
            "some", "all", "none"
        ],
        "defaultOperator": "some",
        "initialEmptyWhere": True,
        "fieldSettings": {
            "validateValue": JsCode(
                "function (val) { return val < 10 ? null : {error: 'Too many cars, see validateValue()', fixedValue: 9}; }")
        },
        "subfields": {
            "vendor": {
                "type": "select",
                "fieldSettings": {
                    "listValues": ["Ford", "Toyota", "Tesla"]
                },
                "valueSources": ["value"]
            },
            "year": {
                "type": "number",
                "fieldSettings": {
                    "min": 1990,
                    "max": 2021
                },
                "valueSources": ["value"]
            }
        }
    },
    "prox1": {
        "label": "prox",
        "tooltip": "Proximity search",
        "type": "text",
        "operators": ["proximity"]
    },
    "num": {
        "label": "Number",
        "type": "number",
        "preferWidgets": ["number"],
        "fieldSettings": {
            "min": -1,
            "max": 5
        },
        "funcs": ["linear_regression"],
    },
    "slider": {
        "label": "Slider",
        "type": "number",
        "preferWidgets": ["slider", "rangeslider"],
        "valueSources": ["value", "field"],
        "fieldSettings": {
            "min": 0,
            "max": 100,
            "step": 1,
            "marks": {
                '0': "0%",
                '100': "100%"
            },
            "validateValue": JsCode("""
                function (val, fieldSettings) {
                    const ret = val < 50 ? null : {
                        error: {key: "custom:INVALID_SLIDER_VALUE", args: {val}},
                        fixedValue: 49
                    };
                    return ret;
                }
            """)
        },
        # overrides
        "widgets": {
            "slider": {
                "widgetProps": {
                    "valuePlaceholder": "..Slider"
                }
            },
        }
    },
    "date": {
        "label": "Date",
        "type": "date",
        "valueSources": ["value"],
        "fieldSettings": {
            "dateFormat": "DD-MM-YYYY",
        }
    },
    "time": {
        "label": "Time",
        "type": "time",
        "valueSources": ["value"],
        "defaultOperator": "between"
    },
    "datetime": {
        "label": "DateTime",
        "type": "datetime",
        "valueSources": ["value", "func"]
    },
    "datetime2": {
        "label": "DateTime2",
        "type": "datetime",
        "valueSources": ["field"]
    },
    "color": {
        "label": "Color",
        "type": "select",
        "valueSources": ["value"],
        "fieldSettings": {
            "showSearch": True,
            "listValues": [
                {"value": "yellow", "title": "Yellow"},
                {"value": "green", "title": "Green"},
                {"value": "orange", "title": "Orange"}
            ]
        }
    },
    "color2": {
        "label": "Color2",
        "type": "select",
        "fieldSettings": {
            "listValues": {
                "yellow": "Yellow",
                "green": "Green",
                "orange": "Orange",
                "purple": "Purple"
            }
        }
    },
    "multicolor": {
        "label": "Colors",
        "type": "multiselect",
        "fieldSettings": {
            "showSearch": True,
            "listValues": {
                "yellow": "Yellow",
                "green": "Green",
                "orange": "Orange"
            },
            "allowCustomValues": True
        }
    },
    "selecttree": {
        "label": "Color (tree)",
        "type": "treeselect",
        "fieldSettings": {
            "treeExpandAll": True,
            "treeValues": [
                {"value": "1", "title": "Warm colors"},
                {"value": "2", "title": "Red", "parent": "1"},
                {"value": "3", "title": "Orange", "parent": "1"},
                {"value": "4", "title": "Cool colors"},
                {"value": "5", "title": "Green", "parent": "4"},
                {"value": "6", "title": "Blue", "parent": "4"},
                {"value": "7", "title": "Sub blue", "parent": "6"},
                {"value": "8", "title": "Sub sub blue and a long text", "parent": "7"}
            ]
        }
    },
    "multiselecttree": {
        "label": "Colors (tree)",
        "type": "treemultiselect",
        "fieldSettings": {
            "treeExpandAll": True,
            "treeValues": [
                {"value": "1", "title": "Warm colors", "children": [
                    {"value": "2", "title": "Red"},
                    {"value": "3", "title": "Orange"}
                ]},
                {"value": "4", "title": "Cool colors", "children": [
                    {"value": "5", "title": "Green"},
                    {"value": "6", "title": "Blue", "children": [
                        {"value": "7", "title": "Sub blue", "children": [
                            {"value": "8", "title": "Sub sub blue and a long text"}
                        ]}
                    ]}
                ]}
            ]
        }
    },
    "stock": {
        "label": "In stock",
        "type": "boolean",
        "defaultValue": True,
        "mainWidgetProps": {
            "labelYes": "+",
            "labelNo": "-"
        }
    }
}

config = {
    'settings': settings,
    'funcs': funcs,
    'fields': fields,
}

# Initial tree
tree = {
    'type': 'group',
    'properties': {
        'conjunction': 'OR'
    },
    'children': [
        {
            'type': 'rule',
            'properties': {
                'fieldSrc': 'field',
                'field': 'stock',
                'operator': 'equal',
                'value': [False],
                'valueSrc': ['value'],
                'valueError': [None],
                'valueType': ['boolean']
            }
        },
        {
            'type': 'rule',
            'properties': {
                'fieldSrc': 'field',
                'field': 'slider',
                'operator': 'equal',
                'value': [35],
                'valueSrc': ['value'],
                'valueError': [None],
                'valueType': ['number']
            }
        },
        {
            'type': 'rule_group',
            'properties': {
                'conjunction': 'AND',
                'not': False,
                'field': 'results',
                'fieldSrc': 'field'
            },
            'children': [
                {
                    'type': 'rule',
                    'properties': {
                        'fieldSrc': 'field',
                        'field': 'results.product',
                        'operator': 'select_equals',
                        'value': ['abc'],
                        'valueSrc': ['value'],
                        'valueError': [None],
                        'valueType': ['select']
                    }
                },
                {
                    'type': 'rule',
                    'properties': {
                        'fieldSrc': 'field',
                        'field': 'results.score',
                        'operator': 'greater',
                        'value': [8],
                        'valueSrc': ['value'],
                        'valueError': [None],
                        'valueType': ['number']
                    }
                }
            ]
        },
        {
            'type': 'rule',
            'properties': {
                'fieldSrc': 'field',
                'field': 'num',
                'operator': 'between',
                'value': [2, 4],
                'valueSrc': ['value', None],
                'valueError': [None, None, None],
                'valueType': ['number', 'number']
            }
        },
        {
            'type': 'rule',
            'properties': {
                'fieldSrc': 'func',
                'field': {
                    'func': 'lower',
                    'args': {
                        'str': {
                            'valueSrc': 'value',
                            'value': 'aaa'
                        }
                    }
                },
                'operator': 'equal',
                'value': [
                    {
                        'func': 'lower',
                        'args': {
                            'str': {
                                'valueSrc': 'value',
                                'value': 'AAA'
                            }
                        }
                    }
                ],
                'valueSrc': ['func'],
                'valueError': [None],
                'valueType': ['text']
            }
        },
        {
            'type': 'rule',
            'properties': {
                'fieldSrc': 'field',
                'field': 'user.login',
                'operator': 'equal',
                'value': ['denis'],
                'valueSrc': ['value'],
                'valueError': [None],
                'valueType': ['text']
            }
        },
        {
            'type': 'rule',
            'properties': {
                'fieldSrc': 'field',
                'field': 'user.login',
                'operator': 'equal',
                'value': ['user.firstName'],
                'valueSrc': ['field'],
                'valueError': [None],
                'valueType': ['text']
            }
        },
        {
            'type': 'rule_group',
            'properties': {
                'mode': 'array',
                'operator': 'all',
                'fieldSrc': 'field',
                'valueType': [],
                'value': [],
                'valueSrc': [],
                'not': False,
                'conjunction': 'AND',
                'valueError': [],
                'field': 'cars'
            },
            'children': [
                {
                    'type': 'rule',
                    'properties': {
                        'fieldSrc': 'field',
                        'field': 'cars.year',
                        'operator': 'equal',
                        'value': [2021],
                        'valueSrc': ['value'],
                        'valueError': [None],
                        'valueType': ['number']
                    }
                }
            ]
        },
        {
            'type': 'group',
            'properties': {
                'conjunction': 'AND',
                'not': False
            },
            'children': [
                {
                    'type': 'rule',
                    'properties': {
                        'fieldSrc': 'field',
                        'field': 'slider',
                        'operator': 'equal',
                        'value': [40],
                        'valueSrc': ['value'],
                        'valueError': [None],
                        'valueType': ['number']
                    }
                },
                {
                    'type': 'group',
                    'properties': {
                        'conjunction': 'OR',
                        'not': True
                    },
                    'children': [
                        {
                            'type': 'rule',
                            'properties': {
                                'fieldSrc': 'field',
                                'field': 'multiselecttree',
                                'operator': 'multiselect_not_equals',
                                'value': [['2', '3']],
                                'valueSrc': ['value'],
                                'valueError': [None],
                                'valueType': ['treemultiselect']
                            }
                        },
                        {
                            'type': 'rule',
                            'properties': {
                                'fieldSrc': 'field',
                                'field': 'bio',
                                'operator': 'like',
                                'value': ['Long text'],
                                'valueSrc': ['value'],
                                'valueError': [None],
                                'valueType': ['text']
                            }
                        }
                    ]
                }
            ]
        }
    ]
}

# Condition tree
query_string = condition_tree(
    config,
    # return_type="sql",
    always_show_buttons=True,
    tree=tree,
    # key="my_tree"
)

st.write(query_string)
