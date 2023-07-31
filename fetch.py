# fetch.py
from flask import Flask, render_template, request,session, redirect, url_for
import mysql.connector

def fetch(mysql):
    cur = mysql.cursor()

    cur.execute("SELECT id+1, name, hall, mobile, date, guest FROM booking order by date asc")
    booking = cur.fetchall()

    # Close the cursor
    cur.close()

    return render_template('/booking')
