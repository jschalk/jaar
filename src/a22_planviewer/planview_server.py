from flask import Flask, jsonify, request
from flask_cors import CORS
from src.a22_planviewer.planview_filters import (
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
            plan_tree_display_dict = plan_label(data)
        elif mode == "Plan Tasks":
            plan_tree_display_dict = plan_tasks(data)
        elif mode == "Plan Fund":
            plan_tree_display_dict = plan_fund(data)
        elif mode == "Plan Awardees":
            plan_tree_display_dict = plan_awardees(data)
        elif mode == "Plan Reasons":
            plan_tree_display_dict = plan_reasons(data)
        elif mode == "Plan Facts":
            plan_tree_display_dict = plan_facts(data)
        elif mode == "Plan Time":
            plan_tree_display_dict = plan_time(data)
        elif mode == "static_dict_testing":
            plan_tree_display_dict = {"amy23": {"x1": {}, "x2": {}, "x3": {"x4": {}}}}
        else:
            plan_tree_display_dict = {"Mode not loaded correctly": "Contact support"}

        return jsonify(
            {"mode": mode, "result": plan_tree_display_dict, "believer_name": "Sue"}
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    planviewer.run(debug=True, port=5000)
