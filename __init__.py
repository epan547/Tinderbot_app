from flask import Flask, redirect, url_for, request, render_template
import json
from flask_wtf import Form
from wtforms import TextField
from  NamesCode.Web_Fulfilling_Name_Request import main as get_names
app = Flask(__name__)
from NamesCode.Web_Name_Feedback import main as train_names
from categories_mvp1 import main as get_category_lines
from categories_mvp1 import adjust_weight_web as train_category
from categories_mvp1 import initialize_all_dicts

#adjust_weight_web(adjust, key_word ,category_dict, pickup_line, all_dicts)
# adjust is modifier


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/display/', methods = ['POST','GET'])
def display(PULs=None,keyname=None):
    PULs = request.args['PULs']  # counterpart for url_for()
    Name = request.args['keyname']
    message = json.loads(PULs)
    if request.method == 'POST':
        # Getting weight for PUL1
        train1 = request.form.get('training1')
        modifier1 = 0
        if train1 == 'good':
            modifier1 = 2
        if train1 == 'ok':
            modifier1 = 1
        if train1 == 'bad':
            modifier1 = -2
        if train1 == 'wrong':
            modifier1 = -3
        train_names(Name,message[0],modifier1)

        # Getting weight for PUL2
        train2 = request.form.get('training2')
        modifier2 = 0
        if train2 == 'good':
            modifier2 = 2
        if train2 == 'ok':
            modifier2 = 1
        if train2 == 'bad':
            modifier2 = -2
        if train2 == 'wrong':
            modifier2 = -3
        train_names(Name,message[1],modifier2)

        # Getting weight for PUL3
        train3 = request.form.get('training3')
        modifier3 = 0
        if train3 == 'good':
            modifier3 = 2
        if train3 == 'ok':
            modifier3 = 1
        if train3 == 'bad':
            modifier3 = -2
        if train3 == 'wrong':
            modifier3 = -3
        train_names(Name,message[2],modifier3)

        return redirect(url_for('index'))
    return render_template('display.html', PULs=message)

@app.route('/namebot', methods = ['POST','GET'])
def namebot():
    if request.method == 'POST':
        # do stuff when the form is submitted
        name = request.form['keyword']
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        PULs = get_names(str(name))
        print(PULs)
        if PULs == "No Lines.":
            PULs = get_names("random")
        elif len(PULs) == 1:
            extra = get_names('random')
            PULs += extra[0:2]
        elif len(PULs) == 2:
            extra = get_names('random')
            PULs += extra[1]
        messages = json.dumps(PULs)
        return redirect(url_for('display',PULs=messages, keyname=name))

    # show the form, it wasn't submitted
    return render_template('namebot.html')

@app.route('/temp_display/', methods = ['POST','GET'])
# Used to be a temporary display, is now the display page for categories code
def temp_display(PULs=None,keyword=None):
    PULs = request.args['PULs']  # counterpart for url_for()
    keyword = request.args['keyword']
    message = json.loads(PULs) #pickuplines in readable form
    if request.method == 'POST':
        all_dicts = initialize_all_dicts()
        list_and_cat = get_category_lines(keyword)
        category_dict = list_and_cat[1]
        all_dicts = list_and_cat[2]

        # Getting weight for PUL1
        train1 = request.form.get('training1')
        modifier1 = 0
        if train1 == 'good':
            modifier1 = 2
        if train1 == 'ok':
            modifier1 = 1
        if train1 == 'bad':
            modifier1 = -2
        if train1 == 'wrong':
            modifier1 = -3
        train_category(modifier1, str(keyword) ,category_dict, message[0], all_dicts)

        # Getting weight for PUL2
        train2 = request.form.get('training2')
        modifier2 = 0
        if train2 == 'good':
            modifier2 = 2
        if train2 == 'ok':
            modifier2 = 1
        if train2 == 'bad':
            modifier2 = -2
        if train2 == 'wrong':
            modifier2 = -3
        train_category(modifier2, str(keyword) ,category_dict, message[1], all_dicts)

        # Getting weight for PUL3
        train3 = request.form.get('training3')
        modifier3 = 0
        if train3 == 'good':
            modifier3 = 2
        if train3 == 'ok':
            modifier3 = 1
        if train3 == 'bad':
            modifier3 = -2
        if train3 == 'wrong':
            modifier3 = -3
        train_category(modifier3, str(keyword) ,category_dict, message[2], all_dicts)

        return redirect(url_for('index'))
    return render_template('temp_display.html', PULs=message)

@app.route('/categorybot', methods = ['POST','GET'])
def categorybot():
    if request.method == 'POST':
        # do stuff when the form is submitted
        keyword = request.form['keyword']
        list_and_cat = get_category_lines(keyword)
        PULs = list_and_cat[0]
        if PULs is None or len(PULs) < 1:
            PULs = get_names("random")
        elif len(PULs) == 1:
            extra = get_names('random')
            PULs += extra[0:2]
        elif len(PULs) == 2:
            extra = get_names('random')
            PULs += extra[1]
        messages = json.dumps(PULs)
        return redirect(url_for('temp_display', PULs=messages, keyword=keyword))

    # show the form, it wasn't submitted
    return render_template('categorybot.html')


if __name__ == '__main__':
   app.run('0.0.0.0',debug=True)
