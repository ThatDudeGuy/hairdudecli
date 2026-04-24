import sys
import math
from enum import Enum
from requests import Response

class StatusCode(Enum):
    Success = 200
    Redirect = 302
    BadInput = 400
    Unauthorized = 401
    ResourceUnavailable = 404
    ServerFailure = 500
    RateLimitExceeded = 503

class StatusCodeParser():
    def parse(response: Response) -> StatusCode:
        if response.status_code == StatusCode.ServerFailure.value:
            Logger.error("Server is offline. Contact he who shall not be named.", end="\r\n")
            sys.exit(1)
        elif response.status_code != StatusCode.Success.value:
            if response.status_code >= 400:
                if response.headers.get("ErrorMessage") or response.headers.get("errormessage"):
                    Logger.error(f"{response.headers.get("errormessage")}", end="\r\n")
                else:
                    Logger.error("Unkown Server error. Service may impacted, contact he who shall not be named.")
                    sys.exit(1)
            
        return StatusCode(response.status_code)


class ByteFactor():
    BYTES = "b"
    KILOBYTES = "KB"
    MEGABYTES = "MB"
    GIGABYTES = "GB"
    TERABYTES = "TB"

class FileSize():
    def __init__(self, total_bytes:int):
        self.total = total_bytes
        self.factor = ByteFactor.BYTES
        
        totalTB = (total_bytes * 8) / (8 * 10**12)
        if(math.floor(totalTB) > 0):
            self.total = round(totalTB, 2)
            self.factor = ByteFactor.TERABYTES
        
        totalGB = (total_bytes * 8) / (8 * 10**9)
        if math.floor(totalGB) > 0:
            self.total = round(totalGB, 2)
            self.factor = ByteFactor.GIGABYTES

        totalMB = (total_bytes * 8) / (8 * 10**6)
        if math.floor(totalMB) > 0:
            self.total = round(totalMB, 2)
            self.factor = ByteFactor.MEGABYTES

        totalKB = (total_bytes * 8) / (8 * 10**3)
        if math.floor(totalKB) > 0:
            self.total = round(totalKB, 2)
            self.factor = ByteFactor.KILOBYTES
            
    def __repr__(self):
        return f"{self.total} {self.factor}"

class Logger():
    previous_msg_length = 0

    def log(msg, end='\n'):
        if '\r' in end:
            print(msg + " " * (Logger.previous_msg_length - len(msg)), end=end)
        else:
            print(msg, end=end)
        Logger.previous_msg_length = len(msg)

    def warn(msg, end='\n'):
        Logger.log(f"[WARNING] {msg}", end)

    def error(msg, end='\n', is_bug=False):
        if is_bug:
            Logger.log(f"[ERROR] {msg} | Report this bug by using command 'hd-drive report'", end)
        else:
            Logger.log(f"[ERROR] {msg}", end)
