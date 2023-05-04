from storage import Students, Classes, Subjects, CCAs

ccas = CCAs()
students = Students()
classes = Classes()
#record = {'cca_name': 'Volleyball', 'type': 'Sports'}
member = {'student_name': 'Juan', 'cca_name': 'Volleyball', 'role': 'Captain'}
record = {'student_name': 'Kieran', 'age': 18, 
         'year_enrolled': 2022, 'grad_year': 2023,
         'class_name': '22S27'}
print(classes.get('22S27'))
# students.display_all()
