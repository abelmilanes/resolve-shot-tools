import os
import gazu

kitsu_admin = os.environ["TX_KITSU_ADMIN"]
kitsu_paswd = os.environ["TX_KITSU_PASWD"]


def get_kitsu(url):
    try:
        # print(url)
        gazu.set_host(url+"/api")
        gazu.set_event_host(url+"/")
        gazu.log_in(kitsu_admin, kitsu_paswd)
        print("Gazu connected to: \n"+gazu.get_host())
    except Exception as e:
        print("Not connected to Kitsu")
        print(e)
        pass


def get_project(proj_name):
    project = gazu.project.get_project_by_name(proj_name)
    print("Kitsu project: ", project)
    return project


if __name__ == "__main__":
    pass
