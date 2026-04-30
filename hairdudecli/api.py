import os
import sys
import json
import time
import requests
import urllib3
import ast
# Take this off if a trusted CA is ever imported
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from requests import Response
from hairdudecli.commands import Command
from requests.cookies import cookiejar_from_dict
from hairdudecli.utils import Logger, FileSize, StatusCode, StatusCodeParser
from hairdudecli.local_file_handler import (
    save_local_data,
    get_local_data,
    get_cookie_jar,
    DATA_PATH
)

# base_url = "https://24.22.134.130:10412/api" if "hairdude" not in os.environ["USER"] else "https://10.0.0.50:10412/api"
base_url = "https://10.0.0.50:10412/api"


def requires_cookie(func):
    def wrapper(*args, **kwargs):
        attempts = 0
        while attempts < 2:
            result: Response = func(*args, **kwargs)
            status = StatusCodeParser.parse(result)
            
            if status == StatusCode.Success or result.status_code == StatusCode.Redirect:
                break
            else:
                creds = get_local_data(["user", "pass"])
                if len(creds) == 2:
                    login([Command.LOGIN, creds["user"], creds["pass"]])
            time.sleep(1)
            attempts += 1

        if attempts >= 2:
            Logger.error(
                f"Max retried exceeded. Try again. If you think this is an issue with the tool itself, run the command 'hdcli {Command.REPORT}' "
                "or create an issue here: https://github.com/ThatDudeGuy/hairdudecli/issues"
            )
        return result
    return wrapper

@requires_cookie
def report(args: list[str], cookieJar=None) -> Response:
    pass

def login(args: list[str]) -> Response:
    start = args.index(Command.LOGIN)
    # The syntax checker ensures that the username and password is present
    user = args[start + 1]
    passw = args[start + 2]

    try:
        response = requests.post(f"{base_url}", json={"user": user, "pass": passw}, verify=False)
        # Parser will handle any failures
        StatusCodeParser.parse(response)
    except Exception as e:
        Logger.error(f"Server Unreachable: {e}")
        sys.exit(1)
    
    save_local_data([("last_known_cookie", f"{response.cookies.get_dict()}")])
    Logger.log("Login successful!")

    prompt = get_local_data(["ask_to_save_creds"])

    if prompt is None or (isinstance(prompt, dict) and len(prompt) == 0) or prompt.get("ask_to_save_creds") is False:
        answer = input("Do you want to keep your credentials saved? (y/n): ")
        if answer.lower() == 'y':
            save_local_data( [("user", user), ("pass", passw)] )

            answer = input("Remember my decision? (y/n): ")

            if answer.lower() == 'n':
                save_local_data([("ask_to_save_creds", False)])
            elif answer.lower() == 'y':
                save_local_data([("ask_to_save_creds", True)])
                Logger.log("Got it, won't ask again. If you need to change your credentials, run the login -force command at the end")
    else:
        save_local_data([
            ("user", user), 
            ("pass", passw), 
        ])

    return response


@requires_cookie
def upload_files(args: list[str], cookieJar=None) -> Response:
    start = args.index(Command.UPLOAD)
    filename = None
    path = "/" # defaults to user's root path
    fileData = None

    total_uploads = len(args) // 2
    total_data = 0

    data_captured = False

    for i in range(start + 1, len(args)):
        if args[i] == "-c":
            data_captured = False
            path = "/"
            continue

        if data_captured is False:
            filepath = args[i]
            data_captured = True
        else:
            path = args[i]
            if '.' in path:
                Logger.error(f"Upload target '{path}' appears to be a filepath, must be directory.")
                sys.exit(1)

        try:
            with open(filepath, "r") as local_file:
                fileData = bytes(local_file.buffer.read())
                total_data += len(fileData)
                filename = filepath.split('/')[-1] if '\\' not in filepath else filepath.split('\\')[-1]
        except FileNotFoundError:
            Logger.error(f"No file was found at given path: {filepath}\nDouble check the given path and whether your file does indeed exist.", end="\r\n")
            sys.exit(1)
        except IsADirectoryError:
            Logger.error(f"Expected a filepath, got directory instead. Did you mean to put '{filepath}' as your upload target?", end="\r\n")
            sys.exit(1)
        except Exception as e:
            Logger.error(f"{e} | i = {i} | Copy this output, run command 'hd-drive report' and paste the output to report this bug.", end="\r\n")
            sys.exit(1)

        Logger.log(f"Uploading {filename:^30s} {str(FileSize(len(fileData))):<8s} | {i:2d} / {total_uploads:<2d}", end="\r")

        response = requests.post(
            url=f"{base_url}/upload",
            data=fileData,
            cookies=get_cookie_jar() if cookieJar is None else cookieJar,
            verify=False,
            headers={"filename": filename, "path": path}
        )

        if response.status_code != StatusCode.Success.value:
            total_data -= len(fileData)

    Logger.log(f"Complete! You uploaded {str(FileSize(total_data)):^8s} worth of data.", end="\r\n") if response.status_code == StatusCode.Success.value else None
    return response

@requires_cookie
def download_files(args: list[str], cookieJar=None) -> Response:
    selections = []
    numbers_used = set()
    paths = get_user_files_and_directories(None)
    filepaths:list = ast.literal_eval(paths.headers.get("paths"))
    
    answer = None
    while answer != "" and answer != "done":
        try:
            if len(selections) == 0:
                answer = input(f"Type in the corresponding value of the file you would like to download and hit enter: {answer}")
            else:
                answer = input(f"Provide another value or enter an empty line to complete this process. Your selections: {selections} ")

            answer = int(answer)
        except:
            pass

        if isinstance(answer, int) and (answer >= 1 and answer <= len(filepaths)):
            if answer in numbers_used:
                print(f"{filepaths[answer - 1]} has already been selected, skipping.")
                continue
            numbers_used.add(answer)
            selections.append(filepaths[answer - 1])
        elif answer == "" or answer == "done":
            print("No selections receieved, exiting.")
        else:
            print(f"Bad Input. You need to provide an integer value between the values 1-{len(filepaths)}: ")          
    
    response = requests.post(
        url=f"{base_url}/download",
        json={"paths": ";".join(selections) if len(selections) > 1 else f"{selections[0]+';'}"},
        cookies=get_cookie_jar() if cookieJar is None else cookieJar,
        verify=False,
        stream=True
    )
    
    # TODO: Catch the error if permission is denied
    with open("/tmp/requested_files.zip", "w") as requested_files:
        requested_files.buffer.write(response.content)
        Logger.log("Downloaded requested files in '/tmp/requested_files.zip'")

    return response

@requires_cookie
def move_file(args: list[str], cookieJar=None) -> Response:
    start = args.index(Command.MOVE)

    response = requests.get(url=f"{base_url}/move", cookies=get_cookie_jar() if cookieJar is None else cookieJar, verify=False)

# TODO: Display the file size of each file in the console
@requires_cookie
def get_user_files_and_directories(args: list[str], cookieJar=None) -> Response:
    response = requests.get(url=f"{base_url}/files", cookies=get_cookie_jar() if cookieJar is None else cookieJar, verify=False)

    if response.status_code == StatusCode.Success.value:
        paths = response.json()
        paths = paths["files"].split(';')
    else:
        return response

    path = []
    organized_paths: list[str] = []

    for i in range(len(paths)):
        if '.' not in paths[i] and '/' not in paths[i]:
            if len(path) != 0:
                organized_paths.append("".join(path))
                path.clear()
            path.append(paths[i])
        elif '.' not in paths[i] and '/' in paths[i]:
            path.append(paths[i])
        elif '.' in paths[i] and '/' in paths[i]:
            if len(path) != 0:
                path.append(paths[i])
                organized_paths.append("".join(path))
                root = path[0]
                path.clear()
                path.append(root)
        else:
            if len(path) != 0:
                organized_paths.append("".join(path))
                path.clear()
            organized_paths.append(paths[i])

    remove = []
    for path in organized_paths:
        if '.' not in path and '/' not in path:
            remove.append(path)
    for value in remove:
        organized_paths.remove(value)

    count = 1
    for path in organized_paths:
        Logger.log(f"{count:>3d}. {path}")
        count += 1

    response.headers["paths"] = str(organized_paths)
    return response
