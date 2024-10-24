# models.py
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_string = db.Column(db.String(200), nullable=False)
    rule_ast = db.Column(db.Text, nullable=False)

    def __init__(self, rule_string, rule_ast):
        self.rule_string = rule_string
        self.rule_ast = json.dumps(rule_ast.to_dict())  