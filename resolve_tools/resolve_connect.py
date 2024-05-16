
"""
DaVinci Resolve needs to be running for a script to be invoked.

For a Resolve script to be executed from an external folder, the script needs to know of the API location.
You may need to set the these environment variables to allow for your Python installation to pick up the appropriate dependencies as shown below:

    Mac OS X:
    RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
    RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"

    Windows:
    RESOLVE_SCRIPT_API="%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
    RESOLVE_SCRIPT_LIB="C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
    PYTHONPATH="%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\"

    Linux:
    RESOLVE_SCRIPT_API="/opt/resolve/Developer/Scripting"
    RESOLVE_SCRIPT_LIB="/opt/resolve/libs/Fusion/fusionscript.so"
    PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
    (Note: For standard ISO Linux installations, the path above may need to be modified to refer to /home/resolve instead of /opt/resolve)
"""

import sys


def resolve():
    sys.path.append('/mnt/apps/linux/resolve/Developer/Scripting/Modules')
    sys.path.append('/mnt/apps/linux/resolve/libs/Fusion')
    import DaVinciResolveScript as bmd
    return bmd.scriptapp("Resolve")


try:
    dr = resolve()
    pm = dr.GetProjectManager()
    rp = pm.GetCurrentProject()  # Get current project
    print(dr.GetProductName(), dr.GetVersionString())


except Exception as ex:
    print("Resolve not running: \n", ex)
    sys.exit()
    pass


def current_project():
    return pm.GetCurrentProject()


def current_timeline():
    return rp.GetCurrentTimeline()


def render_presets():
    return rp.GetRenderPresets()


def render_jobs():
    return rp.GetRenderJobList()
