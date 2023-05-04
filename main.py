from flask import Flask, render_template, request
from front import app


if __name__ == '__main__':
    app.run('0.0.0.0')

classes = Classes()
subjects = Subjects()
ccas = CCAs()
activities = Activities()

ccas.get('band')