# from listeners import actions
# from listeners import shortcuts
# from listeners import views
from listeners import commands
from listeners import events
from listeners import messages


def register_listeners(app):
    # actions.register(app)
    # shortcuts.register(app)
    # views.register(app)
    commands.register(app)
    events.register(app)
    messages.register(app)
