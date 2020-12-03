import sys
from PySide2 import QtWidgets, QtSvg

app = QtWidgets.QApplication(sys.argv)
svgWidget = QtSvg.QSvgWidget(r"D:\creative seed\script\todo_list\icons\check.svg")
svgWidget.setGeometry(50,50,759,668)
svgWidget.show()

sys.exit(app.exec_())