from flask import Flask, request, redirect, render_template, session, flash
import re
import pprint
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'emailvalid')
app.secret_key = "2145sdsd54s5d45sd"

@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/success')
def display():
    query = "SELECT email, date_format(created_at, '%c/%d/%y %r') as date  FROM emailvalid;"
    emails = mysql.query_db(query)
    new_email =emails[len(emails)-1]['email']
    return render_template('success.html', emails = emails, new_email = new_email)


@app.route('/email', methods=['POST'])
def create():
    
    email = request.form['email']
    email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    if len(email) < 1:
        flash(u"Your email cannot be empty!","error")
    else:
        if not email_regex.match(email):
            flash(u"Email is not valid!","error")
        else:
            
            query = "SELECT email FROM emailvalid"
            emails = mysql.query_db(query)
            found_email = False
            for n in emails:
                if email == n['email']:
                    found_email = True
                    flash(u"Email is existed in database!","error")

            if not found_email:
                
                query = "INSERT INTO emailvalid (email, created_at) VALUES (:email,NOW())"           
                
                data = {
                        'email': email,
                    }
                
                mysql.query_db(query, data)
                return redirect('/success')
    return redirect('/')


app.run(debug=True)
