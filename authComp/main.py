from .src.Tokens import TOKENS
from manager._Manager import Manager

def main_auth():
    
    manager = Manager(token=TOKENS)

    manager.start_listening_messages()