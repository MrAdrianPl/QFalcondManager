
class falcond_profile():
    def __init__(self):
        self.scheduler = Schedulers()
        self.performance_mode = PerformanceMode()
        self.end_script = Script()
        self.start_script = Script()
        self.executable_name = ExecName()
        self.v3cache = v3dchache()


class Schedulers():
    def __init__(self):
        self.schedulers = ["none", "bpfland", "lavd", "rusty", "flash"]
        self.scheduler_mode = ["default", "gaming", "power", "latency", "server"]
        self.scheduler_default = "none"
        self.current_scheduler = "none"
        self.current_scheduler_mode = "default"
        
        
    def set_current_scheduler(self,scheduler):
        self.current_scheduler = scheduler

    def set_current_scheduler_mode(self,mode):
        self.current_scheduler_mode = mode

    
class PerformanceMode():
    def __init__(self):
        self.enabled = ["true","false"]
        self.current_enabled = "true"
        

    def set_peformance_mode(self,mode_enabled):
        self.current_enabled = mode_enabled

class Script():
    def __init__(self):
        self.script = ""
        

    def set_script(self,script):
        self.script = script

class ExecName():
    def __init__(self):
        self.ExecName = ""
        

    def set_execname(self,name):
        self.ExecName = name

class v3dchache():
    def __init__(self):
        self.modes = ["none", "cache", "freq"]
        self.mode = ""
        

    def set_mode(self,mode):
        self.mode = mode        