from __future__ import absolute_import, unicode_literals

import octoprint.plugin

class HelloWorldPlugin(octoprint.plugin.StartupPlugin):
    def on_after_startup(self):
        self._logger.info("Hello World!")


__plugin_name__ = "conn_plugin"
__plugin_version__ = "1.0.0"
__plugin_description__ = ""
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = HelloWorldPlugin()
