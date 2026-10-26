#!/usr/bin/env python3

import logging
import sys

# Note: Using PySide6 to match your Mac virtual environment
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class AdWindow(QDialog):
    """ This class represents a window that matches screen dimensions perfectly without using OS fullscreen. """

    def __init__(self, ad_slogan, parent=None):
        super(AdWindow, self).__init__(parent)
        self.setWindowTitle("Full Screen Notification")

        # 1. REMOVE ALL BORDERS AND FORCE IT TO STAY ON TOP
        # This removes the Mac title bar entirely so there is no green/yellow/red buttons at all.
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # 2. MATCH SCREEN DIMENSIONS MANUALY TO PREVENT MAC FULLSCREEN OVERRIDE
        # This gets your Mac screen geometry and stretches the window to match it exactly.
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        
        # Set the exact geometry (X=0, Y=0, Width, Height)
        self.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())
        
        # Lock the size completely so it cannot be shrunk or resized by dragging
        self.setFixedSize(screen_geometry.width(), screen_geometry.height())

        # Create a layout to center the text on the black screen
        layout = QVBoxLayout()
        
        self.label = QLabel(ad_slogan)
        
        # Style the text so it stands out clearly in the center
        font = self.label.font()
        font.setPointSize(36)  # Large text for visibility
        self.label.setFont(font)
        self.label.setStyleSheet("color: white; font-weight: bold;")
        self.label.setAlignment(Qt.AlignCenter) # Center horizontally and vertically

        # Set a dark background so the text is easily readable
        self.setStyleSheet("background-color: #1e1e1e;")

        layout.addWidget(self.label)
        self.setLayout(layout)

    def closeEvent(self, event):
        # Ignore the close event so that the window can't be closed normally
        event.ignore()


class Adware(QApplication):
    """ This class manages the launch of the application window. """

    def __init__(self, args):
        super(Adware, self).__init__(args)

    @property
    def advert_slogans(self):
        """ Slogans of the promoted adds. Only 1 item needed. """
        return (
            'This is a Full Screen Simulation Experiment.',
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

    # Create our application and display the window
    adware = Adware(sys.argv)
    windows = adware.show_ads()

    sys.exit(adware.exec())
