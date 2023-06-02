import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

#  this is a comment boang
# test commit number 2
# test commit 3

def show_page(frame):
    widget.addWidget(frame)
    widget.setCurrentIndex(widget.currentIndex() + 1)

# Test Commit
def goto_user_dash():
    user_dash = UserDash()
    show_page(user_dash)


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("gui/login.ui", self)
        username = self.inputusername
        password = self.inputpass
        self.registerbtn.clicked.connect(self.goto_registration_page)
        self.loginbtn.clicked.connect(self.goto_dashboard)

    def goto_registration_page(self):
        register = Register()
        show_page(register)

    def goto_dashboard(self):
        dashboard = UserDash()
        show_page(dashboard)


class Register(QMainWindow):
    def __init__(self):
        super(Register, self).__init__()
        loadUi("gui/registration.ui", self)
        first_name = self.txtfname
        last_name = self.txtlname
        mid_name = self.txtmid
        number = self.txtnumber
        address = self.txtaddress
        username = self.txtusername
        password = self.txtpass
        confirmpass = self.txtconfirm
        self.registerbtn.clicked.connect(self.register_now)
        self.backbtn.clicked.connect(self.goto_login_page)

    def goto_login_page(self):
        login = Login()
        show_page(login)

    def register_now(self):
        # code to execute when registering an account
        pass


class UserDash(QMainWindow):
    def __init__(self):
        super(UserDash, self).__init__()
        loadUi("gui/userdash.ui", self)
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
        login = Login()
        show_page(login)


class Plot_locator(QMainWindow):
    def __init__(self):
        super(Plot_locator, self).__init__()
        loadUi("gui/plot_locator.ui", self)
        self.backbtn.clicked.connect(goto_user_dash)
        self.searchbtn.clicked.connect(self.search_plot)
        txtfname = self.txtfname
        txtlname = self.txtlname
        dob = self.dob
        dod = self.dod

    def search_plot(self):
        # code to searchf for the plot
        pass


class Search_record(QMainWindow):
    def __init__(self):
        super(Search_record, self).__init__()
        loadUi("gui/search_record.ui", self)
        self.backbtn.clicked.connect(goto_user_dash)
        self.searchbtn.clicked.connect(self.search_record)
        txtfname = self.txtfname
        txtlname = self.txtlname
        dob = self.dob
        dod = self.dod

    def search_record(self):
        # code to search record from database
        pass

class Booking_services(QMainWindow):
    def __init__(self):
        super(Booking_services, self).__init__()
        loadUi("gui/bookservices.ui", self)
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
        loadUi("gui/book_interment.ui", self)
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
        loadUi("gui/plot_reservation.ui", self)
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
        loadUi("gui/map.ui", self)
        self.backbtn.clicked.connect(goto_user_dash)


class Transaction_page(QMainWindow):
    def __init__(self):
        super(Transaction_page, self).__init__()
        loadUi("gui/transaction.ui", self)
        self.backbtn.clicked.connect(goto_user_dash)


class About_us(QMainWindow):
    def __init__(self):
        super(About_us, self).__init__()
        loadUi("gui/aboutus.ui", self)
        self.backbtn.clicked.connect(goto_user_dash)


app = QApplication(sys.argv)
login = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(login)
widget.show()
app.exec()
