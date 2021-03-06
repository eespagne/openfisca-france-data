# -*- coding: utf-8 -*-

"""This is the launcher script for the ViTables application."""



from __future__ import print_function

#       Copyright (C) 2005-2007 Carabos Coop. V. All rights reserved
#       Copyright (C) 2008-2011 Vicent Mas. All rights reserved
#
#       This program is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program.  If not, see <http://www.gnu.org/l.icenses/>.
#
#       Author:  Vicent Mas - vmas@vitables.org

__docformat__ = 'restructuredtext'


import locale
from optparse import OptionParser
import sys
import os.path

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtGui

def main(args):
    """The application launcher.

    First of all, translators are loaded. Then the GUI is shown and the events
    loop is started.
    """

    app = QtGui.QApplication(args)
    # These imports must be done after the QApplication has been instantiated
    from vitables.vtapp import VTApp
    from vitables.preferences import vtconfig

    # Specify the organization's Internet domain. When the Internet
    # domain is set, it is used on Mac OS X instead of the organization
    # name, since Mac OS X applications conventionally use Internet
    # domains to identify themselves
    app.setOrganizationDomain('vitables.org')
    app.setOrganizationName('ViTables')
    app.setApplicationName('ViTables')
    app.setApplicationVersion(vtconfig.getVersion())
    config = vtconfig.Config()

    # Localize the application using the system locale
    # numpy seems to have problems with decimal separator in some locales
    # (catalan, german...) so C locale is always used for numbers.
    locale.setlocale(locale.LC_ALL, '')
    locale.setlocale(locale.LC_NUMERIC, 'C')
    language = locale.getlocale()[0]
    # Future translations (if any) will use resource files
    # vt_translator = QTranslator()
    # vt_translator.load('vitables_%s' % language, config.translations_dir)
    # qt_translator = QTranslator()
    # qt_translator.load('qt_%s' % language, config.translations_dir)
    # app.installTranslator(vt_translator)
    # app.installTranslator(qt_translator)

    # Parse the command line
    parser = OptionParser(prog='vitables', version=vtconfig.getVersion(),
        usage='''%prog [options] [h5file]''')
    parser.add_option('-m', '--mode', dest='mode', choices=['r', 'a'],
        help='mode access for a database', metavar='MODE')
    parser.add_option('-d', '--dblist', dest='dblist',
        help='a file with the list of databases to be open', metavar='h5list')
    parser.set_defaults(mode='a', dblist='')
    (options, h5files) = parser.parse_args()
    if options.dblist:
        # Other options and positional arguments are silently ignored
        options.mode = ''
        h5files = []

    # Start the application
    del config
    vtapp = VTApp(mode=options.mode, dblist=options.dblist, h5files=h5files)
    vtapp.gui.show()
    app.exec_()

if __name__ == '__main__':
    # How to run in Mac OS X
    if (sys.platform == 'darwin'
        and not sys.executable.endswith('MacOS/Python')
        and getattr(sys, 'frozen', None) != 'macosx_app'):
        # When running this script under Mac OS X from the command line
        # (but not as an app), the ``pythonw`` interpreter must be used
        # instead of the ordinary ``python``.
        os.execvp('pythonw', ['pythonw', __file__] + sys.argv[1:])

    main(sys.argv)