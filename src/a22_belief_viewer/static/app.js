// Global state
let planTreeData = null;
let show_partners = true;
let show_awardunits = false;
let show_awardheirs = false;
let show_awardlines = false;
let show_laborunit = false;
let show_laborheir = false;
let show_level = false;
let show_moment_label = false;
let show_task = false;
let show_descendant_task_count = false;
let show_active = false;
let show_chore = false;
let show_star = false;
let show_reasonunits = false;
let show_reasonheirs = false;
let show_factunits = false;
let show_factheirs = false;
let show_fund_share = false;
let show_fund_onset = false;
let show_fund_cease = false;
let show_fund_iota = false;
let show_fund_ratio = false;
let show_all_partner_cred = false;
let show_all_partner_debt = false;
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
    const show_partnersCheckbox = document.getElementById('show_partners');
    const show_awardunitsCheckbox = document.getElementById('show_awardunits');
    const show_awardheirsCheckbox = document.getElementById('show_awardheirs');
    const show_awardlinesCheckbox = document.getElementById('show_awardlines');
    const show_laborunitCheckbox = document.getElementById('show_laborunit');
    const show_laborheirCheckbox = document.getElementById('show_laborheir');
    const show_levelCheckbox = document.getElementById('show_level');
    const show_moment_labelCheckbox = document.getElementById('show_moment_label');
    const show_taskCheckbox = document.getElementById('show_task');
    const show_descendant_task_countCheckbox = document.getElementById('show_descendant_task_count');
    const show_activeCheckbox = document.getElementById('show_active');
    const show_choreCheckbox = document.getElementById('show_chore');
    const show_starCheckbox = document.getElementById('show_star');
    const show_reasonunitsCheckbox = document.getElementById('show_reasonunits');
    const show_reasonheirsCheckbox = document.getElementById('show_reasonheirs');
    const show_factunitsCheckbox = document.getElementById('show_factunits');
    const show_factheirsCheckbox = document.getElementById('show_factheirs');
    const show_fund_shareCheckbox = document.getElementById('show_fund_share');
    const show_fund_onsetCheckbox = document.getElementById('show_fund_onset');
    const show_fund_ceaseCheckbox = document.getElementById('show_fund_cease');
    const show_fund_iotaCheckbox = document.getElementById('show_fund_iota');
    const show_fund_ratioCheckbox = document.getElementById('show_fund_ratio');
    const show_all_partner_credCheckbox = document.getElementById('show_all_partner_cred');
    const show_all_partner_debtCheckbox = document.getElementById('show_all_partner_debt');
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
    show_partnersCheckbox.addEventListener('change', function () { show_partners = this.checked; renderPlanTree(); });
    show_awardunitsCheckbox.addEventListener('change', function () { show_awardunits = this.checked; renderPlanTree(); });
    show_awardheirsCheckbox.addEventListener('change', function () { show_awardheirs = this.checked; renderPlanTree(); });
    show_awardlinesCheckbox.addEventListener('change', function () { show_awardlines = this.checked; renderPlanTree(); });
    show_laborunitCheckbox.addEventListener('change', function () { show_laborunit = this.checked; renderPlanTree(); });
    show_laborheirCheckbox.addEventListener('change', function () { show_laborheir = this.checked; renderPlanTree(); });
    show_levelCheckbox.addEventListener('change', function () { show_level = this.checked; renderPlanTree(); });
    show_moment_labelCheckbox.addEventListener('change', function () { show_moment_label = this.checked; renderPlanTree(); });
    show_taskCheckbox.addEventListener('change', function () { show_task = this.checked; renderPlanTree(); });
    show_descendant_task_countCheckbox.addEventListener('change', function () { show_descendant_task_count = this.checked; renderPlanTree(); });
    show_activeCheckbox.addEventListener('change', function () { show_active = this.checked; renderPlanTree(); });
    show_choreCheckbox.addEventListener('change', function () { show_chore = this.checked; renderPlanTree(); });
    show_starCheckbox.addEventListener('change', function () { show_star = this.checked; renderPlanTree(); });
    show_reasonunitsCheckbox.addEventListener('change', function () { show_reasonunits = this.checked; renderPlanTree(); });
    show_reasonheirsCheckbox.addEventListener('change', function () { show_reasonheirs = this.checked; renderPlanTree(); });
    show_factunitsCheckbox.addEventListener('change', function () { show_factunits = this.checked; renderPlanTree(); });
    show_factheirsCheckbox.addEventListener('change', function () { show_factheirs = this.checked; renderPlanTree(); });
    show_fund_shareCheckbox.addEventListener('change', function () { show_fund_share = this.checked; renderPlanTree(); });
    show_fund_onsetCheckbox.addEventListener('change', function () { show_fund_onset = this.checked; renderPlanTree(); });
    show_fund_ceaseCheckbox.addEventListener('change', function () { show_fund_cease = this.checked; renderPlanTree(); });
    show_fund_iotaCheckbox.addEventListener('change', function () { show_fund_iota = this.checked; renderPlanTree(); });
    show_fund_ratioCheckbox.addEventListener('change', function () { show_fund_ratio = this.checked; renderPlanTree(); });
    show_all_partner_credCheckbox.addEventListener('change', function () { show_all_partner_cred = this.checked; renderPlanTree(); });
    show_all_partner_debtCheckbox.addEventListener('change', function () { show_all_partner_debt = this.checked; renderPlanTree(); });
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
    loadPlanTreeData();
});

// Fetch tree data from server
async function loadPlanTreeData() {
    try {
        const response = await fetch('/api/beliefunit_view');
        beliefViewData = await response.json();
        planTreeData = beliefViewData.planroot;
        renderPlanTree();
    } catch (error) {
        console.error('Error loading tree data:', error);
        document.getElementById('planTreeContainer').innerHTML = '<p>Error loading tree data</p>';
    }
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
    const indent = '&nbsp;'.repeat(level * 2);
    const levelIndicator = show_level ? ` level${planUnit._level}` : '';
    const taskIndicator = planUnit.task && show_task ? ' TASK' : '';
    const descendant_task_countIndicator = show_descendant_task_count ? ` tasks: ${planUnit._descendant_task_count}` : '';
    const activeIndicator = planUnit._active && show_active ? '-ACTIVE' : '';
    const choreIndicator = planUnit._chore && show_chore ? '-CHORE' : '';
    const starIndicator = show_star ? ` star${planUnit.star}` : '';
    const fund_shareIndicator = show_fund_share ? ` [${planUnit.fund_share}]` : '';
    const root_booleanIndicator = planUnit.root && show_root_boolean ? '(ROOT)' : '';
    const uidIndicator = planUnit._uid && show_uid ? ` uid${planUnit._uid}` : '';

    const fund_onsetIndicator = show_fund_onset ? ` onset-${planUnit._fund_onset}` : '';
    const fund_ceaseIndicator = show_fund_cease ? ` cease-${planUnit._fund_cease}` : '';
    const fund_iotaIndicator = show_fund_iota ? ` (iota: ${planUnit.fund_iota})` : '';
    const fund_ratioIndicator = show_fund_ratio ? ` ratio-${planUnit._fund_ratio}` : '';


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
    ${taskIndicator}
    ${descendant_task_countIndicator}
    ${fund_shareIndicator}
    ${fund_onsetIndicator}
    ${fund_ceaseIndicator}
    ${fund_iotaIndicator}
    ${fund_ratioIndicator}
    ${activeIndicator}
    ${choreIndicator}
    ${root_booleanIndicator}</i>
    ${render_with_indent(planUnit.partners, indent, show_partners)}
    ${render_with_indent(planUnit.parent_rope, indent, show_parent_rope)}
    ${renderFlatReadableJson(planUnit.awardunits, indent, show_awardunits)}
    ${renderFlatReadableJson(planUnit._awardheirs, indent, show_awardheirs)}
    ${renderFlatReadableJson(planUnit._awardlines, indent, show_awardlines)}
    ${renderFlatReadableJson(planUnit.laborunit._partys, indent, show_laborunit)}
    ${renderFlatReadableJson(planUnit._laborheir._partys, indent, show_laborheir)}
    ${renderReasonReadableJson(planUnit.reasonunits, indent, show_reasonunits)}
    ${renderReasonReadableJson(planUnit._reasonheirs, indent, show_reasonheirs)}
    ${renderFlatReadableJson(planUnit.factunits, indent, show_factunits)}
    ${renderFlatReadableJson(planUnit._factheirs, indent, show_factheirs)}
    ${render_with_indent(planUnit._all_partner_cred, indent, show_all_partner_cred)}
    ${render_with_indent(planUnit._all_partner_debt, indent, show_all_partner_debt)}
    ${render_with_indent(planUnit.gogo_want, indent, show_gogo_want)}
    ${render_with_indent(planUnit.stop_want, indent, show_stop_want)}
    ${render_with_indent(planUnit._gogo_calc, indent, show_gogo_calc)}
    ${render_with_indent(planUnit._stop_calc, indent, show_stop_calc)}
    ${render_with_indent(planUnit.addin, indent, show_addin)}
    ${render_with_indent(planUnit.begin, indent, show_begin)}
    ${render_with_indent(planUnit.close, indent, show_close)}
    ${render_with_indent(planUnit.denom, indent, show_denom)}
    ${render_with_indent(planUnit.morph, indent, show_morph)}
    ${render_with_indent(planUnit.numor, indent, show_numor)}
    ${render_with_indent(planUnit._active_hx, indent, show_active_hx)}
  </div>\n
`;
    // Add children
    if (planUnit._kids) {
        Object.values(planUnit._kids).forEach(child => {
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
