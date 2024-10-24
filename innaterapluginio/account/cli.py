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

from innaterapluginio.account.commands.destroy import account_destroy_cmd
from innaterapluginio.account.commands.forgot import account_forgot_cmd
from innaterapluginio.account.commands.login import account_login_cmd
from innaterapluginio.account.commands.logout import account_logout_cmd
from innaterapluginio.account.commands.password import account_password_cmd
from innaterapluginio.account.commands.register import account_register_cmd
from innaterapluginio.account.commands.show import account_show_cmd
from innaterapluginio.account.commands.token import account_token_cmd
from innaterapluginio.account.commands.update import account_update_cmd


@click.group(
    "account",
    commands=[
        account_destroy_cmd,
        account_forgot_cmd,
        account_login_cmd,
        account_logout_cmd,
        account_password_cmd,
        account_register_cmd,
        account_show_cmd,
        account_token_cmd,
        account_update_cmd,
    ],
    short_help="Manage Innatera account",
)
def cli():
    pass
