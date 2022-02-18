from __future__ import absolute_import, unicode_literals

import octoprint.plugin

class HelloWorldPlugin(octoprint.plugin.StartupPlugin,octoprint.plugin.TemplatePlugin):
    def on_after_startup(self):
        self._logger.info("TESTING")


__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = HelloWorldPlugin()
