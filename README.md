## Project Report – Part 1: Design Decisions

### **Functional Parts:**

• For camplist.html, two scenarios need to be considered: whether the selected date has bookings or doesn't have any bookings. Therefore, an If statement should be used for display, and only necessary information like name, campsite, and occupancy should be displayed.

• Make a booking, all nights of the booking should be added to the database, so a loop from the first night until the last night is necessary. On the bookingform.html page, I set the date to read-only to avoid users changing the date on this page while the available sites do not update accordingly. They can go back to select another date to ensure the displayed sites are always available. After submitting, a 'booking successful' message and booking details will be displayed.

• Search customer, as this part only displays information, the default GET method is suitable. Get the search data to compare with the database using %LIKE%, so with partial text matched, the appropriate customers can be displayed. When I finished this display, I noticed that editing a customer would require the customer to be displayed first, so it’s an efficient way to grab the customer’s ID when displaying them and add an edit button on the same page. The edit button will direct to a new route to handle the data afterward.

• For adding a customer, validate each input, such as allowing only letters for the name, only numbers for the phone, and ensuring the email has an @ symbol. I used some regex to set a special pattern to achieve the validation. After submitting, an 'add successful' message and customer details will be displayed.

• For editing a customer, I noticed that it would duplicate the ‘Search Customer’ display. So, I integrated both routes to make it “Search/Edit Customer.” In addition, editing a customer can share the same page with adding a customer as the required input information is the same. I used an If statement to do this.

• For the report, I decided to make a multiple select in case the user wants to see multiple reports at once. I used a left join for display because all the selected customers should be displayed even if they don’t have any bookings. In SQL booking table, each row is a booking for one night. The number of times 'customer' appears in the booking table represents the total number of nights booked. The report is ordered by booking nights descending, so all the customers who had booking history can be displayed at the top.


### **Bootstrap Layout:**

• Even though this is a simple web page, the home button is still essential to make the web look more professional, so the navbar-brand with the text “Selwyn Campground” can lead the user to the home page. A welcome picture is displayed on the home page only. The navbar is sticky to the top, so it stays displayed on the page when the user scrolls down.

• All pages use justify-content-center, and all titles use the same top margin and font size. This can make the user interface consistent throughout.

• Careful use of form-check ensures the invalid-feedback class is on the same grid with the input that needs validation. Also, form-control and form-label make the form format look nicer.

• For the table display, I chose 'table-hover' and 'table-bordered' to make it stand out and fixed the first row of the table.

• For multiple select, I put a disabled and sticky-top option “Hold Ctrl to select multiple customers” to indicate to the user that they can select multiple customers.
<br>
<br>

## Project Report – Part 2: Database questions

1.

```mysql
CREATE TABLE IF NOT EXISTS `customers` (
`customer_id` INT NOT NULL AUTO_INCREMENT,
`firstname` VARCHAR(45) NULL,
`familyname` VARCHAR(60) NOT NULL,
`email` VARCHAR(255) NULL,
`phone` VARCHAR(12) NULL,
PRIMARY KEY (`customer_id`));
```

2.

```mysql
CONSTRAINT `customer`
 FOREIGN KEY (`customer`)
 REFERENCES `scg`.`customers` (`customer_id`)
 ON DELETE NO ACTION
 ON UPDATE NO ACTION;
```

3.

```mysql
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P1', '5');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P4', '2');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P2', '3');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P5', '8');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P3', '2');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U1', '6');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U2', '2');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U3', '4');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U4', '4');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U5', '2');
```

4.

```
Table: bookings 
New column: order_date 
Data type : datetime 
```

5.
<p>Add a login/register page with fields for a username (which can be the email address) and password for authentication. Create a separate 'users' table to store user credentials, including a securely hashed password.</p>
<p>In the 'bookings' table, add a 'payment_status' column to track the payment status of the booking, such as "paid online" or "pay upon arrival." This will help in effectively managing the payment statuses of bookings.</p>
<br>

## References: 

Unsplash. https://unsplash.com/photos/woman-and-a-dog-inside-outdoor-tent-near-body-of-water-eDgUyGu93Yw

Bootstrap. https://icons.getbootstrap.com/icons/house-heart-fill/