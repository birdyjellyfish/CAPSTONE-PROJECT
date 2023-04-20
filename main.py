from flask import Flask, render_template, request

from front import *

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

@app.route('/view')
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

    if request.args.get('choice') in choices:
        choice = request.args.get('choice')
        page_type = 'result'
        title = 'The information is as follows:'
        ## .get the appropriate data from idk where juan pls help
        data={
                'Student Name':'Kaelin',
                'Student CCA': 'Band'
            }
        
    return render_template('view.html',
                          choices = choices,
                          page_type = page_type,
                          form_meta = form_meta,
                          form_data = form_data,
                          data = data,
                          title = title)


@app.route('/edit')
def edit():
    return render_template('edit.html')

if __name__ == '__main__':
    app.run('0.0.0.0')
