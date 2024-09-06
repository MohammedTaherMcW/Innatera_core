% import json
% import os
% import click
%
% def _escape(text):
%   return text.replace('"', '\"')
% end
%
% def _escape_path(path):
%   return path.replace('\\\\', '/').replace('\\', '/').replace('"', '\\"')
% end
%
% @click.option(
%     "-O",
%     "--project-option",
%     "project_options",
%     multiple=True,
%     help="A `name=value` pair", )
%
% def get_debug_configuration():
%   return {
%     "version": "0.2.0",
%     "configurations": [
%       {
%         "name": "Python Debugger: Current File",
%         "type": "debugpy",
%         "request": "launch",
%         "program": "${file}",
%         "console": "integratedTerminal"
%       }
%     ]
%   }
% end
%
% def get_debug_launch_configuration():
%   launch_config = get_debug_configuration()
%   return launch_config
% end
%
// AUTOMATICALLY GENERATED FILE. PLEASE DO NOT MODIFY IT MANUALLY
//
// Innatera Debugger
//
// Documentation: https://docs.platformio.org/en/latest/plus/debugging.html
// Configuration: https://docs.platformio.org/en/latest/projectconf/sections/env/options/debug/index.html

{{ json.dumps(get_debug_launch_configuration(), indent=4, ensure_ascii=False) }}
