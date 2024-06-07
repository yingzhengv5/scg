
# <center>Project Report</center>

## <center>Part 1: Design Decisions</center>

After walking through the brief, I decided to focus on getting the functional aspects working first and then dive into the layout later, because getting the core functionalities working first would be the key for the entire project. I knew that tweaking the layout could be time-consuming, since I'd need to continuously test and adjust it to get the desired results.

For the camplist.html, I had to consider two scenarios: whether the selected date had bookings or not. To address this, I decided to implement an if statement to control the display. I made sure to include only the essential information like name, campsite, and occupancy. There is no need to display customer ID because it’s useless for office staff; they don’t need to know that information. This way, I can keep the interface clean.

Next up was the booking process. I knew that adding a booking meant adding all nights of the booking to the database. So, I set up a loop to iterate from the first night to the last. On the bookingform.html page, I made the date field read-only to prevent users from altering it directly on that page. This ensured that the available sites always matched the selected date. According to my experience, usually after making a booking from a website, the booking details always displayed on the screen for users to review, so I made the same thing.

When it came to searching for customers, I opted for the default GET method since this part only involved displaying information. Using the %LIKE% comparison in SQL, I could match partial text to retrieve relevant customer data. However, at the beginning, I didn’t consider the full name was entered, which is the situation there should be a space between the first name and family name, so I fixed my code to ensure it can pass the full name check as well. At this point, I also noticed that editing a customer’s route would require the customer to be displayed first, so it’s an efficient way to grab the customer’s ID when displaying them and add an edit button on the same page. The edit button can direct to a new route to handle the data afterward.

For adding a customer, I implemented thorough input validation using regex patterns. This ensured that only valid data was accepted, such as letters for the name, and numbers for the phone. After clicking the update button, the updated details were displayed for user review.

As I mentioned earlier, that searching for customers and editing customers could share a template, so I merged both routes into a single "Search/Edit Customer" feature on the home page. This not only simplified the user experience but also reduced redundancy in the codebase. Additionally, the edit customer display should be the same as adding a customer, so I decided to share a template for both functions, using If statements to control the flow.

For generating reports, when I wrote this route for the first time, I only allowed the user to select one customer each time. But after rereading the page 7 requirement “Considered order and layout,” my understanding is if there are multiple reports, I should consider the order of the layout. So I decided to use a multiple select option instead; this can cater to users who may want to view multiple reports at a time. I used a left join in SQL to ensure that all selected customer reports were displayed, even if the customer had no bookings; the data should be displayed as 0. The total nights of booking are the total rows of displayed results, so I counted the ‘customer’ appears time for this data. As for average occupancy, after testing, I made only 2 decimals displayed to make the table clean. If users see multiple reports at once, the table order is descending by the nights so whoever has a booking history can be displayed prioritized.

In addition to the decisions above, I added a Go Back button to the last template of each route. This can give users an easy way back to the functional page; for example, to add another booking or edit another customer, they can click the button on the page directly as opposed to relying on the browser go-back arrow.

In terms of the user interface, I wanted to make it user-friendly. Even though this is a simple web page, the home button is still essential to make the web look more professional; "Selwyn Campground" on navbar realized this function. After I walked through the other campground websites, I made a welcome picture on the home page because I think this can create a positive first impression for visitors even though this is only for office staff use. To enhance usability, I made the navbar sticky, ensuring it remained visible as users scrolled through the content.

Consistency is the key to the entire interface design. I used justify-content-center for justification and used the same size font on the same level of text. Form elements were styled using form-control and form-label classes for a pretty look, while form-check ensured that validation feedback is reasonable.

To make tabular data more interactive, I opted for 'table-hover' and 'table-bordered' styles, enhancing readability. Additionally, I implemented a sticky-top option for multiple select, prompting users to hold Ctrl to select multiple customers, thereby improving usability and offering a guide for users.

In summary, every decision I made was meant to enhance functionality, usability, and aesthetics, creating a user-friendly and clean display on the Selwyn Camp internal system.
<br>
<br>

## <center>Part 2: Database questions</center>

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
<ul>
    <li>Table: bookings</li>
    <li>New column: order_date</li>
    <li>Data type : datetime</li>
</ul>

5.
<p>Add a login/register page with fields for a username (which can be the email address) and password for authentication. Create a separate 'users' table to store user credentials, including a securely hashed password.</p>
<p>In the 'bookings' table, add a 'payment_status' column to track the payment status of the booking, such as "paid online" or "pay upon arrival." This will help in effectively managing the payment statuses of bookings.</p>
<br>

## <center>References:</center> 

Unsplash. https://unsplash.com/photos/woman-and-a-dog-inside-outdoor-tent-near-body-of-water-eDgUyGu93Yw

Bootstrap. https://icons.getbootstrap.com/icons/house-heart-fill/