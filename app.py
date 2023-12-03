from flask import Flask, render_template, request, url_for, flash, redirect, abort, send_file
from flask import jsonify


# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

# it was getting clutterd so heres a bit of cleanup
def interleave_strings(str1, str2):
    result = ''
    min_len = min(len(str1), len(str2))

    for i in range(min_len):
        result += str1[i] + str2[i]

    result += str1[min_len:] + str2[min_len:]

    return result

@app.route('/home_btn_selector', methods=['POST'])
def home_btn_selector():
    menu_option = request.form['menu_option']
    
    if(menu_option == 'admin'):
        return redirect(url_for('admin'))
    elif(menu_option == 'reserve'):
        return redirect(url_for('reservation'))
    else:
        flash('Invaild option selected.')

    return redirect(url_for('home'))


@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/reservation')
def reservation():
    return render_template('reservations.html')
@app.route('/')
def home():
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002,debug=True, use_reloader=True)