from easy.massage import failed, success, inform, warn, test
from defoult_config import default_config
import json
import sys
import os
import sys

class Config:
    def __init__(self, Version):
        self.default_config_path = "Configs"
        self.default_config_name = "Config.json"
        self.config = None
        if (len(sys.argv) > 1):
            self.config = self.config_red (sys.argv[1])
            if (Version != self.get_value(parameter1="Version of config")):
                failed (f"VERSION IS INCORECT. Expected = {Version}, bat got {self.get_value(parameter1="Version of config")}")
                self.create_config()
        else:
            failed(f"Dont got config file as argument...")
            self.create_config()

    def Refresh (self, TG_LOG):
        t = self.config_red (sys.argv[1])
        if (t != self.config):
            TG_LOG(warn("Config was changed! Reloading nesesery compounents. . ."))
            sys.exit(0)
    def create_config(self):
        if input("Create a config template? (Yes/No): ").strip().lower() in ('yes', 'y'):
            try:
                self.check_and_create_dir(self.default_config_path)
                with open(f"{self.default_config_path}/{self.default_config_name}", 'w') as f:
                    json.dump(default_config, f, indent=4)
                success(f"File '{self.default_config_path}/{self.default_config_name}' created successfuly!.")
                exit()
            except Exception as err:
                failed(f"Cant create config file: {err}")
        else:
            inform("The creation of the configuration file has been canceled.")
        sys.exit(0)

    def check_and_create_dir(self, dir_path):   # Пере і створює в разі чого вказану директорію 
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
            except Exception as err:
                failed(f"Cant create {dir_path} directiry: {err}")            
            inform(f"Directory '{dir_path}' created succesfuly.")

    def config_red (self, config_path):
        try:
            with open(config_path, 'r') as file:
                return json.load(file)
        except Exception as err:
            failed(f"Cant open config file: {err}")

    def get_value (self, parameter1 = None, parameter2 = None, parameter3 = None, parameter4 = None):
        try:
            if parameter4 != None:
                return (self.config[parameter1][parameter2][parameter3][parameter4])
            elif parameter3 != None:
                return (self.config[parameter1][parameter2][parameter3])
            elif parameter2 != None:
                return (self.config[parameter1][parameter2])
            elif parameter1 != None:
                return (self.config[parameter1])
        except Exception as e:
            failed(f"ERROR while reading config: {e}")