#!/usr/bin/env python3

import logging
import sys

from PySide6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class AdWindow(QDialog):
    """ This class represents a window that locks into full screen mode and blocks minimization on Windows. """

    def __init__(self, ad_slogan, parent=None):
        super(AdWindow, self).__init__(parent)
        self.setWindowTitle("Full Screen Notification")

        # 1. REMOVE BORDERS AND FORCE IT TO STAY ON TOP
        # FramelessWindowHint strips the title bar. WindowStaysOnTopHint keeps it above other apps.
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # 2. MATCH MONITOR RESOLUTION EXACTLY
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        
        # Set layout geometry and lock the size so it cannot be resized
        self.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())
        self.setFixedSize(screen_geometry.width(), screen_geometry.height())

        # Create a layout to center the text
        layout = QVBoxLayout()
        
        self.label = QLabel(ad_slogan)
        
        # Style the text so it stands out in the center
        font = self.label.font()
        font.setPointSize(36)  
        self.label.setFont(font)
        self.label.setStyleSheet("color: white; font-weight: bold;")
        self.label.setAlignment(Qt.AlignCenter) 

        # Set a dark background covering the whole monitor
        self.setStyleSheet("background-color: #1e1e1e;")

        layout.addWidget(self.label)
        self.setLayout(layout)

    def closeEvent(self, event):
        # Ignore standard close events (like Alt + F4)
        event.ignore()

    def changeEvent(self, event):
        # 3. BLOCKS MINIMIZATION AND "HIDE" TRICKS
        # If the window state changes (user minimizes or switches desktops), force it back open.
        if event.type() == event.WindowStateChange:
            if self.isMinimized() or not self.isVisible():
                self.setWindowState(Qt.WindowNoState)  # Reset state to normal window
                self.show()                           # Force visibility
                self.raise_()                         # Snap to the very front
        super(AdWindow, self).changeEvent(event)


class Adware(QApplication):
    """ This class manages the launch of the application window. """

    def __init__(self, args):
        super(Adware, self).__init__(args)

    @property
    def advert_slogans(self):
        return (
            'Windows 11 Full Screen Lab Simulation.',
        )

    def create_ad_window(self, ad_slogan):
        window = AdWindow(ad_slogan=ad_slogan)
        window.show()
        return window

    def show_ads(self):
        ad_windows = []
        for advert in self.advert_slogans:
            ad_window = self.create_ad_window(advert)
            ad_windows.append(ad_window)

        return ad_windows


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    adware = Adware(sys.argv)
    windows = adware.show_ads()

    # Note: exec() is used in PySide6 instead of the older exec_() from PySide2
    sys.exit(adware.exec())
