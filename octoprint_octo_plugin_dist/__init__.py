from __future__ import absolute_import, unicode_literals

import octoprint.plugin
import socket



class HelloWorldPlugin(octoprint.plugin.StartupPlugin,octoprint.plugin.TemplatePlugin):
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(('192.168.1.103',42069))
        self._socket.send(bytes("TEST_PRINTER"))

    def on_after_startup(self):
        self._logger.info("TESTING")


__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = HelloWorldPlugin()
