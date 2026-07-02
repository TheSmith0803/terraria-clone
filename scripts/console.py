

class Console:
    def __init__(self):
        self.functions = {
            "godmode": self.god_mode,
            "give": self.give_item,
            "teleport": self.teleport,
        }
    
    def god_mode(self):
        pass

    def give_item(self):
        pass

    def teleport(self):
        pass

    def execute(self, command):
        func = self.functions.get(command)

        if func is None:
            print('unknown command')
            return
        
        func()