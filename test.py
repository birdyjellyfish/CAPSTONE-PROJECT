from storage import Students, Classes, Subjects, CCAs

ccas = CCAs()
students = Students()
record = {'cca_name': 'Volleyball', 'type': 'Sports'}
ccas.add(record)
member = {'student_name': 'Juan', 'cca_name': 'Volleyball', 'role': 'Captain'}
print(ccas.add_member(member))
print(ccas.get_member('Kaelin'))
