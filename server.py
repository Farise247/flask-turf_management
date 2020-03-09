from flask import *
from flask_table import Table, Col
app = Flask(__name__)
app.secret_key="skjkfhhaskughwargr"

class Results(Table):
    id = Col('Id', show=False)
    date = Col('Date Of Booking')
    name = Col('Name')
    turf_location = Col('Turf Location')

@app.route('/view_booking')
def view():
    fin = open('booking_history.txt','r')
    data = fin.read()
    data = data.split("\n")
    for i in range(len(data)):
        data[i] = data[i].split(",")

    return render_template('disp-details.html', data=data)

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin_login.html')

@app.route('/login_admin', methods = ['POST'])
def login_admin():
    usr = request.form['name']
    password = request.form['password']
    if(usr == 'crack' and password == 'thermo-flask'):
        
        resp =  make_response(render_template('admin_home.html'))
        resp.set_cookie("userID",usr)
        session['username'] = usr
        return resp
    else:
        return "Login Error!"

@app.route('/add_manager')
def add_manager_temp():
    return render_template('add_manager.html')

@app.route('/added_manager', methods = ['GET'])
def add_manager():
    turf_location = request.args.get('turf_location')
    manager_name = request.args.get('manager_name')
    password = request.args.get('password')
    
    fin = open('manager_details.txt','a')
    fin.write(str(turf_location)+",")
    fin.write(str(manager_name)+",")
    fin.write(str(password)+"\n")
    fin.close()

    return redirect(url_for('home'))

@app.route('/price_list')
def price_home():
    return render_template('price_list.html')

@app.route('/added_pricelist', methods = ['GET'])
def add_price():
    turf_location = request.args.get('turf_location')
    price = request.args.get('price')
    seats = request.args.get('seats')

    fin = open('price_list.txt','a')
    fin.write(str(turf_location)+",")
    fin.write(str(price)+",")
    fin.write(str(seats)+"\n")
    fin.close()

    return redirect(url_for('home'))

@app.route('/manager')
def manager():
    return render_template('manager_login.html')

@app.route('/login_manager', methods = ['POST'])
def login_manager():
    usr = request.form['name']
    password = request.form['password']

    fin = open('manager_details.txt','r')
    data = fin.read()
    data = data.split("\n")
    for i in range(len(data)):
        data[i] = data[i].split(",")
        if(data[i][1]==usr):
            if(data[i][2]==password):
                return render_template('manager_home.html')
            else:
                app.logger.info(data[i][1])
                return "Login Error!"

@app.route('/manager_home')
def manager_home():
    return render_template('manager_home.html')
    
@app.route('/logout')
def logout():
    session.pop('username',None)
    return render_template('logout.html')    

@app.route('/check_rates')
def check_rates():
    return render_template('check_rates.html')

@app.route('/checking_rates', methods = ['GET'])
def checking_rates():
    turf_location = request.args.get('turf_location')

    fin = open('price_list.txt','r')
    data = fin.read()
    data = data.split("\n")
    for i in range(len(data)):
        data[i] = data[i].split(",")
        if(data[i][0] == turf_location):
            return render_template('display_rate.html', price = data[i][1])
    return "Error in Location Entered"
    

@app.route('/user')
def user():
    return render_template('user_landing.html')

@app.route('/user/login')
def user_signin():
    return render_template('user_login.html')

@app.route('/user/home')
def user_home():
    return render_template('user_home.html')

@app.route('/login_user', methods = ['POST'])
def login_user():
    usr = request.form['name']
    password = request.form['password']

    fin = open('user_details.txt','r')
    data = fin.read()
    data = data.split("\n")
    for i in range(len(data)):
        data[i] = data[i].split(",")
        if(data[i][0]==usr):
            if(data[i][1]==password):
                return render_template('user_home.html')
            else:
                app.logger.info(data[i][1])
                return "Login Error!"  

@app.route('/user/check_rates')
def user_rate():
    return render_template('user-check-rates.html')

@app.route('/user/checking/rates', methods = ['GET'])
def user_schecking_rates():
    turf_location = request.args.get('turf_location')

    fin = open('price_list.txt','r')
    data = fin.read()
    data = data.split("\n")
    for i in range(len(data)):
        data[i] = data[i].split(",")
        if(data[i][0] == turf_location):
            return render_template('user-display-rate.html', price = data[i][1])
    return "Error in Location Entered"


@app.route('/availability/form')
def available():
    return render_template('availability-form.html')

@app.route('/availability/disp')
def available_display():
    turf_location = request.args.get('turf_location')

    fin = open('price_list.txt','r')
    data = fin.read()
    data = data.split("\n")
    for i in range(len(data)):
        data[i] = data[i].split(",")
        if(data[i][0] == turf_location):
            return render_template('display-avail.html', seats = data[i][2])
    return "Error in Location Entered"
    
@app.route('/book/turf/form')
def book_turf():
    return render_template('book-turf.html')

@app.route('/booking/turf')
def booking():
    turf_location = request.args.get('turf_location')
    name = request.args.get('name')
    date = request.args.get('date')

    fin = open('booking_history.txt','a')
    fin.write(str(date)+",")
    fin.write(str(name)+",")
    fin.write(str(turf_location)+"\n")

    fin.close()

    return render_template('booking-success.html')






if(__name__ == '__main__'):
    app.run(debug = True, port = 8000)
