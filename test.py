from userControl import UC
reload(UC)



class mainBoard(UC.UserControl):

    def fplop(truc, button, ctrl, alt, shift):
        print(button, ctrl, alt, shift)
        print("ntm")
    def fprint(*args):
        print(args)
    def load(self):
        self.listObj = UC.UserControl(self, name="listObj")
        self.detailsObj = UC.UserControl(self, name="detailsObj")
        self.listObj.height = 10
        self.listObj.width = 200
        self.detailsObj.height = 60
        self.detailsObj.width = 20
        self.listObj.color["background"] = "main"
        self.listObj.colorTheme["main"] = 0xbada55
        self.detailsObj.color["background"] = "main"
        self.detailsObj.colorTheme["main"] = 0x8b6c42

        self.listObj.eventClickHandler(1, self.fprint, "lol", ctrl=True)
        self.listObj.eventClickHandler(1, self.fplop, ctrl=True, alt=True)
        self.listObj.eventClickHandler(1, self.fplop, ctrl=True, alt=True)
        self.listObj.eventHandler(UC.UserControl.Event.APPLYATTACH, self.fprint, "c d'la merde")
        self.listObj.attach(top=(UC.Attach.POS, 15), bottom=UC.Attach.FORM, left=UC.Attach.NONE, right=(UC.Attach.POS, 90), margin=(5,45,5,5))
        self.detailsObj.attach(top=(UC.Attach.POS, 10), bottom=(UC.Attach.POS, 10), left=UC.Attach.FORM, right=(UC.Attach.CTRL, self.listObj), margin=5)


plop = mainBoard(name="My super Auto Rig")
plop.load()







def fplop(button, ctrl, alt, shift):
    print(button, ctrl, alt, shift)
    print("ntm")
def fprint(*args):
    print(args)

plop = UC.UserControl(name="mainBoard")
listObj = UC.UserControl(plop, name="listObj")
detailsObj = UC.UserControl(plop, name="detailsObj")

listObj.attach(top=(UC.Attach.POS, 15), bottom=UC.Attach.FORM, left=UC.Attach.NONE, right=(UC.Attach.POS, 90), margin=(5,45,5,5))
# detailsObj.attach(top=(UC.Attach.POS, 10), bottom=(UC.Attach.POS, 10), left=UC.Attach.FORM, right=(UC.Attach.CTRL, listObj), margin=5)

# listObj.height = 10
# listObj.width = 200
# detailsObj.height = 60
# detailsObj.width = 20
# listObj.color["background"] = "main"
# detailsObj.color["background"] = "secondary"
# listObj.eventClickHandler(1, fprint, "lol", ctrl=True)
# listObj.eventClickHandler(1, fplop, ctrl=True, alt=True)
# listObj.eventClickHandler(1, fplop, ctrl=True, alt=True)
# listObj.eventHandler(UC.UserControl.Event.APPLYATTACH, fprint, "c d'la merde")

plop.load()

