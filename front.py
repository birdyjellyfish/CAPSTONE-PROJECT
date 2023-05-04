from flask import Flask, render_template, request

app = Flask(__name__)

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
            form_data = {'Activity Name': '', 
                         'Start Date': '',
                        'Description': '',
                        'End Date': ''}
            title = 'Add Activity:'
            page_type = 'form'
            form_meta = {'action': '/add?confirm', 'method': 'post'}

    if 'confirm' in request.args:
        keys = list(request.form.keys())
        page_type = 'form'
        title = 'Please confirm the following details'
        tdtype = 'hidden'
        button = 'Yes'
        form_data = {}
        for i in keys:
            form_data[f'{i}'] = request.form[f'{i}']
        form_meta = {'action': '/add?result', 'method': 'post'}

    if 'result' in request.args:
        keys = list(request.form.keys())
        ## check if record is present
        ## if record not present:
        ## add to whatever use keys = list(request.form.keys()) to get student name and cca/activity
        keys = list(request.form.keys())
        page_type = 'success'
        title = 'You have successfully added the following record!'
        form_data = {}
        for i in keys:
            form_data[f'{i}'] = request.form[f'{i}']

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
                           tdtype=tdtype)


@app.route('/view', methods=['GET', 'POST'])
def view():
    page_type = 'new'
    title = 'What would you like to view?'
    choices = ['Student', 'Class', 'CCA', 'Activity']
    form_meta = {'action': '/view?view', 'method': 'get'}
    form_data = {'choice': ''}
    data = {}
    choice = ''
    key = ''
    file = 'view.html'
    error = ''

    if request.args.get('choice') in choices:
        choice = request.args.get('choice')
        page_type = 'search'
        title = f'Please enter the {choice} you would like to search for:'
        ## .get the appropriate data from idk where juan pls help
        form_meta = {'action': '/view?searched', 'method': 'post'}

    if 'searched' in request.args:
        # get data from databases, data u get will be a dictionary, use the search method
        key = list(request.form.keys())[0]
        # key is Student Class CCA or Activity
        if request.form[key] == 'kaelin':
            title = f'{key}: {request.form[key]}'
            page_type = 'result'
        else:
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
                           error=error)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    page_type = 'new'
    title = 'What would you like to edit?'
    choices = ['Add CCA Member', 'Add Activity Participant', 'Edit CCA Member', 'Edit Activity Participant', 'Remove CCA Member', 'Remove Activity Participant']
    form_meta = {'action': '/edit?edit', 'method': 'get'}
    form_data = {'Student Name': ''}
    choice = ''
    data = None
    key = ''
    name = ''
    new = ''
    error = ''
    type = ''
    action = 'remove'
    tdtype='text'

    if request.args.get('choice') in choices:
        choice = request.args.get('choice')
        page_type = 'search'
        type = 'CCA' if choice in ['Add CCA Member', 'Edit CCA Member', 'Remove CCA Member'] else 'Activity'
        if choice in ['Add CCA Member', 'Add Activity Participant']:
            action = 'add'
            form_data['Role'] = ''
            if type == 'Activity':
                form_data['Award'] = ''
                form_data['Hours'] = ''
        elif choice in ['Edit CCA Member', 'Edit Activity Participant']:
            action  = 'edit'
        # action will remain as removed if its remove cca member/remove activity participant
        form_data[type] = ''
        title = f'Please enter the Student Name and {type}'
        form_meta = {'action': '/edit?searched', 'method': 'post'}
        
    if 'searched' in request.args:
        # if not found render error page - html file but not created yet
        #still need?? ~ Moses
        # three diff titles for edit/remove/add
        action = request.form['action']
        # keys = list(request.form.keys())
        # for item in keys:
        #     if item != 'Student Name':
        #         type = item
        page_type = 'verify'
        form_data = dict(request.form)
        form_data.pop('action')
        for item in list(form_data.keys()):
            if item != 'Student Name':
                type = item
        if action != 'add':
            form_data['Role'] ='?'
            if type == 'Activity':
                form_data['Award'] = '?'
                form_data['Hours'] = '?' # those question mark stuff get from database
  
        # check if student exists or not
        if False: # if student does not exist
            page_type = 'search'
            error = 'Student does not exist'
            title = f'Please enter the Student Name and {type}'
            form_meta = {'action': '/edit?searched', 'method': 'post'}
        else:
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
            pass # remove from database
        page_type = 'success'
        title = f'The following record has been {word}!'

    return render_template('edit.html',
                           page_type=page_type,
                           title=title,
                           choice=choice,
                           form_meta=form_meta,
                           choices=choices,
                           data=data,
                           key=key,
                           name=name,
                           new=new,
                           error=error,
                           form_data=form_data,
                           type=type,
                          action=action,
                          tdtype=tdtype)