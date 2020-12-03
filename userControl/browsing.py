class Browsing(object):
    class item():
        def __init__(self, name, elem, image=None, info="", icon=None):
            self.name = name
            self.elem = elem
            self.image = image
            self.icon = icon
            self.info = info
            self.deep = 0
            self.parent = None
            self.displayElem = {}
            self.selected = False
            
        def setParent(self, parent):
            if self.parent is not None:
                self.parent.removeChildren(self)
            parent.addChildren(self)

        def addDisplayElem(self, dispElem, name):
            self.displayElem[name] = dispElem
            pass

        def getDisplayElemBy(self, name):
            return self.displayElem[name]
        
        def selection(self, val):
            self.selected = val
            for d in self.displayElem.values():
                d.selection(val)

        def returnRoot(self):
            if self.parent is not None:
                return self.parent.returnRoot()
            else:
                return self

    class folder(item):
        def __init__(self, name, elem):
            Browsing.item.__init__(self, name, elem)
            self._childrens = []
            self.icon = "arrowBottom"
            self.isDeployed = True
            self.area = None
            self.selecteds = []

        def deploying(self, val):
            self.isDeployed = val
            if val:
                self.icon = "arrowBottom"
            else:
                self.icon = "arrowRight"
            for e in self.displayElem.values():
                e.icon = self.icon
                e.refresh()
            # self.displayElem.icon = self.icon
            # self.displayElem.refresh()
            self.area.visibility(self.isDeployed)
            # cmds.formLayout(self.area, e=True, vis=self.isDeployed)

        def deployingAll(self, val):
            self.deploying(val)
            for f in self._childrens:
                if f.__class__ is Browsing.folder:
                    Browsing.folder.deployingAll(f, val)

        def addChildren(self, child):
            self._childrens.append(child)
            child.parent = self

        def removeChildren(self, child):
            self._childrens.remove(child)
            child.parent = None
        
        def getAllParent(self):
            if self.parent is None:
                return "/"
            return self.getAllParent() + "/" + self.name

    def __init__(self):
        # super(Browsing, self).__init__()
        self.folders = {}
        self.items = {}
        self.root = Browsing.folder(".", None)
        self.selecteds = []
        self.multiSelect = True
        self.addable = True
    
    def deleteAllItemsFolders(self):
        self.folders = {}
        self.items = {}
        self.root = Browsing.folder(".", None)

    def addFolder(self, name, elem, parent=None):
        f = Browsing.folder(name, elem)

        if parent is None:
            f.setParent(self.root)
            f.deep = 1
        else:
            f.setParent(parent)
            f.deep = f.parent.deep + 1
        self.folders[elem] = f
        return f
    
    def addItem(self, name, elem, parent=None, image=None, info="", icon=None):
        i = Browsing.item(name, elem, image=image, info=info, icon=icon)

        if parent is None:
            i.setParent(self.root)
        else:
            i.setParent(parent)
            i.deep = i.parent.deep + 1
        self.items[elem] = i
        return i

    def importBrows(self, imp):
        self.root = imp.root

    def _clickItem(self, item, displayElem, mod):
        for t in item.returnRoot().selecteds:
            if (mod != 1 or item.parent != t.parent or not self.multiSelect):
                t.selection(False)
                # t.displayElem.selection(False)
        if mod != 1:
            item.returnRoot().selecteds = []
        if mod <= 1:
            if item.selected:
                item.selection(False)
                item.returnRoot().selecteds.remove(item)
            else:
                item.selection(True)
                item.returnRoot().selecteds.append(item)
        # selection = [x.elem for x in self.selecteds if x.displayElem.selected]
        self.runEvent("changeSelection", item.returnRoot().selecteds)


    def select(self, selection, value):
        '''display the lines in selection as selected in the tree
        selection: the lines to be select
        value: True to select
        '''
        pass
