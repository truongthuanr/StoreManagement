from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from config.config import *

# Khởi tạo templates
templates = Jinja2Templates(directory="templates")

def render_template(request: Request, template_name: str, context: dict = {}) -> HTMLResponse:
    # Lấy user từ middleware
    user = getattr(request.state, "user", None)
    # Merge context
    context = {
        **context,
        "request": request,
        "user": user,
    }
    return templates.TemplateResponse(template_name, context)
