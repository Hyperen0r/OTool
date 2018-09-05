class NamedContainer:

    def __init__(self, name):
        self.name = name
        self.items = []

    def addItem(self, item):
        self.items.append(item)