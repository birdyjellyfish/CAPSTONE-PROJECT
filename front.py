from flask import Flask, render_template, request
from datetime import datetime
from storage import Students, Classes, Subjects, CCAs, Activities

classes = Classes()
subjects = Subjects()
ccas = CCAs()
activities = Activities()
students = Students()

app = Flask(__name__)


def validate_date(date: str):
    """Validate a given date based on ISO 8601 YYYY-MM-DD format"""
    date = date.strip()

    format = "%Y-%m-%d"
    try:
        res = bool(datetime.strptime(date, format))
    except ValueError:
        res = False

    if res:
        year, month, day = date.split('-')
        if len(year) == 4 and len(month) == 2 and len(day) == 2:
            return True
    return False


def has_error(data: dict):
    '''
    Checks if items in a dict are empty and removes whitespace
    Returns an error message for the last value that is empty, otherwise returns False
    '''
    for key, value in data.items():
        data[key] = value.strip()  #remove accidental whitespace
        if not value:
            return f'Please do not leave the {key} empty'
    return False


@app.route('/')
def index():
    '''
    displays the index page at /
    '''
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    page_type = 'new'
    title = 'What would you like to add?'
    form_meta = {'action': '/add?add', 'method': 'get'}
    form_data = {'choice': ''}
    choices = ['CCA', 'Activity']
    button = ''
    tdtype = ''
    error = ''

    if request.args.get('choice') in choices:
        choice = request.args.get('choice')
        tdtype = 'text'
        button = 'Submit'
        if choice == 'CCA':
            #check if the person chose cca or actiity then render the appropriate stuff
            #later get the data back from the form again and use functions to add it to the tables
            form_data = {'CCA Name': '', 'CCA Type': ''}
            title = 'Add CCA:'
            page_type = 'form'
            form_meta = {'action': '/add?confirm', 'method': 'post'}
        else:
            form_data = {
                'Activity Name': '',
                'Start Date': '',
                'Description': '',
                'End Date': ''
            }
            title = 'Add Activity:'
            page_type = 'form'
            form_meta = {'action': '/add?confirm', 'method': 'post'}

    if 'confirm' in request.args:
        page_type = 'form'
        title = 'Please confirm the following details'
        tdtype = 'text'
        button = 'Submit'
        form_data = dict(request.form)
        error = has_error(form_data)
        if 'Activity Name' in form_data.keys():  # validate date if activity
            if not form_data['End Date']:
                error = 'Please ensure the date is in the correct format'

        if error:  # if there is an error, return to new form page
            form_meta = {'action': '/add?confirm', 'method': 'post'}
        else:  # otherwise, move on
            form_meta = {'action': '/add?result', 'method': 'post'}
            tdtype = 'hidden'
            button = 'Yes'

    if 'result' in request.args:
        ## check if record is present
        form_data = dict(request.form)
        if ccas.add({
                'cca_name': form_data['CCA Name'],
                'type': form_data['CCA Type']
        }) != False:  #will return False if cca already exists
            page_type = 'success'
            title = 'You have successfully added the following record!'
        else:
            title = f'ERROR! The CCA {form_data["CCA Name"]} already exists'
    # else:
    # page_type = ''
    # name = request.form['Student Name']
    # title = f'ERROR! The student {name} already exists'

    return render_template('add.html',
                           page_type=page_type,
                           title=title,
                           form_meta=form_meta,
                           form_data=form_data,
                           choices=choices,
                           button=button,
                           tdtype=tdtype,
                           error=error)


@app.route('/view', methods=['GET', 'POST'])
def view():
    page_type = 'new'
    title = 'What would you like to view?'
    choices = ['Student', 'Class', 'CCA', 'Activity']
    form_meta = {'action': '/view?view', 'method': 'get'}
    form_data = {'choice': ''}
    table_header = {}
    data = {}
    choice = ''
    key = ''
    file = 'view.html'
    error = ''

    if request.args.get('choice') in choices:
        choice = request.args.get('choice')
        page_type = 'search'
        title = f'Which {choice} you would like to search for?'
        ## .get the appropriate data from idk where juan pls help
        form_meta = {'action': '/view?searched', 'method': 'post'}

    if 'searched' in request.args:
        # get data from databases, data u get will be a dictionary, use the search method
        key = list(request.form.keys())[0]
        form_data = dict(request.form)
        # key is Student Class CCA or Activity
        if key == 'Student':
            table_header = {'student_name': 'Student Name',
                            'age': 'Age',
                            'year_enrolled': 'Year Enrolled',
                           'grad_year': 'Graduation Year',
                           'class_name': 'Class',
                           'student_id': 'Student ID'}
            data = students.get(form_data[key])
        elif key == 'Class':
            table_header = {'class_name': 'Class',
                            'level': 'Level',
                           'class_id': 'Class ID'}
            data = classes.get_info(form_data[key])
        elif key == 'CCA':
            table_header = {'cca_name': 'CCA Name',
                            'type': 'Type',
                           'cca_id': 'CCA ID'}
            data = ccas.get(form_data[key])
        else:
            table_header = {'activity_name': 'Activity Name',
                            'start_date': 'Start Date',
                           'end_date': 'End Date',
                           'description': 'Description',
                           'activity_id': 'Activity ID'}
            data = activities.get(form_data[key])

        if data:  # if in database
            title = f'{key}: {form_data[key]}'
            page_type = 'result'
            # get from database
        else:  # if not in database, user will re-enter the form
            page_type = 'search'
            error = f'{key} does not exist'
            choice = key
            title = f'Please enter the {key} you would like to search for:'
            form_meta = {'action': '/view?searched', 'method': 'post'}

    return render_template(file,
                           choices=choices,
                           page_type=page_type,
                           form_meta=form_meta,
                           form_data=form_data,
                           data=data,
                           title=title,
                           choice=choice,
                           key=key,
                           error=error,
                           table_header=table_header)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    page_type = 'new'
    title = 'What would you like to edit?'
    choices = [
        'Add CCA Member', 'Add Activity Participant', 'Edit CCA Member',
        'Edit Activity Participant', 'Remove CCA Member',
        'Remove Activity Participant'
    ]
    form_meta = {'action': '/edit?edit', 'method': 'get'}
    form_data = {'Student Name': ''}
    choice = ''
    key = ''
    error = ''
    type = ''
    action = 'remove'
    tdtype = 'text'

    if request.args.get('choice') in choices:
        choice = request.args.get('choice')
        page_type = 'search'
        type = 'CCA' if choice in [
            'Add CCA Member', 'Edit CCA Member', 'Remove CCA Member'
        ] else 'Activity'
        if choice in ['Add CCA Member', 'Add Activity Participant']:
            action = 'add'
            form_data['Role'] = ''
            if type == 'Activity':
                form_data['Award'] = ''
                form_data['Hours'] = ''
        elif choice in ['Edit CCA Member', 'Edit Activity Participant']:
            action = 'edit'
        # action will remain as removed if its remove cca member/remove activity participant
        form_data[type] = ''
        title = f'Please enter the Student Name and {type}'
        form_meta = {'action': '/edit?searched', 'method': 'post'}

    if 'searched' in request.args:
        action = request.form['action']
        page_type = 'verify'
        form_data = dict(request.form)
        form_data.pop('action')
        error = has_error(form_data)
        type = 'Activity' if 'Hours' in form_data.keys() else 'CCA'

        if False:  # if student does not exist
            error = 'Student does not exist'
        if error:
            form_meta = {'action': '/edit?searched', 'method': 'post'}
        else:
            if action != 'add':
                form_data['Role'] = '?'
                if type == 'Activity':
                    form_data['Award'] = '?'
                    form_data[
                        'Hours'] = '?'  # those question mark stuff get from database
            form_meta = {'action': '/edit?success', 'method': 'post'}

        if action == 'add':
            title = 'Please confirm that you would like to add the following'
            tdtype = 'hidden'
        elif action == 'edit':
            title = 'Please edit the following details'
        else:
            title = 'Please confirm that you would like to delete the following record'
            tdtype = 'hidden'

    if 'success' in request.args:
        action = request.form['action']
        form_data = dict(request.form)
        form_data.pop('action')
        # edit the data from the database
        if action == 'add':
            word = 'added'
            pass
            # add form_data into database
        elif action == 'edit':
            word = 'edited'
            pass
            # edit new data
        elif action == 'remove':
            word = 'removed'
            pass  # remove from database
        page_type = 'success'
        title = f'The following record has been {word}!'

    return render_template('edit.html',
                           page_type=page_type,
                           title=title,
                           choice=choice,
                           form_meta=form_meta,
                           choices=choices,
                           key=key,
                           error=error,
                           form_data=form_data,
                           action=action,
                           tdtype=tdtype)
