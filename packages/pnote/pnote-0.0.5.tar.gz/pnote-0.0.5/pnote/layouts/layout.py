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
        return [p.relative_to(self.paths["files"]) for p in paths]

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
        return os.path.join(self.todaysubdir(), self.todayname())
    
    def todaypath(self):
        return os.path.join(self.paths["files"],self.todaysubpath())
