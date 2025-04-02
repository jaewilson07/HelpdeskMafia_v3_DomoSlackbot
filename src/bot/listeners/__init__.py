# from listeners import actions
# from listeners import shortcuts
# from listeners import views
from src.bot.listeners import commands
from src.bot.listeners import events
from src.bot.listeners import messages


def register_listeners(app):
    # actions.register(app)
    # shortcuts.register(app)
    # views.register(app)
    commands.register(app)
    events.register(app)
    messages.register(app)
