from fastapi import status, Request, Response
from datetime import datetime
import json
import os


async def confirm_deletion(request: Request, call_next):
    if request.method == "DELETE":
        deletion_confirmed = input("Sure to delete? [y/n]") == "y"

        if deletion_confirmed:
            response = await call_next(request)
            return response
        else:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        response = await call_next(request)
        return response


async def log_operations(request: Request, call_next):
    data = {
        "endpoint_URL": str(request.url.path),
        "method": request.method,
        "timestamp": str(datetime.now())
    }
    response = await call_next(request)

    data["response_code"] = response.status_code

    if os.path.exists("log.json"):
        with open("log.json", "r") as f:
            file_data = json.load(f)
        file_data.append(data)
        with open("log.json", "w") as f:
            json.dump(file_data, f, indent=2)
    else:
        with open("log.json", "w") as f:
            json.dump([data], f, indent=2)
    return response
