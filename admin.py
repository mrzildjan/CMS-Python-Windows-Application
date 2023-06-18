import datetime
import sys

from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QWidget, QComboBox, \
    QHBoxLayout
from PyQt5.QtGui import QIcon
import psycopg2
import re
from datetime import date, datetime

current_date_time = datetime.now()

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


def retrieve_latest_ids():
    conn = psycopg2.connect(host='localhost', user='postgres', password='password',
                            dbname='cms')  # change password
    cursor = conn.cursor()

    # Retrieve the latest plot_id and rel_id from their respective tables
    cursor.execute("SELECT plot_id FROM PLOT ORDER BY plot_date DESC LIMIT 1;")
    latest_plot_id = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(rel_id) FROM RELATIVE;")
    latest_rel_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return latest_plot_id, latest_rel_id


def check_plot_existence(plot_yard, plot_row, plot_col):
    plot_id = f"{plot_yard}{plot_row}{plot_col}"

    # Query to check if the plot ID exists in the PLOT table
    query = f"SELECT COUNT(*) FROM PLOT WHERE PLOT_ID = '{plot_id}'"

    # Execute the query and fetch the result
    result = execute_query_fetch(query)

    # Check if the result count is greater than 0
    if result and result[0][0] > 0:
        return True  # Plot exists
    else:
        return False  # Plot does not exist


def check_plot_status(plot_yard, plot_row, plot_col):
    plot_id = f"{plot_yard}{plot_row}{plot_col}"
    query = f"SELECT plot_status FROM PLOT WHERE PLOT_ID = '{plot_id}'"

    # Execute the query and fetch the result
    result = execute_query_fetch(query)

    # Check if the result exists and has at least one row
    if result and len(result) > 0:
        plot_status = result[0][0]
        return plot_status  # Return the plot status
    else:
        return None  # Plot does not exist


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


def show_message_box(message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(message)
    msg_box.setWindowTitle("Information")
    msg_box.exec_()


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

            if not (first_name.replace(" ", "").isalpha() and last_name.isalpha() and (
                    mid_name == "" or mid_name.isalpha())):
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
                               f"'{username}', '{password}', 't', '{current_date_time}', '{current_date_time}')"

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
        self.transactionbtn.clicked.connect(self.goto_view_transaction)

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

    def goto_view_transaction(self):
        view_transaction = View_transaction()
        show_page(view_transaction)

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
        self.backbtn.clicked.connect(self.goto_admin_dash)
        self.plot_name_filter.currentTextChanged.connect(self.display_plot)
        global plot_yard
        plot_yard = self.plot_name_filter.currentText()
        self.display_plot(plot_yard)

    def goto_admin_dash(self):
        admin_dash = AdminDash()
        show_page(admin_dash)

    def display_plot(self, plot_yard):
        query = f"SELECT PLOT_ID, PLOT_YARD, PLOT_ROW, PLOT_COL, PLOT_STATUS FROM PLOT WHERE PLOT_YARD = '{plot_yard}';"

        # Execute the query and fetch the results
        results = execute_query_fetch(query)

        if not results:
            message = 'No results found'
            show_message_box(message)
            return
        else:
            # Clear the existing table content
            self.plot_table.clearContents()

            # Set the table row count to the number of fetched results
            self.plot_table.setRowCount(len(results))

            # Populate the table with the fetched results
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.plot_table.setItem(row_idx, col_idx, item)

                # Create a combobox widget for actions
                actions_combo = QComboBox()
                actions_combo.addItem("Select")
                actions_combo.addItem("Edit")
                actions_combo.addItem("Save")
                actions_combo.addItem("Delete")
                actions_combo.currentIndexChanged.connect(self.handle_action)

                # Set the combobox as the cell widget for the action column
                self.plot_table.setCellWidget(row_idx, len(row_data), actions_combo)

    def handle_action(self):
        action = self.sender().currentText()

        if action == "Edit":
            self.edit_plot()
        elif action == "Save":
            self.save_plot()
        elif action == "Delete":
            self.delete_plot()
        else:
            pass

    def get_selected_row_data(self):
        row_idx = self.plot_table.currentRow()
        plot_id = self.plot_table.item(row_idx, 0).text()
        yard = self.plot_table.item(row_idx, 1).text()
        row = self.plot_table.item(row_idx, 2).text()
        col = self.plot_table.item(row_idx, 3).text()
        return plot_id, yard, row, col

    def edit_plot(self):
        plot_id, yard, row, col = self.get_selected_row_data()
        # prints, to check the selected values > see console for values
        print('EDIT')
        print(plot_id)
        print(yard)
        print(row)
        print(col)

        # perform a query to make the the row editable

    def save_plot(self):
        plot_id, yard, row, col = self.get_selected_row_data()
        # prints, to check the selected values > see console for values
        print('SAVE')
        print(plot_id)
        print(yard)
        print(row)
        print(col)

        # perform a query to save the edited row

    def delete_plot(self):
        # prints, to check the selected values > see console for values
        plot_id, yard, row, col = self.get_selected_row_data()
        print('DELETE')
        print(plot_id)
        print(yard)
        print(row)
        print(col)

        show_error_message(f"Are you sure you want to delete PLOT ID '{plot_id}' ?")
        # if okay button is clicked. perform query to delete
        self.display_plot(self)


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
        self.checkbtn.clicked.connect(self.display_plot_status)
        self.reservebtn.clicked.connect(self.reserve_now)

    def goto_reservation_management(self):
        reservation_management = Reservation_management()
        show_page(reservation_management)

    def display_plot_status(self):
        plot_yard = self.plot_yard.currentText()
        plot_row = self.plot_row.currentText()
        plot_col = self.plot_col.currentText()

        plot_status = check_plot_status(plot_yard, plot_row, plot_col)
        if plot_status is not None:
            self.plot_status.setText(plot_status)
        else:
            self.plot_status.setText("Available")

    def reserve_now(self):
        # Get the values from the UI
        plot_yard = self.plot_yard.currentText()
        plot_row = self.plot_row.currentText()
        plot_col = self.plot_col.currentText()
        plot_status = self.plot_status.text()
        user_id = get_current_user_id()

        if plot_status == "":
            error_message = "Please Choose Plot Location"
            show_error_message(error_message)
            return

        if any(value == "" for value in [plot_yard, plot_row, plot_col, plot_status]):
            # Display error message for null values
            error_message = "Please fill in all fields."
            show_error_message(error_message)
            return

        # Check if the plot already exists
        if check_plot_existence(plot_yard, plot_row, plot_col):
            error_message = "Chosen Plot is Unavailable, Please select a different plot."
            show_error_message(error_message)
        else:
            plot_query = f"INSERT INTO PLOT (plot_col, plot_row, plot_yard, plot_status, plot_date) \
                          VALUES ('{plot_col}', '{plot_row}', '{plot_yard}', 'Reserved', '{current_date_time}' )"

            # Execute the plot query
            plot_result = execute_query(plot_query)

            if plot_result:
                latest_plot_id, latest_rel_id = retrieve_latest_ids()

                transaction_query = f"INSERT INTO TRANSACTION (trans_type, trans_status, trans_date, user_id, rel_id, plot_id)"

                if latest_rel_id is not None:
                    transaction_query += f"VALUES ('Reserved', 'Pending', '{current_date_time}', '{user_id}', '{latest_rel_id}','{latest_plot_id}')"
                else:
                    transaction_query += f"VALUES ('Reserved', 'Pending', '{current_date_time}', '{user_id}', NULL, '{latest_plot_id}')"

                # Execute the transaction query
                transaction_result = execute_query(transaction_query)

                # Check if the queries were successful
                if transaction_result:
                    # Booking successful
                    success_message = "Reservation Successful!"
                    show_success_message(success_message)

                    self.goto_reservation_management()
                else:
                    # Error message for failed execution
                    error_message = "Reservation Failed, Please try again."
                    show_error_message(error_message)
            else:
                # Error message for failed execution
                error_message = "Reservation Failed, Please try again."
                show_error_message(error_message)


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
        self.checkbtn.clicked.connect(self.display_plot_status)

    def goto_booking_management(self):
        booking = Booking_management()
        show_page(booking)

    def display_plot_status(self):
        plot_yard = self.plot_name.currentText()
        plot_row = self.plot_row.currentText()
        plot_col = self.plot_col.currentText()

        plot_status = check_plot_status(plot_yard, plot_row, plot_col)
        if plot_status is not None:
            self.plot_status.setText(plot_status)
        else:
            self.plot_status.setText("Available")

    def book_now(self):
        # Get the values from the UI
        dec_fname = self.dec_fname.text()
        dec_mname = self.dec_mname.text()
        dec_lname = self.dec_lname.text()
        dec_dob = self.dec_dob.date().toString("yyyy-MM-dd")
        dec_dod = self.dec_dod.date().toString("yyyy-MM-dd")
        dec_doi = self.dec_doi.date().toString("yyyy-MM-dd")
        user_id = get_current_user_id()
        plot_yard = self.plot_name.currentText()
        plot_row = self.plot_row.currentText()
        plot_col = self.plot_col.currentText()
        plot_status = self.plot_status.text()

        if plot_status == "":
            error_message = "Please Choose Plot Location"
            show_error_message(error_message)
            return

        if any(value == "" for value in
               [dec_fname, dec_lname, dec_dob, dec_dod, dec_doi, plot_yard, plot_row, plot_col, plot_status]):
            # Display error message for null values
            error_message = "Please fill in all fields."
            show_error_message(error_message)
            return

        if not (dec_fname.replace(" ", "").isalpha() and dec_lname.isalpha() and (
                dec_mname == "" or dec_mname.isalpha())):
            # Display error message for non-letter values
            error_message = "Name fields should only contain letters."
            show_error_message(error_message)
            return

        # Check if the plot already exists
        if check_plot_existence(plot_yard, plot_row, plot_col):
            error_message = "Chosen Plot is Unavailable, Please select a different plot."
            show_error_message(error_message)
        else:
            relative_query = f"INSERT INTO RELATIVE (rel_fname, rel_mname, rel_lname, rel_dob, rel_date_death, rel_date_interment, user_id) \
                              VALUES ('{dec_fname}', '{dec_mname}', '{dec_lname}', '{dec_dob}', '{dec_dod}', '{dec_doi}','{user_id}')"
            plot_query = f"INSERT INTO PLOT (plot_col, plot_row, plot_yard, plot_status, plot_date) \
                          VALUES ('{plot_col}', '{plot_row}', '{plot_yard}', 'Booked', '{current_date_time}' )"

            # Execute the queries
            relative_result = execute_query(relative_query)
            plot_result = execute_query(plot_query)

            latest_plot_id, latest_rel_id = retrieve_latest_ids()
            print("rel  ", latest_rel_id)
            print("plot  ", latest_plot_id)
            record_query = f"INSERT INTO RECORD (rec_lastpay_date, rec_lastpay_amount, rec_status, plot_id, rel_id, user_id) " \
                           f"VALUES ('{current_date_time}', 500.00, 'Booked', '{latest_plot_id}', '{latest_rel_id}', '{user_id}');"

            transaction_query = f"INSERT INTO TRANSACTION ( trans_type, trans_status, trans_date, user_id, rel_id, plot_id)" \
                                f"VALUES ( 'Booked'  , 'Fully Paid' , '{current_date_time}', '{user_id}', '{latest_rel_id}', '{latest_plot_id}');"

            record_result = execute_query(record_query)
            transaction_result = execute_query(transaction_query)

            # Check if the queries were successful
            if relative_result and plot_result and record_result and transaction_result:
                # Booking successful
                success_message = "Booking Successful!"
                show_success_message(success_message)

                self.goto_booking_management()
            else:
                # Error message for failed execution
                error_message = "Booking Failed, Please try again."
                show_error_message(error_message)


class View_transaction(QMainWindow):
    def __init__(self):
        super(View_transaction, self).__init__()
        loadUi("gui/transaction.ui", self)
        self.backbtn.clicked.connect(goto_admin_dash)
        global user_id
        user_id = get_current_user_id()
        self.display_reservations()
        self.display_bookings()

    def display_reservations(self):
        query = f"SELECT T.TRANS_ID , P.PLOT_YARD, P.PLOT_ROW, P.PLOT_COL, T.TRANS_STATUS FROM TRANSACTION T INNER JOIN PLOT P USING (PLOT_ID) \
                WHERE T.USER_ID = '{user_id}' AND T.TRANS_TYPE = 'Reserved' ORDER BY T.TRANS_ID,  P.PLOT_DATE DESC;"

        # Execute the query and fetch the results
        results = execute_query_fetch(query)

        # Clear the existing table content
        self.reservation_table.clearContents()

        # Set the table row count to the number of fetched results
        self.reservation_table.setRowCount(len(results))

        # Populate the table with the fetched results
        for row_idx, row_data in enumerate(results):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.reservation_table.setItem(row_idx, col_idx, item)

    def display_bookings(self):
        query = f"SELECT T.TRANS_ID , P.PLOT_YARD, P.PLOT_ROW, P.PLOT_COL, RL.REL_FNAME, RL.REL_MNAME, RL.REL_LNAME, RL.rel_dob, RL.rel_date_death FROM PLOT P \
                INNER JOIN TRANSACTION T USING (PLOT_ID) INNER JOIN RELATIVE RL USING (REL_ID) WHERE T.USER_ID = '{user_id}' AND T.TRANS_TYPE = 'Booked' ORDER BY T.TRANS_ID, P.PLOT_DATE DESC;"

        # Execute the query and fetch the results
        results = execute_query_fetch(query)

        # Clear the existing table content
        self.booking_table.clearContents()

        # Set the table row count to the number of fetched results
        self.booking_table.setRowCount(len(results))

        # Populate the table with the fetched results
        for row_idx, row_data in enumerate(results):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.booking_table.setItem(row_idx, col_idx, item)


app = QApplication(sys.argv)
login = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(login)
widget.show()
widget.showFullScreen()
app.exec()
