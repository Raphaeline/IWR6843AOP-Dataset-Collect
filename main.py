import os
import sys
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))
common_path = os.path.join(current_dir, 'common')
if common_path not in sys.path:
    sys.path.insert(0, common_path)


# PySide2 Imports
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt

# Window Class
from gui_core import Window

# Demo List
from common.demo_defines import *

# Logging (possible levels: DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Uncomment this line for logging with timestamps
logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S', level=logging.INFO)

# logging.basicConfig(format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

if __name__ == '__main__':
    for key in DEVICE_DEMO_DICT.keys():
        DEVICE_DEMO_DICT[key]["demos"] = [
            x for x in DEVICE_DEMO_DICT[key]["demos"] if x in BUSINESS_DEMOS["Industrial"]]

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    main = Window(size=size, title="Industrial Visualizer")
    main.show()
    sys.exit(app.exec_())
