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
    const indent = '&nbsp;'.repeat(level * 4);
    const choreIndicator = planUnit.chore ? ' 🔧' : '';

    // Build award heirs HTML
    let awardHeirsHtml = '';
    if (planUnit.awardheirs && planUnit.awardheirs.length > 0 && !hideAwards) {
        planUnit.awardheirs.forEach(heir => {
            awardHeirsHtml += `<br>${indent}&nbsp;&nbsp;<small>• ${heir.awardee_title}: Credit ${heir.cred_weight}, Debt ${heir.debt_weight}</small>`;
        });
    }

    // Start with current node
    let html = `<div>${indent}• ${planUnit.plan_label}${choreIndicator}${awardHeirsHtml}</div>\n`;

    // Add children
    if (planUnit.kids) {
        Object.values(planUnit.kids).forEach(child => {
            html += renderPlanUnit(child, level + 1);
        });
    }

    return html;
}