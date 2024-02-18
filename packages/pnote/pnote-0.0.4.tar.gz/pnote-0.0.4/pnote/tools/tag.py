from pnote.tools.tool import Tool
import argparse

class ToolTag(Tool):

    def add_parser(self,subparsers):
        p = subparsers.add_parser("tag", description="Manage your notes tags")
        p.add_argument("-s", "--subpaths", help="Subpaths to edit", nargs="+")
        p.add_argument("-a", "--add", help="Add tags to notes", nargs="+")
        p.add_argument("-d", "--delete", help="Delete tags from notes", nargs="+")

    def run(self, project, args):
        if args.subpaths:
            if args.add:
                project.addtags(args.subpaths,args.add)
            elif args.delete:
                project.deletetags(args.subpaths,args.delete)
        else:
            if args.delete:
                project.obliteratetags(args.delete)
            else:
                for tag in project.listtags():
                    print(tag)
