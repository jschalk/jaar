from flask import Flask, jsonify, render_template_string
from src.a03_group_logic.group import awardlink_shop
from src.a05_plan_logic.plan import planunit_shop

app = Flask(__name__)


# Create some sample data
root = planunit_shop("Project Root")
child1 = planunit_shop("Phase 1", task=True)
child2 = planunit_shop("Phase 2")
subchild1 = planunit_shop("Task 1.1", task=True)
subchild2 = planunit_shop("Task- 1.2")

# Build the tree
root.add_kid(child1)
root.add_kid(child2)
child1.add_kid(subchild1)
child1.add_kid(subchild2)

# Add some award links
root.set_awardlink(awardlink_shop("Manager", give_force=0.5, take_force=0.2))
root.set_awardlink(awardlink_shop("Team Lead", give_force=0.3, take_force=0.1))
child1.set_awardlink(awardlink_shop("Developer A", give_force=1, take_force=0.8))
subchild1.set_awardlink(awardlink_shop("Junior Dev", give_force=0.7, take_force=0.9))


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
            <input type="checkbox" id="hideAwards">
            <label for="hideAwards">Hide Award Links</label>
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
    return jsonify(root.to_dict())


if __name__ == "__main__":
    app.run(debug=True)
