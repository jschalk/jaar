from flask import Flask, jsonify, request
from flask_cors import CORS
from src.a05_plan_logic.plan import PlanUnit
from src.a06_believer_logic.believer_main import (
    get_from_dict as get_believerunit_from_dict,
)
from src.a22_plan_viewer.planview_filters import (
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


def get_planunits_list(believerunit_dict: dict) -> list[PlanUnit]:
    x_believerunit = get_believerunit_from_dict(believerunit_dict)
    x_believerunit.settle_believer()
    return x_believerunit._plan_dict.values()


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

        planunits_list = get_planunits_list(data)

        if mode == "Plan Label":
            plan_tree_display_dict = plan_label(planunits_list)
        elif mode == "Plan Tasks":
            plan_tree_display_dict = plan_tasks(planunits_list)
        elif mode == "Plan Fund":
            plan_tree_display_dict = plan_fund(planunits_list)
        elif mode == "Plan Awardees":
            plan_tree_display_dict = plan_awardees(planunits_list)
        elif mode == "Plan Reasons":
            plan_tree_display_dict = plan_reasons(planunits_list)
        elif mode == "Plan Facts":
            plan_tree_display_dict = plan_facts(planunits_list)
        elif mode == "Plan Time":
            plan_tree_display_dict = plan_time(planunits_list)
        elif mode == "static_dict_testing":
            plan_tree_display_dict = {"amy23": {"x1": {}, "x2": {}, "x3": {"x4": {}}}}
        else:
            plan_tree_display_dict = {"Mode not loaded correctly": "Contact support"}

        return jsonify(
            {"mode": mode, "result": plan_tree_display_dict, "believer_name": "Sue"}
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@planviewer.route("/set_flask_fund_pool", methods=["POST"])
def set_flask_fund_pool():
    data = request.get_json()
    flask_fund_pool = data.get("number")

    # You can do whatever you want with the number here.
    print(f"Received number: {flask_fund_pool}")
    # For now, just return a confirmation.
    return jsonify({"status": "success", "received": flask_fund_pool})


if __name__ == "__main__":
    planviewer.run(debug=True, port=5000)
