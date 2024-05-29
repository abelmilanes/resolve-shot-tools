# resolve_tools/resolve_connect.py

import sys


class ResolveConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResolveConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        sys.path.append('/mnt/apps/linux/resolve/Developer/Scripting/Modules')
        sys.path.append('/mnt/apps/linux/resolve/libs/Fusion')
        try:
            import DaVinciResolveScript as bmd
            self.dr = bmd.scriptapp("Resolve")
            self.pm = self.dr.GetProjectManager()
            self.rp = self.pm.GetCurrentProject()
            print(self.dr.GetProductName(), self.dr.GetVersionString())
        except ImportError as e:
            print("Failed to import DaVinci Resolve Script module:", e)
            sys.exit(1)
        except Exception as ex:
            print("Resolve not running:", ex)
            sys.exit(1)

    def get_current_project(self):
        return self.pm.GetCurrentProject()

    def get_current_timeline(self):
        return self.rp.GetCurrentTimeline()

    def get_render_presets(self):
        return self.rp.GetRenderPresets()

    def get_render_jobs(self):
        return self.rp.GetRenderJobList()

# Example usage:
# resolve_conn = ResolveConnection()
# current_project = resolve_conn.get_current_project()
