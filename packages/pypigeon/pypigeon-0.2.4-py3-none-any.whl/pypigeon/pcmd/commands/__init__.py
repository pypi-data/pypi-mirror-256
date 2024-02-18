from .auth import AuthCommands
from .base_commands import BaseCommands
from .cde import CdeCommands
from .pdd import PddCommands


class Commands(BaseCommands):
    auth = AuthCommands
    cdeset = CdeCommands
    pdd = PddCommands
