"""Script to run Banquet, the batch name markup tool."""

__docformat__ = 'restructuredtext'

try:
    import psyco
    psyco.full()
except ImportError:
    pass

import gtk

def main ():
    from model import MainModel
    from controller import MainController
    from view import MainView

    m = MainModel()
    v = MainView()
    c = MainController(m, v)

    gtk.main()


if __name__ == '__main__':
    main()
