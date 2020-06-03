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
    address = db.relationship('Address', backref='employee', uselist=False)
    birth_date = db.Column(db.DateTime)
    salary = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, first_name, last_name, email, birth_date, salary):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.birth_date = birth_date
        self.salary = salary

    def __repr__(self):
        return f'Employee({self.first_name}, {self.last_name})'


# Address Model
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    post_code = db.Column(db.String(6), nullable=False)
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
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'birth_date', 'salary', 'created')


# Address Schema
class AddressSchema(ma.Schema):
    class Meta:
        fields = ('id', 'city', 'post_code', 'street', 'number', 'employee_id')


# Init shchemas
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
address_schema = AddressSchema()

@app.route('/employees', methods=['POST'])
def add_employee():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    birth_date_str = request.json['birth_date']
    year, month, day = birth_date_str.split('-')
    birth_date = datetime(int(year), int(month), int(day))
    salary = request.json['salary']

    employee = Employee(first_name, last_name, email, birth_date, salary)

    db.session.add(employee)
    db.session.commit()

    return employee_schema.jsonify(employee)


@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    result = employees_schema.dump(employees)
    return jsonify(result)


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


@app.route('/employees/<int:id>/address', methods=['PUT'])
def update_employee_address(id):
    pass

# Run server
if __name__ == '__main__':
    app.run(debug=True)