from ajenti.com import implements
from ajenti.api import *
from ajenti.ui import *
from ajenti import apis


class ServicesPlugin(CategoryPlugin):
    text = 'Services'
    icon = '/dl/services/icon.png'
    folder = 'system'

    def on_init(self):
        self.svc_mgr = self.app.get_backend(apis.services.IServiceManager)
        
    def on_session_start(self):
        self._labeltext = ''

    def get_ui(self):
        ui = self.app.inflate('services:main')
        ts = ui.find('list')

        lst = sorted(self.svc_mgr.list_all(), key=lambda x: x.status)
        for svc in lst:
            if svc.status == 'running':
                ctl = UI.HContainer(
                          UI.TipIcon(text='Stop', icon='/dl/core/ui/stock/service-stop.png', id='stop/' + svc.name),
                          UI.TipIcon(text='Restart', icon='/dl/core/ui/stock/service-restart.png', id='restart/' + svc.name)
                      )
            else:
                ctl = UI.TipIcon(text='Start', icon='/dl/core/ui/stock/service-run.png', id='start/' + svc.name)
            fn = '/dl/core/ui/stock/service-' + ('run.png' if svc.status == 'running' else 'stop.png')
            row = UI.DTR(
                    UI.Image(file=fn),
                    UI.Label(text=svc.name),
                    ctl
                  )
            ts.append(row)
        return ui

    @event('button/click')
    def on_click(self, event, params, vars=None):
        if params[0] == 'start':
            self.svc_mgr.start(params[1])
        if params[0] == 'restart':
            self.svc_mgr.restart(params[1])
        if params[0] == 'stop':
            self.svc_mgr.stop(params[1])
