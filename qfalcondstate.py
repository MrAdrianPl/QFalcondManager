import time

from PyQt6.QtCore import pyqtSlot, pyqtSignal, QThread,QSize,Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout,QHBoxLayout, QTextEdit,QStackedWidget,QPushButton,QSizePolicy
from qfgui import StandardLableTemplate,StandardButtonTemplate
from qffunctions import LoadFalcondStatus,LoadFalcondHistory

class FalcondBackgroundStateChecking(QThread):
    """
    rather simplistic way to monitor falcond history and status
    """
    resultAvailable = pyqtSignal(object)
    
    def __init__(self):
        QThread.__init__(self)


        # mark the thread is alive
        self.alive = True

    def run(self):
        
        print("Thread :: start")

        for i in range(1, 30):
            time.sleep(1)

            if not self.alive:
                break

        if not self.alive:
            print("Thread :: Computation cancelled")
            return            
        
        falcond_status_data = LoadFalcondStatus()
        falcond_history_data = LoadFalcondHistory()
    
        print("Thread :: end")

        
        result = {
            "current_falcond_status": falcond_status_data
            ,"falcond_history_data": falcond_history_data
        }

        # emit result to the AppWidget
        self.resultAvailable.emit(result)        

    def stop(self):
        # mark this thread as not alive
        self.alive = False
        # wait for it to really finish
        #self.wait()    


class FalcondInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        BUTTONSIZE = QSize(50,30)
        self.MainLayout = QVBoxLayout()
        self.TopButtons = QHBoxLayout()
        self.StatusLayout = QHBoxLayout()
        self.HistoryLayout = QVBoxLayout()

        falcond_current_status_label = StandardLableTemplate('Falcond Status',QSize(120,30))
        falcond_history_lable = StandardLableTemplate('Falcond History',QSize(120,30))
        
        
        reload_now_button = StandardButtonTemplate('⟲',BUTTONSIZE,lambda: self.ReloadDisplayedText(self.LoadFalcondDataAsDict()))

        plr = self.PlayResumeButton()
        plr.pause_button.clicked.connect(self.StopRunning)
        plr.resume_button.clicked.connect(self.ResumeRunning)

        self.TopButtons.addWidget(plr,alignment=Qt.AlignmentFlag.AlignLeft)
        self.TopButtons.addWidget(reload_now_button,alignment=Qt.AlignmentFlag.AlignRight)

        self.HistoryText = QTextEdit()
        self.HistoryText.setReadOnly(True)

        self.StatusText = QTextEdit()
        self.StatusText.setMaximumHeight(60)
        self.StatusText.setReadOnly(True)
        
        self.ReloadDisplayedText(self.LoadFalcondDataAsDict())
        
        self.StatusLayout.addWidget(falcond_current_status_label)
        self.StatusLayout.addWidget(self.StatusText)

        self.HistoryLayout.addWidget(falcond_history_lable,alignment=Qt.AlignmentFlag.AlignCenter)
        self.HistoryLayout.addWidget(self.HistoryText)

        self.MainLayout.addLayout(self.TopButtons)
        self.MainLayout.addLayout(self.StatusLayout)
        self.MainLayout.addLayout(self.HistoryLayout)

        self.running_thread = None
        
        self.setLayout(self.MainLayout)
    
    class PlayResumeButton(QStackedWidget):
        def __init__(self):
            super().__init__()
            BUTTONSIZE = QSize(50,30)
            

            self.pause_button = QPushButton('■')
            self.pause_button.setMaximumSize(BUTTONSIZE)
            self.pause_button.setSizePolicy(QSizePolicy.Policy.Maximum,QSizePolicy.Policy.Maximum)

            self.resume_button = QPushButton('▶')
            self.resume_button.setMaximumSize(BUTTONSIZE)
            self.pause_button.setSizePolicy(QSizePolicy.Policy.Maximum,QSizePolicy.Policy.Maximum)
            
            self.setSizePolicy(QSizePolicy.Policy.Maximum,QSizePolicy.Policy.Maximum)
            self.setMaximumSize(BUTTONSIZE)

            
            self.pause_button.clicked.connect(self.dSwapButton)
            self.resume_button.clicked.connect(self.dSwapButton)
            
            self.addWidget(self.pause_button)
            self.addWidget(self.resume_button)
            
            
            
            
        def dSwapButton(self):
            if self.currentWidget() == self.pause_button:
                
                self.setCurrentWidget(self.resume_button)
                
            else:
                self.setCurrentWidget(self.pause_button)
                



    
    @pyqtSlot()
    def StartRunning(self):
        self.running_thread = FalcondBackgroundStateChecking()
        self.running_thread.resultAvailable.connect(self.GetResults)
        self.running_thread.start()
        print('Async load of falcond data')
    
    
    @pyqtSlot(object)
    def GetResults(self, result):
        
        print('falcond data was loaded')
        
        self.ReloadDisplayedText(result)
        

        self.running_thread.start()

    @pyqtSlot()
    def ResumeRunning(self):
        print('falcond data loading was restored')
        self.running_thread = FalcondBackgroundStateChecking()
        self.running_thread.start()

    @pyqtSlot()
    def StopRunning(self):
        print('falcond data loading was interupted')
        self.running_thread.stop()
        self.running_thread = None

    @staticmethod
    def LoadFalcondDataAsDict():
           
        result = {
            "current_falcond_status": LoadFalcondStatus()
            ,"falcond_history_data": LoadFalcondHistory()
        }

        return result   

    def ReloadDisplayedText(self,data:dict):
        self.StatusText.setText(data.get('current_falcond_status'))
        self.HistoryText.setText(data.get('falcond_history_data'))