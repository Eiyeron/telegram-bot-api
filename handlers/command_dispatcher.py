

class CommandDispatcher:
    def __init__(self):
        self.commands = {}

    def add_command(self, command, callback):
        self.commands[command] = callback

    def on_text(self, tg, message):
        for command, callback in self.commands.items():
            if message.text.startswith(command):
                callback(tg, message)
