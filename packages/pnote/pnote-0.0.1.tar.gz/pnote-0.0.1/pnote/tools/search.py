from pnote.tools.tool import Tool
import argparse

class ToolSearch(Tool):

    def add_parser(self,subparsers):
        p = subparsers.add_parser("search", description="Perform search operation on your notes")
        p.add_argument("-g", "--grep", help="Grep an expression")
        p.add_argument("-n", "--name", help="Search for a note path", nargs="?", default=argparse.SUPPRESS)
        p.add_argument("-t", "--tag", help="Search for a note with a tag")

    def run(self, project, args):
        if args.grep:
            first=True
            for entry in project.grep(args.grep):
                if not first:
                    print()
                subpath=entry[0]
                print("=> "+subpath)
                for line in entry[1]:
                    ln=line[0]
                    content=line[1]
                    print("L{}: {}".format(ln,content))
                first=False
        elif args.tag:
            for subpath in project.searchtag(args.tag):
                print(subpath)
        elif args.name or args.name is None:
            [ print(subpath) for subpath in project.find(args.name) ]


