from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:shubhangi%4097@localhost:3306/pythondb1'
db = SQLAlchemy(app)

# Define the model for student registration
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    institute = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)

@app.route("/enter")
def getHome():
    return render_template('home.html')
@app.route('/register', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        institute = request.form['institute']
        course = request.form['course']

        new_student = Student(name=name, email=email, institute=institute, course=course)
        db.session.add(new_student)
        db.session.commit()

        return 'Student registered successfully!'
    return render_template('register.html')

# API endpoint to get all student registrations
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    result = [{'id': student.id, 'name': student.name, 'email': student.email,
               'institute': student.institute, 'course': student.course}
              for student in students]
    return jsonify(result)

# API endpoint to add a new student registration
@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    new_student = Student(name=data['name'], email=data['email'],
                          institute=data['institute'], course=data['course'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student added successfully'})

# API endpoint to delete a student registration
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted successfully'})
    else:
        return jsonify({'message': 'Student not found'})

# API endpoint to update a student registration
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if student:
        data = request.json
        student.name = data['name']
        student.email = data['email']
        student.institute = data['institute']
        student.course = data['course']
        db.session.commit()
        return jsonify({'message': 'Student updated successfully'}), 200
    else:
        return jsonify({'message': 'Student not found'}),

# API endpoint to get students by course
@app.route('/students/course/<string:course>', methods=['GET'])
def get_students_by_course(course):
    students = Student.query.filter_by(course=course).all()
    if students:
        result = [{'id': student.id, 'name': student.name, 'email': student.email,
                   'institute': student.institute, 'course': student.course}
                  for student in students]
        return jsonify(result)
    else:
        return jsonify({'message': 'No students found for the given course'}), 404

if __name__ == "__main__":
    app.run(debug=True)
