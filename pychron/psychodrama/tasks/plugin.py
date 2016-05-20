# ===============================================================================
# Copyright 2016 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# ============= enthought library imports =======================
import select
from traits.api import Str
# ============= standard library imports ========================
import os
import socket
from threading import Thread
# ============= local library imports  ==========================
from apptools.preferences.preference_binding import bind_preference

from pychron.envisage.tasks.base_plugin import BasePlugin
from pychron.psychodrama.psychodrama_command_server import PsychoDramaCommandServer


class PsychoDramaPlugin(BasePlugin):

    def start(self):
        """
        start listening for commands
        @return:
        """
        s = PsychoDramaCommandServer()
        s.start()

# ============= EOF =============================================