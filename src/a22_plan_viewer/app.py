from flask import Flask, jsonify, render_template_string
from src.a03_group_logic.group import awardlink_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a22_plan_viewer.plan_viewer import get_plan_view_dict

app = Flask(__name__)


sue_believer = believerunit_shop("Sue", "accord23")
casa_rope = sue_believer.make_l1_rope("casa")
clean_rope = sue_believer.make_rope(casa_rope, "cleaning work")
mop_rope = sue_believer.make_rope(clean_rope, "mop")
sweep_rope = sue_believer.make_rope(clean_rope, "sweep")
sue_believer.add_plan(casa_rope, 3)
sue_believer.add_plan(clean_rope, 3)
sue_believer.add_plan(mop_rope, 3, task=True)
sue_believer.add_plan(sweep_rope, 3, task=True)

# Add some award links
sue_believer.edit_plan_attr(casa_rope, awardlink=awardlink_shop("Manager", 0.5, 0.2))
sue_believer.edit_plan_attr(casa_rope, awardlink=awardlink_shop("Team Lead", 0.3, 0.1))
sue_believer.edit_plan_attr(casa_rope, awardlink=awardlink_shop("Developer A", 1, 0.8))
sue_believer.edit_plan_attr(casa_rope, awardlink=awardlink_shop("Junior Dev", 0.7, 0.9))
sue_believer.settle_believer()
plan_view_dict = get_plan_view_dict(sue_believer.planroot)


@app.route("/")
def index():
    """Serve the main HTML page"""
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>PlanUnit Tree</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>PlanUnit Tree Structure</h1>
        
        <div class="controls">
            <input type="checkbox" id="show_belief_label">
            <label for="show_belief_label">show_belief_label</label>
            <input type="checkbox" id="show_task">
            <label for="show_task">show_task</label>
            <input type="checkbox" id="show_active">
            <label for="show_active">show_active</label>
            <input type="checkbox" id="show_star">
            <label for="show_star">show_star</label>
            <input type="checkbox" id="show_parent_rope">
            <label for="show_parent_rope">show_parent_rope</label>
            <input type="checkbox" id="show_root_boolean">
            <label for="show_root_boolean">show_root_boolean</label>
            <input type="checkbox" id="show_uid">
            <label for="show_uid">show_uid</label>
            <input type="checkbox" id="show_awardlinks">
            <label for="show_awardlinks">show_awardlinks</label>
        </div>
        
        <div id="treeContainer" class="tree-display"></div>
        
        <script src="/static/app.js"></script>
    </body>
    </html>
    """
    return render_template_string(template)


@app.route("/api/tree")
def get_tree():
    """API endpoint to get the tree data as JSON"""
    # return jsonify(root.to_dict())
    return jsonify(plan_view_dict)


if __name__ == "__main__":
    app.run(debug=True)
