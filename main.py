#this file is the main entry point for my application

from PyQt5 import QtWidgets # Import the PyQt5 module
import sys

from UI_design import Ui_Form
# This file holds the MainWindow and all other design related things
              

class SearchApp(QtWidgets.QMainWindow, Ui_Form):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_Form.__init__(self)
       # super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in UI_design.py file automatically
                            # It sets up layout and widgets that are defined
    def push(self):  
        
        self.lineEdit.setText(value)

        
        

def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = SearchApp()                 # set the form to be the SearchApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


# if we're running file directly and not importing it
if __name__ == '__main__':
    main()           
