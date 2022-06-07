from __future__ import absolute_import, unicode_literals

import octoprint.plugin
import socket
from os.path import exists
from .client import client

class Plugin(octoprint.plugin.StartupPlugin,
             octoprint.plugin.TemplatePlugin,
             octoprint.plugin.SettingsPlugin,
             octoprint.plugin.AssetPlugin,
             octoprint.plugin.EventHandlerPlugin,
             octoprint.plugin.ShutdownPlugin):


    def on_after_startup(self):
        self._logger.info("TESTING")
        self.__client = client(self)
        self._logger.info("STARTED CLIENT")

    def on_shutdown(self):
        self.__client.shutDown()

    def get_settings_defaults(self):
        return dict(freq=5)

    def get_template_vars(self):
        return dict(freq=self._settings.get(["freq"]))

__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_name__ = "REPrin3D"
__plugin_implementation__ = Plugin()
