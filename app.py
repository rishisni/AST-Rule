# from flask import Flask, request, jsonify, render_template
# from models import db, Rule
# from rule_ast import create_rule, combine_rules, evaluate_rule

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rules.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize the database
# db.init_app(app)

# # @app.before_first_request
# # def create_tables():
# #     db.create_all()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/create_rule', methods=['POST'])
# def create_rule_api():
#     rule_string = request.json.get('rule')
#     if not rule_string:
#         return jsonify({"error": "Rule is missing"}), 400
    
#     # Parse the rule and create the AST
#     rule_ast = create_rule(rule_string)
    
#     # Check if the rule_ast is None, indicating a parsing error
#     if rule_ast is None:
#         return jsonify({"error": "Failed to parse rule"}), 400
    
#     # Check if rule_ast has a to_dict method
#     if not hasattr(rule_ast, 'to_dict'):
#         return jsonify({"error": "Invalid rule AST format"}), 500
    
#     try:
#         # Convert rule AST to dictionary
#         rule_ast_dict = json.dumps(rule_ast.to_dict())
        
#         # Save the rule to the database
#         new_rule = Rule(rule_string=rule_string, rule_ast=rule_ast_dict)
#         db.session.add(new_rule)
#         db.session.commit()
        
#         return jsonify({"message": "Rule created successfully!"}), 201
#     except Exception as e:
#         # Catch any other errors
#         return jsonify({"error": str(e)}), 500


# @app.route('/evaluate_rule', methods=['POST'])
# def evaluate_rule_api():
#     rule_id = request.json.get('rule_id')
#     data = request.json.get('data')  # This would contain user attributes like age, department, etc.

#     if not rule_id or not data:
#         return jsonify({"error": "Rule ID or data is missing"}), 400

#     # Fetch the rule from the database
#     rule = Rule.query.filter_by(id=rule_id).first()
#     if not rule:
#         return jsonify({"error": "Rule not found"}), 404

#     # Evaluate the rule against the user data
#     rule_ast = rule.get_ast()
#     result = evaluate_rule(rule_ast, data)
#     return jsonify({"result": result})



# @app.route('/combine_rules', methods=['POST'])
# def combine_rules_api():
#     rule_ids = request.form.getlist('rule_ids')
    
#     # Fetch all rules to combine
#     rules = Rule.query.filter(Rule.id.in_(rule_ids)).all()
#     rule_asts = [rule.get_ast() for rule in rules]

#     # Combine them
#     combined_ast = combine_rules(rule_asts)

#     # Store combined rule in DB
#     combined_rule = Rule(rule_string="Combined Rule", rule_ast=combined_ast)
#     db.session.add(combined_rule)
#     db.session.commit()

#     return jsonify({"message": "Rules combined successfully!", "combined_rule_id": combined_rule.id})


# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()  # Create tables if they don't exist
#     app.run(debug=True)

# app.py
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, Rule
from parser import parse_rule_string_to_ast
from evaluator import evaluate_rule  # Assuming you have an evaluate_rule function implemented
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rules.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json.get('rule_string')
    rule_ast = request.json.get('rule_ast')  # Assuming this is coming from the request

    if isinstance(rule_ast, str):
        # If rule_ast is a string, use it directly
        rule_ast_json = rule_ast
    else:
        # If it's an object, ensure it has the to_dict() method
        rule_ast_json = json.dumps(rule_ast.to_dict())

    new_rule = Rule(rule_string=rule_string, rule_ast=rule_ast_json)
    # Add additional logic to save the new_rule as needed



@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_route():
    rule_id = request.json.get('rule_id')
    data = request.json.get('data')  # Data in JSON format

    rule = Rule.query.get(rule_id)
    if not rule:
        return jsonify({"error": "Rule not found"}), 404

    rule_ast = json.loads(rule.rule_ast)  # Load the AST from the database

    try:
        result = evaluate_rule(rule_ast, data)  # Evaluate the rule against the provided data
        return jsonify({"evaluation_result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/rules', methods=['GET'])
def get_rules():
    rules = Rule.query.all()
    return jsonify([{"id": rule.id, "rule_string": rule.rule_string, "rule_ast": json.loads(rule.rule_ast)} for rule in rules])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
