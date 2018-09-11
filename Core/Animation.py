from Core.Utils import create_item
from Core.Config import get_config
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

class Animation:

    def __init__(self, name=""):
        self.actors = dict()
        self._name = name

    def addStage(self, stage):
        actor = stage.actor()
        if actor in self.actors:
            self.actors[actor].append(stage)
        else:
            self.actors[actor] = [stage]

    def actorsCount(self):
        return len(self.actors)

    def stagesCount(self, actor=""):
        if not actor:
            actor = next(iter(self.actors.keys()))

        if self.actorsCount() > 1:
            return len(self.actors[actor])
        else:
            return len(next(iter(self.actors.values())))

    def name(self):
        return self._name or (next(iter(self.actors.values())))[0].name()

    def actor(self):
        return iter(self.actors.keys())

    def stage(self, actor, index):
        if self.actorsCount() > 1:
            return self.actors[actor][index]
        else:
            return next(iter(self.actors.values()))[index]
