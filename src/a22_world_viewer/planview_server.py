from flask import Flask, jsonify, request
from flask_cors import CORS
from src.a22_world_viewer.planview_filters import (
    etl_clean,
    etl_enrich,
    etl_flatten,
    plan_awardees,
    plan_facts,
    plan_fund,
    plan_label,
    plan_reasons,
    plan_tasks,
    plan_time,
)

planviewer = Flask(__name__)
CORS(planviewer)


@planviewer.route("/modes", methods=["GET"])
def get_modes():
    modes_list = [
        "Plan Label",
        "Plan Tasks",
        "Plan Fund",
        "Plan Awardees",
        "Plan Reasons",
        "Plan Facts",
        "Plan Time",
        "etl_clean",
        "etl_flatten",
        "etl_enrich",
        "static_dict_testing",
    ]
    return jsonify(modes_list)


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

        if mode == "Plan Label":
            result = plan_label(data)
        elif mode == "Plan Tasks":
            result = plan_tasks(data)
        elif mode == "Plan Fund":
            result = plan_fund(data)
        elif mode == "Plan Awardees":
            result = plan_awardees(data)
        elif mode == "Plan Reasons":
            result = plan_reasons(data)
        elif mode == "Plan Facts":
            result = plan_facts(data)
        elif mode == "Plan Time":
            result = plan_time(data)
        elif mode == "etl_clean":
            result = etl_clean(data)
        elif mode == "etl_enrich":
            result = etl_enrich(data)
        elif mode == "etl_flatten":
            result = etl_flatten(data)
        elif mode == "static_dict_testing":
            result = {"amy23": {"x1": {}, "x2": {}, "x3": {"x4": {}}}}
        else:
            # default mode: just return data unchanged
            result = data

        return jsonify({"mode": mode, "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    planviewer.run(debug=True, port=5000)
