# update.py

import mysql.connector

def update(mysql, request):
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

            return '/booking'
        else:
            cur.close()
            return '/booking'
