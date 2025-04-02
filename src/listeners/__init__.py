# from listeners import actions
# from listeners import shortcuts
# from listeners import views
from src.listeners import commands
from src.listeners import events
from src.listeners import messages


def register_listeners(app):
    # actions.register(app)
    # shortcuts.register(app)
    # views.register(app)
    commands.register(app)
    events.register(app)
    messages.register(app)
