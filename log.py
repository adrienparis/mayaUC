import sys
try:
    import maya.cmds as cmds
except:
    print("no maya")

DEBUG = True


def info(*args):
    if len(args) >= 1:
        if len(args) >= 2:
            print("(i) - " + str(args[0]) + " -> " + str(args[1:]))
        else:
            print("(i) - " + str(args[0]))

def warning(*args):
    if len(args) >= 1:
        if "maya" in sys.modules:
            cmds.warning(args)
        else:
            if len(args) >= 2:
                print("/!\\ - " + str(args[0]) + " -> " + str(args[1:]))
            else:
                print("/!\\ - " + str(args[0]))

def error(*args):
    if len(args) >= 1:
        if "maya" in sys.modules:
            cmds.error(args)
        else:
            if len(args) >= 2:
                print("(X) - " + str(args[0]) + " -> " + str(args[1:]))
            else:
                print("(X) - " + str(args[0]))

class debug():
    @staticmethod
    def info(*args):
        if not DEBUG:
            return
        if len(args) >= 1:
            if len(args) >= 2:
                print("[D] - " + "(i) - " + str(args[0]) + " -> " + str(args[1:]))
            else:
                print("[D] - " + "(i) - " + str(args[0]))

    @staticmethod
    def warning(*args):
        if not DEBUG:
            return
        if len(args) >= 1:
            if "maya" in sys.modules:
                cmds.warning(args)
            else:
                if len(args) >= 2:
                    print("[D] - " + "/!\\ - " + str(args[0]) + " -> " + str(args[1:]))
                else:
                    print("[D] - " + "/!\\ - " + str(args[0]))

    @staticmethod
    def error(*args):
        if not DEBUG:
            return
        if len(args) >= 1:
            if "maya" in sys.modules:
                cmds.error(args)
            else:
                if len(args) >= 2:
                    print("[D] - " + "(X) - " + str(args[0]) + " -> " + str(args[1:]))
                else:
                    print("[D] - " + "(X) - " + str(args[0]))