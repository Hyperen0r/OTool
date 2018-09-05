import sys
import logging

from Core.Config import get_config
from Windows.AppSelector import AppSelector
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    logging.basicConfig(filemode="w",
                        filename="logs.log",
                        level=logging.getLevelName(get_config().get("LOG", "level")),
                        format='%(asctime)s - [%(levelname)s] - %(name)s : %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    if not get_config().get("LOG", "enabled"):
        logger = logging.getLogger()
        logger.disabled = True

    logging.info(" =============== STARTING LOGGING ===============")

    app = QApplication(sys.argv)
    window = AppSelector()
    window.setAppStyle(app)
    window.show()
    sys.exit(app.exec_())