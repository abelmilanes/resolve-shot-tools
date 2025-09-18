import re
from proj_tools.proj_data import Config


class NamingConvention:
    def __init__(self):
        self.config = Config().get_config()

    def naming(self, category, preset="", args_dict=None):

        if category == "image":
            name = self.config['naming_convention'][category][preset]['file']
            path = self.config['naming_convention'][category][preset]['path']
            if args_dict:
                for k, v in args_dict.items():
                    if k in name:
                        name = re.sub(k, v, name)
                        path = re.sub(k, v, path)

            return {"path": path, "name": name}

        if category == "shotid":
            pfix = self.config['naming_convention'][category]['pfix']
            pad = self.config['naming_convention'][category]['pad']
            shotid = [pfix, pad]
            if args_dict:
                shotid[0] = re.sub("<sequence>", args_dict['seq'], pfix)
                shotid[1] = str(int(args_dict['id'])).zfill(int(pad))
                shotid = ''.join(shotid)
                return shotid

        if category == "paths":
            path = self.config['naming_convention'][category][preset]['path']
            if args_dict:
                for k, v in args_dict.items():
                    path = re.sub(k, v, path)
                return path


if __name__ == "__main__":
    naming_convention = NamingConvention()

    # Example usage
    # shot = naming_convention.naming('shotid', args_dict={"seq": "sht", "id": 40})
    # print(naming_convention.naming('image', 'plate', {"shotid": shot, "track": "SRC", "release": "R1"}))
    #
    # Example tests
    # print(naming_convention.naming('shotid', args_dict={"seq": "sht", "id": 40}))
    # print(naming_convention.naming('image', 'plate', {"shotid": "sht040", "track": "SRC"}))
