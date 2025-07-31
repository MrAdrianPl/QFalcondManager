import os
from qffunctions import GetGlobalProfiles,GetLocalProfiles,FALCOND_SETTINGS_PATH,FALCOND_USER_SETTINGS_PATH


def ReturnMe():
    return os.popen("/bin/bash -c 'logname'").read().strip()

def CreateUserFolder():
    if not FALCOND_USER_SETTINGS_PATH.exists():
        os.system(f"/bin/bash -c 'mkdir {FALCOND_USER_SETTINGS_PATH}'")

def CopyGlobalProfiles():
    global_profiles_list = GetGlobalProfiles()
    local_profiles_list = GetLocalProfiles()

    profiles_to_copy = [ item for item in global_profiles_list if item not in local_profiles_list ]

    profile_names = ','.join(str(profile_name) for profile_name in profiles_to_copy)
    
    os.system(f"/bin/bash -c 'cp {FALCOND_SETTINGS_PATH}/{{{profile_names}}} {FALCOND_USER_SETTINGS_PATH}'")

def TakeOwnershipOfFolderAndFiles():
    userprofilesowner:str = os.popen(f"ls -ld {FALCOND_USER_SETTINGS_PATH} | awk '{{print $3}}'").read()     
    setup_user = ReturnMe()

    if userprofilesowner != setup_user:
        os.system(f'chown -R {setup_user} {FALCOND_USER_SETTINGS_PATH}')

def RunSetup():
    CreateUserFolder()
    CopyGlobalProfiles()
    TakeOwnershipOfFolderAndFiles()

if __name__ == "__main__":
    RunSetup()