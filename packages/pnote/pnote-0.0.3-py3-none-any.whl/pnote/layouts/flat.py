from pnote.layouts.layout import Layout

class LayoutFlat(Layout):

    def __init__(self, conf, paths):
        Layout.__init__(self, conf, paths)
        self.paths=paths

    def todaysubdir(self):
        return ""
