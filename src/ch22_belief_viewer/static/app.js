// Global state
let planTreeData = null;
let show_voices = true;
let show_voice_cred_shares = false;
let show_voice_debt_shares = false;
let show_voice_credor_pool = false;
let show_voice_debtor_pool = false;
let show_voice_irrational_voice_debt_shares = false;
let show_voice_inallocable_voice_debt_shares = false;
let show_voice_fund_give = false;
let show_voice_fund_take = false;
let show_voice_fund_agenda_give = false;
let show_voice_fund_agenda_take = false;
let show_voice_fund_agenda_ratio_give = false;
let show_voice_fund_agenda_ratio_take = false;
let show_voice_membership_group_title = true;
let show_voice_membership_group_cred_shares = false;
let show_voice_membership_group_debt_shares = false;
let show_voice_membership_credor_pool = false;
let show_voice_membership_debtor_pool = false;
let show_voice_membership_fund_agenda_give = false;
let show_voice_membership_fund_agenda_ratio_give = false;
let show_voice_membership_fund_agenda_ratio_take = false;
let show_voice_membership_fund_agenda_take = false;
let show_voice_membership_fund_give = false;
let show_voice_membership_fund_take = false;
let show_planroot = true;
let show_awardunits = false;
let show_awardheirs = false;
let show_awardlines = false;
let show_laborunit = false;
let show_laborheir = false;
let show_level = false;
let show_moment_label = false;
let show_pledge = false;
let show_descendant_pledge_count = false;
let show_active = false;
let show_task = false;
let show_star = false;
let show_reasonunits = false;
let show_reasonheirs = false;
let show_factunits = false;
let show_factheirs = false;
let show_plan_fund_total = false;
let show_fund_onset = false;
let show_fund_cease = false;
let show_fund_grain = false;
let show_fund_ratio = false;
let show_all_voice_cred = false;
let show_all_voice_debt = false;
let show_gogo_want = false;
let show_stop_want = false;
let show_gogo_calc = false;
let show_stop_calc = false;
let show_addin = false;
let show_begin = false;
let show_close = false;
let show_denom = false;
let show_morph = false;
let show_numor = false;
let show_active_hx = false;
let show_parent_rope = false;
let show_root_boolean = false;
let show_uid = false;

// Initialize the app when DOM loads
document.addEventListener('DOMContentLoaded', function () {
    const show_voicesCheckbox = document.getElementById('show_voices');
    const show_voice_cred_sharesCheckbox = document.getElementById('show_voice_cred_shares')
    const show_voice_debt_sharesCheckbox = document.getElementById('show_voice_debt_shares')
    const show_voice_credor_poolCheckbox = document.getElementById('show_voice_credor_pool')
    const show_voice_debtor_poolCheckbox = document.getElementById('show_voice_debtor_pool')
    const show_voice_irrational_voice_debt_sharesCheckbox = document.getElementById('show_voice_irrational_voice_debt_shares')
    const show_voice_inallocable_voice_debt_sharesCheckbox = document.getElementById('show_voice_inallocable_voice_debt_shares')
    const show_voice_fund_giveCheckbox = document.getElementById('show_voice_fund_give')
    const show_voice_fund_takeCheckbox = document.getElementById('show_voice_fund_take')
    const show_voice_fund_agenda_giveCheckbox = document.getElementById('show_voice_fund_agenda_give')
    const show_voice_fund_agenda_takeCheckbox = document.getElementById('show_voice_fund_agenda_take')
    const show_voice_fund_agenda_ratio_giveCheckbox = document.getElementById('show_voice_fund_agenda_ratio_give')
    const show_voice_fund_agenda_ratio_takeCheckbox = document.getElementById('show_voice_fund_agenda_ratio_take')
    const show_voice_membership_group_titleCheckbox = document.getElementById('show_voice_membership_group_title')
    const show_voice_membership_group_cred_sharesCheckbox = document.getElementById('show_voice_membership_group_cred_shares')
    const show_voice_membership_group_debt_sharesCheckbox = document.getElementById('show_voice_membership_group_debt_shares')
    const show_voice_membership_credor_poolCheckbox = document.getElementById('show_voice_membership_credor_pool')
    const show_voice_membership_debtor_poolCheckbox = document.getElementById('show_voice_membership_debtor_pool')
    const show_voice_membership_fund_agenda_giveCheckbox = document.getElementById('show_voice_membership_fund_agenda_give')
    const show_voice_membership_fund_agenda_ratio_giveCheckbox = document.getElementById('show_voice_membership_fund_agenda_ratio_give')
    const show_voice_membership_fund_agenda_ratio_takeCheckbox = document.getElementById('show_voice_membership_fund_agenda_ratio_take')
    const show_voice_membership_fund_agenda_takeCheckbox = document.getElementById('show_voice_membership_fund_agenda_take')
    const show_voice_membership_fund_giveCheckbox = document.getElementById('show_voice_membership_fund_give')
    const show_voice_membership_fund_takeCheckbox = document.getElementById('show_voice_membership_fund_take')
    const show_planrootCheckbox = document.getElementById('show_planroot');
    const show_awardunitsCheckbox = document.getElementById('show_awardunits');
    const show_awardheirsCheckbox = document.getElementById('show_awardheirs');
    const show_awardlinesCheckbox = document.getElementById('show_awardlines');
    const show_laborunitCheckbox = document.getElementById('show_laborunit');
    const show_laborheirCheckbox = document.getElementById('show_laborheir');
    const show_levelCheckbox = document.getElementById('show_level');
    const show_moment_labelCheckbox = document.getElementById('show_moment_label');
    const show_pledgeCheckbox = document.getElementById('show_pledge');
    const show_descendant_pledge_countCheckbox = document.getElementById('show_descendant_pledge_count');
    const show_activeCheckbox = document.getElementById('show_active');
    const show_taskCheckbox = document.getElementById('show_task');
    const show_starCheckbox = document.getElementById('show_star');
    const show_reasonunitsCheckbox = document.getElementById('show_reasonunits');
    const show_reasonheirsCheckbox = document.getElementById('show_reasonheirs');
    const show_factunitsCheckbox = document.getElementById('show_factunits');
    const show_factheirsCheckbox = document.getElementById('show_factheirs');
    const show_plan_fund_totalCheckbox = document.getElementById('show_plan_fund_total');
    const show_fund_onsetCheckbox = document.getElementById('show_fund_onset');
    const show_fund_ceaseCheckbox = document.getElementById('show_fund_cease');
    const show_fund_grainCheckbox = document.getElementById('show_fund_grain');
    const show_fund_ratioCheckbox = document.getElementById('show_fund_ratio');
    const show_all_voice_credCheckbox = document.getElementById('show_all_voice_cred');
    const show_all_voice_debtCheckbox = document.getElementById('show_all_voice_debt');
    const show_gogo_wantCheckbox = document.getElementById('show_gogo_want');
    const show_stop_wantCheckbox = document.getElementById('show_stop_want');
    const show_gogo_calcCheckbox = document.getElementById('show_gogo_calc');
    const show_stop_calcCheckbox = document.getElementById('show_stop_calc');
    const show_addinCheckbox = document.getElementById('show_addin');
    const show_beginCheckbox = document.getElementById('show_begin');
    const show_closeCheckbox = document.getElementById('show_close');
    const show_denomCheckbox = document.getElementById('show_denom');
    const show_morphCheckbox = document.getElementById('show_morph');
    const show_numorCheckbox = document.getElementById('show_numor');
    const show_active_hxCheckbox = document.getElementById('show_active_hx');
    const show_parent_ropeCheckbox = document.getElementById('show_parent_rope');
    const show_root_booleanCheckbox = document.getElementById('show_root_boolean');
    const show_uidCheckbox = document.getElementById('show_uid');

    // Set up checkbox event listener
    show_voicesCheckbox.addEventListener('change', function () { show_voices = this.checked; renderVoicesData(); });
    show_voice_cred_sharesCheckbox.addEventListener('change', function () { show_voice_cred_shares = this.checked; renderVoicesData(); });
    show_voice_debt_sharesCheckbox.addEventListener('change', function () { show_voice_debt_shares = this.checked; renderVoicesData(); });
    show_voice_credor_poolCheckbox.addEventListener('change', function () { show_voice_credor_pool = this.checked; renderVoicesData(); });
    show_voice_debtor_poolCheckbox.addEventListener('change', function () { show_voice_debtor_pool = this.checked; renderVoicesData(); });
    show_voice_irrational_voice_debt_sharesCheckbox.addEventListener('change', function () { show_voice_irrational_voice_debt_shares = this.checked; renderVoicesData(); });
    show_voice_inallocable_voice_debt_sharesCheckbox.addEventListener('change', function () { show_voice_inallocable_voice_debt_shares = this.checked; renderVoicesData(); });
    show_voice_fund_giveCheckbox.addEventListener('change', function () { show_voice_fund_give = this.checked; renderVoicesData(); });
    show_voice_fund_takeCheckbox.addEventListener('change', function () { show_voice_fund_take = this.checked; renderVoicesData(); });
    show_voice_fund_agenda_giveCheckbox.addEventListener('change', function () { show_voice_fund_agenda_give = this.checked; renderVoicesData(); });
    show_voice_fund_agenda_takeCheckbox.addEventListener('change', function () { show_voice_fund_agenda_take = this.checked; renderVoicesData(); });
    show_voice_fund_agenda_ratio_giveCheckbox.addEventListener('change', function () { show_voice_fund_agenda_ratio_give = this.checked; renderVoicesData(); });
    show_voice_fund_agenda_ratio_takeCheckbox.addEventListener('change', function () { show_voice_fund_agenda_ratio_take = this.checked; renderVoicesData(); });
    show_voice_membership_group_titleCheckbox.addEventListener('change', function () { show_voice_membership_group_title = this.checked; renderVoicesData(); });
    show_voice_membership_group_cred_sharesCheckbox.addEventListener('change', function () { show_voice_membership_group_cred_shares = this.checked; renderVoicesData(); });
    show_voice_membership_group_debt_sharesCheckbox.addEventListener('change', function () { show_voice_membership_group_debt_shares = this.checked; renderVoicesData(); });
    show_voice_membership_credor_poolCheckbox.addEventListener('change', function () { show_voice_membership_credor_pool = this.checked; renderVoicesData(); });
    show_voice_membership_debtor_poolCheckbox.addEventListener('change', function () { show_voice_membership_debtor_pool = this.checked; renderVoicesData(); });
    show_voice_membership_fund_agenda_giveCheckbox.addEventListener('change', function () { show_voice_membership_fund_agenda_give = this.checked; renderVoicesData(); });
    show_voice_membership_fund_agenda_ratio_giveCheckbox.addEventListener('change', function () { show_voice_membership_fund_agenda_ratio_give = this.checked; renderVoicesData(); });
    show_voice_membership_fund_agenda_ratio_takeCheckbox.addEventListener('change', function () { show_voice_membership_fund_agenda_ratio_take = this.checked; renderVoicesData(); });
    show_voice_membership_fund_agenda_takeCheckbox.addEventListener('change', function () { show_voice_membership_fund_agenda_take = this.checked; renderVoicesData(); });
    show_voice_membership_fund_giveCheckbox.addEventListener('change', function () { show_voice_membership_fund_give = this.checked; renderVoicesData(); });
    show_voice_membership_fund_takeCheckbox.addEventListener('change', function () { show_voice_membership_fund_take = this.checked; renderVoicesData(); });
    show_planrootCheckbox.addEventListener('change', function () { show_planroot = this.checked; renderPlanTree(); });
    show_awardunitsCheckbox.addEventListener('change', function () { show_awardunits = this.checked; renderPlanTree(); });
    show_awardheirsCheckbox.addEventListener('change', function () { show_awardheirs = this.checked; renderPlanTree(); });
    show_awardlinesCheckbox.addEventListener('change', function () { show_awardlines = this.checked; renderPlanTree(); });
    show_laborunitCheckbox.addEventListener('change', function () { show_laborunit = this.checked; renderPlanTree(); });
    show_laborheirCheckbox.addEventListener('change', function () { show_laborheir = this.checked; renderPlanTree(); });
    show_levelCheckbox.addEventListener('change', function () { show_level = this.checked; renderPlanTree(); });
    show_moment_labelCheckbox.addEventListener('change', function () { show_moment_label = this.checked; renderPlanTree(); });
    show_pledgeCheckbox.addEventListener('change', function () { show_pledge = this.checked; renderPlanTree(); });
    show_descendant_pledge_countCheckbox.addEventListener('change', function () { show_descendant_pledge_count = this.checked; renderPlanTree(); });
    show_activeCheckbox.addEventListener('change', function () { show_active = this.checked; renderPlanTree(); });
    show_taskCheckbox.addEventListener('change', function () { show_task = this.checked; renderPlanTree(); });
    show_starCheckbox.addEventListener('change', function () { show_star = this.checked; renderPlanTree(); });
    show_reasonunitsCheckbox.addEventListener('change', function () { show_reasonunits = this.checked; renderPlanTree(); });
    show_reasonheirsCheckbox.addEventListener('change', function () { show_reasonheirs = this.checked; renderPlanTree(); });
    show_factunitsCheckbox.addEventListener('change', function () { show_factunits = this.checked; renderPlanTree(); });
    show_factheirsCheckbox.addEventListener('change', function () { show_factheirs = this.checked; renderPlanTree(); });
    show_plan_fund_totalCheckbox.addEventListener('change', function () { show_plan_fund_total = this.checked; renderPlanTree(); });
    show_fund_onsetCheckbox.addEventListener('change', function () { show_fund_onset = this.checked; renderPlanTree(); });
    show_fund_ceaseCheckbox.addEventListener('change', function () { show_fund_cease = this.checked; renderPlanTree(); });
    show_fund_grainCheckbox.addEventListener('change', function () { show_fund_grain = this.checked; renderPlanTree(); });
    show_fund_ratioCheckbox.addEventListener('change', function () { show_fund_ratio = this.checked; renderPlanTree(); });
    show_all_voice_credCheckbox.addEventListener('change', function () { show_all_voice_cred = this.checked; renderPlanTree(); });
    show_all_voice_debtCheckbox.addEventListener('change', function () { show_all_voice_debt = this.checked; renderPlanTree(); });
    show_gogo_wantCheckbox.addEventListener('change', function () { show_gogo_want = this.checked; renderPlanTree(); });
    show_stop_wantCheckbox.addEventListener('change', function () { show_stop_want = this.checked; renderPlanTree(); });
    show_gogo_calcCheckbox.addEventListener('change', function () { show_gogo_calc = this.checked; renderPlanTree(); });
    show_stop_calcCheckbox.addEventListener('change', function () { show_stop_calc = this.checked; renderPlanTree(); });
    show_addinCheckbox.addEventListener('change', function () { show_addin = this.checked; renderPlanTree(); });
    show_beginCheckbox.addEventListener('change', function () { show_begin = this.checked; renderPlanTree(); });
    show_closeCheckbox.addEventListener('change', function () { show_close = this.checked; renderPlanTree(); });
    show_denomCheckbox.addEventListener('change', function () { show_denom = this.checked; renderPlanTree(); });
    show_morphCheckbox.addEventListener('change', function () { show_morph = this.checked; renderPlanTree(); });
    show_numorCheckbox.addEventListener('change', function () { show_numor = this.checked; renderPlanTree(); });
    show_active_hxCheckbox.addEventListener('change', function () { show_active_hx = this.checked; renderPlanTree(); });
    show_parent_ropeCheckbox.addEventListener('change', function () { show_parent_rope = this.checked; renderPlanTree(); });
    show_root_booleanCheckbox.addEventListener('change', function () { show_root_boolean = this.checked; renderPlanTree(); });
    show_uidCheckbox.addEventListener('change', function () { show_uid = this.checked; renderPlanTree(); });

    // Load initial tree data
    loadBeliefData();
});

// Fetch tree data from server
async function loadBeliefData() {
    try {
        const response = await fetch('/api/beliefunit_view');
        beliefViewData = await response.json();
        planTreeData = beliefViewData.planroot;
        voicesData = beliefViewData.voices;
        renderPlanTree();
        renderVoicesData();
    } catch (error) {
        console.error('Error loading tree data:', error);
        document.getElementById('planTreeContainer').innerHTML = '<p>Error loading tree data</p>';
        document.getElementById('planTreeContainer').innerHTML = '<p>Error loading tree data</p>';
    }
}


// Render VoicesData and its membership attributes
function renderVoicesData() {
    const voices_container = document.getElementById('voicesContainer');
    voices_container.innerHTML = buildVoicesHtml(voicesData);
}

function buildVoicesHtml(voicesData) {
    if (!voicesData || !show_voices) {
        return "";
    }
    const voices_indent = '&nbsp;'.repeat(2);
    const member_title_indent = '&nbsp;'.repeat(3);
    const membership_indent = '&nbsp;'.repeat(5);

    let html = '';
    Object.values(voicesData).forEach(voice => {
        html += `<br>${voices_indent}${voice.voice_name}`;
        if (show_voice_cred_shares) { html += `<br>${voices_indent}    ${voice.voice_cred_shares_readable}` };
        if (show_voice_debt_shares) { html += `<br>${voices_indent}    ${voice.voice_debt_shares_readable}` };
        if (show_voice_credor_pool) { html += `<br>${voices_indent}    ${voice.credor_pool_readable}` };
        if (show_voice_debtor_pool) { html += `<br>${voices_indent}    ${voice.debtor_pool_readable}` };
        if (show_voice_irrational_voice_debt_shares) { html += `<br>${voices_indent}    ${voice.irrational_voice_debt_shares_readable}` };
        if (show_voice_inallocable_voice_debt_shares) { html += `<br>${voices_indent}    ${voice.inallocable_voice_debt_shares_readable}` };
        if (show_voice_fund_give) { html += `<br>${voices_indent}    ${voice.fund_give_readable}` };
        if (show_voice_fund_take) { html += `<br>${voices_indent}    ${voice.fund_take_readable}` };
        if (show_voice_fund_agenda_give) { html += `<br>${voices_indent}    ${voice.fund_agenda_give_readable}` };
        if (show_voice_fund_agenda_take) { html += `<br>${voices_indent}    ${voice.fund_agenda_take_readable}` };
        if (show_voice_fund_agenda_ratio_give) { html += `<br>${voices_indent}    ${voice.fund_agenda_ratio_give_readable}` };
        if (show_voice_fund_agenda_ratio_take) { html += `<br>${voices_indent}    ${voice.fund_agenda_ratio_take_readable}` };
        console.info(voice)
        Object.values(voice.memberships).forEach(membership => {
            if (show_voice_membership_group_title) { html += `<br><b>${member_title_indent}${membership.group_title_readable}</b>` };
            if (show_voice_membership_group_cred_shares) { html += `<br>${membership_indent}${membership.group_cred_shares_readable}` };
            if (show_voice_membership_group_debt_shares) { html += `<br>${membership_indent}${membership.group_debt_shares_readable}` };
            if (show_voice_membership_credor_pool) { html += `<br>${membership_indent}${membership.credor_pool_readable}` };
            if (show_voice_membership_debtor_pool) { html += `<br>${membership_indent}${membership.debtor_pool_readable}` };
            if (show_voice_membership_fund_agenda_give) { html += `<br>${membership_indent}${membership.fund_agenda_give_readable}` };
            if (show_voice_membership_fund_agenda_ratio_give) { html += `<br>${membership_indent}${membership.fund_agenda_ratio_give_readable}` };
            if (show_voice_membership_fund_agenda_ratio_take) { html += `<br>${membership_indent}${membership.fund_agenda_ratio_take_readable}` };
            if (show_voice_membership_fund_agenda_take) { html += `<br>${membership_indent}${membership.fund_agenda_take_readable}` };
            if (show_voice_membership_fund_give) { html += `<br>${membership_indent}${membership.fund_give_readable}` };
            if (show_voice_membership_fund_take) { html += `<br>${membership_indent}${membership.fund_take_readable}` };
            // html += `<br>${voices_indent}${voice.voice_name}`;
        });
    });
    return html
}

// Render the tree structure
function renderPlanTree() {
    if (!planTreeData) {
        return;
    }

    const container = document.getElementById('planTreeContainer');
    container.innerHTML = renderPlanUnit(planTreeData, 0);
}

// Recursively render a PlanUnit and its children
function renderPlanUnit(planUnit, level) {
    if (!show_planroot) {
        return "";
    }
    const indent = '&nbsp;'.repeat(level * 2);
    const levelIndicator = show_level ? ` level${planUnit.tree_level}` : '';
    const pledgeIndicator = planUnit.pledge && show_pledge ? ' PLEDGE' : '';
    const descendant_pledge_countIndicator = show_descendant_pledge_count ? ` pledges: ${planUnit.descendant_pledge_count}` : '';
    const activeIndicator = planUnit.active && show_active ? '-ACTIVE' : '';
    const taskIndicator = planUnit.task && show_task ? '-task' : '';
    const starIndicator = show_star ? ` star${planUnit.star}` : '';
    const plan_fund_totalIndicator = show_plan_fund_total ? ` [${planUnit.plan_fund_total}]` : '';
    const uidIndicator = planUnit.uid && show_uid ? ` uid${planUnit.uid}` : '';

    const fund_onsetIndicator = show_fund_onset ? ` onset-${planUnit.fund_onset}` : '';
    const fund_ceaseIndicator = show_fund_cease ? ` cease-${planUnit.fund_cease}` : '';
    const fund_grainIndicator = show_fund_grain ? ` (iota: ${planUnit.fund_grain})` : '';
    const fund_ratioIndicator = show_fund_ratio ? ` ratio-${planUnit.fund_ratio}` : '';


    // Build award links HTML using separate function
    const moment_labelHtml = render_moment_label(planUnit.moment_label, planUnit.knot, show_moment_label);

    // Start with current node
    let html = `
  <div>
    ${indent}• 
    ${moment_labelHtml}
    ${planUnit.plan_label}
    <i>${levelIndicator}
    ${starIndicator}
    ${uidIndicator}
    ${pledgeIndicator}
    ${descendant_pledge_countIndicator}
    ${plan_fund_totalIndicator}
    ${fund_onsetIndicator}
    ${fund_ceaseIndicator}
    ${fund_grainIndicator}
    ${fund_ratioIndicator}
    ${activeIndicator}
    ${taskIndicator}
    ${root_booleanIndicator}</i>
    ${render_with_indent(planUnit.voices, indent, show_voices)}
    ${render_with_indent(planUnit.parent_rope, indent, show_parent_rope)}
    ${renderFlatReadableJson(planUnit.awardunits, indent, show_awardunits)}
    ${renderFlatReadableJson(planUnit.awardheirs, indent, show_awardheirs)}
    ${renderFlatReadableJson(planUnit.awardlines, indent, show_awardlines)}
    ${renderFlatReadableJson(planUnit.laborunit._partys, indent, show_laborunit)}
    ${renderFlatReadableJson(planUnit.laborheir._partys, indent, show_laborheir)}
    ${renderReasonReadableJson(planUnit.reasonunits, indent, show_reasonunits)}
    ${renderReasonReadableJson(planUnit.reasonheirs, indent, show_reasonheirs)}
    ${renderFlatReadableJson(planUnit.factunits, indent, show_factunits)}
    ${renderFlatReadableJson(planUnit.factheirs, indent, show_factheirs)}
    ${render_with_indent(planUnit.all_voice_cred, indent, show_all_voice_cred)}
    ${render_with_indent(planUnit.all_voice_debt, indent, show_all_voice_debt)}
    ${render_with_indent(planUnit.gogo_want, indent, show_gogo_want)}
    ${render_with_indent(planUnit.stop_want, indent, show_stop_want)}
    ${render_with_indent(planUnit.gogo_calc, indent, show_gogo_calc)}
    ${render_with_indent(planUnit.stop_calc, indent, show_stop_calc)}
    ${render_with_indent(planUnit.addin, indent, show_addin)}
    ${render_with_indent(planUnit.begin, indent, show_begin)}
    ${render_with_indent(planUnit.close, indent, show_close)}
    ${render_with_indent(planUnit.denom, indent, show_denom)}
    ${render_with_indent(planUnit.morph, indent, show_morph)}
    ${render_with_indent(planUnit.numor, indent, show_numor)}
    ${render_with_indent(planUnit.active_hx, indent, show_active_hx)}
  </div>\n
`;
    // Add children
    if (planUnit.kids) {
        Object.values(planUnit.kids).forEach(child => {
            html += renderPlanUnit(child, level + 1);
        });
    }
    return html;
}

function renderFlatReadableJson(flat_readables, indent, show_readable) {
    if (!flat_readables || Object.keys(flat_readables).length === 0 || !show_readable) {
        return '';
    }

    let html = '';
    Object.values(flat_readables).forEach(link => {
        html += `<br>${indent}${link.readable}`;
    });
    return html;
}
function renderReasonReadableJson(n3_readables, indent, show_readable) {
    if (!n3_readables || Object.keys(n3_readables).length === 0 || !show_readable) {
        return '';
    }

    let html = '';
    Object.values(n3_readables).forEach(link => {
        // top-level readable
        html += `<br>${indent}${link.readable || ''}`;

        // second level (cases)
        if (link.cases && Object.keys(link.cases).length > 0) {
            Object.values(link.cases).forEach(child => {
                html += `<br>${indent}${child.readable || ''}`;
            });
        }
    });
    return html;
}
function render_moment_label(moment_label, knot, show_moment_label) {
    if (!moment_label || !show_moment_label) {
        return '';
    }
    return ` ${knot}${moment_label}...`;
}
function render_with_indent(str, indent, show_bool) {
    if (!str || !show_bool) {
        return '';
    }
    return `<br>${indent}${str}`;
}
