class Package:

    def __init__(self, name):
        self.name = name
        self.unknownModuleCount = 0
        self.modules = dict()
        return

    def addModule(self, name, module):
        if name in self.modules:
            return False
        else:
            self.modules[name] = module
            return True

    def getModuleFromName(self, name):
        if name in self.modules:
            return self.modules[name]
        else:
            return None

    def getAnimationFromName(self, name):
        for moduleName, animations in self.modules.items():
            for animationName, animation in animations.items():
                if name == animationName:
                    return animation

    def hasAnimation(self):
        for moduleName, animations in self.modules.items():
            for animation in animations:
                return True
        return False

    def moduleCount(self):
        return len(self.modules.keys())