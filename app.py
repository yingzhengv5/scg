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
        # Get customer's booking information for the selected date
        connection.execute("SELECT * FROM bookings join sites on site = site_id inner join customers on customer = customer_id where booking_date= %s;",(campDate,))
        camperList = connection.fetchall()
        return render_template("camperlist.html", camperlist = camperList, campdate = campDate)

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
        # Check occupancy and date then display available sites
        connection.execute("select * from sites where occupancy >= %s AND site_id not in (select site from bookings where booking_date between %s AND %s);",(occupancy,firstNight,lastNight))
        siteList = connection.fetchall()
        return render_template("bookingform.html", customerlist = customerList, bookingdate = bookingDate, sitelist = siteList, bookingnights = bookingNights, occupancy = occupancy)    

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
    return redirect(url_for("booking_added"))

@app.route("/booking/add/successful")
def booking_added():
    return render_template("bookingsuccess.html")

@app.route("/customer/search")
def search_customer():
    # Set a variable to get user's input from url
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
        # Get the new customer's information and display it 
        connection.execute("SELECT * FROM customers WHERE firstname=%s AND familyname=%s AND email=%s AND phone=%s;",\
                           (firstName, familyName, emailAddress, phoneNumber))
        newCustomer = connection.fetchone()
        # return add successful information 
        return render_template("addsuccess.html", new_customer=newCustomer)
    
@app.route("/customer/edit", methods=['GET','POST'])
def edit_customer():
    # Get customerID from matched customers
    if request.method == 'GET':
        customerID = request.args.get('customer_id')
        connection = getCursor()
        connection.execute("SELECT * FROM customers WHERE customer_id=%s;", (customerID,))
        customer_details = connection.fetchone()
        return render_template("add_or_edit_customer.html", customer = customer_details)
        
    else: 
        # Update customer information in database
        customerID = request.form.get('customer_id')
        firstName = request.form.get('firstname')
        familyName = request.form.get('familyname')
        phoneNumber = request.form.get('phone')
        emailAddress = request.form.get('email')
        connection = getCursor()
        connection.execute("UPDATE customers SET firstname=%s, familyname=%s, email=%s, phone=%s WHERE customer_id=%s;",\
                        (firstName, familyName, emailAddress, phoneNumber, customerID))
        # Get the customer's updated information and display it 
        connection.execute("SELECT * FROM customers WHERE customer_id=%s;",(customerID,))
        updateCustomer = connection.fetchone()
        # return add successful information 
        return render_template("updatesuccess.html", update_customer=updateCustomer )

@app.route("/summary_report", methods=['GET','POST'])
def summary_report():
    if request.method == 'GET':
        # Show customer's names for user to choose
        connection = getCursor()
        connection.execute("SELECT * FROM customers;")
        customerList = connection.fetchall()
        return render_template("selectcustomer.html", customerlist = customerList)
    else:
        # Get all customer's id into a list
        customerIDs = request.form.getlist('customer_id')
        connection = getCursor()
        # Get required information like name, nights, avg occupancy
        # The number of times 'customer' appears in the booking table represents the total number of nights booked
        # Round two decimals for average occupancy
        sql = """ 
        SELECT c.customer_id, c.firstname, c.familyname, COUNT(b.customer) AS nights, ROUND(AVG(b.occupancy),2) AS average
        FROM customers c 
        LEFT JOIN bookings b ON c.customer_id=b.customer
        WHERE c.customer_id IN (%s) 
        GROUP BY c.customer_id 
        ORDER BY COUNT(b.customer) DESC
        """
        # Create a string of placeholders "%" with the same quantity as customerIDs
        placeholders = ", ".join(["%s"] * len(customerIDs))
        # Use placeholders variable to replace the "%"" in sql
        sql = sql % placeholders
        # Convert list to tuple so Mysql can execute it correctly
        val = tuple(customerIDs,)
        connection.execute(sql, val)
        report_details = connection.fetchall()
        return render_template("report.html", reports = report_details )    