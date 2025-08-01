import os
from qffunctions import GetGlobalProfiles,GetLocalProfiles,FALCOND_SETTINGS_PATH,FALCOND_USER_SETTINGS_PATH
from pwd import getpwnam
from shutil import copyfile

def CreateUserFolder():
    if not FALCOND_USER_SETTINGS_PATH.exists():
        os.mkdir(FALCOND_USER_SETTINGS_PATH)

def CopyGlobalProfiles():
    global_profiles_list = GetGlobalProfiles()
    local_profiles_list = GetLocalProfiles()

    profiles_to_copy = [ item for item in global_profiles_list if item not in local_profiles_list ]

    profile_names = ','.join(str(profile_name) for profile_name in profiles_to_copy)
    
    for profile in profile_names:
        copyfile(FALCOND_SETTINGS_PATH / profile, FALCOND_USER_SETTINGS_PATH)

def TakeOwnershipOfFolderAndFiles():
    setup_user = os.getlogin()
    uid = getpwnam(setup_user).pw_uid
    gid = getpwnam(setup_user).pw_gid    
    os.chown(FALCOND_USER_SETTINGS_PATH,uid,gid)

def RunSetup():
    CreateUserFolder()
    CopyGlobalProfiles()
    TakeOwnershipOfFolderAndFiles()

if __name__ == "__main__":
    RunSetup()