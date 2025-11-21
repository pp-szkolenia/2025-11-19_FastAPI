from fastapi import status, Request, Response


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
