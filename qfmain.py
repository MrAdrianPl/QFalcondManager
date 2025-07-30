import sys
from PyQt6.QtWidgets import (QApplication
                             ,QMainWindow
                             ,QVBoxLayout
                             ,QWidget
                             ,QTabWidget)

from qfgui import app_main_panel,not_saved_dialog,profiles_stack
from qfalcondstate import FalcondInfoWidget

class MainWindow(QMainWindow):

    ### Build Itself ###
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QFalcond Profile Manager")

        self.resize(800, 1000)

        #tabs = self.Tab_Headers()
        tab_bar = QTabWidget()
        main_panel = app_main_panel()
        info_panel = FalcondInfoWidget()

        mainl = QVBoxLayout()
        w = QWidget()
        
        tab_bar.addTab(main_panel,"Profile Managment")
        tab_bar.addTab(info_panel,"Falcond Info")

        tab_bar.currentChanged.connect( lambda index: info_panel.StopRunning() if index == 0 else print('') )
        tab_bar.currentChanged.connect( lambda index: info_panel.StartRunning() if index == 1 else print('') )

        mainl.addWidget(tab_bar)

        
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