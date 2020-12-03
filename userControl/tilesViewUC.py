import maya.cmds as cmds
from pymel.all import *

import log

from .UC import *
from browsing import Browsing
from tileUC import TileUC

class DockTilesUC(UserControl):
    _sizeImage = 100
    
    def resizeTilesView(self):
        h = cmds.scrollLayout(self.scrLay, q=True, h=True)
        w = cmds.scrollLayout(self.scrLay, q=True, w=True)
        size = math.trunc((w - 4) / self._sizeImage)
        if size == 0:
            return

        nbChild = cmds.gridLayout(self.grdLay, q=True, nch=True )
        rows = max((nbChild - 1) / size + 1, 1)
        if h < rows * self._sizeImage:
            size = math.trunc((w - 16) / self._sizeImage)
            if size == 0:
                return

            nbChild = cmds.gridLayout(self.grdLay, q=True, nch=True )
            rows = max((nbChild - 1) / size + 1, 1)

        cmds.gridLayout(self.grdLay, e=True, numberOfColumns=size )
        cmds.gridLayout(self.grdLay, e=True, numberOfRows= rows )


    def load(self):
        self.scrLay = cmds.scrollLayout(parent=self.layout,
                                    horizontalScrollBarThickness=160,
                                    verticalScrollBarThickness=16,
                                    cr=True, rc=Callback(self.resizeTilesView))
        self.grdLay = cmds.gridLayout(numberOfColumns=3, cr=False, ag=True, cellWidthHeight=(self._sizeImage, self._sizeImage))
        cmds.formLayout(self.layout, edit=True, attachForm=[(self.scrLay, 'top', 0),(self.scrLay, 'bottom', 0),(self.scrLay, 'left', 0), (self.scrLay, 'right', 0)])
        
        for t in self._childrens:
            t.setParent(self.grdLay)
            t.load()

class TilesViewUC(UserControl, Browsing):
    
    _styleIcon = 'iconAndTextVertical'
    _sizeImage = 100

    def __init__(self, parent, multiSelect=True):
        UserControl.__init__(self, parent)
        Browsing.__init__(self)
        self.name = "TilesView" + self.name
        self.scrlLay = ""
        self.currentFold = self.root
        self.tabs = None

    # def _clickItem(self, item, displayElem, mod):
        
    #     for t in self.selecteds:
    #         if (mod != 1 or item.parent != t.parent or not self.multiSelect):
    #             t.displayElem.selection(False)
    #     if mod != 1:
    #         self.selecteds = []
    #     if mod <= 1:
    #         if displayElem.selected:
    #             displayElem.selection(False)
    #             self.selecteds.remove(item)
    #         else:
    #             displayElem.selection(True)
    #             self.selecteds.append(item)
    #     selection = [x.elem for x in self.selecteds if x.displayElem.selected]
    #     self.runEvent("changeSelection", selection)

    def _loadFolder(self, fold):
        self.currentFold = fold
        if self.tabs is not None and cmds.tabLayout(self.tabs, q=True, exists=True):
            cmds.deleteUI(self.tabs)
        if self.addable:
            self.tabs = cmds.tabLayout(snt=True, parent=self.layout, ntc=Callback(self.newElem, fold))
        else:
            self.tabs = cmds.tabLayout(parent=self.layout)

        for f in fold._childrens:
            if f.__class__ is Browsing.folder:
                area = DockTilesUC(self.tabs)
                area.name = f.name
                if self.addable:
                    newElem = TileUC(area, getIcon("add"), "New")
                    newElem.eventHandler("click", self.newElem, f)
                if fold is not self.root:
                    folderPar = TileUC(area, getIcon("folderBig"), "..")
                    folderPar.eventHandler("click", self.clickFolder, fold.parent)
                for i in f._childrens:
                    if i.__class__ is Browsing.folder:
                        i.addDisplayElem(TileUC(area, getIcon("folderBig"), i.name), "tilesView")
                        i.displayElem["tilesView"].eventHandler("click", self.clickFolder, f)
                    else:
                        i.addDisplayElem(TileUC(area, i.image, i.name, i.icon), "tilesView")
                        i.displayElem["tilesView"].eventHandler("click", self._clickItem, i)
                area.load()
        cmds.formLayout(self.layout, edit=True, attachForm=[(self.tabs, 'top', 0),(self.tabs, 'bottom', 0),(self.tabs, 'left', 0), (self.tabs, 'right', 0)])

    def load(self):
        self._loadFolder(self.root)


    def newElem(self, folder, tile=None, mod=None):
        self.runEvent("newElem", folder.elem)
        pass

    def clickFolder(self, item, tile, mod):
        self._loadFolder(item)