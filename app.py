from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
from datetime import date
from datetime import timedelta
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/campers", methods=['GET','POST'])
def campers():
    if request.method == "GET":
        return render_template("datepickercamper.html", currentdate = datetime.now().date())
    else:
        campDate = request.form.get('campdate')
        connection = getCursor()
        connection.execute("SELECT * FROM bookings join sites on site = site_id inner join customers on customer = customer_id where booking_date= %s;",(campDate,))
        camperList = connection.fetchall()
        return render_template("camperlist.html", camperlist = camperList)

@app.route("/booking", methods=['GET','POST'])
def booking():
    if request.method == "GET":
        return render_template("datepicker.html", currentdate = datetime.now().date())
    else:
        bookingNights = request.form.get('bookingnights')
        bookingDate = request.form.get('bookingdate')
        occupancy = request.form.get('occupancy')
        firstNight = date.fromisoformat(bookingDate)

        lastNight = firstNight + timedelta(days=int(bookingNights))
        connection = getCursor()
        connection.execute("SELECT * FROM customers;")
        customerList = connection.fetchall()
        connection.execute("select * from sites where occupancy >= %s AND site_id not in (select site from bookings where booking_date between %s AND %s);",(occupancy,firstNight,lastNight))
        siteList = connection.fetchall()
        return render_template("bookingform.html", customerlist = customerList, bookingdate=bookingDate, sitelist = siteList, bookingnights = bookingNights, occupancy = occupancy)    

@app.route("/booking/add", methods=['POST'])
def makebooking():
    # get customer booking information from bookingform
    siteId = request.form.get('site')
    customerId = request.form.get('customer')
    bookingDate = request.form.get('bookingdate')
    firstNight = date.fromisoformat(bookingDate)
    bookingNight = request.form.get('bookingnights')
    occupancy = request.form.get('occupancy')
    connection = getCursor() 
    # Add all booking nights to database
    for night in range (int(bookingNight)):
        booking_date = firstNight + timedelta(days=night)
        connection.execute("INSERT INTO bookings(site, customer, booking_date, occupancy) \
                       VALUES(%s, %s, %s, %s);",(siteId, customerId, booking_date, occupancy,))
    return render_template("bookingsuccess.html")