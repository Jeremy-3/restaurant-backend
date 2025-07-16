from fastapi import FastAPI,Request
#from app.api import  user, auth,roles,permissions,role_permissions,employees,position,lob,department
# from app.schemas.response import ResponseModel
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware
import logging
app = FastAPI()

# app.include_router(auth.router)
# app.include_router(user.router)
# app.include_router(permissions.router)
# app.include_router(roles.router)
# app.include_router(role_permissions.router)
# app.include_router(employees.router)
# app.include_router(position.router)
# app.include_router(lob.router)
# app.include_router(department.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configure logger
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Format for log messages
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseModel(
            success=False,
            message=exc.detail,
            errors=None
        ).model_dump()
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = []
    for err in exc.errors():
        # Get field name from location
        loc = err.get("loc", [])
        field = loc[-1] if loc else "unknown"
        message = err.get("msg", "Invalid input")
        formatted_errors.append({
            "field": field,
            "message": message
        })

    return JSONResponse(
        status_code=422,
        content=ResponseModel(
            success=False,
            message="Validation Error",
            errors={"details": formatted_errors}
        ).model_dump()
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ResponseModel(
            success=False,
            message="Internal Server Error",
            errors={"details": str(exc)}
        ).model_dump()
    )

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logging.error(str(exc))
    return JSONResponse(
        status_code=500,
        content=ResponseModel(
            success=False,
            message="A database error occurred",
            errors=None
            # errors={"details": str(exc)}
        ).model_dump()
    )

   