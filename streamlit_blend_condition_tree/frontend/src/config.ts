import {AntdConfig, Config} from "@react-awesome-query-builder/antd";

const defaultConfig: Config = {
    ...(AntdConfig),
    conjunctions: {
        AND: {
            ...AntdConfig.conjunctions.AND,
            formatConj: (children, _conj, not) =>
                (not ? '~' : '') + '(' + children.join(' & ') + ')',
        },
        OR: {
            ...AntdConfig.conjunctions.OR,
            formatConj: (children, _conj, not) =>
                (not ? '~' : '') + '(' + children.join(' | ') + ')',
        }
    },
    operators: {
        ...AntdConfig.operators,
        equal: {
            ...AntdConfig.operators.equal,
            formatOp: (field, op, value, valueSrcs, valueTypes, opDef, operatorOptions, isForDisplay, fieldDef) => {
                if (valueTypes == "boolean") {
                    return value == 'true' ? field : `~${field}`
                }
                return `${field} == ${value}`;
            }
        },
        not_equal: {
            ...AntdConfig.operators.not_equal,
            formatOp: (field, op, value, valueSrcs, valueTypes, opDef, operatorOptions, isForDisplay, fieldDef) => {
                if (valueTypes == "boolean") {
                    return value == 'true' ? `~${field}` : field
                }
                return `${field} != ${value}`;
            }
        },
        between: {
            ...AntdConfig.operators.between,
            formatOp: (field, op, values, valueSrcs, valueTypes, opDef, operatorOptions, isForDisplay) =>
                typeof values !== 'string' ? `(${values.first()} <= ${field} <= ${values.get(1)})` : ''
        },
        not_between: {
            ...AntdConfig.operators.not_between,
            formatOp: (field, op, values, valueSrcs, valueTypes, opDef, operatorOptions, isForDisplay) =>
                typeof values !== 'string' ? `~(${values.first()} <= ${field} <= ${values.get(1)})` : ''
        },
        is_null: {
            ...AntdConfig.operators.is_null,
            formatOp: (field, op, value, valueSrc, valueType, opDef, operatorOptions, isForDisplay) =>
                `${field}.isnull()`
        },
        is_not_null: {
            ...AntdConfig.operators.is_not_null,
            formatOp: (field, op, value, valueSrc, valueType, opDef, operatorOptions, isForDisplay) =>
                `~${field}.isnull()`
        },
        like: {
            ...AntdConfig.operators.like,
            formatOp: (field, op, value, valueSrc, valueType, opDef, operatorOptions, isForDisplay) =>
                `${field}.str.contains(${value}, regex=True)`
        },
        not_like: {
            ...AntdConfig.operators.not_like,
            formatOp: (field, op, value, valueSrc, valueType, opDef, operatorOptions, isForDisplay) =>
                `~${field}.str.contains(${value}, regex=True)`
        },
        starts_with: {
            ...AntdConfig.operators.starts_with,
            formatOp: (field, op, value, valueSrc, valueType, opDef, operatorOptions, isForDisplay) =>
                `${field}.str.startswith(${value})`
        },
        ends_with: {
            ...AntdConfig.operators.ends_with,
            formatOp: (field, op, value, valueSrc, valueType, opDef, operatorOptions, isForDisplay) =>
                `${field}.str.endswith(${value})`
        },
        is_empty: {
            ...AntdConfig.operators.is_empty,
            formatOp: (field, op, value, valueSrc, valueType, opDef, operatorOptions, isForDisplay) =>
                `${field} == ""`
        },
        is_not_empty: {
            ...AntdConfig.operators.is_not_empty,
            formatOp: (field, op, value, valueSrc, valueType, opDef, operatorOptions, isForDisplay) =>
                `${field} != ""`
        },
        select_any_in: {
            ...AntdConfig.operators.select_any_in,
            formatOp: (field, op, values, valueSrc, valueType, opDef, operatorOptions, isForDisplay) => {
                if (valueSrc == "value" && Array.isArray(values))
                    return `${field}.isin([${values.join(", ")}])`;
                else
                    return `${field}.isin(${values})`;
            },
        },
        select_not_any_in: {
            ...AntdConfig.operators.select_not_any_in,
            formatOp: (field, op, values, valueSrc, valueType, opDef, operatorOptions, isForDisplay) => {
                if (valueSrc == "value" && Array.isArray(values))
                    return `~${field}.isin([${values.join(", ")}])`;
                else
                    return `~${field}.isin(${values})`;
            },
        },
        multiselect_contains: {
            ...AntdConfig.operators.multiselect_contains,
            formatOp: (field, op, values, valueSrc, valueType, opDef, operatorOptions, isForDisplay) => {
                if (valueSrc == "value" && Array.isArray(values)) {
                    return `${field}.str.contains([${values.join(", ")}])`;
                } else
                    return `${field}.str.contains(${values})`;
            },
        },
        multiselect_not_contains: {
            ...AntdConfig.operators.multiselect_not_contains,
            formatOp: (field, op, values, valueSrc, valueType, opDef, operatorOptions, isForDisplay) => {
                if (valueSrc == "value" && Array.isArray(values)) {
                    return `~${field}.str.contains([${values.join(", ")}])`;
                } else
                    return `~${field}.str.contains(${values})`;
            },
        }

    },
    types: {
        ...AntdConfig.types,
        text: {
            ...AntdConfig.types.text,
            excludeOperators: ["proximity"],
        }
    }
}

export {defaultConfig}