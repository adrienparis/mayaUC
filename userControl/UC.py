import os
from copy import copy
import maya.cmds as cmds
from pymel.all import *
import log

class Color():
    def __init__(self):
        self.highlight = 0x5285a6
        # self.main = 0x99e1d9
        # self.button = 0x99e1d9
        # self.background = 0x5d576b
        # self.text = 0xfffaf3
        # self.highlight = 0xe7466c
        self.main = 0x404040
        self.button = 0x606060
        self.background = 0x303030
        self.text = 0x5285a6
        self.warning = 0xec281a

def getIcon(icon):
    if icon is not None:
        img = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, "icon", icon + ".png")
        if os.path.isfile(img):
            return img
    img = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, "icon",  "missingIcon.png")
    if os.path.isfile(img):
        return img

def hexToRGB(hexa):
    """
    :hexa:
    """
    rgb = []
    rgb.append((round(hexa / 0x10000) % 0x100) / 0x100)
    rgb.append((round(hexa / 0x100) % 0x100) / 0x100)
    rgb.append(float(hexa % 0x100) / 0x100)
    return rgb

class Attach(object):
    NONE = 0
    FORM = 1
    POS = 2
    CTRL = 3

    def __init__(self, parent):
        self.parent = parent
        self.margin = [0,0,0,0]
        self.none = 0
        self.form = 0
        self.position = 0
        self.controller = 0
        self._attachs = {}
        self._an = []
        self._af = []
        self._ap = []
        self._ac = []

    def __getattribute__(self,name):
        if name == 'none' or name == 'form' or name == 'position' or name == 'controller':
            self._createAttach()
            if name == 'none':
                return object.__getattribute__(self, "_an")
            elif name == 'form':
                return object.__getattribute__(self, "_af")
            elif name == 'position':
                return object.__getattribute__(self, "_ap")
            elif name == 'controller':
                return object.__getattribute__(self, "_ac")
        else:
            return object.__getattribute__(self, name)

    @staticmethod
    def __sideToValue(side):
        if side == "top" : return 0
        if side == "bottom" : return 1
        if side == "left" : return 2
        if side == "right" : return 3

    def _createAttach(self):
        self._an = []
        self._af = []
        self._ap = []
        self._ac = []
        for key, value in self._attachs.items():
            if type(value) is int:
                if value == Attach.NONE:
                    self._an.append((self.parent.layout, key))
                if value == Attach.FORM:
                    self._af.append((self.parent.layout, key, self.margin[Attach.__sideToValue(str(key))]))
            elif type(value) is tuple and len(value) == 2:
                if value[0] == Attach.POS:
                    self._ap.append((self.parent.layout, key, self.margin[Attach.__sideToValue(str(key))], value[1]))
                if value[0] == Attach.CTRL:
                    if type(value[1]) is str or type(value[1]) is unicode:
                        self._ac.append((self.parent.layout, key, self.margin[Attach.__sideToValue(str(key))], value[1]))
                    else:
                        try:
                            self._ac.append((self.parent.layout, key, self.margin[Attach.__sideToValue(str(key))], value[1].layout))
                        except AttributeError:
                            log.debug.warning(value[1] + "is not supported")

    def attach(self, margin, attachs):
        #check if margin is (0), (0,0) or (0,0,0,0)

        # self.margin = [0,0,0,0]
        if margin != -1:
            if type(margin) is int:
                self.margin = [margin, margin, margin, margin]
            if type(margin) is tuple and len(margin) == 2:
                self.margin = [margin[0], margin[0], margin[1], margin[1]]
            if type(margin) is tuple and len(margin) == 4:
                self.margin = [margin[0], margin[1], margin[2], margin[3]]
        self._attachs.update(attachs)

class UserControl(object):
    """ 
    Creating a userControl
    """

    class Event():
        LOAD = 1
        UNLOAD = 2
        REFRESH = 3
        RELOAD = 4
        SELFKILL = 5
        APPLYATTACH = 6


    increment = 0

    def __init__(self, parent):
        """Initialize
        
        :parent: str formlayout
        """
        # super(UserControl, self).__init__()
        self.parentUC = None
        self.parentLay = None
        self.layout = None
        self.setParent(parent)
        self._childrens = []
        self._commands = {}
        self.name = "UC"
        self.color = Color()
        self.bgc = 0xa00000
        self.visible = True
        self.width = -1
        self.height = -1
        self.initWidth = 30
        self.initHeight = 30
        self.loaded = False
        self.pins = Attach(self)
        self.layout = None

    def _load(self):
        if self.name == "UC":
            name = self.__class__.__name__ + str(UserControl.increment)
            UserControl.increment += 1
        else:
            name = self.name
        # log.debug.info("loading " + self.__class__.__name__ + "...")
        if not self.loaded:
            if self.parentLay is None:
                if cmds.workspaceControl(name, exists=1):
                    cmds.deleteUI(name)
                self.parentLay = cmds.workspaceControl(name, retain=False, iw=self.initWidth, ih=self.initHeight, floating=True)
            if self.height == -1 or self.width == -1:
                self.layout = cmds.formLayout(name , parent=self.parentLay, bgc=hexToRGB(self.color.background), vis=self.visible)
            elif not self.height == -1 and self.width == -1:
                self.layout = cmds.formLayout(name , parent=self.parentLay, bgc=hexToRGB(self.color.background), vis=self.visible, h=self.height)
            elif self.height == -1 and not self.width == -1:
                self.layout = cmds.formLayout(name , parent=self.parentLay, bgc=hexToRGB(self.color.background), vis=self.visible, w=self.width)
            else:
                self.layout = cmds.formLayout(name , parent=self.parentLay, bgc=hexToRGB(self.color.background), h=self.height, w=self.width, vis=self.visible)
            self.loaded = True
            for c in self._childrens:
                c.parentLay = self.layout
            object.__getattribute__(self, "load")()
        else:
            # log.debug.warning(name + " is already loaded")
            if self.height == -1 or self.width == -1:
                cmds.formLayout(self.layout, e=True, parent=self.parentLay)
            else:
                cmds.formLayout(self.layout, e=True, parent=self.parentLay, h=self.height, w=self.width)
        
        for c in self._childrens:
            c.load()
        if self.parentUC is not None:
            self.parentUC.applyAttach()
        self.applyAttach()
        self.runEvent(self.Event.LOAD)

    def _refresh(self):
        if self.loaded:
            # log.debug.info("refresh " + self.__class__.__name__ + "...")
            object.__getattribute__(self, "refresh")()
            for c in self._childrens:
                c.refresh()
            self.runEvent(self.Event.REFRESH)
  
    def _unload(self):
        if self.layout is None:
            return
        # log.debug.info("unload " + self.__class__.__name__ + "...")
        self.loaded = False
        for c in self._childrens:
            c.unload()
        object.__getattribute__(self, "unload")()
        if cmds.formLayout(self.layout, exists=1):
            cmds.deleteUI(self.layout)
        if cmds.workspaceControl(self.parentLay, exists=1):
            cmds.deleteUI(self.parentLay)
        self.loaded = False
        self.runEvent(self.Event.UNLOAD)

    def load(self):
        if self.__class__.__name__ is "UserControl":
            return
        log.debug.warning("[" + self.__class__.__name__ + "][load] method is not implemented")

    def refresh(self):
        if self.__class__.__name__ is "UserControl":
            return
        log.debug.warning("[" + self.__class__.__name__ + "][refresh] method is not implemented")

    def unload(self):
        if self.__class__.__name__ is "UserControl":
            return
        log.debug.warning("[" + self.__class__.__name__ + "][unload] method is not implemented")

    def reload(self):
        # log.debug.info("reload " + self.__class__.__name__ + "...")
        self.unload()
        self.load()
        self.runEvent(self.Event.RELOAD)

    def killSelf(self):
        
        if not self.loaded:
            if cmds.workspaceControl(name, exists=1):
                cmds.deleteUI(name)
            self.runEvent(self.Event.SELFKILL)

    def __getattribute__(self,name):
        if name == 'load':
            return object.__getattribute__(self, "_load")
        elif name == 'refresh':
            return object.__getattribute__(self, "_refresh")
        elif name == 'unload':
            return object.__getattribute__(self, "_unload")
        else:
            return object.__getattribute__(self, name)

    def visibility(self, vis):
        """Set the vibility of the UserControl

        :vis: boolean True=Visible False=Invisible
        """
        self.visible = vis
        if self.loaded:
            cmds.formLayout(self.layout, e=True, vis=vis)

    def attach(self, margin=(-1), **kwargs):
        """Attach the form to his parent

        Use Attach.NONE or Attach.FORM or (Attach.POS, [pos]) or (Attach.CTRL, [ctrl]) where [pos] is an Int and [ctrl] is a UserControl or a layout to the followings arguments

        :top:
        :bottom:
        :left:
        :right:

        :margin: 0 or (0,0) or (0,0,0,0) -> all or (top, bottom) or (top, bottom, left, right)
        """
        at = kwargs.items()
        keys = ["top", "bottom", "left", "right"]
        at = { k:v for k,v in at if k in keys }
        self.pins.attach(margin, at)


    def applyAttach(self):
        if len(self._childrens) == 0:
            return
        af = []
        ap = []
        ac = []
        an = []

        for ch in self._childrens:
            af += ch.pins.form
            ap += ch.pins.position
            ac += ch.pins.controller
            an += ch.pins.none
        if not(af == [] and af == [] and af == [] and af == []):
            cmds.formLayout(self.layout, edit=True,attachForm=af,attachPosition=ap,attachControl=ac,attachNone=an)
        self.runEvent(self.Event.APPLYATTACH)

    def setParent(self, parent):

        if parent is None:
            self.parentLay = parent
            self.parentUC = parent
            self.color = Color()
        elif type(parent) is str or type(parent) is unicode:
            self.parentLay = parent
        else:
            try:
                if self.parentUC is not None:
                    self.parentUC.delChildren(self)
                self.parentUC = parent
                self.parentLay = parent.layout
                self.parentUC.addChildren(self)
                self.color = parent.color
            except:
                log.debug.error(str(parent) + " of type " + str(type(parent)) + " is unreadable")
        if self.layout is not None and self.parentLay is not None:
            cmds.formLayout(self.layout, edit=True, parent=self.parentLay)


    def addChildren(self, child):
        self._childrens.append(child)

    def delChildren(self, child):
        self._childrens.remove(child)

    def eventHandler(self, event, c, *args):
        """Execute the given command when the UC call an [Event]
            event: type of Event
            c : function you want to call (some event might send more argument than your function ask)
            *args: Other argument you want to give
        """
        if not event in self._commands:
            self._commands[event] = []
        self._commands[event].append((c, args))
    def runEvent(self, event, *args):
        if not event in self._commands:
            return
        for c in self._commands[event]:
            if c[0] is None:
                # cmds.error("Event \"" + event + "\" call a function not implemented yet -WIP-")
                log.debug.warning("Event \"" + event + "\" call a function not implemented yet -WIP-")
                continue
            a = c[1] + args
            c[0](*a)

    def __str__(self):
        return str(self.layout)

log.debug.info("UC Loaded")