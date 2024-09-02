# Copyright
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys


class PreStartUp:
    """Necessary steps for environment, Python and Qt"""

    @staticmethod
    def set_qt_application_name():
        from PySide6.QtCore import QCoreApplication
        QCoreApplication.setApplicationName('my app name')
        QCoreApplication.setOrganizationName('my org name')

    @staticmethod
    def set_qt_application_version():
        from PySide6.QtCore import QCoreApplication
        QCoreApplication.setApplicationVersion('my app version')

    @staticmethod
    def inject_environment_variables():
        # Qt expects 'qtquickcontrols2.conf' at root level, but the way we handle resources does not allow that.
        # So we need to override the path here
        os.environ['QT_QUICK_CONTROLS_CONF'] = ':/data/qtquickcontrols2.conf'

        if sys.platform == "linux":
            # Use x11 backend (this enables drop shadow on Linux)
            os.environ["QT_QPA_PLATFORM"] = "xcb"


class StartUp:
    """Necessary steps for myapp"""

    @staticmethod
    def import_resources():
        # noinspection PyUnresolvedReferences
        import myapp.generated_resources

    @staticmethod
    def import_bindings():
        # noinspection PyUnresolvedReferences
        import myapp.pyobjects

    @staticmethod
    def start_application():
        from myapp.application import MyApplication
        app = MyApplication(sys.argv)

        app.set_window_icon()
        app.set_up_signals()
        app.set_up_imports()
        app.set_up_window_event_filter()
        app.start_engine()
        app.set_up_window_effects()
        app.verify()

        sys.exit(app.exec())


def perform_startup():
    we = PreStartUp()
    we.set_qt_application_name()
    we.set_qt_application_version()
    we.inject_environment_variables()

    we = StartUp()
    we.import_resources()
    we.import_bindings()
    we.start_application()
