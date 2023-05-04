from storage import Students, Classes, Subjects, CCAs, Activities

ccas = CCAs()
students = Students()
classes = Classes()
activities = Activities()
print(ccas.get_student('Kieran'))
print(classes.get('22S27'))
