from Core.Utils import create_item
from Core.Config import get_config
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

class Animation:

    def __init__(self):
        self.actors = dict()

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
        return (next(iter(self.actors.values())))[0].name()

    def actor(self):
        return iter(self.actors.keys())

    def stage(self, actor, index):
        if self.actorsCount() > 1:
            return self.actors[actor][index]
        else:
            return next(iter(self.actors.values()))[index]

    def toItem(self):

        animIcon = get_config().get("PLUGIN", "defaultAnimationIcon")
        actorIcon = get_config().get("PLUGIN", "defaultActorIcon")

        item = None

        if self.actorsCount() > 1:
            animItem = create_item(self.name(), animIcon)
            item = animItem

            i = 1
            for actor, stages in self.actors.items():
                actorItem = create_item("Actor " + str(i), actorIcon)
                animItem.addChild(actorItem)
                i += 1

                j = 1
                for stage in stages:
                    actorItem.addChild(stage.toItem("Stage " + str(j)))
                    j += 1
        else:
            for actor, stages in self.actors.items():

                if len(stages) > 1:
                    animItem = create_item(self.name(), animIcon)
                    item = animItem

                    for j, stage in enumerate(stages):
                        animItem.addChild(stage.toItem("Stage " + str(j+1)))
                else:
                    for stage in stages:
                        item = stage.toItem()
        return item
