from fastapi import HTTPException


class APIError(HTTPException):
    status_code: int = 501
    detail: str = ""

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)
