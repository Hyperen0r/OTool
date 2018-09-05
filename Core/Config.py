import configparser
import os

DEFAULT_CONFIG_FILE = "conf.ini"


def create_config():
    """
    Create default config file
    :return: default config object
    """
    config = configparser.ConfigParser()

    config.add_section("CONFIG")
    config.set("CONFIG", "bFirstTime", "True")
    config.set("CONFIG", "bUseModOrganizer", "True")
    config.set("CONFIG", "lastName", "")
    config.set("CONFIG", "lastIcon", "")

    config.add_section("PLUGIN")
    config.set("PLUGIN", "name", "OSelector")
    config.set("PLUGIN", "defaultPluginIcon", "omu_suneclipse")
    config.set("PLUGIN", "defaultPackageIcon", "omu_skyrim")
    config.set("PLUGIN", "defaultFolderIcon", "omu_lib")
    config.set("PLUGIN", "defaultSetIcon", "omu_plus")
    config.set("PLUGIN", "defaultAnimationIcon", "omu_sticktpose")
    config.set("PLUGIN", "defaultActorIcon", "omu_genders")
    config.set("PLUGIN", "defaultStageIcon", "omu_stickdance00")
    config.set("PLUGIN", "defaultMaleIcon", "omu_male")
    config.set("PLUGIN", "defaultFemaleIcon", "omu_female")
    config.set("PLUGIN", "maxItemPerPage", "25")
    config.set("PLUGIN", "maxItemStringLength", "25")

    config.add_section("PATHS")
    config.set("PATHS", "installFolder", "")
    config.set("PATHS", "pluginFolder", "meshes/0SA/_MyOSA/anim_1/")
    config.set("PATHS", "pluginInstall", "meshes/0SA/mod/__install/plugin/")

    config.add_section("LOG")
    config.set("LOG", "enabled", "True")
    config.set("LOG", "level", "INFO")

    with open(DEFAULT_CONFIG_FILE, 'w') as config_file:
        config.write(config_file)

    return config


def load_config():
    """
    Load config from file. If it does not exist, it creates it.
    :return: config object
    """
    if not os.path.exists(DEFAULT_CONFIG_FILE):
        config = create_config()
    else:
        config = configparser.ConfigParser()
        config.read(DEFAULT_CONFIG_FILE)
    return config


CONFIG = load_config()


def get_config():
    """
    :return: config object
    """
    return CONFIG


def save_config():
    """ Save configuration in a file """
    with open(DEFAULT_CONFIG_FILE, 'w') as config_file:
        get_config().write(config_file)
