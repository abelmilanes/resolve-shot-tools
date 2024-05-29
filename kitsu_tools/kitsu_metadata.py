import gazu

from kitsu_tools.kitsu_connect import get_kitsu
from proj_tools.proj_data import Config


def shot_metadata(proj, shot_id):
    conf = Config().get_config()
    server = conf[conf['project']['alias']]['kitsu_host']
    get_kitsu(server)
    print("%s:\n%s - %s" % ("Pulling Kitsu Data for", proj, shot_id))
    project = gazu.project.get_project_by_name(proj)
    shots = gazu.shot.all_shots_for_project(project)
    gazu_shot = ''
    for s in shots:
        if s['name'] == shot_id:
            gazu_shot = gazu.shot.get_shot(s['id'])
    return gazu_shot


if __name__ == "__main__":
    pass
