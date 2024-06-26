# Copyright (c) 2014-present PlatformIO <contact@platformio.org>
#
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

from platformio.debug.config.base import DebugConfigBase


class QemuDebugConfig(DebugConfigBase):
    DEFAULT_PORT = ":1234"
    GDB_INIT_SCRIPT = """
define pio_reset_halt_target
    monitor system_reset
end

define pio_reset_run_target
    monitor system_reset
end

target extended-remote $DEBUG_PORT
$LOAD_CMDS
pio_reset_halt_target
$INIT_BREAK
"""
