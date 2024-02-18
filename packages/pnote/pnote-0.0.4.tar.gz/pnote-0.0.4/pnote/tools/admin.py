from pnote.tools.tool import Tool
import argparse

class ToolAdmin(Tool):

    def add_parser(self,subparsers):
        self.p = subparsers.add_parser("admin", description="Manage your notes tags")
        self.p.add_argument("-f", "--fix", help="fix new and delete note files", action='store_true')

    def run(self, project, args):
        if args.fix:
            project.fix()
        else:
            self.p.print_help()
