import os, json, platform, socket, sqlite3
from datetime import datetime
from pathlib import Path

class Metadata:

    def __init__(self, paths):
        self.paths=paths
        self.today=datetime.today()

        ## Create folders
        self.paths["metadata"]=os.path.join(self.paths["root"], "metadata.db")

        ## Init database
        self.con=sqlite3.connect(self.paths["metadata"])
        cur=self.con.cursor()
        tables=cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='files'; """).fetchall()

        if len(tables) == 0:
            cur.execute("CREATE TABLE files(id INTEGER PRIMARY KEY AUTOINCREMENT, subpath TEXT UNIQUE, created REAL, hostname TEXT, platform TEXT);")
            self.con.commit()
            cur.execute("CREATE TABLE tags(id INTEGER, name TEXT, FOREIGN KEY(id) REFERENCES files(id));")
            self.con.commit()

    def create(self, subpath):
        cur=self.con.cursor()
        cur.execute("""INSERT INTO files(subpath,created,hostname,platform) values('{}',{},'{}','{}')""".format(
            subpath,
            datetime.today().timestamp(),
            socket.gethostname(),
            platform.platform()
        ))
        self.con.commit()

    def delete(self,subpath):
        cur=self.con.cursor()
        cur.execute('SELECT id FROM files WHERE subpath="{}"'.format(subpath))
        subpath_id=list(cur.fetchone())[0]
        cur.execute('DELETE FROM tags WHERE id={}'.format(subpath_id))
        cur.execute('DELETE FROM files WHERE id={}'.format(subpath_id))
        self.con.commit()

    def addtag(self, subpath, tag):
        cur=self.con.cursor()
        cur.execute('SELECT id FROM files WHERE subpath="{}"'.format(subpath))
        subpath_id=list(cur.fetchone())[0]
        cur.execute('INSERT INTO tags(id, name) VALUES({},"{}")'.format(subpath_id,tag))
        self.con.commit()

    def deletetag(self, subpath, tag):
        cur=self.con.cursor()
        cur.execute('SELECT id FROM files WHERE subpath="{}"'.format(subpath))
        subpath_id=list(cur.fetchone())[0]
        cur.execute('DELETE FROM tags WHERE id={} AND name="{}"'.format(subpath_id,tag))
        self.con.commit()

    def obliteratetag(self, tag):
        cur=self.con.cursor()
        cur.execute('DELETE FROM tags WHERE name="{}"'.format(tag))
        self.con.commit()

    def searchtag(self,tag):
        cur=self.con.cursor()
        ids=[i[0] for i in cur.execute('SELECT id FROM tags WHERE name="{}"'.format(tag)) ]
        subpaths=[cur.execute('SELECT subpath FROM files WHERE id={}'.format(i)).fetchone()[0] for i in ids]
        return subpaths

    def listtags(self):
        cur=self.con.cursor()
        tags=[i[0] for i in cur.execute('SELECT DISTINCT name FROM tags') ]
        return tags

    def fix_deleted(self):
        cur=self.con.cursor()
        for result in cur.execute("SELECT subpath FROM files"):
            subpath=result[0]
            path=os.path.join(self.paths["files"], subpath)
            if not os.path.exists(path):
                print("Deletion detected => " + subpath)
                self.delete(subpath)

    def fix_new(self, layout):
        cur=self.con.cursor()
        for subpath in layout.flatten():
            result=cur.execute('SELECT * from files where subpath="{}"'.format(subpath))
            if len(result.fetchall()) <= 0 :
                print("New file detected => "+str(subpath))
                self.create(subpath)

    def flatten_ordered(self, desc=False):
        cur=self.con.cursor()
        if not desc:
            result=cur.execute("SELECT subpath FROM files ORDER BY id")
        else:
            result=cur.execute("SELECT subpath FROM files ORDER BY id DESC")
        result=[subpath[0] for subpath in result.fetchall()]
        return result
