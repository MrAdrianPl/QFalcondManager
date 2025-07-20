import os
from qfprops import falcond_profile
from pathlib import Path

FALCOND_SETTINGS_PATH:Path = Path("/usr/share/falcond/profiles")
FALCOND_USER_SETTINGS_PATH:Path = FALCOND_SETTINGS_PATH / "user"

def GetGlobalProfiles():
    global_profiles_list = []
    path:Path

    if FALCOND_SETTINGS_PATH.exists():

        for path in FALCOND_SETTINGS_PATH.iterdir():
            if path.is_file():
                global_profiles_list.append(path.name)
    
    return global_profiles_list
        

def GetLocalProfiles():
    local_profiles_list = []
    path:Path

    if FALCOND_USER_SETTINGS_PATH.exists():

        for path in FALCOND_USER_SETTINGS_PATH.iterdir():
            if path.is_file():
                local_profiles_list.append(path.name)
    
    return local_profiles_list

def LoadProfile(path_to_profile):
    profile_props = {}
    this_falcond_profile = falcond_profile()
    with open(path_to_profile) as profile:
        try:
            for line in profile.readlines():
                if line.strip() != "" and line.strip() is not None:
                    property_name,property_value = line.split("=")
                    profile_props[property_name.strip()] = property_value.strip()
        except ValueError:
            pass

    start_script:str = profile_props.get('start_script','')
    stop_script:str = profile_props.get('stop_script','')
    exec_name:str = profile_props.get('name','')
    this_falcond_profile.end_script.set_script(stop_script.removeprefix("\"").removesuffix("\""))
    this_falcond_profile.start_script.set_script(start_script.removeprefix("\"").removesuffix("\""))
    this_falcond_profile.executable_name.set_execname(exec_name.removeprefix("\"").removesuffix("\""))
    this_falcond_profile.scheduler.set_current_scheduler(profile_props.get('scx_sched',''))
    this_falcond_profile.scheduler.set_current_scheduler_mode(profile_props.get('scx_sched_props',''))
    this_falcond_profile.v3cache.set_mode(profile_props.get('vcache_mode',''))
    this_falcond_profile.performance_mode.set_peformance_mode(profile_props.get('performance_mode','performance_mode'))    


    return this_falcond_profile

def EmptyProfile():
    return falcond_profile()

def LoadSpecifiedProfile(profile_name):
        if profile_name is not None:
            return LoadProfile(FALCOND_USER_SETTINGS_PATH / profile_name)    
        
def RemoveProfile(profile_name):       
    os.remove(FALCOND_USER_SETTINGS_PATH / profile_name) 
