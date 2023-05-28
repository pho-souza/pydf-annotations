import json
import os


class Config_file:
    def __init__(self,  cfg_file: str = ""):
        self.default_config()
        if cfg_file != "" and os.path.isfile(cfg_file):
            self.__file = open(cfg_file, mode='r', encoding = 'utf-8')
            self.__config_file = json.load(self.__file)
        else:
            self.__config_file = self.__default
        self.validate()
        
    def change_cfg(self,  parameter,  new_value):
        self.config[parameter] = new_value
    
    # @property
    def get_cfg(self,  parameter: str):
        return self.config[parameter]
  
    @property
    def config(self):
        return self.__config_file["config"]

    def save(self,  path):
        json_save = json.dumps(self.__config_file,  indent=4)
        with open(path,  mode="w",  encoding="utf-8") as f:
            f.write(json_save)

    def validate(self):
        for default in self.default:
            if default in self.config.keys() is False:
                default_value = self.default[default]
                self.change_cfg(parameter=default,  new_value=default_value)

    @property
    def default(self):
        return self.__default["config"]

    def default_config(self):
        self.__default = {}
        self.__default["config"] = {
        }
        default = self.__default["config"]
        
        # Default values
        # project_folder = os.path.abspath(pathlib.Path(__file__).parent)
        project_folder = os.path.abspath("app")
        # project_folder = re.sub("\\\\",  "/",  project_folder)
        
        template_folder = project_folder + "/templates/"
        default.setdefault("DEFAULT_TEMPLATE",  "template_html.html")
        default.setdefault("IMG_FOLDER",  "img/")
        default.setdefault("TEMPLATE_FOLDER",  template_folder)
        default.setdefault("DEFAULT_COLOR",  [1.0,  1.0,  0.0])
        default.setdefault("INTERSECTION_LEVEL",  0.1)
        default.setdefault("COLUMNS",  1)
        default.setdefault("TOLERANCE",  0.1)
        default.setdefault("ADJUST_COLOR",  True)
        default.setdefault("ADJUST_DATE",  True)
        default.setdefault("ADJUST_TEXT",  True)
        default.setdefault("IMAGE",  True)
        default.setdefault("INK",  True)
        default.setdefault("ADJUST_COLOR",  True)
        