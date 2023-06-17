import datetime
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QIcon
import psycopg2
import re
from datetime import date, datetime

current_date = date.today()

# Define the global variable
logged_in_username = None
logged_in_password = None

def execute_query_fetch(query):
    conn = psycopg2.connect(host='localhost', user='postgres', password='password', dbname='cms')
    cursor = conn.cursor()

    try:
        # Execute the query
        cursor.execute(query)

        # Fetch the results if needed
        results = cursor.fetchall()

        # Commit the changes
        conn.commit()

        # Return the results if needed
        return results

    except psycopg2.Error as e:
        # Handle any errors that occur during execution
        print(f"Error executing query: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

def execute_query(query):
    conn = psycopg2.connect(host='localhost', user='postgres', password='password', dbname='cms')
    cursor = conn.cursor()

    try:
        # Execute the query
        cursor.execute(query)

        # Commit the changes
        conn.commit()

        # Return True to indicate successful execution
        return True

    except psycopg2.Error as e:
        # Handle any errors that occur during execution
        print(f"Error executing query: {e}")

        # Return False to indicate failed execution
        return False

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

def get_current_user_id():

    username = logged_in_username
    password = logged_in_password
    query = f"SELECT user_id FROM USERS WHERE user_username = '{username}' AND  user_password = '{password}'"

    result = execute_query_fetch(query)

    if result:
        user_id = result[0][0]
        return user_id
    else:
        return None
def show_page(frame):
    widget.addWidget(frame)
    widget.setCurrentIndex(widget.currentIndex() + 1)

def goto_admin_dash():
    admin_dash = AdminDash()
    show_page(admin_dash)

def show_error_message(message):
    message_box = QtWidgets.QMessageBox()
    message_box.critical(None, "Error", message)
    message_box.setStyleSheet("QMessageBox { background-color: white; }")

def show_success_message(message):
    message_box = QtWidgets.QMessageBox()
    message_box.setWindowTitle("Success")
    message_box.setText(message)
    icon = QIcon("images/check.png")  # Replace "path/to/icon.png" with the actual path to your icon file
    message_box.setIconPixmap(icon.pixmap(64, 64))  # Set the icon to a custom pixmap

    ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
    message_box.setDefaultButton(ok_button)
    message_box = message_box
    message_box.exec_()

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("gui/login.ui", self)
        self.registerbtn.clicked.connect(self.goto_registration_page)
        self.loginbtn.clicked.connect(self.login)

    def goto_registration_page(self):
        register = Register()
        show_page(register)

    def goto_dashboard(self):
        dashboard = AdminDash()
        show_page(dashboard)

    def login(self):
        # Access the global variables
        global logged_in_username
        global logged_in_password

        username = self.inputusername.text()
        password = self.inputpass.text()

        try:
            # Check for null values in input fields
            if any(value == "" for value in [username, password]):
                # Display error message for null values
                error_message = "Please fill in all fields."
                show_error_message(error_message)
                return

            # Query to check if username and password exist and user_is_admin and is_account_admin are True
            query = f"SELECT * FROM USERS WHERE USER_USERNAME = '{username}' AND USER_PASSWORD = '{password}' AND USER_IS_ADMIN = 't'"

            # Fetch the results
            results = execute_query_fetch(query)

            # Check if a matching row is found
            if results:
                # Store the values in global variables
                logged_in_username = username
                logged_in_password = password

                # Successful login, redirect to dashboard
                self.goto_dashboard()

            else:
                # If no matching row found, then either the user credentials are invalid or the account is not admin
                # Check if the issue is with admin access
                query = f"SELECT * FROM USERS WHERE USER_USERNAME = '{username}' AND USER_PASSWORD = '{password}'"
                results = execute_query_fetch(query)
                if results:
                    error_message = "You are not authorized to access the admin dashboard."
                else:
                    # Invalid login, show error message
                    error_message = "Invalid username or password. Please try again."

                show_error_message(error_message)

        except Exception as e:
            # Handle any exceptions during database operations
            error_message = f"An error occurred: {str(e)}"
            show_error_message(error_message)


class Register(QMainWindow):
    def __init__(self):
        super(Register, self).__init__()
        loadUi("gui/registration.ui", self)
        self.registerbtn.clicked.connect(self.register_now)
        self.backbtn.clicked.connect(self.goto_login_page)
        self.message_box = None

    def goto_login_page(self):
        login = Login()
        show_page(login)

    def register_now(self):
        first_name = self.txtfname.text()
        last_name = self.txtlname.text()
        mid_name = self.txtmid.text()
        number = self.txtnumber.text()
        address = self.txtaddress.text().lower()
        username = self.txtusername.text()
        password = self.txtpass.text()
        confirmpass = self.txtconfirm.text()

        try:
            # Check for null values in input fields
            if any(value == "" for value in [first_name, last_name, number, address, username, password, confirmpass]):
                # Display error message for null values
                error_message = "Please fill in all fields."
                show_error_message(error_message)
                return

            if not (first_name.replace(" ", "").isalpha() and last_name.isalpha() and (mid_name == "" or mid_name.isalpha())):
                # Display error message for non-letter values
                error_message = "Name fields should only contain letters."
                show_error_message(error_message)
                return

            # Validate number field
            if not number.isdigit():
                # Display error message for non-digit number
                error_message = "Mobile Number should only contain digits."
                show_error_message(error_message)
                return

            # Validate email address
            email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_regex, address):
                error_message = "Invalid email address. Please enter a valid email."
                show_error_message(error_message)
                return

            if password == confirmpass:
                # Insert the data into the USERS table
                insert_query = f"INSERT INTO USERS (USER_FNAME, USER_MNAME, USER_LNAME, USER_NUMBER, USER_EMAIL, " \
                               f"USER_USERNAME, USER_PASSWORD, USER_IS_ADMIN, USER_CREATED_AT, USER_UPDATED_AT) " \
                               f"VALUES ('{first_name}', '{mid_name}', '{last_name}', '{number}', '{address}', " \
                               f"'{username}', '{password}', 't', '{current_date}', '{current_date}')"

                # Execute the query and check if it was successful
                if execute_query(insert_query):
                    # Registration successful message
                    success_message = "Registration Successful!"
                    show_success_message(success_message)

                    self.goto_login_page()
                else:
                    # Error message for failed execution
                    error_message = "Registration failed. Please try again."
                    show_error_message(error_message)

            else:
                # Passwords don't match, show error message
                error_message = "Passwords do not match. Please try again."
                show_error_message(error_message)

        except (Exception, psycopg2.Error) as error:
            # Error message in case of failure
            QtWidgets.QMessageBox.critical(self, "Error", f"Registration Failed!\n\nError Message: {str(error)}")

class AdminDash(QMainWindow):
    def __init__(self):
        super(AdminDash, self).__init__()
        loadUi("gui/admindash.ui", self)
        self.record_man_btn.clicked.connect(self.goto_record_management)
        self.plot_man_btn.clicked.connect(self.goto_plot_management)
        self.reser_man_btn.clicked.connect(self.goto_reservation_management)
        self.booking_man_btn.clicked.connect(self.goto_booking_management)
        self.logoutbtn.clicked.connect(self.goto_login_page)

    def goto_record_management(self):
        record_management = Record_management()
        show_page(record_management)

    def goto_plot_management(self):
        plot_management = Plot_management()
        show_page(plot_management)

    def goto_reservation_management(self):
        reservation = Reservation_management()
        show_page(reservation)

    def goto_booking_management(self):
        booking = Booking_management()
        show_page(booking)

    def goto_login_page(self):
        login = Login()
        show_page(login)

class Record_management(QMainWindow):
    def __init__(self):
        super(Record_management, self).__init__()
        loadUi("gui/record_management.ui", self)
        self.backbtn.clicked.connect(goto_admin_dash)
        self.add_rec_btn.clicked.connect(self.goto_add_record_page)
        txtfname = self.txtfname
        txtlname = self.txtlname
        dob = self.dob
        dod = self.dod


    def goto_add_record_page(self):
        add_record = Add_record()
        show_page(add_record)

class Add_record(QMainWindow):
    def __init__(self):
        super(Add_record, self).__init__()
        loadUi("gui/add_dead_record.ui", self)
        self.backbtn.clicked.connect(self.goto_record_management)
        self.checkbtn.clicked.connect(self.check_plot_status)
        self.add_rec_btn.clicked.connect(self.add_record)
        fname = self.dec_fname
        mname = self.dec_mname
        lname = self.dec_lname
        DOB = self.dec_dob
        DOD = self.dec_dod
        DOI = self.dec_doi
        plot_name = self.plot_name
        plot_column = self.plot_column
        plot_row = self.plot_row
        plot_status = self.plot_status

    def goto_record_management(self):
        record_management = Record_management()
        show_page(record_management)

    def check_plot_status(self):
        # code to check the plot status
        pass

    def add_record(self):
        # code to add the dead record to the database
        pass

class Plot_management(QMainWindow):
    def __init__(self):
        super(Plot_management, self).__init__()
        loadUi("gui/plot_management.ui", self)
        self.backbtn.clicked.connect(goto_admin_dash)
        plot_name_filter = self.plot_name_filter

class Reservation_management(QMainWindow):
    def __init__(self):
        super(Reservation_management, self).__init__()
        loadUi("gui/reservation_management.ui", self)
        self.add_res_btn.clicked.connect(self.goto_reservation_page)
        self.backbtn.clicked.connect(goto_admin_dash)
        plot_name_filter = self.plot_name_filter

    def goto_reservation_page(self):
        reservation_page = Reservation_page()
        show_page(reservation_page)

class Reservation_page(QMainWindow):
    def __init__(self):
        super(Reservation_page, self).__init__()
        loadUi("gui/plot_reservation.ui", self)
        self.backbtn.clicked.connect(self.goto_reservation_management)
        self.reservebtn.clicked.connect(self.reservenow)
        self.checkbtn.clicked.connect(self.check_plot_status)
        txtfname = self.txtfname
        txtlname = self.txtlname
        mobile = self.mobile
        address = self.txtaddress
        plot_name = self.plot_name
        plot_row = self.plot_row
        plot_column = self.plot_column
        plot_status = self.plot_status
        plot_price = self.plot_price


    def goto_reservation_management(self):
        reservation_management = Reservation_management()
        show_page(reservation_management)

    def check_plot_status(self):
        # code to check plot status
        pass

    def reservenow(self):
        # code to add the reservation
        pass
class Booking_management(QMainWindow):
    def __init__(self):
        super(Booking_management, self).__init__()
        loadUi("gui/booking_management.ui", self)
        self.add_book_btn.clicked.connect(self.goto_booking_page)
        self.backbtn.clicked.connect(goto_admin_dash)
        plot_name_filter = self.plot_name_filter

    def goto_booking_page(self):
        booking = Booking_page()
        show_page(booking)

class Booking_page(QMainWindow):
    def __init__(self):
        super(Booking_page, self).__init__()
        loadUi("gui/book_interment.ui", self)
        self.backbtn.clicked.connect(self.goto_booking_management)
        self.booknowbtn.clicked.connect(self.book_now)
        cus_fname = self.cus_fname
        cus_lname = self.cus_lname
        mobile = self.mobile
        address = self.txtaddress
        dec_fname = self.dec_fname
        dec_mname = self.dec_mname
        dec_lname = self.dec_lname
        dec_dob = self.dec_dob
        dec_dod = self.dec_dod
        dec_doi = self.dec_doi


    def goto_booking_management(self):
        booking = Booking_management()
        show_page(booking)

    def check_plot_status(self):
        # code to check plot status for booking interment
        pass

    def book_now(self):
        # code to add the booking
        pass


app = QApplication(sys.argv)
login = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(login)
widget.show()
widget.showFullScreen()
app.exec()
