class Command():
    LOGIN = "login"
    UPLOAD = "upload"
    DOWNLOAD = "download"
    MOVE = "mv"
    GET_FILES = "getfiles"
    REPORT = "report"

COMMANDS = frozenset(
    [
        Command.LOGIN, 
        Command.UPLOAD,
        Command.DOWNLOAD,
        Command.MOVE,
        Command.GET_FILES,
        Command.REPORT,
    ]
)
