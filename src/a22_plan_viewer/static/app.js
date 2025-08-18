// Global state
let treeData = null;
let show_awardlinks = false;
let show_belief_label = false;
let show_task = false;
let show_star = false;

// Initialize the app when DOM loads
document.addEventListener('DOMContentLoaded', function () {
    const show_awardlinksCheckbox = document.getElementById('show_awardlinks');
    const show_belief_labelCheckbox = document.getElementById('show_belief_label');
    const show_taskCheckbox = document.getElementById('show_task');
    const show_starCheckbox = document.getElementById('show_star');

    // Set up checkbox event listener
    show_awardlinksCheckbox.addEventListener('change', function () {
        show_awardlinks = this.checked;
        renderTree();
    });
    show_belief_labelCheckbox.addEventListener('change', function () {
        show_belief_label = this.checked;
        renderTree();
    });
    show_taskCheckbox.addEventListener('change', function () {
        show_task = this.checked;
        renderTree();
    });
    show_starCheckbox.addEventListener('change', function () {
        show_star = this.checked;
        renderTree();
    });

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
    const taskIndicator = planUnit.task && show_task ? ' TASK' : '';
    const starIndicator = planUnit.star && show_star ? ` star${planUnit.star}` : '';
    // const taskIndicator = planUnit.task ? ` ${planUnit.task}` : '';

    // Build award links HTML using separate function
    const awardLinksHtml = renderAwardLinks(planUnit.awardlinks, indent, show_awardlinks);
    const belief_labelHtml = render_belief_label(planUnit.belief_label, planUnit.knot, show_belief_label);

    // Start with current node
    let html = `<div>${indent}• ${belief_labelHtml}${planUnit.plan_label}${starIndicator}${taskIndicator}${awardLinksHtml}</div>\n`;

    // Add children
    if (planUnit._kids) {
        Object.values(planUnit._kids).forEach(child => {
            html += renderPlanUnit(child, level + 1);
        });
    }

    return html;
}

// Render award links for a PlanUnit
function renderAwardLinks(awardlinks, indent, show_awardlinks) {
    if (!awardlinks || Object.keys(awardlinks).length === 0 || !show_awardlinks) {
        return '';
    }

    let html = '';
    Object.values(awardlinks).forEach(link => {
        html += `<br>${indent}&nbsp;&nbsp;<small>• ${link.awardee_title}: Take ${link.take_force}, Give ${link.give_force}</small>`;
    });

    return html;
}
function render_belief_label(belief_label, knot, show_belief_label) {
    if (!belief_label || !show_belief_label) {
        return '';
    }

    return ` ${knot}${belief_label}...`;
}
