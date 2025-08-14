from flask import Flask, jsonify, render_template_string

app = Flask(__name__)


class PlanUnit:
    def __init__(self, plan_label, chore=False):
        self.plan_label = plan_label
        self._chore = chore  # Boolean attribute
        self._awardheirs = (
            []
        )  # List of dictionaries with awardee_title, cred_weight, debt_weight
        self._kids = {}  # Dictionary of child PlanUnits

    def add_child(self, child_plan_unit):
        """Add a child PlanUnit"""
        self._kids[child_plan_unit.plan_label] = child_plan_unit

    def get_children(self):
        """Get all child PlanUnits"""
        return self._kids.values()

    def add_awardheir(self, awardee_title, cred_weight=0.0, debt_weight=0.0):
        """Add an award heir entry"""
        self._awardheirs.append(
            {
                "awardee_title": awardee_title,
                "cred_weight": cred_weight,
                "debt_weight": debt_weight,
            }
        )

    def to_dict(self):
        """Convert PlanUnit to dictionary for JSON serialization"""
        return {
            "plan_label": self.plan_label,
            "chore": self._chore,
            "awardheirs": self._awardheirs,
            "kids": {label: child.to_dict() for label, child in self._kids.items()},
        }


# Create some sample data
root = PlanUnit("Project Root")
child1 = PlanUnit("Phase 1", chore=True)
child2 = PlanUnit("Phase 2")
subchild1 = PlanUnit("ChoreT 1.1", chore=True)
subchild2 = PlanUnit("ChoreT 1.2")

# Build the tree
root.add_child(child1)
root.add_child(child2)
child1.add_child(subchild1)
child1.add_child(subchild2)

# Add some award heirs
root.add_awardheir("Manager", cred_weight=0.5, debt_weight=0.2)
root.add_awardheir("Team Lead", cred_weight=0.3, debt_weight=0.1)
child1.add_awardheir("Developer A", cred_weight=1.0, debt_weight=0.8)
subchild1.add_awardheir("Junior Dev", cred_weight=0.7, debt_weight=0.9)


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
            <label for="hideAwards">Hide Award Heirs</label>
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
