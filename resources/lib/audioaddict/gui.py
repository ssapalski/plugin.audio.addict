"""
    audioaddict.gui
    Classes to provide GUI elements not available in all versions of the Kodi
    Python API.
"""

import xbmcgui


class TextViewer(xbmcgui.WindowXMLDialog):
    def __new__(cls, *args, **kwargs):
        return super(TextViewer, cls).__new__(cls,
                                              "DialogTextViewer.xml",
                                              None)

    def __init__(self, header, text):
        self.header = header
        self.text = text

    def onInit(self):
        self.getControl(1).setLabel(self.header)
        self.getControl(5).setText(self.text)
