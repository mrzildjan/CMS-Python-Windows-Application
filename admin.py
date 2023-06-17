import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

def show_page(frame):
    widget.addWidget(frame)
    widget.setCurrentIndex(widget.currentIndex() + 1)

def goto_admin_dash():
    admin_dash = AdminDash()
    show_page(admin_dash)

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
        dashboard = AdminDash()
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
