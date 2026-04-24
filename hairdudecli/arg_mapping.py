import hairdudecli.api
from types import FunctionType
from hairdudecli.commands import Command
from hairdudecli.syntax_checker import SyntaxChecker


ARGS_MAP:dict[str, FunctionType] = {
    Command.LOGIN: {
        "check_syntax": SyntaxChecker.login,
        "run_command": hairdudecli.api.login,
    },
    Command.UPLOAD: {
        "check_syntax": SyntaxChecker.upload,
        "run_command": hairdudecli.api.upload_files,
    },
    Command.DOWNLOAD: {
        "check_syntax": SyntaxChecker.download,
        "run_command": hairdudecli.api.download_files,
    },
    Command.MOVE: {
        "check_syntax": SyntaxChecker.move,
        "run_command": hairdudecli.api.move_file,
    },
    Command.GET_FILES: {
        "check_syntax": SyntaxChecker.get_files,
        "run_command": hairdudecli.api.get_user_files_and_directories,
    },
    Command.REPORT: {
        "check_syntax": SyntaxChecker.report,
        "run_command": hairdudecli.api.report,
    }
}

def dispatch_command(args: list[str]):
    for command in args:
        if command in ARGS_MAP:
            # validates syntax and exits upon bad syntax
            ARGS_MAP[command]["check_syntax"](args)
            # below is only ran if syntax is valid
            ARGS_MAP[command]["run_command"](args)

