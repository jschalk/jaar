// Global state
let treeData = null;
let hideAwards = false;

// Initialize the app when DOM loads
document.addEventListener('DOMContentLoaded', function () {
    const hideAwardsCheckbox = document.getElementById('hideAwards');

    // Set up checkbox event listener
    hideAwardsCheckbox.addEventListener('change', function () {
        hideAwards = this.checked;
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
    const taskIndicator = planUnit.task ? ' 🔧' : '';
    // const taskIndicator = planUnit.task ? ` ${planUnit.task}` : '';

    // Build award links HTML using separate function
    const awardLinksHtml = renderAwardLinks(planUnit.awardlinks, indent, hideAwards);

    // Start with current node
    let html = `<div>${indent}• ${planUnit.plan_label}${taskIndicator}${awardLinksHtml}</div>\n`;

    // Add children
    if (planUnit._kids) {
        Object.values(planUnit._kids).forEach(child => {
            html += renderPlanUnit(child, level + 1);
        });
    }

    return html;
}

// Render award links for a PlanUnit
function renderAwardLinks(awardlinks, indent, hideAwards) {
    if (!awardlinks || Object.keys(awardlinks).length === 0 || hideAwards) {
        return '';
    }

    let html = '';
    Object.values(awardlinks).forEach(link => {
        html += `<br>${indent}&nbsp;&nbsp;<small>• ${link.awardee_title}: Take ${link.take_force}, Give ${link.give_force}</small>`;
    });

    return html;
}