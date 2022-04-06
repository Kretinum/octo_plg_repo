from __future__ import absolute_import, unicode_literals

import octoprint.plugin
import socket
from os.path import exists
from .client import client

class HelloWorldPlugin(octoprint.plugin.StartupPlugin,octoprint.plugin.TemplatePlugin):


    def on_after_startup(self):
        self._logger.info("TESTING")
        self.__client = client(self)
        self._logger.info("STARTED CLIENT")

    def on_shutdown(self):
        self.__client.shutDown()


__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = HelloWorldPlugin()
