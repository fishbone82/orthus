# tcp plugin for hh
from base import plugin_base
from args import address, port


class plugin(plugin_base):
    use_args = (address, port)
    description = "Simple TCP plugin for HH"
    status = -1
    data = None

    def check(self):
        return self.status, self.data