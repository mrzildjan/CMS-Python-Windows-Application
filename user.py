import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QIcon
import psycopg2
from datetime import date

def execute_query_fetch(query):
    conn = psycopg2.connect(host='localhost', user='postgres', password='johnjohnkaye14', dbname='cms') # change password
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
    conn = psycopg2.connect(host='localhost', user='postgres', password='johnjohnkaye14', dbname='cms') # change password
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


# Get the current date
current_date = date.today()
# Define the global variable
logged_in_username = None
logged_in_password = None

def show_page(frame):
    widget.addWidget(frame)
    widget.setCurrentIndex(widget.currentIndex() + 1)

def goto_user_dash():
    user_dash = UserDash()
    show_page(user_dash)


def show_error_message(message):
    message_box = QtWidgets.QMessageBox()
    message_box.critical(None, "Error", message)
    message_box.setStyleSheet("QMessageBox { background-color: white; }")

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("guimain/login.ui", self)
        self.registerbtn.clicked.connect(self.goto_registration_page)
        self.loginbtn.clicked.connect(self.login)

    def goto_registration_page(self):
        register = Register()
        show_page(register)

    def goto_dashboard(self):
        dashboard = UserDash()
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

            # Execute the query to check if username and password exist
            query = f"SELECT * FROM \"USER\" WHERE USER_USERNAME = '{username}' AND USER_PASSWORD = '{password}'"

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
        loadUi("guimain/registration.ui", self)
        self.registerbtn.clicked.connect(self.register_now)
        self.backbtn.clicked.connect(self.goto_login_page)
        self.message_box = None

    def goto_login_page(self):
        login = Login()
        show_page(login)

    def show_success_message(self, message):
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle("Success")
        message_box.setText(message)
        icon = QIcon("images/check.png")  # Replace "path/to/icon.png" with the actual path to your icon file
        message_box.setIconPixmap(icon.pixmap(64, 64))  # Set the icon to a custom pixmap

        ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
        message_box.setDefaultButton(ok_button)
        self.message_box = message_box
        message_box.exec_()

    def register_now(self):
        first_name = self.txtfname.text()
        last_name = self.txtlname.text()
        mid_name = self.txtmid.text()
        number = self.txtnumber.text()
        address = self.txtaddress.text()
        username = self.txtusername.text()
        password = self.txtpass.text()
        confirmpass = self.txtconfirm.text()

        try:
            # Check for null values in input fields
            if any(value == "" for value in
                   [first_name, last_name, number, address, username, password, confirmpass]):
                # Display error message for null values
                error_message = "Please fill in all fields."
                show_error_message(error_message)
                return

            if not (first_name.isalpha() and last_name.isalpha() and (mid_name == "" or mid_name.isalpha())):
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

            if password == confirmpass:

                # Insert the data into the "USER" table
                insert_query = f"INSERT INTO \"USER\" (USER_FNAME, USER_MNAME, USER_LNAME, USER_NUMBER, USER_EMAIL, " \
                               f"USER_USERNAME, USER_PASSWORD, USER_CREATED_AT, USER_UPDATED_AT) " \
                               f"VALUES ('{first_name}', '{mid_name}', '{last_name}', '{number}', '{address}', " \
                               f"'{username}', '{password}', '{current_date}', '{current_date}')"

                # Execute the query and check if it was successful
                if execute_query(insert_query):
                    # Registration successful message
                    success_message = "Registration Successful!"
                    self.show_success_message(success_message)

                    # Redirect to login page if OK button is clicked
                    if self.message_box and self.message_box.clickedButton() == self.message_box.button(
                            QtWidgets.QMessageBox.Ok):
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


class UserDash(QMainWindow):
    def __init__(self):
        super(UserDash, self).__init__()
        loadUi("guimain/userdash.ui", self)
        self.plotlocatorbtn.clicked.connect(self.goto_plot_locator_page)
        self.searchrecordbtn.clicked.connect(self.goto_search_record_page)
        self.bookbtn.clicked.connect(self.goto_booking_services)
        self.viewmapbtn.clicked.connect(self.goto_map_page)
        self.transactionbtn.clicked.connect(self.goto_transaction_page)
        self.aboutusbtn.clicked.connect(self.goto_aboutus_page)
        self.logoutbtn.clicked.connect(self.goto_login_page)


    def goto_plot_locator_page(self):
        plot_locator = Plot_locator()
        show_page(plot_locator)

    def goto_search_record_page(self):
        search_record = Search_record()
        show_page(search_record)

    def goto_booking_services(self):
        booking_services = Booking_services()
        show_page(booking_services)

    def goto_map_page(self):
        map_view = Map_view()
        show_page(map_view)

    def goto_transaction_page(self):
        transaction = Transaction_page()
        show_page(transaction)

    def goto_aboutus_page(self):
        about_us = About_us()
        show_page(about_us)

    def goto_login_page(self):
        self.reset_global_variables()

    def reset_global_variables(self):
        global logged_in_username, logged_in_password
        logged_in_username = None
        logged_in_password = None
        login = Login()
        show_page(login)


class Plot_locator(QMainWindow):
    def __init__(self):
        super(Plot_locator, self).__init__()
        loadUi("guimain/plot_locator.ui", self)
        self.backbtn.clicked.connect(goto_user_dash)
        self.searchbtn.clicked.connect(self.search_plot)
        # Set placeholder text for dob and dod QDateEdit widgets
        # Set display format for dob and dod QDateEdit widgets
        self.dob.setDisplayFormat("yyyy-MM-dd")
        self.dod.setDisplayFormat("yyyy-MM-dd")

    def search_plot(self):
        txtfname = self.txtfname.text()
        txtlname = self.txtlname.text()
        dob = self.dob.text()
        dod = self.dod.text()

        # Construct the query
        query = f"SELECT P.PLOT_YARD, P.PLOT_ROW, P.PLOT_COL, R.REL_FNAME, R.REL_MNAME, R.REL_LNAME, R.REL_DOB, R.REL_DATE_DEATH \
        FROM PLOT P INNER JOIN RECORD USING(PLOT_ID) INNER JOIN RELATIVE R USING(REL_ID) \
        WHERE R.REL_FNAME = '{txtfname}'"

        if txtlname:
            query += f" AND R.REL_LNAME = '{txtlname}'"

        if dob:
            query += f" AND R.REL_DOB = '{dob}'"

        if dod:
            query += f" AND R.REL_DATE_DEATH = '{dod}'"

        query += ";"

        # Execute the query and fetch the results
        results = execute_query_fetch(query)

        # Clear the existing table content
        self.plotlocatortable.clearContents()

        # Set the table row count to the number of fetched results
        self.plotlocatortable.setRowCount(len(results))

        # Populate the table with the fetched results
        for row_idx, row_data in enumerate(results):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.plotlocatortable.setItem(row_idx, col_idx, item)


class Search_record(QMainWindow):
    def __init__(self):
        super(Search_record, self).__init__()
        loadUi("guimain/search_record.ui", self)
        self.backbtn.clicked.connect(goto_user_dash)
        self.by_date.setVisible(False)
        self.dob.setDisplayFormat("yyyy-MM-dd")
        self.dod.setDisplayFormat("yyyy-MM-dd")
        self.search.currentTextChanged.connect(self.perform)

    def perform(self, text):
        txtfname = self.txtfname.text()
        txtlname = self.txtlname.text()
        dob = self.dob.text()
        dod = self.dod.text()

        if text == "Search by Name":
            self.by_date.setVisible(False)

            # Construct the query
            query = f"SELECT P.PLOT_YARD, P.PLOT_ROW, P.PLOT_COL, R.REL_FNAME, R.REL_MNAME, R.REL_LNAME, R.REL_DOB, R.REL_DATE_DEATH, R.REL_DATE_INTERMENT, R.REL_DATE_EXHUMATION \
                            FROM PLOT P INNER JOIN RECORD USING(PLOT_ID) INNER JOIN RELATIVE R USING(REL_ID) \
                            WHERE R.REL_FNAME = '{txtfname}'"

            if txtlname:
                query += f" AND R.REL_LNAME = '{txtlname}'"

            query += ";"

            # Execute the query and fetch the results
            results = execute_query_fetch(query)

            # Clear the existing table content
            self.record_table.clearContents()

            # Set the table row count to the number of fetched results
            self.record_table.setRowCount(len(results))

            # Populate the table with the fetched results
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.record_table.setItem(row_idx, col_idx, item)

        else:
            self.by_date.setVisible(True)

            # Construct the query
            query = f"SELECT P.PLOT_YARD, P.PLOT_ROW, P.PLOT_COL, R.REL_FNAME, R.REL_MNAME, R.REL_LNAME, R.REL_DOB, R.REL_DATE_DEATH, R.REL_DATE_INTERMENT, R.REL_DATE_EXHUMATION \
                                        FROM PLOT P INNER JOIN RECORD USING(PLOT_ID) INNER JOIN RELATIVE R USING(REL_ID) \
                                        WHERE R.REL_FNAME = '{txtfname}'"

            if txtlname:
                query += f" AND R.REL_LNAME = '{txtlname}'"
            if txtlname:
                query += f" AND R.REL_LNAME = '{txtlname}'"
            if txtlname:
                query += f" AND R.REL_LNAME = '{txtlname}'"

            query += ";"

            # Execute the query and fetch the results
            results = execute_query_fetch(query)

            # Clear the existing table content
            self.record_table.clearContents()

            # Set the table row count to the number of fetched results
            self.record_table.setRowCount(len(results))

            # Populate the table with the fetched results
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.record_table.setItem(row_idx, col_idx, item)

class Booking_services(QMainWindow):
    def __init__(self):
        super(Booking_services, self).__init__()
        loadUi("guimain/bookservices.ui", self)
        self.bookforintermentbtn.clicked.connect(self.goto_book_interment)
        self.plotreservationbtn.clicked.connect(self.goto_plot_reservation)
        self.backbtn.clicked.connect(goto_user_dash)

    def goto_book_interment(self):
        book_interment = Book_interment()
        show_page(book_interment)
    def goto_plot_reservation(self):
        plot_reservation = Plot_reservation()
        show_page(plot_reservation)


class Book_interment(QMainWindow):
    def __init__(self):
        super(Book_interment, self).__init__()
        loadUi("guimain/book_interment.ui", self)
        self.backbtn.clicked.connect(self.goto_booking_services)
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

    def goto_booking_services(self):
        booking_services = Booking_services()
        show_page(booking_services)

    def check_plot_status(self):
        # code to check plot status for booking interment
        pass

    def book_now(self):
        # code to add the booking
        pass


class Plot_reservation(QMainWindow):
    def __init__(self):
        super(Plot_reservation, self).__init__()
        loadUi("guimain/plot_reservation.ui", self)
        self.backbtn.clicked.connect(self.goto_booking_services)
        self.checkbtn.clicked.connect(self.check_plot_status)
        self.reservebtn.clicked.connect(self.reservenow)
        txtfname = self.txtfname
        txtlname = self.txtlname
        mobile = self.mobile
        address = self.txtaddress
        plot_name = self.plot_name
        plot_row = self.plot_row
        plot_column = self.plot_column
        plot_status = self.plot_status
        plot_price = self.plot_price



    def goto_booking_services(self):
        booking_services = Booking_services()
        show_page(booking_services)

    def check_plot_status(self):
        # code to check plot status
        pass

    def reservenow(self):
        # code to add the reservation
        pass

class Map_view(QMainWindow):
    def __init__(self):
        super(Map_view, self).__init__()
        loadUi("guimain/map.ui", self)
        self.backbtn.clicked.connect(goto_user_dash)


class Transaction_page(QMainWindow):
    def __init__(self):
        super(Transaction_page, self).__init__()
        loadUi("guimain/transaction.ui", self)
        self.backbtn.clicked.connect(goto_user_dash)


class About_us(QMainWindow):
    def __init__(self):
        super(About_us, self).__init__()
        loadUi("guimain/aboutus.ui", self)
        self.backbtn.clicked.connect(goto_user_dash)


app = QApplication(sys.argv)
login = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(login)
widget.setGeometry(100, 100, 1336, 768)
widget.showFullScreen()
sys.exit(app.exec())
