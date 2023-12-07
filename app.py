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


@app.route('/update_admin_seating_chart', methods=['POST'])
def update_admin_seating_chart():
    reservation_file = './reservations.txt'
    password_file = './passcodes.txt'
    username = request.json.get('menu_option_username')
    password = request.json.get('menu_option_password')
    login_verified = False

    message = 'Printing Seating Chart...'
   
    # this is to check if the username and pass match
    with open(password_file, 'r') as file:
        for line in file:
            stored_username, stored_password = line.strip().split(', ')
            if username == stored_username and password == stored_password:
                login_verified = True
                break


    total_sales = 0
    seating_chart = [['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O']]
    # this is to update seating chart
    with open(reservation_file, 'r') as file:
        for line in file:
            name, row, column, ecode = line.strip().split(', ')
            seating_chart[int(row)][int(column)] = 'X'
            match int(column):
                case 0:
                    total_sales += 100
                case 1:
                    total_sales += 75
                case 2:
                    total_sales += 50
                case 3:
                    total_sales += 100
                case _:
                    print("There has been an invaild input, please check the txt file")

    if login_verified:
        return jsonify(seating_chart=seating_chart,message=message,total_sales=("Total Sales: $"+str(total_sales)))
    else:
        flash('Invalid username or password.')
        # return redirect(url_for('home'))  Return nothing so the error happens on the client side

@app.route('/update_reservation_seating_chart', methods=['POST'])
def update_reservation_seating_chart():
    reservation_file = './reservations.txt'
    fname = request.json.get('menu_option_FName')
    lname = request.json.get('menu_option_LName') # well guess last name isnt used.... weird
    input_seat = request.json.get('menu_option_seat')
    input_row = request.json.get('menu_option_row')
    ekey = interleave_strings(fname,"INFOTC4320")
    string_to_send = "{0}, {1}, {2}, {3}\n".format(fname,input_row,input_seat,ekey)
    

    message = ''
    # this is to update seating chart therefore make sure it runs before trying to add a new seat
    seating_chart = [['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['O','O','O','O']]
    with open(reservation_file, 'r') as file:
        for line in file:
            name, row, column, ecode = line.strip().split(', ')
            seating_chart[int(row)][int(column)] = 'X'
    if(input_seat):
        if(seating_chart[int(input_row)][int(input_seat)] == "O"):
            seating_chart[int(input_row)][int(input_seat)] = "X"
            with open(reservation_file, 'a') as f:
                f.write(string_to_send)
            message = "Congratulations {0}! Row: {1}, Seat: {2}, is now reserved for you. Enjoy your trip!\nYour eticket number is: {3}".format(fname,str(int(input_row)+1),str(int(input_seat)+1),ekey)
        else:
            message = "The Row: {0}, Seat: {1} is currently reserved by someone else. Please choose a diffrent seat".format(str(int(input_row)+1),str(int(input_seat)+1))


    return jsonify(seating_chart=seating_chart,message=message)
    

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