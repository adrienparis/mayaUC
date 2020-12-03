import maya.cmds as cmds
from pymel.all import *

import log

from .UC import *

class TileUC(UserControl):
    increment = 0
    sizeImage = 100
    style = 'iconAndTextVertical'

    def __init__(self, parent, image, text, icon=None):
        UserControl.__init__(self, parent)
        self.image = image
        self.icon = icon
        self.text = text
        self.name = text + "Tile" + self.name + str(TileUC.increment)
        self.selected = False
        TileUC.increment += 1
        self.iconLay = None

    def load(self):
        cmds.formLayout(self.layout, e=True, bgc=hexToRGB(self.color.highlight), ebg=self.selected)
        self.btnLay = cmds.iconTextButton(self.name, parent=self.layout, style=self.style, image1=self.image,
                            label=self.text, w=self.sizeImage, h=self.sizeImage, sic=True, c=Callback(self.clickCommand))

        if self.icon is not None:
            self.iconLay = cmds.image(parent=self.layout, image=getIcon(self.icon), bgc=hexToRGB(0x1d1d1d))
            cmds.formLayout(self.layout, edit=True,
                            attachForm=[(self.btnLay, "top", 0), (self.btnLay, "bottom", 0), 
                                        (self.btnLay, "left", 0), (self.btnLay, "right", 0), 
                                        (self.iconLay, "top", 5), (self.iconLay, "right", 5)],
                            attachNone=[(self.iconLay, "left"), (self.iconLay, "bottom")])
        else:
            cmds.formLayout(self.layout, edit=True,
                            attachForm=[(self.btnLay, "top", 2), (self.btnLay, "bottom", 2), 
                                        (self.btnLay, "left", 2), (self.btnLay, "right", 2)])
    def refresh(self):
        if self.icon is not None and self.iconLay is not None:
            cmds.image(self.iconLay, e=True, image=getIcon(self.icon))

    def setIcon(self, icon):
        self.icon = icon
        if self.iconLay is None:
            self.iconLay = cmds.image(parent=self.layout, image=getIcon(self.icon), bgc=hexToRGB(0x1d1d1d))
            cmds.formLayout(self.layout, edit=True,
                            attachForm=[(self.iconLay, "top", 5), (self.iconLay, "right", 5)],
                            attachNone=[(self.iconLay, "left"), (self.iconLay, "bottom")])


    def selection(self, b):
        self.selected = b
        if cmds.formLayout(self.layout, q=True, exists=True):
            cmds.formLayout(self.layout, e=True, ebg=self.selected)

    def clickCommand(self):
        self.mods = cmds.getModifiers()
        self.runEvent("click", self, self.mods)
