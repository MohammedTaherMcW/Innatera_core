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

from Innatera import app
from Innatera.commands.settings import cli


def test_settings_check(clirunner, validate_cliresult):
    result = clirunner.invoke(cli, ["get"])
    validate_cliresult(result)
    assert result.output
    for item in app.DEFAULT_SETTINGS.items():
        assert item[0] in result.output
