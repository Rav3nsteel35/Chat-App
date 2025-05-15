# Regenerate the PDF decision tree file
import graphviz

# Create the decision tree diagram again
dot = graphviz.Digraph()

# Root node
dot.node("A", "Collateral?")

# Collateral = Yes branch
dot.node("B", "Income?")
dot.edge("A", "B", label="Yes")

# Income sub-branches
dot.node("C", "Yes")  # Income = High
dot.node("D", "Yes")  # Income = Low
dot.edge("B", "C", label="High")
dot.edge("B", "D", label="Low")

# Collateral = No branch
dot.node("E", "Credit?")
dot.edge("A", "E", label="No")

# Credit sub-branches
dot.node("F", "No")  # Credit = Bad
dot.node("G", "No")  # Credit = Good
dot.edge("E", "F", label="Bad")
dot.edge("E", "G", label="Good")

# Render to PDF again
pdf_output_path = '/mnt/data/decision_tree_regenerated.pdf'
dot.render(pdf_output_path, format='pdf', cleanup=False)
pdf_output_path
