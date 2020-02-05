"""
File: ui.py

Contributor(s):
    Cabana,  Gabriel  | cabg2101
    Lalonde, Philippe | lalp2803

Date(s):
    2020-01-29 (Creation)

Description:
    User interface designed for intuitive control and monitoring of the
    HexaphobUS robot.

S4-H20 | GRO400
"""

# --------------------------------------------

import math
import os
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QIcon, QPainter, QPalette
from PyQt5.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QWidget)

# --------------------------------------------

ARROW_W = 60
ARROW_H = 30
BUTTON_W = 120
BUTTON_H = 60
INFO_W = 190
INFO_H = 30
SV_NBR = 12
SV_W = 100
SV_H = 30
TRACK_W = 250
TRACK_H = 50
UI_X = 80
UI_Y = 80
UI_W = 800
UI_H = 600
UI_MIN_W = 480
UI_MIN_H = 360

WINDOW_NAME = "HexaphobUS UI"
BUTTON_STOP = "STOP"
BUTTON_INIT = "POS INIT"
BUTTON_PRG1 = "PRG1"
SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SEP = os.path.sep
LOGO = 'img' + SEP + 'hexaphobus_logo.png'

# --------------------------------------------


class RobotTracking(QWidget):
    """
    The 'RobotTracking' class is a QWidget subclass that allows the user
    to follow the robot position from an initialized origin point.
    """

    def __init__(self):
        super().__init__()

        self._distance_origin = 0
        self._robot_x_pos = 200
        self._robot_y_pos = 200
        self._target_x_pos = 250
        self._target_y_pos = 250
        self._vel = 60  # pixels per second

        #self.setMouseTracking(True)
        self.timer = QTimer(self)
        #self.timer.timeout.connect(self.changePosition)
        self.timer.start(round(1000 / self._vel))
        self.initTracking()

    def initTracking(self):
        # Initialize the Qt robot tracking widget.

        self.setMinimumSize(UI_MIN_W, UI_MIN_H)
        self.label = QLabel(self)
        self.label.resize(TRACK_W, TRACK_H)
        self.show()

    def changePosition(self,direction):
        # Update the target positions.
        if direction == "UP":
            self._robot_y_pos -= 10
        elif direction == "DOWN":
            self._robot_y_pos += 10
        elif direction == "RIGHT":
            self._robot_x_pos += 10
        elif direction == "LEFT":
            self._robot_x_pos -= 10
        self.moveRobot(self._robot_x_pos, self._robot_y_pos)
        self.update()       


    def moveRobot(self, robotX, robotY):
        # Event that updates the mouse position relative to the origin
        # according to mouse motion.

        _distance_origin = round(
            ((robotY - self._target_y_pos)**2
             + (robotX - self._target_x_pos)**2)**0.5
        )

        self.label.setText("Coordinates (x; y): ({}; {})\
                           \nDistance from origin: {}"
                           .format(robotX, robotY, _distance_origin))

        self.update()

    def initPosition(self):
        # Event that updates the origin point according to mouse press.

        self._target_x_pos = self._robot_x_pos
        self._target_y_pos = self._robot_y_pos
        self.update()

    def paintEvent(self, event):
        # Event that draws a line between the object position and its
        # origin.

        q = QPainter()
        q.begin(self)
        q.drawLine(self._robot_x_pos, self._robot_y_pos,
                   self._target_x_pos, self._target_y_pos)


class MainWindow(QWidget):
    """
    The 'MainWindow' class is a QWidget subclass that allows the user
    to monitor various robot items, control the robot and track its
    position with another QWidget subclass ('RobotTracking' class).
    """

    def __init__(self):
        super().__init__()

        # Servos
        self._servo_edits = list()
        self._servo_labels = list()

        # Layouts
        self.global_layout = QVBoxLayout()

        self.top_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()

        self.servo_layout_1 = QVBoxLayout()
        self.servo_layout_2 = QVBoxLayout()
        self.servo_layout_3 = QVBoxLayout()
        self.servo_layout_4 = QVBoxLayout()
        self.tracking_layout = QVBoxLayout()
        

        self.info_layout = QVBoxLayout()
        self.prog_layout = QVBoxLayout()
        self.move_layout = QGridLayout()

        # Buttons
        self.button_up = QPushButton("\u2191")
        self.button_down = QPushButton("\u2193")
        self.button_left = QPushButton("\u2190")
        self.button_right = QPushButton("\u2192")

        self.button_stop = QPushButton(BUTTON_STOP)
        self.button_init = QPushButton(BUTTON_INIT)
        self.button_prog = QPushButton(BUTTON_PRG1)

        # Edits and labels
        self.speed_edit = QLineEdit()
        self.energy_edit = QLineEdit()
        self.speed_label = QLabel()
        self.energy_label = QLabel()

        self.initUI()

    def initUI(self):
        # Initialize the Qt user interface.

        self.setGeometry(UI_X, UI_Y, UI_W, UI_H)
        self.setWindowTitle(WINDOW_NAME)

        self.tracking = RobotTracking()

        self.addServos()
        self.setSizeButtons()
        self.setConnexions()
        self.setInfo()
        self.setLayoutDependencies()
        self.addWidgets()
        self.setLayout(self.global_layout)
        self.show()

    def addServos(self):
        # Add servomotor edits and labels used to monitor their state.

        for index in range(SV_NBR):
            self._servo_edits.append(QLineEdit())
            self._servo_edits[index].setFixedSize(SV_W, SV_H)

            self._servo_labels.append(QLabel())
            self._servo_labels[index].setAlignment(Qt.AlignCenter)
            self._servo_labels[index].setText("Servo{:02d}".format(index + 1))

    def setSizeButtons(self):
        # Fix button size according to type.

        self.button_up.setFixedSize(ARROW_W, ARROW_H)
        self.button_down.setFixedSize(ARROW_W, ARROW_H)
        self.button_left.setFixedSize(ARROW_W, ARROW_H)
        self.button_right.setFixedSize(ARROW_W, ARROW_H)

        self.button_stop.setFixedSize(BUTTON_W, BUTTON_H)
        self.button_init.setFixedSize(BUTTON_W, BUTTON_H)
        self.button_prog.setFixedSize(BUTTON_W, BUTTON_H)

    def setConnexions(self):
        self.button_init.clicked.connect(self.tracking.initPosition)
        self.button_up.clicked.connect(lambda:self.tracking.changePosition("UP"))
        self.button_down.clicked.connect(lambda:self.tracking.changePosition("DOWN"))
        self.button_right.clicked.connect(lambda:self.tracking.changePosition("RIGHT"))
        self.button_left.clicked.connect(lambda:self.tracking.changePosition("LEFT"))

    def setInfo(self):
        #Set information size and text display.

        self.speed_edit.setFixedSize(INFO_W, INFO_H)
        self.energy_edit.setFixedSize(INFO_W, INFO_H)
        self.speed_label.setText("Vitesse :")
        self.energy_label.setText("Énergie :")

    def setLayoutDependencies(self):
        # Add inner layouts to outer layouts (creates a parent-child
        # structure).

        self.global_layout.addLayout(self.top_layout)
        self.global_layout.addLayout(self.bottom_layout)

        self.top_layout.addLayout(self.servo_layout_1)
        self.top_layout.addLayout(self.servo_layout_2)
        self.top_layout.addLayout(self.tracking_layout)
        self.top_layout.addLayout(self.servo_layout_3)
        self.top_layout.addLayout(self.servo_layout_4)

        self.bottom_layout.addLayout(self.info_layout)
        self.bottom_layout.addLayout(self.prog_layout)
        self.bottom_layout.addLayout(self.move_layout)
        self.bottom_layout.addWidget(self.button_stop)

    def strechServoLayouts(self):
        # Add padding between widgets and/or layout walls in the
        # servomotor layouts.

        self.servo_layout_1.addStretch(1)
        self.servo_layout_2.addStretch(1)
        self.servo_layout_3.addStretch(1)
        self.servo_layout_4.addStretch(1)

    def addWidgets(self):
        # Add widgets to various layouts.

        self.strechServoLayouts()

        for counter, (edit, label) in \
            enumerate(zip(self._servo_edits, self._servo_labels)):

            if counter < math.ceil(SV_NBR/4):
                self.servo_layout_1.addWidget(label)
                self.servo_layout_1.addWidget(edit)
                self.servo_layout_1.addStretch(1)
            elif counter < math.ceil(SV_NBR/2):
                self.servo_layout_2.addWidget(label)
                self.servo_layout_2.addWidget(edit)
                self.servo_layout_2.addStretch(1)
            elif counter < math.ceil(SV_NBR*3/4):
                self.servo_layout_3.addWidget(label)
                self.servo_layout_3.addWidget(edit)
                self.servo_layout_3.addStretch(1)
            elif counter < SV_NBR:
                self.servo_layout_4.addWidget(label)
                self.servo_layout_4.addWidget(edit)
                self.servo_layout_4.addStretch(1)

        self.tracking_layout.addWidget(self.tracking)

        self.info_layout.addWidget(self.speed_label)
        self.info_layout.addWidget(self.speed_edit)
        self.info_layout.addWidget(self.energy_label)
        self.info_layout.addWidget(self.energy_edit)

        self.prog_layout.addWidget(self.button_init)
        self.prog_layout.addWidget(self.button_prog)

        self.move_layout.addWidget(self.button_up, 0, 1, 1, 1)
        self.move_layout.addWidget(self.button_down, 1, 1)
        self.move_layout.addWidget(self.button_left, 1, 0)
        self.move_layout.addWidget(self.button_right, 1, 2)

# --------------------------------------------


if __name__ == '__main__':
    # Create a Qt application and window to display.

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(SCRIPT_DIR + SEP + LOGO))
    window = MainWindow()

    # Set style
    palette = window.palette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    window.setPalette(palette)

    # Display
    sys.exit(app.exec_())
