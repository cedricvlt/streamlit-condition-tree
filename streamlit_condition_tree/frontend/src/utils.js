// stole from https://github.com/andfanilo/streamlit-echarts/blob/main/streamlit_echarts/frontend/src/utils.ts Thanks andfanilo
function mapObject(obj, fn, keysToIgnore) {
    let keysToMap = Object.keys(obj)
    return keysToMap.reduce((res, key) => {
        if (!keysToIgnore.includes(key)) {
            res[key] = fn(obj[key]);
            return res
        }
        res[key] = obj[key];
        return res

    }, {})
}

function deepMap(obj, fn, keysToIgnore = []) {
    const deepMapper = (val) =>
        val !== null && typeof val === "object" ? deepMap(val, fn) : fn(val)
    if (Array.isArray(obj)) {
        return obj.map(deepMapper)
    }
    if (typeof obj === "object") {
        return mapObject(obj, deepMapper, keysToIgnore)
    }
    return obj
}

export { deepMap }