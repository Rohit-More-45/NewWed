# add.py
from flask import Flask, render_template, request,session, redirect, url_for
import mysql.connector

@app.route()
def add(mysql, request):
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
        return render_template('/booking')

    return 'add.html'