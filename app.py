# This is the main python file for the app 
# we will import flask and sqlalchemy to use in our code
from flask import Flask, request, jsonify
from models import db, Employee
import config

app = Flask(__name__)
app.config.from_object(config.Config)
db.init_app(app)

# when debug is true we can see the error as a developer if we make it false it will just show internal error
if __name__ == '__main__':
    app.run(debug=True)

@app.before_first_request
def create_tables():
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()

# querring all the required things from the database

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([{'id': emp.id, 'name': emp.name, 'position': emp.position, 'salary': emp.salary} for emp in employees])

# int id refers to the type of data we are going to enter in that place
# to perform CRUD operation we use put get delete post

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify({'id': employee.id, 'name': employee.name, 'position': employee.position, 'salary': employee.salary})

@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    new_employee = Employee(name=data['name'], position=data['position'], salary=data['salary'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'id': new_employee.id, 'name': new_employee.name, 'position': new_employee.position, 'salary': new_employee.salary}), 201

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.json
    employee = Employee.query.get_or_404(id)
    employee.name = data['name']
    employee.position = data['position']
    employee.salary = data['salary']
    db.session.commit()
    return jsonify({'id': employee.id, 'name': employee.name, 'position': employee.position, 'salary': employee.salary})

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return '', 204


