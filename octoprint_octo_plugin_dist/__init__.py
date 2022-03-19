from __future__ import absolute_import, unicode_literals

import octoprint.plugin
import socket
from os.path import exists
import client

class HelloWorldPlugin(octoprint.plugin.StartupPlugin,octoprint.plugin.TemplatePlugin):


    def on_after_startup(self):
        self._logger.info("TESTING")
        #self.__client = client()
        self._logger.info("STARTED CLIENT")


__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = HelloWorldPlugin()
