from typing import Any, Optional
from werkzeug.exceptions import BadRequest
from wtforms.csrf.core import CSRF

def generate_csrf(secret_key: Optional[Any] = ..., token_key: Optional[Any] = ...): ...
def validate_csrf(data: Any, secret_key: Optional[Any] = ..., time_limit: Optional[Any] = ..., token_key: Optional[Any] = ...) -> None: ...

class _FlaskFormCSRF(CSRF):
    meta: Any = ...
    def setup_form(self, form: Any): ...
    def generate_csrf_token(self, csrf_token_field: Any): ...
    def validate_csrf_token(self, form: Any, field: Any) -> None: ...

class CSRFProtect:
    def __init__(self, app: Optional[Any] = ...) -> None: ...
    def init_app(self, app: Any): ...
    def protect(self) -> None: ...
    def exempt(self, view: Any): ...
    def error_handler(self, view: Any): ...

class CsrfProtect(CSRFProtect):
    def __init__(self, app: Optional[Any] = ...) -> None: ...

class CSRFError(BadRequest):
    description: str = ...