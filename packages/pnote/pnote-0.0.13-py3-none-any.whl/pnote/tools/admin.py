from pnote.tools.tool import Tool
import argparse

class ToolAdmin(Tool):

    def add_parser(self,subparsers):
        self.p = subparsers.add_parser("admin", description="Manage your notes tags")
        self.p.add_argument("-f", "--fix", help="fix new and delete note files", action='store_true')
        self.p.add_argument("--import", help="Import file(s) to notes", nargs="+", dest="imports")
        self.p.add_argument("--timestamp", help="Timestamp to use for file(s) import")


    def run(self, project, args):
        if args.fix:
            project.fix()
        elif args.imports:
            if args.timestamp:
                for f in args.imports:
                    project.addfile(f,int(args.timestamp))
            else:
                for f in args.imports:
                    project.addfile(f)
        else:
            self.p.print_help()
