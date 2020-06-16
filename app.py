from flask import Flask, request, jsonify, abort
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
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True)
    address = db.relationship('Address', backref='employee', uselist=False)
    birthDate = db.Column(db.DateTime)
    salary = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, firstName, lastName, email, birthDate, salary):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.birthDate = birthDate
        self.salary = salary

    def __repr__(self):
        return f'Employee({self.firstName}, {self.lastName})'


# Address Model
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    post_code = db.Column(db.String(6), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

    def __init__(self, city, post_code, street, number, employee_id):
        self.city = city
        self.post_code = post_code
        self.street = street
        self.number = number
        self.employee_id = employee_id

    def __repr__(self):
        return f'Address({self.city}, {self.street}, {self.number}'


# Employee Schema
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstName', 'lastName', 'email', 'birthDate', 'salary', 'created')


# Address Schema
class AddressSchema(ma.Schema):
    class Meta:
        fields = ('id', 'city', 'post_code', 'street', 'number', 'employee_id')


# Init shchemas
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
address_schema = AddressSchema()

# API Routes

@app.route('/employees', methods=['POST'])
def add_employee():
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    birthDate_str = request.json['birthDate']
    year, month, day = birthDate_str.split('-')
    birthDate = datetime(int(year), int(month), int(day))
    salary = request.json['salary']

    employee = Employee(firstName, lastName, email, birthDate, salary)

    db.session.add(employee)
    db.session.commit()

    return employee_schema.jsonify(employee)


@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    print(employees)
    result = employees_schema.dump(employees)
    return jsonify(result)


@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    if employee:    
        return employee_schema.jsonify(employee)
    else:
        abort(404)


@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)
    if employee:    
        firstName = request.json['firstName']
        lastName = request.json['lastName']
        email = request.json['email']
        birthDate_str = request.json['birthDate']
        year, month, day = birthDate_str.split('-')
        birthDate = datetime(int(year), int(month), int(day))
        salary = request.json['salary']

        employee.firstName = firstName
        employee.lastName = lastName
        employee.email = email
        employee.birthDate = birthDate
        employee.salary = salary

        db.session.commit()

        return employee_schema.jsonify(employee)
    else:
        abort(404)


@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)

    if employee:
        employee_id = employee.id
        db.session.delete(employee)

        address = Address.query.get(employee_id)
        if address:
            db.session.delete(address)
        db.session.commit()
        return jsonify({'result': 'true'})
    else:
        abort(404)


@app.route('/employees/<int:id>/address', methods=['POST'])
def add_employee_address(id):
    employee = Employee.query.get(id)

    if employee:
        city = request.json['city']
        post_code = request.json['post_code']
        street = request.json['street']
        number = int(request.json['number'])

        address = Address(city, post_code, street, number, id)

        db.session.add(address)
        db.session.commit()

        return address_schema.jsonify(address)
    else:
        abort(404)



@app.route('/employees/<int:id>/address', methods=['GET'])
def get_employee_address(id):
    employee = Employee.query.get(id)
    if employee:    
        address = Address.query.filter_by(employee_id=employee.id).first()
        if address:
            return address_schema.jsonify(address)
        abort(404)
    abort(404)


@app.route('/employees/<int:id>/address', methods=['PUT'])
def update_employee_address(id):
    employee = Employee.query.get(id)
    if employee:    
        address = Address.query.filter_by(employee_id=employee.id).first()
        if address:
            city = request.json['city']
            post_code = request.json['post_code']
            street = request.json['street']
            number = int(request.json['number'])

            address.city = city
            address.post_code = post_code
            address.street = street
            address.number = number

            db.session.commit()

            return address_schema.jsonify(address)

        abort(404)
    abort(404)


# Run server
if __name__ == '__main__':
    app.run(debug=True)
