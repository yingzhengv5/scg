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

@app.route("/customer/search")
def search_customer():
    # Check if a search parameter is provided in url (when user is redirected to here)
    searchCustomer = request.args.get('search_customer')
    if searchCustomer:
        connection = getCursor()
        # Search for matching customers, including partial text matches
        connection.execute("SELECT * FROM customers WHERE firstname LIKE %s OR familyname LIKE %s OR phone LIKE %s;",\
                            (f"%{searchCustomer}%", f"%{searchCustomer}%", f"%{searchCustomer}%"))
        matchedCustomers = connection.fetchall()
        return render_template("matchedcustomer.html", matched_customers = matchedCustomers)
    # Get search data if it doesn't exist
    else:
        return render_template("searchcustomer.html")
    
@app.route("/customer/add", methods=['GET','POST'])  
def add_customer():
    if request.method == "GET":
        return render_template("add_or_edit_customer.html")
    else:
        # Get customer details
        firstName = request.form.get('firstname')
        familyName = request.form.get('familyname')
        phoneNumber = request.form.get('phone')
        emailAddress = request.form.get('email')
        connection = getCursor()
        # Add to database
        connection.execute("INSERT INTO customers(firstname, familyname, email, phone) VALUES(%s,%s,%s,%s);",\
                           (firstName, familyName, emailAddress, phoneNumber))
        # return add successful information by redirect to anther route with "successful" in url  
        return redirect(url_for("add_success"))
    
@app.route("/customer/add/successful")
def add_success():
    return render_template("addsuccess.html")
    
@app.route("/customer/edit", methods=['GET','POST'])
def edit_customer():
    if request.method == 'GET':
        # For user access from search customer page directly, customerID exist
        customerID = request.args.get('customer_id')
        if customerID:
        # Retrieve customer information from database  
            connection = getCursor()
            connection.execute("SELECT * FROM customers WHERE customer_id=%s;", (customerID,))
            customer_details = connection.fetchone()
            return render_template("add_or_edit_customer.html", customer = customer_details)
        # If user accessed the edit page directly, redirect to search customer page
        else:
            return redirect(url_for('search_customer'))
        
    elif request.method == 'POST':
        # Update customer information
        customerID = request.form.get('customer_id')
        firstName = request.form.get('firstname')
        familyName = request.form.get('familyname')
        phoneNumber = request.form.get('phone')
        emailAddress = request.form.get('email')
        connection = getCursor()
        connection.execute("UPDATE customers SET firstname=%s, familyname=%s, email=%s, phone=%s WHERE customer_id=%s;",\
                        (firstName, familyName, emailAddress, phoneNumber, customerID))
        return render_template("updatesuccess.html")