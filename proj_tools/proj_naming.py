import re
from proj_tools.proj_data import config


def naming(category, preset="", args_dict=None):
    config_data = config()
    if category == "image":
        name = config_data['naming_convention'][category][preset]['file']
        path = config_data['naming_convention'][category][preset]['path']
        if args_dict:
            for k, v in args_dict.items():
                if k in name:
                    name = re.sub(k, v, name)
                    path = re.sub(k, v, path)

        return {"path": path, "name": name}

    if category == "shotid":
        pfix = config_data['naming_convention'][category]['pfix']
        if not pfix:
            pfix = ""
        pad = config_data['naming_convention'][category]['pad']
        shotid = [pfix, pad]
        if args_dict:
            shotid[0] = re.sub("sequence", args_dict['seq'], pfix)
            shotid[1] = str(int(args_dict['id'])).zfill(int(pad))
            shotid = ''.join(shotid)
            return shotid


if __name__ == "__main__":
    pass

# Tests
# shot = naming('shotid', "name", {"seq": "sht", "id": 40})
# print(naming('image', 'plate', {"shotid": shot, "track": "SRC", "release": "R1"}))
