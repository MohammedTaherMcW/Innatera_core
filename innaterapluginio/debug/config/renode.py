# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from innaterapluginio.debug.config.base import DebugConfigBase


class RenodeDebugConfig(DebugConfigBase):
    DEFAULT_PORT = ":3333"
    GDB_INIT_SCRIPT = """
define pio_reset_halt_target
    monitor machine Reset
    $LOAD_CMDS
    monitor start
end

define pio_reset_run_target
    pio_reset_halt_target
end

target extended-remote $DEBUG_PORT
$LOAD_CMDS
$INIT_BREAK
monitor start
"""

    @property
    def server_ready_pattern(self):
        return super().server_ready_pattern or (
            "GDB server with all CPUs started on port"
        )
