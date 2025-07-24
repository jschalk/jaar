from flask import Flask, jsonify, request
from flask_cors import CORS

planviewer = Flask(__name__)
CORS(planviewer)


# Example ETL functions
def etl_clean(data):
    # Just delete null or empty fields
    if isinstance(data, dict):
        return {k: v for k, v in data.items() if v not in (None, "", [], {})}
    return data


def etl_enrich(data):
    # Add a field to every object
    if isinstance(data, dict):
        data["enriched"] = "yes"
    return data


def etl_flatten(data):
    # Example: flatten a dict of dicts (one level)
    if isinstance(data, dict):
        flat = {}
        for k, v in data.items():
            if isinstance(v, dict):
                for sub_k, sub_v in v.items():
                    flat[f"{k}.{sub_k}"] = sub_v
            else:
                flat[k] = v
        return flat
    return data


@planviewer.route("/process", methods=["POST"])
def process_json():
    try:
        json_data = request.get_json()
        if not isinstance(json_data, dict):
            raise ValueError("Input JSON must be an object")

        mode = json_data.get("_mode", "default")
        data = json_data.get("data")

        if data is None:
            raise ValueError("Missing 'data' field in request")

        if mode == "clean":
            result = etl_clean(data)
        elif mode == "enrich":
            result = etl_enrich(data)
        elif mode == "flatten":
            result = etl_flatten(data)
        else:
            # default mode: just return data unchanged
            result = data

        return jsonify({"mode": mode, "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    planviewer.run(debug=True, port=5000)
