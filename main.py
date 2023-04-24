"""from flask import Flask, render_template, request
import front

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
    form_meta={
        'action':'/add?add',
        'method': 'get'
    }
    form_data={'choice': ''}
    choices = ['CCA', 'Activity']
    button = ''
    tdtype = ''

    if request.args.get('choice') in choices:
        choice = request.args.get('choice') 
        tdtype = 'text'
        button = 'submit'
        if choice == 'CCA':
            #check if the person chose cca or actiity then render the appropriate stuff
            #later get the data back from the form again and use functions to add it to the tables
            form_data={
                'Student Name':'',
                'Student CCA': ''
            }
            title = 'Please enter the student name and student CCA'
            page_type = 'form'
            form_meta={
            'action':'/add?confirm',
            'method': 'post'
        }
        else:
            form_data={
                'Student Name':'',
                'Student Activity': ''
            }
            title = 'Please enter the student name and student activity'
            page_type = 'form'
            form_meta={
            'action':'/add?confirm',
            'method': 'post'
        }
    
    if 'confirm' in request.args:
        keys = list(request.form.keys())
        print(keys)
        page_type = 'form'
        title = 'Please confirm the following details'
        tdtype = 'hidden'
        button = 'confirm'
        form_data = {
            f'{keys[0]}': request.form[f'{keys[0]}'],
            f'{keys[1]}': request.form[f'{keys[1]}']
        }
        form_meta={
            'action':'/add?result',
            'method': 'post'
        }

    if 'result' in request.args:
        keys = list(request.form.keys())
    ## check if record is present
    ## if record not present:
        ## add to whatever use keys = list(request.form.keys()) to get student name and cca/activity
        keys = list(request.form.keys())
        page_type = 'success'
        title = 'You have successfully added the following record!'
        form_data = {
                f'{keys[0]}': request.form[f'{keys[0]}'],
                f'{keys[1]}': request.form[f'{keys[1]}']
            }

    # else:
        # page_type = ''
        # name = request.form['Student Name']
        # title = f'ERROR! The student {name} already exists'
       
    return render_template('add.html',
                           page_type = page_type,
                           title = title,
                           form_meta = form_meta,
                           form_data = form_data,
                           choices = choices,
                           button = button,
                           tdtype = tdtype
                          )

@app.route('/view', methods=['GET', 'POST'])
def view():
    page_type = 'new'
    title = 'What would you like to view?'
    choices = ['Student', 'Class', 'CCA', 'Activity']
    form_meta={
        'action':'/view?view',
        'method': 'get'
    }
    form_data={'choice': ''}
    data = {}
    choice = ''
    key = ''

    if request.args.get('choice') in choices:
        choice = request.args.get('choice')
        page_type = 'search'
        title = f'Please enter the {choice} you would like to search for:'
        ## .get the appropriate data from idk where juan pls help
        form_meta={
        'action':'/view?searched',
        'method': 'post'
    }

    if 'searched' in request.args:
        # get data from databases, data u get will be a dictionary, use the search method
        # assign it to data and it should work
        key = list(request.form.keys()) 
        data = {'name':'band', 'type': 'music', 'cca_id': '12'}
        title = f'{key[0]}: {request.form[key[0]]}'
        page_type = 'result'
        
    return render_template('view.html',
                          choices = choices,
                          page_type = page_type,
                          form_meta = form_meta,
                          form_data = form_data,
                          data = data,
                          title = title,
                          choice = choice,
                          key = key)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    page_type = 'new'
    title = 'Would you like to edit a CCA or an activity?'
    choices = ['CCA', 'Activity']
    form_meta={
        'action':'/edit?edit',
        'method': 'get'
    }
    choice = ''
    data = {}
    key = ''
    name = ''
    new = ''

    if request.args.get('choice') in choices:
        choice = request.args.get('choice')
        page_type = 'search'
        title = f'Please enter the name of the student you would like to change the {choice} of:'
        form_meta = {
            'action':'/edit?searched',
            'method': 'post'
        }

    if 'searched' in request.args:
        key = list(request.form.keys())
        page_type = 'verify'
        choice = request.form['choice']
        data = {'kaelin':'band'}
        # need if statement for either activity or cca and do the .search .find wtv
        if data is None:
            title = 'Unable to edit, student does not exist'
            page_type = ''
        else:         
            title = 'Please edit the record below'
            form_meta = {
                'action':'/edit?success',
                'method': 'post'
            }

    if 'success' in request.args:
        # do the editing
        # name is just the student name
        # new is either the new cca or new activity
        name = request.form['name']
        new = request.form['edit']
        page_type = 'success'
        title = 'The following record has been updated!'
        choice = request.form['choice']
        
    return render_template('edit.html',
                          page_type = page_type,
                          title = title,
                          choice = choice,
                          form_meta = form_meta,
                          choices = choices,
                          data = data,
                          key = key,
                          name = name,
                          new = new)


if __name__ == '__main__':
    app.run('0.0.0.0')"""

