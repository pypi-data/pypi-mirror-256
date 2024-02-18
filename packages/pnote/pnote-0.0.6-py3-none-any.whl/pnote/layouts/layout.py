from pathlib import Path
from datetime import datetime
import os

class Layout:

    def __init__(self, conf, paths):
        self.conf=conf
        self.paths=paths
        self.today=datetime.today()

    def flatten(self):
        paths=list(Path(self.paths["files"]).rglob("*"))
        result=list()
        for p in paths:
            if os.path.isfile(p):
                result.append(p.relative_to(self.paths["files"]))
        return result

    def create(self):
        file=self.todaypath()
        if not os.path.exists(file):
            open(file, 'a').close()
        return self.todaysubpath()
        
    def todayname(self):
        format=self.today.strftime('%Y-%m-%d')
        return format+self.conf["extension"]

    def todaysubdir(self):
        """
        Must be overriden by child classes
        """
        pass

    def todaysubpath(self):
        subdir=self.todaysubdir()
        if not os.path.exists(self.todaysubdir()):
            Path(os.path.join(self.paths["files"],subdir)).mkdir(parents=True, exist_ok=True)
        return os.path.join(self.todaysubdir(), self.todayname())
    
    def todaypath(self):
        return os.path.join(self.paths["files"],self.todaysubpath())
