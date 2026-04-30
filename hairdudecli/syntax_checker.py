import sys
from pathlib import Path
from hairdudecli.utils import Logger
from hairdudecli.commands import Command

def multi_command_check(args:list[str]) -> bool:
    command_count = 0
    for command in args:
        if Command.exists(command):
            command_count += 1
        if command_count >= 2:
            Logger.error(f"Only one command is allowed at a time. Remove '{command}' and each subsequent command after it.")
            return False

    if command_count == 0:
        Logger.error("No valid commands were given, see docs for proper commands: [link]")
        return False
    else:
        return True


class SyntaxChecker():
    def missing_arg(what_are_you_missing, command_name, some_url=None):
        return f"Missing '{what_are_you_missing}' from '{command_name}' command. See here for proper syntax -> {some_url}"

    def login(args:list[str]):
        command_name = Command.LOGIN
        start = args.index(command_name)
        
        if start + 1 == len(args):
            Logger.error(SyntaxChecker.missing_arg("username and password", command_name))
            sys.exit(1)
        elif start + 2 == len(args):
            Logger.error(f"'{command_name}' command requires 2 parameters, only 1 was given")
            sys.exit(1)

    def upload(args: list[str]):
        """
        All are possible
            -upload /my/file/path.txt (defaults to user's main path)
            -upload /my/file/path.txt /my/text/files
            -upload /my/file/path.txt -c /the/other/path.txt
            -upload /my/file/path.txt /my/text/files -c /the/other/path.txt
            -upload /my/file/path.txt /my/text/files -c /the/other/path.txt /other/files
        """
        command_name = Command.UPLOAD
        start = args.index(command_name)
        c_count = 0

        if start + 1 == len(args):
            Logger.error(SyntaxChecker.missing_arg("path to local file and path to upload to", command_name))
            sys.exit(1)

        for i in range(start + 1, len(args)):
            if args[i] == '-c':
                c_count += 1
                if i + 1 == len(args):
                    Logger.error("Chaining detected '-c', but no additional paths were given")
                    sys.exit(1)
            
            if c_count > 24:
                Logger.error("Max file limit exceeded. Cannot input more than 25 files in a request.")
                sys.exit(1)

    def download(args: list[str]):
        """
        hdcli -download
        hdcli -download /pictures/ <- Can specify a directory for a smaller list of options
        """
        start = args.index(Command.DOWNLOAD)

        for i in range(start + 1, len(args)):
            if not Path.is_dir(args[i]):
                Logger.error(f"Expected directory as argument. '{args[i]}' is not a directory")
                sys.exit(1)

    def move(args: list[str]):
        pass

# Don't know if I need this as a spearate api
    def get_files(args: list[str]):
        """
        hdcli -get-files
        hdcli -get-files /pictures/ <- Can specify a directory for a smaller list of options
        """
        start = args.index(Command.GET_FILES)

        for i in range(start + 1, len(args)):
            if not Path.is_dir(args[i]):
                Logger.error(f"Expected directory as argument. '{args[i]}' is not a directory")
                sys.exit(1)

    def report(args: list[str]):
        pass
