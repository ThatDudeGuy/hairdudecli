class Command():
    LOGIN = "login"
    UPLOAD = "upload"
    DOWNLOAD = "download"
    MOVE = "mv"
    GET_FILES = "getfiles"
    REPORT = "report"

    COMMANDS = frozenset(
        [
            LOGIN, 
            UPLOAD,
            DOWNLOAD,
            MOVE,
            GET_FILES,
            REPORT,
        ]
    )


    def exists(command) -> bool:
        return command in Command.COMMANDS
