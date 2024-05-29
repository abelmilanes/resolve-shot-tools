import re
from typing import Dict, Optional, Union
from proj_tools.proj_data import Config

class NamingConvention:
    def __init__(self):
        self.config_data = Config().get_config()

    def naming(self, category: str, preset: str = "", args_dict: Optional[Dict[str, str]] = None) -> Union[Dict[str, str], str]:
        """Generate naming convention based on category and preset with optional arguments.

        Args:
            category (str): The category of naming convention ('image' or 'shotid').
            preset (str, optional): The preset for the category. Defaults to "".
            args_dict (Optional[Dict[str, str]], optional): Dictionary of arguments for replacements. Defaults to None.

        Returns:
            Union[Dict[str, str], str]: A dictionary with 'path' and 'name' for 'image' category, or a 'shotid' string.
        """
        if category == "image":
            return self._get_image_naming(preset, args_dict)
        elif category == "shotid":
            return self._get_shotid_naming(args_dict)
        else:
            raise ValueError(f"Unknown category: {category}")

    def _get_image_naming(self, preset: str, args_dict: Optional[Dict[str, str]]) -> Dict[str, str]:
        """Generate naming for image category based on preset and arguments.

        Args:
            preset (str): The preset for the image category.
            args_dict (Optional[Dict[str, str]]): Dictionary of arguments for replacements.

        Returns:
            Dict[str, str]: A dictionary with 'path' and 'name'.
        """
        name = self.config_data['naming_convention']['image'][preset]['file']
        path = self.config_data['naming_convention']['image'][preset]['path']
        if args_dict:
            name = self._replace_args(name, args_dict)
            path = self._replace_args(path, args_dict)
        return {"path": path, "name": name}

    def _get_shotid_naming(self, args_dict: Optional[Dict[str, str]]) -> str:
        """Generate shot ID based on arguments.

        Args:
            args_dict (Optional[Dict[str, str]]): Dictionary of arguments for replacements.

        Returns:
            str: The generated shot ID.
        """
        pfix = self.config_data['naming_convention']['shotid'].get('pfix', "")
        pad = int(self.config_data['naming_convention']['shotid']['pad'])
        if args_dict:
            seq = args_dict.get('seq', "")
            shot_id = str(int(args_dict.get('id', 0))).zfill(pad)
            shotid = f"{seq}{pfix}{shot_id}"
            return shotid
        else:
            raise ValueError("args_dict must be provided for 'shotid' category")

    @staticmethod
    def _replace_args(template: str, args_dict: Dict[str, str]) -> str:
        """Replace placeholders in the template string with values from args_dict.

        Args:
            template (str): The template string with placeholders.
            args_dict (Dict[str, str]): Dictionary of arguments for replacements.

        Returns:
            str: The template string with placeholders replaced by actual values.
        """
        for k, v in args_dict.items():
            template = re.sub(rf"\b{k}\b", v, template)
        return template


if __name__ == "__main__":
    naming_convention = NamingConvention()

    # Example usage
    # shot = naming_convention.naming('shotid', args_dict={"seq": "sht", "id": 40})
    # print(naming_convention.naming('image', 'plate', {"shotid": shot, "track": "SRC", "release": "R1"}))
    #
    # Example tests
    # print(naming_convention.naming('shotid', args_dict={"seq": "sht", "id": 40}))
    # print(naming_convention.naming('image', 'plate', {"shotid": "sht040", "track": "SRC"}))
