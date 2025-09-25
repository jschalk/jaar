from flask import Flask, jsonify, render_template_string
from src.ch08_timeline_logic.timeline_main import (
    add_newtimeline_planunit,
    get_default_timeline_config_dict,
)
from src.ch22_belief_viewer.belief_viewer_tool import get_belief_view_dict
from src.ch22_belief_viewer.example22_beliefs import (
    get_beliefunit_irrational_example,
    get_sue_belief_with_facts_and_reasons,
    get_sue_beliefunit,
)

app = Flask(__name__)


def get_belief_viewer_template() -> str:
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>belief_viewer</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Belief Voices and Plan Tree</h1>
        <h5>Each node has a plan_label</h5>
        
        <div class="voices_controls">
            <input type="checkbox" id="show_voices"><label for="show_voices">voices</label>
            <input type="checkbox" id="show_voice_cred_points"><label for="show_voice_cred_points">cred_points</label>
            <input type="checkbox" id="show_voice_debt_points"><label for="show_voice_debt_points">debt_points</label>
            <input type="checkbox" id="show_voice_credor_pool"><label for="show_voice_credor_pool">credor_pool</label>
            <input type="checkbox" id="show_voice_debtor_pool"><label for="show_voice_debtor_pool">debtor_pool</label>
            <input type="checkbox" id="show_voice_irrational_voice_debt_points"><label for="show_voice_irrational_voice_debt_points">irrational_voice_debt_points</label>
            <input type="checkbox" id="show_voice_inallocable_voice_debt_points"><label for="show_voice_inallocable_voice_debt_points">inallocable_voice_debt_points</label>
            <input type="checkbox" id="show_voice_fund_give"><label for="show_voice_fund_give">fund_give</label>
            <input type="checkbox" id="show_voice_fund_take"><label for="show_voice_fund_take">fund_take</label>
            <input type="checkbox" id="show_voice_fund_agenda_give"><label for="show_voice_fund_agenda_give">fund_agenda_give</label>
            <input type="checkbox" id="show_voice_fund_agenda_take"><label for="show_voice_fund_agenda_take">fund_agenda_take</label>
            <input type="checkbox" id="show_voice_fund_agenda_ratio_give"><label for="show_voice_fund_agenda_ratio_give">fund_agenda_ratio_give</label>
            <input type="checkbox" id="show_voice_fund_agenda_ratio_take"><label for="show_voice_fund_agenda_ratio_take">fund_agenda_ratio_take</label>
            <br>
            <input type="checkbox" id="show_voice_membership_group_title"><label for="show_voice_membership_group_title">membership_group_title</label>
            <input type="checkbox" id="show_voice_membership_group_cred_points"><label for="show_voice_membership_group_cred_points">membership_group_cred_points</label>
            <input type="checkbox" id="show_voice_membership_group_debt_points"><label for="show_voice_membership_group_debt_points">membership_group_debt_points</label>
            <input type="checkbox" id="show_voice_membership_credor_pool"><label for="show_voice_membership_credor_pool">membership_credor_pool</label>
            <input type="checkbox" id="show_voice_membership_debtor_pool"><label for="show_voice_membership_debtor_pool">membership_debtor_pool</label>
            <input type="checkbox" id="show_voice_membership_fund_agenda_give"><label for="show_voice_membership_fund_agenda_give">membership_fund_agenda_give</label>
            <input type="checkbox" id="show_voice_membership_fund_agenda_ratio_give"><label for="show_voice_membership_fund_agenda_ratio_give">membership_fund_agenda_ratio_give</label>
            <input type="checkbox" id="show_voice_membership_fund_agenda_ratio_take"><label for="show_voice_membership_fund_agenda_ratio_take">membership_fund_agenda_ratio_take</label>
            <input type="checkbox" id="show_voice_membership_fund_agenda_take"><label for="show_voice_membership_fund_agenda_take">membership_fund_agenda_take</label>
            <input type="checkbox" id="show_voice_membership_fund_give"><label for="show_voice_membership_fund_give">membership_fund_give</label>
            <input type="checkbox" id="show_voice_membership_fund_take"><label for="show_voice_membership_fund_take">membership_fund_take</label>
            
        </div>
        <div id="voicesContainer" class="plan_tree_display"></div>
        <div class="plan_controls">
            <input type="checkbox" id="show_planroot"><label for="show_planroot">planroot</label>
            <input type="checkbox" id="show_level"><label for="show_level">level</label>
            <input type="checkbox" id="show_moment_label"><label for="show_moment_label">moment_label</label>
            <input type="checkbox" id="show_pledge"><label for="show_pledge">pledge</label>
            <input type="checkbox" id="show_descendant_pledge_count"><label for="show_descendant_pledge_count">descendant_pledge_count</label>
            <input type="checkbox" id="show_active"><label for="show_active">active</label>
            <input type="checkbox" id="show_task"><label for="show_task">task</label>
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
            <input type="checkbox" id="show_all_voice_cred"><label for="show_all_voice_cred">_all_voice_cred</label>
            <input type="checkbox" id="show_all_voice_debt"><label for="show_all_voice_debt">_all_voice_debt</label>
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
        
        <div id="planTreeContainer" class="plan_tree_display"></div>
        
        <script src="/static/app.js"></script>
    </body>
    </html>
    """


@app.route("/")
def index():
    """Serve the main HTML page"""
    return render_template_string(get_belief_viewer_template())


@app.route("/api/beliefunit_view")
def get_beliefunit_view():
    """API endpoint to get the BeliefUnit data with readable strings as JSON"""
    # return jsonify(root.to_dict())
    sue_belief = get_sue_belief_with_facts_and_reasons()
    add_newtimeline_planunit(sue_belief, get_default_timeline_config_dict())
    sue_belief.cashout()
    belief_view_dict = get_belief_view_dict(sue_belief)
    return jsonify(belief_view_dict)


if __name__ == "__main__":
    app.run(debug=True)
