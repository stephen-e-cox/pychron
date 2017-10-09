# ===============================================================================
# Copyright 2011 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================



# ============= enthought library imports =======================
from threading import Timer

from traits.api import Range, Event, Bool, on_trait_change, Property, Float, Int
from traitsui.api import View, Item, ButtonEditor, HGroup, Group

# ============= standard library imports ========================

# ============= local library imports  ==========================
from pychron.hardware.core.abstract_device import AbstractDevice


class FiberLight(AbstractDevice):
    """
    """
    intensity = Property(Range(0, 100.0, mode='slider'), depends_on='_intensity')
    _intensity = Float
    power = Event
    power_label = Property(depends_on='state')
    state = Bool
    auto_onoff = Bool(False)
    name = 'fiber_light'
    timeout = Int(300)
    _timer = None

    def load_additional_args(self, config):
        """
        """
        klass = self.config_get(config, 'General', 'control_module')

        self._cdevice = None
        if klass is not None:
            package = 'pychron.hardware.arduino.arduino_fiber_light_module'
            factory = self.get_factory(package, klass)
            self._cdevice = factory(name=klass,
                                    configuration_dir_name=self.configuration_dir_name)

            return True

    def initialize(self, *args, **kw):
        if self._cdevice:
            self._cdevice.setup_consumer(self._write_intensity)

        return True

    def _write_intensity(self, v):
        if self._cdevice:
            self._cdevice.set_intensity(v / 100 * 255)

    def read_state(self):
        if self._cdevice is not None:
            if self._cdevice.read_state():
                self.state = True
            else:
                self.state = False

    def read_intensity(self, *args):
        if self._cdevice is not None:
            v = self._cdevice.read_intensity()
            if v is not None:
                self._intensity = float('{:0.3n}'.format(v))

    def power_on(self):
        """
        """
        self.state = True
        if self._cdevice is not None:
            self._cdevice.power_on()
            if self.timeout:
                if self.timer:
                    self.timer.cancel()

                self.timer = Timer(self.timeout, self.power_off)
                self.timer.start()

    def power_off(self, *args):
        """
        """
        self.state = False
        if self._cdevice is not None:
            self._cdevice.power_off()

    def _get_intensity(self):
        return int(self._intensity)

    def _set_intensity(self, v):
        """
        """
        self._intensity = int(v)
        if self._cdevice is not None:
            self._cdevice.add_consumable(self._intensity)

    @on_trait_change('power')
    def power_fired(self):
        """
        """
        if self.state:
            self.power_off()
        else:
            self.power_on()

    def _get_power_label(self):
        """
        """
        if self.state:
            s = 'ON'
        else:
            s = 'OFF'
        return s

    def get_control_group(self):
        return Group(HGroup(Item('power', editor=ButtonEditor(label_value='power_label'),
                                 show_label=False),
                            Item('intensity', format_str='%0.2f',
                                 show_label=False,
                                 enabled_when='state')),
                     Item('auto_onoff'),
                     Item('timeout'))

    def traits_view(self):
        return View(self.get_control_group())

# ============= EOF ====================================
