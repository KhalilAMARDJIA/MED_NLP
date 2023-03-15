def extract_json_last_layer(obj):
    result = []
    if isinstance(obj, dict):
        for key in obj:
            result.extend(extract_json_last_layer(obj[key]))
    elif isinstance(obj, list):
        for item in obj:
            result.extend(extract_json_last_layer(item))
    else:
        result.append(obj)
    return result