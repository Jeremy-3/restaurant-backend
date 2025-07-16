from fastapi import HTTPException
from functools import wraps
from typing import Callable,Any,Union,List

def require_role(role_name: str):
    def wrapper(func: Callable):
        @wraps(func)
        def inner(*args: Any, **kwargs: Any):
            user_data = kwargs.get("user") or args[0]

            # If user_data is a dict → get role from "role_name"
            if isinstance(user_data, dict):
                current_role = user_data.get("role_name")
            else:
                # If it's an ORM object
                current_role = getattr(user_data.role, "name", None)

            if not current_role or current_role != role_name:
                raise HTTPException(
                    status_code=403,
                    detail=f"Requires {role_name} role"
                )

            return func(*args, **kwargs)
        return inner
    return wrapper


def check_permissions(required_permission: str):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user_data = kwargs.get("user")

            # If user_data is the dict returned by get_current_user()
            if isinstance(user_data, dict):
                perms = user_data.get("permissions", [])
            elif hasattr(user_data, "role"):  # If it's an ORM object
                perms = [p.permission.name for p in user_data.role.role_permissions]
            else:
                perms = []

            if required_permission not in perms:
                raise HTTPException(
                    status_code=403,
                    detail=f"Missing required permission: {required_permission}"
                )

            return func(*args, **kwargs)
        return inner
    return wrapper