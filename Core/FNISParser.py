import re

from enum import Enum

SYMBOL_FNIS_COMMENT = "'"


class FNISParser:
    class TYPE(Enum):
        BASIC = "^(b)"
        ANIM_OBJ = "^(fu|fuo|o)"
        SEQUENCE = "^(s|so)"
        ADDITIVE = "^(\+)"
        OFFSET = "^(ofa)"
        PAIRED = "^(pa)"
        KILLMOVE = "^(km)"
        UNKNOWN = ""

    class OPTION(Enum):
        ACYCLIC = "(?:,|-)a"
        ANIM_OBJ = "(?:,|-)o"
        TRANSITION = "(?:,|-)Tn"
        HEAD_TRACKING = "(?:,|-)h"
        BLEND_TIME = "(?:,|-)(B\d*\.\d*)"
        KNOWN = "(?:,|-)k"
        BSA = "(?:,|-)bsa"
        STICKY_AO = "(?:,|-)st"
        DURATION = '(?:,|-)(D\d*\.\d*)'
        TRIGGER = "(?:,|-)(T[^\/]*\/\d*\.\d*)"
        NONE = ""

    def __init__(self):
        return

    @staticmethod
    def parseLine(line):
        # See FNIS_FNISBase_List.txt for more information (in FNIS Behavior folder)
        line = line.split(SYMBOL_FNIS_COMMENT)[0].strip()
        regexp = re.compile(r"^(\S*)(?: -(\S*))? (\S*) (\S*)((?:\s(?:\S*))*)")
        found = regexp.search(line)
        if found:
            anim_type = found.group(1)  # Single word (s + b ...)
            anim_options = found.group(2)  # o,a,Tn,B.2, ...
            anim_id = found.group(3)  # ANIM_ID_ ...
            anim_file = found.group(4)  # <path/to/file>.hkx
            anim_obj = found.group(5)  # Chair Ball ...
            return FNISParser.typeFromString(anim_type), \
                   FNISParser.optionsFromString(anim_options), \
                   anim_id, \
                   anim_file, \
                   anim_obj

        return FNISParser.TYPE.UNKNOWN, [], "", "", ""

    @staticmethod
    def typeFromString(string):
        for _type in FNISParser.TYPE:
            regexp = re.compile(_type.value)
            found = regexp.search(string)
            if found:
                return _type
        return FNISParser.TYPE.UNKNOWN

    @staticmethod
    def optionsFromString(string):
        if string:
            options = []
            for option in FNISParser.OPTION:
                regexp = re.compile(option.value)
                found = regexp.search(string)
                if found:
                    options.append(option)
        return [FNISParser.OPTION.NONE]

    @staticmethod
    def getActorNumberFrom(_id):

        # Typical name_Ax_Sy
        regexp = re.compile(r"^(.*)_[aA](\d+)_[sS](\d+)$")
        found = regexp.search(_id)

        if found:
            return int(found.group(2))

        # OSA / OSEX convention
        regexp = re.compile(r"^(.*?)(?:_[Ss](\d+))?_(\d+)$")
        found = regexp.search(_id)
        if found:
            return int(found.group(3))

        # name_[actor][stage] like a11 for actor 1 stage 11
        regexp = re.compile(r"^(.*?)_([a-z])(\d+)$")
        found = regexp.search(_id)
        if found:
            return ord(found.group(2)) - 96

        regexp = re.compile(r"^(.*?)(\d+)([a-zA-Z])$")
        found = regexp.search(_id)
        if found:
            return ord(found.group(3).lower()) - 96

        return -1

    @staticmethod
    def getStageNumberFrom(_id):

        # Typical name_Ax_Sy
        regexp = re.compile(r"^(.*)_[aA](\d+)_[sS](\d+)$")
        found = regexp.search(_id)

        if found:
            return int(found.group(3))

        # OSA / OSEX convention
        regexp = re.compile(r"^(.*?)(?:_[Ss](\d+))?_(\d+)$")
        found = regexp.search(_id)
        if found and found.group(2):
            return int(found.group(2))

        # name_[actor][stage] like a11 for actor 1 stage 11
        regexp = re.compile(r"^(.*?)_([a-z])(\d+)$")
        found = regexp.search(_id)
        if found:
            return int(found.group(3))

        regexp = re.compile(r"^(.*?)(\d+)([a-zA-Z])$")
        found = regexp.search(_id)
        if found:
            return int(found.group(2))

        regexp = re.compile(r"^(.*?)(\d+)$")
        found = regexp.search(_id)
        if found:
            return int(found.group(2))

        return -1

    @staticmethod
    def getAnimationNameFrom(_id):

        # Typical name_Ax_Sy
        regexp = re.compile(r"^(.*)_[aA](\d+)_[sS](\d+)$")
        found = regexp.search(_id)

        if found:
            return found.group(1)

        # OSA / OSEX convention
        regexp = re.compile(r"^(.*?)(?:_[Ss](\d+))?_(\d+)$")
        found = regexp.search(_id)
        if found:
            return found.group(1)

        # name_[actor][stage] like a11 for actor 1 stage 11
        regexp = re.compile(r"^(.*?)_([a-z])(\d+)$")
        found = regexp.search(_id)
        if found:
            return found.group(1)

        regexp = re.compile(r"^(.*?)(\d+)([a-zA-Z])$")
        found = regexp.search(_id)
        if found:
            return found.group(1)

        regexp = re.compile(r"^(.*?)(\d+)$")
        found = regexp.search(_id)
        if found:
            return found.group(1)

        return _id
