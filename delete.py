# delete.py
from flask import Flask, render_template, request,session, redirect, url_for
import mysql.connector

def delete(mysql, request):
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

            return render_template('/booking')
        else:
            cur.close()
            return render_template('/booking')
