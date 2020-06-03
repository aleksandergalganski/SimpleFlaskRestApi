from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import os


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)


# Employee Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True)
    address = db.relationships('Address', backref='employee', uselist=False)
    birth_date = db.Column(db.DateTime)
    salary = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(first_name, last_name, email, address, birth_date, salary):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.birth_date = birth_date
        self.salary = salary

    def __repr__(self):
        return f'Employee({self.first_name}, {self.last_name})'


# Address Model
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    post_code = db.Column(db.Sting(6), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

    def __init__(self, city, post_code, street, number):
        self.city = city
        self.post_code = post_code
        self.street = street
        self.number = number
        
    def __repr__(self):
        return f'Address({self.city}, {self.street}, {self.number}'


# Employee Schema
class EmployeeSchema(ma.Schema):
    pass


# Address Schema
class AddressSchema(ma.Schema):
    pass


@app.route('/employees', method=['POST'])
def add_employee():
    pass


@app.route('/employees', methods=['GET'])
def get_employees():
    pass


@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    pass


@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    pass


@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    pass
# Delete also address asociated with employee


@app.route('/employees/<int:id>/address', methods=['GET'])
def get_employee_address(id):
    pass


@app.route('employees/<int:id>/address', methods=['PUT'])
def update_employee_address(id):
    pass