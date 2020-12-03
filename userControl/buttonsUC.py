import maya.cmds as cmds

import log
from .UC import *


class switchBtn(UserControl):
    def __init__(self, parent, imageOn, imageOff, label, labelOn=None):
        UserControl.__init__(self, parent)
        self.switch = False
        self.imageOn = imageOn
        self.imageOff = imageOff
        self.label = label
        self.height = 22
        self.width = 22
        if labelOn is None:
            self.labelOn = label
        else:
            self.labelOn = labelOn

    def switch(self):
        self.switch = not self.switch
        self.runEvent("switch", self.switch)
        self.refresh()

    def switchTo(self, val):
        self.switch = val
        self.runEvent("switch", self.switch)
        self.refresh()

    def switchOn(self):
        self.switch = True
        self.runEvent("switch", self.switch)
        self.refresh()

    def switchOff(self):
        self.switch = False
        self.runEvent("switch", self.switch)
        self.refresh()

    def load(self):
        self.btnOn = cmds.iconTextButton(parent=self.layout, style='iconOnly', image1=getIcon(self.imageOff), label=self.labelOn, w=22, h=22, sic=True, bgc=hexToRGB(self.color.button),  c=Callback(self.switchTo, False))
        self.btnOff = cmds.iconTextButton(parent=self.layout, style='iconOnly', image1=getIcon(self.imageOn), label=self.label, w=22, h=22, sic=True, bgc=hexToRGB(self.color.button),  c=Callback(self.switchTo, True))
        
        cmds.formLayout( self.layout, edit=True,
                        attachForm=[(self.btnOn, 'top', 0), (self.btnOn, 'bottom', 0), (self.btnOn, 'left', 0), (self.btnOn, 'right', 0),
                                    (self.btnOff, 'top', 0), (self.btnOff, 'bottom', 0), (self.btnOff, 'left', 0), (self.btnOff, 'right', 0)])

    def refresh(self):
        cmds.iconTextButton(self.btnOn, e=True, vis=self.switch)
        cmds.iconTextButton(self.btnOff, e=True, vis=not self.switch)




class IconButtonUC(UserControl):
    def __init__(self):
        UserControl.__init__(self, parent)

    def load(self):
        self.button = cmds.iconTextButton('btnSetServerPath', parent=self.layout, style='iconOnly', image1=getIcon("folder"), label='Switch view', w=22, h=22, sic=True, bgc=[0.45,0.45,0.45])

class TextButtonUC(UserControl):
    def __init__(self, parent, text="OK"):
        UserControl.__init__(self, parent)
        self.text = text
        self.warning = False
        self.greyOut = False
    
    def load(self):
        if self.warning:
            self.button = cmds.button(label=self.text, parent=self.layout, bgc=hexToRGB(self.color.warning), c=Callback(self.runEvent, "click"))
        else:
            self.button = cmds.button(label=self.text, parent=self.layout, bgc=hexToRGB(self.color.button), c=Callback(self.runEvent, "click"))
        cmds.formLayout(self.layout, edit=True,
                        attachForm=[(self.button, 'top', 0), (self.button, 'bottom', 0), (self.button, 'left', 0), (self.button, 'right', 0)])

    def refresh(self):
        cmds.button(self.button, e=True, label=self.text)

class TextFieldUC(UserControl):
    def __init__(self, parent, text=""):
        UserControl.__init__(self, parent)
        self.text = text
        

    def load(self):
        self._textLabel = cmds.textField(parent=self.layout, text=object.__getattribute__(self, "text"))
        cmds.formLayout(self.layout, edit=True,
                        attachForm=[(self._textLabel, 'top', 0), (self._textLabel, 'bottom', 0), (self._textLabel, 'left', 0), (self._textLabel, 'right', 0)])
    
    def refresh(self):
        cmds.textField(self._textLabel, e=True, text=self.text)
        
    def __getattribute__(self,name):
        if name == 'text':
            if self.loaded:
                return cmds.textField(self._textLabel, q=True, text=True)
            else:
                return ""
        else:
            return UserControl.__getattribute__(self, name)

class TextLabelUC(UserControl):
    def __init__(self, parent, text="..."):
        UserControl.__init__(self, parent)
        self.text = text

    def load(self):
        self._textLabel = cmds.text(parent=self.layout, label=self.text)
        cmds.formLayout(self.layout, edit=True,
                        attachForm=[(self._textLabel, 'top', 0), (self._textLabel, 'bottom', 0), (self._textLabel, 'left', 0), (self._textLabel, 'right', 0)])
    
    def refresh(self):
        cmds.text(self._textLabel, e=True, label=self.text)

class ImageUC(UserControl):
    pass