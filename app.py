from flask import Flask, render_template, request,session, redirect, url_for
import mysql.connector

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'qwertyuiopasdfghjklzxcvbnm'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydb'

mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.cursor()
        cur.execute("SELECT * FROM admin_panel WHERE ad_name=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['logged_in'] = True
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html', error=None)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('/'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        mobile = request.form['number']
        date = request.form['date']
        guest = request.form['guest']
        hall = request.form['hall']

        # Save the form data to the database
        cur = mysql.cursor()

        query = "SELECT id FROM booking WHERE name = %s AND mobile = %s AND date = %s AND guest = %s AND hall = %s"
        cur.execute(query, (name, mobile, date, guest, hall))
        existing_data = cur.fetchone()

        if existing_data:
            pass
        else:
            query = "INSERT INTO booking (name, mobile, date, guest, hall) VALUES (%s, %s, %s, %s, %s)"
            values = (name, mobile, date, guest, hall)
            cur.execute(query, values)

        # Commit the changes to the database
        mysql.commit()

        cur.close()

        # Redirect to the booking page after saving
        return redirect('/booking')

    return render_template('add.html')




@app.route('/booking')
def bookings():
    # Create a cursor to execute queries
    cur = mysql.cursor()

    cur.execute("SELECT id+1, name, hall, mobile, date, guest FROM booking order by date asc")
    booking = cur.fetchall()

    # Close the cursor
    cur.close()

    return render_template('booking.html', booking=booking)


@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        update_for = request.form['name']
        contact = request.form['number']
        old_date = request.form['olddate']
        old_hall = request.form['hall']
        new_date = request.form['newdate']
        new_hall = request.form['newhall']

        cur = mysql.cursor()

        cur.execute('SELECT * FROM booking WHERE name=%s AND mobile=%s AND date=%s AND hall=%s',
                    (update_for, contact, old_date, old_hall))
        existing_entry = cur.fetchone()

        if existing_entry:
            # If new_date is provided, update the date
            if new_date:
                cur.execute(
                    'UPDATE booking SET date=%s WHERE name=%s AND mobile=%s AND date=%s',
                    (new_date, update_for, contact, old_date))

            # If new_hall is provided, update the hall
            if new_hall:
                cur.execute(
                    'UPDATE booking SET hall=%s WHERE name=%s AND mobile=%s AND hall=%s',
                    (new_hall, update_for, contact, old_hall))

            mysql.commit()
            cur.close()

            return redirect('/booking')
        else:
            cur.close()
            return redirect('/booking')

@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        contact = request.form['number']
        date = request.form['date']
        hall = request.form['hall']

        # Check if the given combination of name, contact, date, and hall exists in the database

        cur = mysql.cursor()

        query = "SELECT * FROM booking WHERE name = %s AND mobile = %s AND date = %s AND hall = %s"
        cur.execute(query, (name, contact, date, hall))
        existing_data = cur.fetchone()

        if existing_data:
            # If the data exists, perform the delete operation
            delete_query = "DELETE FROM booking WHERE name = %s AND mobile = %s AND date = %s AND hall = %s"
            cur.execute(delete_query, (name, contact, date, hall))
            mysql.commit()

            cur.close()

            return redirect('/booking')
        else:
            cur.close()
            return render_template('/booking', error="Invalid Information")






@app.route('/index')
def index():
    if session.get('logged_in'):
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('/'))

@app.route('/hall1')
def hall1():
    return render_template('hall1.html')
@app.route('/hall2')
def hall2():
    return render_template('hall2.html')
@app.route('/hall3')
def hall3():
    return render_template('hall3.html')
@app.route('/hall4')
def hall4():
    return render_template('hall4.html')
@app.route('/hall5')
def hall5():
    return render_template('hall5.html')

if __name__ == '__main__':
    app.run(debug=True)
