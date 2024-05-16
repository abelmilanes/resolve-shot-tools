#!/usr/bin/python3
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
