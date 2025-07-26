import sys
from PyQt6.QtWidgets import (QApplication
                             ,QMainWindow
                             ,QVBoxLayout
                             ,QWidget)

from qfgui import app_main_panel,not_saved_dialog,profiles_stack

class MainWindow(QMainWindow):

    ### Build Itself ###
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QFalcond Profile Manager")

        self.resize(800, 1000)

        #tabs = self.Tab_Headers()
        main_panel = app_main_panel()

        mainl = QVBoxLayout()
        w = QWidget()
        
        mainl.addWidget(main_panel)
        
        w.setLayout(mainl)

        self.setCentralWidget(w)

    def closeEvent(self, event):
        if profiles_stack.AnyProfilesNeedsToBeSaved():
            dlg = not_saved_dialog(event)
            dlg.exec()
        else:
            event.accept()
                  

if __name__ == "__main__":
    app = QApplication(sys.argv)

    

    
    w = MainWindow()
    w.show()

    app.exec()