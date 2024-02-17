import os
import json


class Application:
    def __init__(self, pathToMainFile: str, title: str = "URPC Application"):
        self.mainFile = pathToMainFile
        self.title = title

    def run(self, args : list = []):
        if self.mainFile is None:
            print(f'File \"{self.mainFile}\" Not Found!')
            return f'File \"{self.mainFile}\" Not Found!'
        if os.path.isfile(self.mainFile):
            print(f"Error: Isn\'t a file: {self.mainFile}")
            return f"Error: Isn\'t a file: {self.mainFile}"

        cfgURPC = self.mainFile + '/cfg/config.json/' # Path to URPC config. More about it on GitHub
        with open(cfgURPC, 'w') as file:
            try:
                json.dump(args, file)
            except:
                print(f'Error while writing config file: {cfgURPC} with data {args}')

        try:
            exec(self.mainFile)
        except:
            print(f"Error while running file \"{self.mainFile}\"")
            return f'Error while running file \"{self.mainFile}'