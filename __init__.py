from flask import Flask, redirect, url_for, request, render_template
import json
from flask_wtf import Form
from wtforms import TextField
from  NamesCode.Web_Fulfilling_Name_Request import main as get_names
app = Flask(__name__)
from NamesCode.Web_Name_Feedback import main as train_names
from categories_mvp1 import main as get_category_lines

# all_dicts = initialize_all_dicts()

# inputs name, pul, value modifier

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/display/', methods = ['POST','GET'])
def display(PULs=None):
    PULs = request.args['PULs']  # counterpart for url_for()
    message = json.loads(PULs)
    if request.method == 'POST':
        #RadioField('training', choices=[('good','bad','ok','wrong')])
        train = request.form.get('training1')
        modifier = 0
        if train == 'good':
            modifier = 2
        if train == 'ok':
            modifier = 1
        if train == 'bad':
            modifier = -2
        if train == 'wrong':
            modifier = -3
        print(train,modifier)
        return redirect(url_for('index'))
    return render_template('display.html', PULs=message)

@app.route('/namebot', methods = ['POST','GET'])
def namebot():
    if request.method == 'POST':
        # do stuff when the form is submitted
        keyword = request.form['keyword']
        # name = request.form['nameword']
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        # os.system("Web_Fulfilling_Name_Request.py " + str(keyword))
        PULs = get_names(str(keyword))
        print(PULs)
        if PULs == "No Lines.":
            PULs = get_names("random")
        elif len(PULs) == 1:
            extra = get_names('random')
            PULs += extra[0:2]
        elif len(PULs) == 2:
            extra = get_names('random')
            PULs = PULs.append(extra[1])
        messages = json.dumps(PULs)
        return redirect(url_for('display',PULs=messages))

    # show the form, it wasn't submitted
    return render_template('namebot.html')


@app.route('/categorybot', methods = ['POST','GET'])
def categorybot():
    if request.method == 'POST':
        # do stuff when the form is submitted
        keyword = request.form['keyword']
        list_and_cat = get_category_lines(keyword)
        PULs = list_and_cat[0]
        cat_dict = list_and_cat[1]
        if PULs is None:
            PULs = get_names("random")
            print('hi')
        elif len(PULs) == 1:
            extra = get_names('random')
            PULs += extra[0:2]
        elif len(PULs) == 2:
            extra = get_names('random')
            PULs = PULs.append(extra[1])
            print('hello')
        print(PULs, type(PULs))
            # Replace this with the categories later
        messages = json.dumps(PULs)
        return redirect(url_for('display',PULs=messages))

    # show the form, it wasn't submitted
    return render_template('categorybot.html')


if __name__ == '__main__':
   app.run(debug = True)
   app.run()
