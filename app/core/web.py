from fastapi.templating import Jinja2Templates


# Central templates instance so route modules can render pages consistently.
templates = Jinja2Templates(directory="templates")

