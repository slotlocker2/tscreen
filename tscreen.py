#!/usr/bin/env python

from PyQt4 import QtGui, QtCore
import time, sys


class OverlayWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        # CONSTANTS
        self.FONT_SIZE = 25 # The font size of the time displayed

        # Timer which fires a signal every 1 second. Used to update the label.
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # Qt Label which displays the time and the current color being painted.
        self.timeLabel = QtGui.QLabel(self)
        self.timeLabel.setTextFormat(QtCore.Qt.RichText)
        self.timeLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.timeLabel.setAutoFillBackground(True)

        # Layout to make sure the Label stays at the center of the screen in case of resize events.    
        self.hLayout = QtGui.QGridLayout(self)
        self.hLayout.setContentsMargins(0,0,0,0) # Make sure the Label extends all the way upto the broders of the widget.
        self.setLayout(self.hLayout)
        self.hLayout.addWidget(self.timeLabel,0,0)
        
        # Palette to paint the background of the label
        self.palette = QtGui.QPalette()

  
        # Passing a hint to the window manager to keep the window above other windows. It is just a hint and does not ensure the window stays on top of other windows.
        self.setWindowFlags( self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint )
        
        # Setting the curor to blank before going full screen.    
        self.setCursor(QtCore.Qt.BlankCursor)

        # showFullSceen used instead of show() to start the app in full screen mode.
        self.showFullScreen()

    def determine_time_color(self):
        ''' Returns a list containing the time and the color as strings'''
        return [time.strftime("%H:%M:%S") ,time.strftime("%H%M%S")] 


    def update_time(self):
        ''' Updates the label with the current time and the color'''
        timecolorArray = self.determine_time_color()
        
        # <font> </font> does not work since it goes all the way up to only 7. Using CSS inside span to get the required size.
        self.labelText = "<b><span style='font-size:%dpt'>" % self.FONT_SIZE+ timecolorArray[0] + "</span></b>" + "<br>" + "#" + "<i>" + timecolorArray[1] + "</i>"
        self.timeLabel.setText(self.labelText)
        self.update_color(timecolorArray[1])

    def update_color(self,colorstring):
        # Converting hex to decimal
        Re = int(colorstring[0:2],16) 
        Gr = int(colorstring[2:4],16)
        Bl = int(colorstring[4:6],16)
        
        role = QtGui.QPalette.Background
        self.palette.setColor(role, QtGui.QColor(Re, Gr, Bl)) 
        role = QtGui.QPalette.WindowText
        self.palette.setColor(role, QtGui.QColor(143, 143, 143)) # Gray goes with most of the colors and is not as much of an eyesore as white is.

        self.timeLabel.setPalette(self.palette)

    #Subclassing the keyPressEvent to close the widget once the Escape Key is pressed.
    def keyPressEvent(self,qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            return QtGui.QWidget.keyPressEvent(self,qKeyEvent)
    


def main():
    app = QtGui.QApplication(sys.argv)
    appins = OverlayWidget()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
