from flask import Flask, jsonify, render_template_string
from src.a07_timeline_logic.timeline_main import (
    add_newtimeline_planunit,
    get_default_timeline_config_dict,
)
from src.a22_belief_viewer.belief_viewer_tool import get_plan_view_dict
from src.a22_belief_viewer.example22_beliefs import (
    get_beliefunit_irrational_example,
    get_sue_belief_with_facts_and_reasons,
    get_sue_beliefunit,
)

app = Flask(__name__)

sue_belief = get_sue_belief_with_facts_and_reasons()
add_newtimeline_planunit(sue_belief, get_default_timeline_config_dict())
sue_belief.cash_out()

plan_view_dict = get_plan_view_dict(sue_belief.planroot)


def get_belief_viewer_template() -> str:
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>belief_viewer</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Belief Partners and Plan Tree</h1>
        <h5>Each node has a plan_label</h5>
        
        <div class="partners_controls">
            <input type="checkbox" id="show_partners"><label for="show_partners">partners</label>
        </div>
        <div class="plan_controls">
            <input type="checkbox" id="show_level"><label for="show_level">level</label>
            <input type="checkbox" id="show_moment_label"><label for="show_moment_label">moment_label</label>
            <input type="checkbox" id="show_task"><label for="show_task">task</label>
            <input type="checkbox" id="show_descendant_task_count"><label for="show_descendant_task_count">descendant_task_count</label>
            <input type="checkbox" id="show_active"><label for="show_active">active</label>
            <input type="checkbox" id="show_chore"><label for="show_chore">chore</label>
            <input type="checkbox" id="show_star"><label for="show_star">star</label>
            <input type="checkbox" id="show_fund_share"><label for="show_fund_share">fund_share</label>
            <input type="checkbox" id="show_fund_onset"><label for="show_fund_onset">fund_onset</label>
            <input type="checkbox" id="show_fund_cease"><label for="show_fund_cease">fund_cease</label>
            <input type="checkbox" id="show_fund_iota"><label for="show_fund_iota">fund_iota</label>
            <input type="checkbox" id="show_fund_ratio"><label for="show_fund_ratio">fund_ratio</label>
            <input type="checkbox" id="show_parent_rope"><label for="show_parent_rope">parent_rope</label>
            <input type="checkbox" id="show_root_boolean"><label for="show_root_boolean">root_boolean</label>
            <input type="checkbox" id="show_uid"><label for="show_uid">uid</label>
            <input type="checkbox" id="show_reasonunits"><label for="show_reasonunits">reasonunits</label>
            <input type="checkbox" id="show_reasonheirs"><label for="show_reasonheirs">reasonheirs</label>
            <input type="checkbox" id="show_factunits"><label for="show_factunits">factunits</label>
            <input type="checkbox" id="show_factheirs"><label for="show_factheirs">factheirs</label>
            <input type="checkbox" id="show_awardunits"><label for="show_awardunits">awardunits</label>
            <input type="checkbox" id="show_awardheirs"><label for="show_awardheirs">awardheirs</label>
            <input type="checkbox" id="show_awardlines"><label for="show_awardlines">awardlines</label>
            <input type="checkbox" id="show_laborunit"><label for="show_laborunit">laborunit</label>
            <input type="checkbox" id="show_laborheir"><label for="show_laborheir">laborheir</label>
            <input type="checkbox" id="show_all_partner_cred"><label for="show_all_partner_cred">_all_partner_cred</label>
            <input type="checkbox" id="show_all_partner_debt"><label for="show_all_partner_debt">_all_partner_debt</label>
            <input type="checkbox" id="show_gogo_want"><label for="show_gogo_want">gogo_want</label>
            <input type="checkbox" id="show_stop_want"><label for="show_stop_want">stop_want</label>
            <input type="checkbox" id="show_gogo_calc"><label for="show_gogo_calc">_gogo_calc</label>
            <input type="checkbox" id="show_stop_calc"><label for="show_stop_calc">_stop_calc</label>
            <input type="checkbox" id="show_addin"><label for="show_addin">addin</label>
            <input type="checkbox" id="show_begin"><label for="show_begin">begin</label>
            <input type="checkbox" id="show_close"><label for="show_close">close</label>
            <input type="checkbox" id="show_denom"><label for="show_denom">denom</label>
            <input type="checkbox" id="show_morph"><label for="show_morph">morph</label>
            <input type="checkbox" id="show_numor"><label for="show_numor">numor</label>
            <input type="checkbox" id="show_active_hx"><label for="show_active_hx">active_hx</label>
        </div>
        
        <div id="planTreeContainer" class="tree-display"></div>
        
        <script src="/static/app.js"></script>
    </body>
    </html>
    """


@app.route("/")
def index():
    """Serve the main HTML page"""
    return render_template_string(get_belief_viewer_template())


@app.route("/api/tree")
def get_tree():
    """API endpoint to get the tree data as JSON"""
    # return jsonify(root.to_dict())
    return jsonify(plan_view_dict)


if __name__ == "__main__":
    app.run(debug=True)
