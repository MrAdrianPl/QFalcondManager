from PyQt6.QtCore import QSize,Qt
from PyQt6.QtWidgets import (QPushButton
                             ,QSizePolicy
                             ,QComboBox
                             ,QLabel
                             ,QHBoxLayout
                             ,QCheckBox
                             ,QLineEdit
                             ,QVBoxLayout
                             ,QFrame
                             ,QStackedWidget
                             ,QWidget
                             ,QRadioButton
                             ,QListWidget)
from qffunctions import GetLocalProfiles,LoadSpecifiedProfile,EmptyProfile,RemoveProfile,FALCOND_USER_SETTINGS_PATH
from qfprops import falcond_profile
def app_main_panel():
    MainWidget = QWidget()
    MainLayout = QVBoxLayout()
    TopLayout = QHBoxLayout()
    MidLayout = QHBoxLayout()

    plist = profile_list(GetLocalProfiles())
    pstack = profiles_stack(plist.profiles_list)
    plist.itemClicked.connect(lambda clicked_profile: pstack.change_to_profile_of_name(clicked_profile.text()))
    

    remove_selected_profile_button = StandardButtonTemplate("Remove Selected Profile",QSize(160,40),lambda: RemoveFromAllLists(plist,pstack))
    input_new_profile_name = StandardInputTemplate("New Profile Name",QSize(200,40),"")
    add_new_profile_button = StandardButtonTemplate("Add New Profile",QSize(160,40),lambda: AddNewProfile(plist,pstack,input_new_profile_name.Input_Field.text()))

    TopLayout.addWidget(add_new_profile_button,alignment=Qt.AlignmentFlag.AlignLeft)
    TopLayout.addLayout(input_new_profile_name)
    TopLayout.addWidget(remove_selected_profile_button,alignment=Qt.AlignmentFlag.AlignLeft)

    MidLayout.addWidget(plist,alignment=Qt.AlignmentFlag.AlignTop)
    MidLayout.addWidget(pstack,alignment=Qt.AlignmentFlag.AlignTop)
    MainLayout.addLayout(TopLayout)
    MainLayout.addLayout(MidLayout)
    MainWidget.setLayout(MainLayout)
    return MainWidget 

class profile_list(QListWidget):
    def __init__(self,profiles_list:list):
        super().__init__()
        self.profiles_list = profiles_list
        self.MainLayout = QVBoxLayout()
        
        self.addItems(self.profiles_list)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        self.setMinimumSize(300,300)
        
    def add_new_profile_to_list(self,profile):
        self.addItem(profile)
        self.profiles_list.append(profile)
        
    def iterAllItems(self):
        for i in range(self.count()):
            yield self.item(i)        

    def get_widget_by_profile_name(self,name):
        for widget in self.iterAllItems():
            if widget.text() == name:
                return widget

    def remove_profile_from_list(self,profile):
        
        self.profiles_list.remove(profile)
        widget_to_remove = self.get_widget_by_profile_name(profile)
        self.takeItem(self.row(widget_to_remove))
        RemoveProfile(profile)
        
class profiles_stack(QStackedWidget):
    def __init__(self,profiles_list:list):
        super().__init__()
        self.DisplayedProfiles = []
        self.ProfilesList = []
        self.load_all_profiles(profiles_list)
        
    def add_profile(self,profile_name):
        if profile_name not in self.ProfilesList:
            new_profile = ProfileElement(profile_name)
            self.ProfilesList.append(profile_name)
            self.DisplayedProfiles.append(new_profile)
            self.addWidget(new_profile)
        else:
            print('profile exists')
    
    def remove_profile(self,profile_name):
        profile:ProfileElement
        self.ProfilesList.remove(profile_name)
        for profile in self.DisplayedProfiles:
            if profile.profile_from_name(profile_name):
                self.removeWidget(profile)

    def load_all_profiles(self,profiles_list):
        for profile in profiles_list:
            self.add_profile(profile)

    def change_to_profile_of_name(self,profile_name):
        profile:ProfileElement
        for profile in self.DisplayedProfiles:
            if profile.profile_from_name(profile_name):
                self.setCurrentWidget(profile)
    

def RemoveFromAllLists(plist:profile_list,pstack:profiles_stack):
    try:
        if plist.currentItem() is None:
            currently_selected_profile = pstack.currentWidget().profile_name
        else:
            currently_selected_profile = plist.currentItem().text()
            
        plist.remove_profile_from_list(currently_selected_profile)
        current_index = pstack.currentIndex()

        pstack.remove_profile(currently_selected_profile)
        if current_index > 1:
            pstack.setCurrentIndex(current_index-1)            
        
    except AttributeError:
        print("Selected Profile Cant Be Removed")

def AddNewProfile(plist:profile_list,pstack:profiles_stack,new_profile_name:str):
    if new_profile_name is not None and new_profile_name != "":
        if not new_profile_name.endswith('.conf'):
            new_profile_name = new_profile_name + '.conf'
        plist.add_new_profile_to_list(new_profile_name)
        pstack.add_profile(new_profile_name)
        pstack.change_to_profile_of_name(new_profile_name)


class ProfileElement(QWidget):
    def __init__(self,profile_name:str):
        super().__init__()
        self.profile_name = profile_name
        self.MainLayout = QVBoxLayout()
        
        if self.profile_name in GetLocalProfiles():
            self.profile_properties:falcond_profile = LoadSpecifiedProfile(self.profile_name)
        else:
            self.profile_properties:falcond_profile = EmptyProfile()

        print(self.profile_name)
        print(self.profile_properties.executable_name.ExecName)
        print(self.profile_properties.scheduler.current_scheduler)
        print(self.profile_properties.scheduler.current_scheduler_mode)
        print(self.profile_properties.performance_mode.current_enabled)
        print(self.profile_properties.v3cache.mode)
        print(self.profile_properties.start_script.script)
        print(self.profile_properties.end_script.script)


        self.Label = StandardLableTemplate(self.profile_name,QSize(200,30))
        self.Save = StandardButtonTemplate("Save",QSize(80,30),self.SaveProfile)
        self.Executable = StandardInputTemplate("Executable Name",QSize(300,30),self.profile_properties.executable_name.ExecName)
        
        self.Scheduler = StandardDropdownTemplate("Scheduler",self.profile_properties.scheduler.schedulers,self.profile_properties.scheduler.current_scheduler)
        self.SchedulerMode = StandardDropdownTemplate("Scheduler Mode",self.profile_properties.scheduler.scheduler_mode,self.profile_properties.scheduler.current_scheduler_mode)
        
        self.Performance = StandardDropdownTemplate("Performance Mode",self.profile_properties.performance_mode.enabled,self.profile_properties.performance_mode.current_enabled)
        self.V3DCache = StandardDropdownTemplate("V3D Cache",self.profile_properties.v3cache.modes,self.profile_properties.v3cache.mode)
        self.StartScript = StandardInputTemplate("Start Script",QSize(300,30),self.profile_properties.start_script.script)
        self.EndScript = StandardInputTemplate("End Script",QSize(300,30),self.profile_properties.end_script.script)

        self.MainLayout.addWidget(self.Label)
        self.MainLayout.addWidget(self.Save)
        self.MainLayout.addLayout(self.Executable)
        self.MainLayout.addLayout(self.Scheduler)
        self.MainLayout.addLayout(self.SchedulerMode)
        self.MainLayout.addLayout(self.Performance)
        self.MainLayout.addLayout(self.V3DCache)
        self.MainLayout.addLayout(self.StartScript)
        self.MainLayout.addLayout(self.EndScript)
        
        self.setLayout(self.MainLayout)

    def SaveProfile(self):
        to_be_saved_as_profile = f"""name = \"{self.Executable.Input_Field.text()}\"
scx_sched = {self.Scheduler.dropdown.currentText()}
scx_sched_props = {self.SchedulerMode.dropdown.currentText()}
performance_mode = {self.Performance.dropdown.currentText()}
vcache_mode = {self.V3DCache.dropdown.currentText()}
start_script = \"{self.StartScript.Input_Field.text()}\"
stop_script = \"{self.EndScript.Input_Field.text()}\" 
"""

        with open( FALCOND_USER_SETTINGS_PATH / self.profile_name, "w") as file:
            file.write(to_be_saved_as_profile)        

    def ReloadProfile(self):
        pass

    def profile_from_name(self,name):
        if self.profile_name == name:
            return self

class StandardCheckboxTemplate(QVBoxLayout):
    def __init__(self,LableName: str,DefValue:bool):
        super().__init__()
        self.def_lable = QLabel(LableName)
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(DefValue)

        inside = QHBoxLayout()
        inside.addWidget(self.def_lable)
        inside.addWidget(self.checkbox)

        self.addLayout(inside)

def SeparatorVertical() -> QFrame:
    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.HLine)
    #separator.setSizePolicy(QSizePolicy.Policy.Minimum,QSizePolicy.Policy.Expanding)
    separator.setLineWidth(1)
    separator.setProperty("class","Layout_Style")
    return separator

def SeparatorHorizontal(width,height) -> QFrame:
    
    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.NoFrame)
    #separator.setSizePolicy(QSizePolicy.Policy.Minimum,QSizePolicy.Policy.Expanding)
    separator.setMaximumSize(width,height)
    separator.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
    separator.setProperty("class","Horizontal_Separator_Style")
    return separator


class StandardDropdownTemplate(QVBoxLayout):
    def __init__(self,LableName: str,ValuesList:list,DefValue:bool):
        super().__init__()
        self.def_lable = QLabel(LableName)
        self.dropdown = QComboBox()
        self.dropdown.addItems(ValuesList)
    
        self.dropdown.setCurrentText(DefValue)
        inside = QHBoxLayout()
        inside.addWidget(self.def_lable)
        inside.addWidget(self.dropdown)
        
    
        self.addLayout(inside)
        self.addWidget(SeparatorVertical())

def StandardButtonTemplate(ButtonText:str,ButtonSize:QSize,ButtonFucntion,Tooltipstr=None) -> QPushButton:
    standard_button = QPushButton(ButtonText)
    standard_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
    standard_button.setFixedSize(ButtonSize)
    standard_button.clicked.connect(ButtonFucntion)

    if Tooltipstr is not None:
        standard_button.setToolTip(Tooltipstr)
        
    return standard_button

def StandardButtonBox(LableName:str,ButtonList:list) -> QWidget:
    def_lable = QLabel(LableName)

    whole = QWidget()
    layout = QVBoxLayout()
    inside = QVBoxLayout()
    inside.addWidget(def_lable)

    for button in ButtonList:
        inside.addWidget(button)
    


    layout.addLayout(inside)
    

    whole.setLayout(layout)

    return whole


def StandardLableTemplate(Lable: str,size:QSize):
    #Add Sample rates dropdown
    def_lable = QLabel(Lable)
    def_lable.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
    def_lable.setMinimumSize(size)

    return def_lable

def StandardRadioButtonTemplate(Lable: str) -> QRadioButton:
    button = QRadioButton(Lable)

    return button

# def StandardIcon(icon_h: int ,icon_w: int,tooltip_text:str):
#     button = QPushButton()
#     button.setFixedSize(QSize(icon_h, icon_w))
#     button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
#     button.setMask(rhombus_mask(icon_h,icon_w))
#     button.setText('!')
#     button.setToolTip(tooltip_text)
#     button.setProperty("class","Warning_Icon")

#     return button   

class StandardInputTemplate(QVBoxLayout):
    def __init__(self,LableName: str,size:QSize,DefaultValues,Tooltipstr=None):
        super().__init__()
        self.def_lable = QLabel(LableName)
        
        self.Input_Field = QLineEdit()
        
        self.Input_Field.setSizePolicy(QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred))
        self.Input_Field.setMinimumSize(size)
        self.Input_Field.setProperty("class","Standard_Input")
        self.Input_Field.setText(DefaultValues)
        self.Input_Field.setMaximumHeight(60)
        
        inside = QHBoxLayout()
        inside.addWidget(self.def_lable)
        inside.addWidget(self.Input_Field)
        self.addLayout(inside)
        self.addWidget(SeparatorVertical())