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

import click

from innaterapluginio.account.org.commands.add import org_add_cmd
from innaterapluginio.account.org.commands.create import org_create_cmd
from innaterapluginio.account.org.commands.destroy import org_destroy_cmd
from innaterapluginio.account.org.commands.list import org_list_cmd
from innaterapluginio.account.org.commands.remove import org_remove_cmd
from innaterapluginio.account.org.commands.update import org_update_cmd


@click.group(
    "account",
    commands=[
        org_add_cmd,
        org_create_cmd,
        org_destroy_cmd,
        org_list_cmd,
        org_remove_cmd,
        org_update_cmd,
    ],
    short_help="Manage organizations",
)
def cli():
    pass
