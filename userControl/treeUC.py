from pymel.all import *
import maya.cmds as cmds

import log
from browsing import Browsing
from .UC import *
from .lineUC import *

class TreeUC(UserControl, Browsing):

    def __init__(self, parent, multiSelect=True):
        UserControl.__init__(self, parent)
        Browsing.__init__(self)
        self.name = "Tree" + self.name
        self.scrlLay = ""


    
    def _loadFolder(self, fold, parent):
        elems = []
        area = UserControl(parent)
        area.color.background = 0x101010 * (fold.deep % 2) + self.color.main
        area.visibility(fold.isDeployed or fold.deep < 1)
        area.load()
        

        for elem in fold._childrens:
            if elem.__class__ is Browsing.folder:
                elem.icon = "arrowBottom"
            elem.addDisplayElem(LineUC(area, elem.name, info=elem.info, icon=elem.icon), "treeView")
            elem.displayElem["treeView"].load()
            elems.append(elem.displayElem["treeView"])
            if elem.__class__ is Browsing.folder:
                elems.append(self._loadFolder(elem, area))
                elem.area = elems[-1]
                elem.displayElem["treeView"].eventHandler("click", self._clickFolder, elem)
            else:
                elem.displayElem["treeView"].eventHandler("click", self._clickItem, elem)
        if self.addable:
            newElem = LineUC(area, "New", icon="addSmall")
            newElem.load()
            newElem.eventHandler("click", self._newElement, fold)
            elems.append(newElem)

        last = None
        for e in elems:
            if last is None:
                e.attach(top=Attach.FORM)
            else:
                e.attach(top=(Attach.CTRL, last))
            if fold is self.root:
                e.attach(left=Attach.FORM)
            else:
                e.attach(left=Attach.FORM, margin=(0,0,15,0))
            e.attach(bottom=Attach.NONE, right=Attach.FORM)
            last = e
        area.applyAttach()
        return area

    def load(self):
        

        if cmds.scrollLayout(self.scrlLay, q=True, ex=True):
            cmds.deleteUI(self.scrlLay)
        self.scrlLay = cmds.scrollLayout(parent=self.layout, childResizable=True, bgc=hexToRGB(0xa5c957))
        t = self._loadFolder(self.root, self.scrlLay)
        
        cmds.formLayout(self.layout, edit=True, attachForm=[(self.scrlLay, 'top', -2),(self.scrlLay, 'bottom', -2),(self.scrlLay, 'left', -2), (self.scrlLay, 'right', -2)])


    def _clickFolder(self, folder, displayElem, mod):
        log.debug("plop")
        if mod == 0:
            folder.deploying(not folder.isDeployed)
        elif mod == 1:
            folder.deployingAll(not folder.isDeployed)

    def _newElement(self, folder, plop1, plop2):
        self.runEvent("newElem", folder.elem)
        pass
