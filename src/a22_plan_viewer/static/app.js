// Global state
let treeData = null;
let show_awardunits = false;
let show_awardheirs = false;
let show_awardlines = false;
let show_level = false;
let show_belief_label = false;
let show_task = false;
let show_descendant_task_count = false;
let show_active = false;
let show_chore = false;
let show_star = false;
let show_factunits = false;
let show_factheirs = false;
let show_fund_share = false;
let show_fund_onset = false;
let show_fund_cease = false;
let show_fund_iota = false;
let show_fund_ratio = false;
let show_all_partner_cred = false;
let show_all_partner_debt = false;
let show_parent_rope = false;
let show_root_boolean = false;
let show_uid = false;

// Initialize the app when DOM loads
document.addEventListener('DOMContentLoaded', function () {
    const show_awardunitsCheckbox = document.getElementById('show_awardunits');
    const show_awardheirsCheckbox = document.getElementById('show_awardheirs');
    const show_awardlinesCheckbox = document.getElementById('show_awardlines');
    const show_levelCheckbox = document.getElementById('show_level');
    const show_belief_labelCheckbox = document.getElementById('show_belief_label');
    const show_taskCheckbox = document.getElementById('show_task');
    const show_descendant_task_countCheckbox = document.getElementById('show_descendant_task_count');
    const show_activeCheckbox = document.getElementById('show_active');
    const show_choreCheckbox = document.getElementById('show_chore');
    const show_starCheckbox = document.getElementById('show_star');
    const show_factunitsCheckbox = document.getElementById('show_factunits');
    const show_factheirsCheckbox = document.getElementById('show_factheirs');
    const show_fund_shareCheckbox = document.getElementById('show_fund_share');
    const show_fund_onsetCheckbox = document.getElementById('show_fund_onset');
    const show_fund_ceaseCheckbox = document.getElementById('show_fund_cease');
    const show_fund_iotaCheckbox = document.getElementById('show_fund_iota');
    const show_fund_ratioCheckbox = document.getElementById('show_fund_ratio');
    const show_all_partner_credCheckbox = document.getElementById('_all_partner_cred');
    const show_all_partner_debtCheckbox = document.getElementById('_all_partner_debt');
    const show_parent_ropeCheckbox = document.getElementById('show_parent_rope');
    const show_root_booleanCheckbox = document.getElementById('show_root_boolean');
    const show_uidCheckbox = document.getElementById('show_uid');

    // Set up checkbox event listener
    show_awardunitsCheckbox.addEventListener('change', function () { show_awardunits = this.checked; renderTree(); });
    show_awardheirsCheckbox.addEventListener('change', function () { show_awardheirs = this.checked; renderTree(); });
    show_awardlinesCheckbox.addEventListener('change', function () { show_awardlines = this.checked; renderTree(); });
    show_levelCheckbox.addEventListener('change', function () { show_level = this.checked; renderTree(); });
    show_belief_labelCheckbox.addEventListener('change', function () { show_belief_label = this.checked; renderTree(); });
    show_taskCheckbox.addEventListener('change', function () { show_task = this.checked; renderTree(); });
    show_descendant_task_countCheckbox.addEventListener('change', function () { show_descendant_task_count = this.checked; renderTree(); });
    show_activeCheckbox.addEventListener('change', function () { show_active = this.checked; renderTree(); });
    show_choreCheckbox.addEventListener('change', function () { show_chore = this.checked; renderTree(); });
    show_starCheckbox.addEventListener('change', function () { show_star = this.checked; renderTree(); });
    show_factunitsCheckbox.addEventListener('change', function () { show_factunits = this.checked; renderTree(); });
    show_factheirsCheckbox.addEventListener('change', function () { show_factheirs = this.checked; renderTree(); });
    show_fund_shareCheckbox.addEventListener('change', function () { show_fund_share = this.checked; renderTree(); });
    show_fund_onsetCheckbox.addEventListener('change', function () { show_fund_onset = this.checked; renderTree(); });
    show_fund_ceaseCheckbox.addEventListener('change', function () { show_fund_cease = this.checked; renderTree(); });
    show_fund_iotaCheckbox.addEventListener('change', function () { show_fund_iota = this.checked; renderTree(); });
    show_fund_ratioCheckbox.addEventListener('change', function () { show_fund_ratio = this.checked; renderTree(); });
    show_all_partner_credCheckbox.addEventListener('change', function () { show_all_partner_cred = this.checked; renderTree(); });
    show_all_partner_debtCheckbox.addEventListener('change', function () { show_all_partner_debt = this.checked; renderTree(); });
    show_parent_ropeCheckbox.addEventListener('change', function () { show_parent_rope = this.checked; renderTree(); });
    show_root_booleanCheckbox.addEventListener('change', function () { show_root_boolean = this.checked; renderTree(); });
    show_uidCheckbox.addEventListener('change', function () { show_uid = this.checked; renderTree(); });

    // Load initial tree data
    loadTreeData();
});

// Fetch tree data from server
async function loadTreeData() {
    try {
        const response = await fetch('/api/tree');
        treeData = await response.json();
        renderTree();
    } catch (error) {
        console.error('Error loading tree data:', error);
        document.getElementById('treeContainer').innerHTML = '<p>Error loading tree data</p>';
    }
}

// Render the tree structure
function renderTree() {
    if (!treeData) {
        return;
    }

    const container = document.getElementById('treeContainer');
    container.innerHTML = renderPlanUnit(treeData, 0);
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
    const belief_labelHtml = render_belief_label(planUnit.belief_label, planUnit.knot, show_belief_label);

    // Start with current node
    let html = `
  <div>
    ${indent}• 
    ${belief_labelHtml}
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
    ${render_new_small_dot(planUnit.parent_rope, indent, show_parent_rope)}
    ${renderFlatReadableJson(planUnit.awardunits, indent, show_awardunits)}
    ${renderFlatReadableJson(planUnit._awardheirs, indent, show_awardheirs)}
    ${renderFlatReadableJson(planUnit._awardlines, indent, show_awardlines)}
    ${renderFlatReadableJson(planUnit.factunits, indent, show_factunits)}
    ${renderFlatReadableJson(planUnit._factheirs, indent, show_factheirs)}
    ${render_new_small_dot(planUnit._all_partner_cred, indent, show_all_partner_cred)}
    ${render_new_small_dot(planUnit._all_partner_debt, indent, show_all_partner_debt)}
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

// Render award links for a PlanUnit
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
function render_belief_label(belief_label, knot, show_belief_label) {
    if (!belief_label || !show_belief_label) {
        return '';
    }

    return ` ${knot}${belief_label}...`;
}
function render_new_small_dot(str, indent, show_bool) {
    if (!str || !show_bool) {
        return '';
    }
    return `<br>${indent}${str}`;
}
