import maya
import pymel
import userControl as UC
import log

print(UC.__package__)

UC.UC.UserControl

win = UC.UC.UserControl(None)
win.name = "Test"


win.initWidth = 400
win.initHeight = 600

cbg = UC.checkBoxGrpUC.CheckBoxGrpUC(win)
cbg.addItem("Alpha", True)
cbg.addItem("Beta")
cbg.addItem("Charlie")
cbg.addItem("Delta")
cbg.attach(top=UC.UC.Attach.FORM, bottom=UC.UC.Attach.NONE, left=UC.UC.Attach.FORM, right=(UC.UC.Attach.POS, 55), margin=5)

img = UC.buttonsUC.IconButtonUC(win)
img.attach(top=(UC.UC.Attach.CTRL, cbg), bottom=UC.UC.Attach.NONE, left=UC.UC.Attach.FORM, right=(UC.UC.Attach.CTRL, cbg), margin=5)

win.load()