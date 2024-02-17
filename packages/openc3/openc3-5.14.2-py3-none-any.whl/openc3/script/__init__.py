# Copyright 2023 OpenC3, Inc.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# This file may also be used under the terms of a commercial license
# if purchased from OpenC3, Inc.

from openc3.api import WHITELIST
from openc3.script.server_proxy import ServerProxy
from openc3.utilities.extract import convert_to_value

API_SERVER = ServerProxy()
RUNNING_SCRIPT = None
DISCONNECT = False
OPENC3_IN_CLUSTER = False
if "openc3-cosmos-cmd-tlm-api" in API_SERVER.generate_url():
    OPENC3_IN_CLUSTER = True


def shutdown_script():
    global API_SERVER
    API_SERVER.shutdown()


def prompt_for_hazardous(target_name, cmd_name, hazardous_description):
    """ """
    message_list = [f"Warning: Command {target_name} {cmd_name} is Hazardous. "]
    if hazardous_description:
        message_list.append(hazardous_description)
    message_list.append("Send? (y/N): ")
    answer = input("\n".join(message_list))
    try:
        return answer.lower()[0] == "y"
    except IndexError:
        return False


def _file_dialog(title, message, filter=None):
    answer = ""
    while len(answer) == 0:
        print(f"{title}\n{message}\n<Type file name>:")
        answer = input()
    return answer


###########################################################################
# START PUBLIC API
###########################################################################


def disconnect_script():
    global DISCONNECT
    DISCONNECT = True


def ask_string(question, blank_or_default=False, password=False):
    answer = ""
    default = None
    if blank_or_default is not True and blank_or_default is not False:
        question += f" (default = {blank_or_default})"
        default = str(blank_or_default)
        allow_blank = True
    else:
        allow_blank = blank_or_default
    while len(answer) == 0:
        print(question + " ")
        answer = input()
        if allow_blank:
            break
    if len(answer) == 0 and default:
        answer = default
    return answer


def ask(question, blank_or_default=False, password=False):
    string = ask_string(question, blank_or_default, password)
    value = convert_to_value(string)
    return value


def message_box(string, *buttons, **options):
    print(f"{string} ({', '.join(buttons)}): ")
    if "details" in options:
        print(f"Details: {options['details']}\n")
    return input()


def vertical_message_box(string, *buttons, **options):
    return message_box(string, *buttons, **options)


def combo_box(string, *buttons, **options):
    return message_box(string, *buttons, **options)


def metadata_input():
    # TODO: Not currently implemented
    pass


def open_file_dialog(title, message="Open File", filter=None):
    _file_dialog(title, message, filter)


def open_files_dialog(title, message="Open File", filter=None):
    _file_dialog(title, message, filter)


def prompt(
    string,
    text_color=None,
    background_color=None,
    font_size=None,
    font_family=None,
    details=None,
):
    print(f"{string}: ")
    if details:
        print(f"Details: {details}\n")
    return input()


###########################################################################
# END PUBLIC API
###########################################################################

from .api_shared import *
from .cosmos_calendar import *
from .commands import *
from .exceptions import *
from .limits import *
from .telemetry import *
from .metadata import *
from .screen import *
from .storage import *

# Define all the WHITELIST methods
current_functions = dir()
for func in WHITELIST:
    if func not in current_functions:
        code = f"def {func}(*args, **kwargs):\n    return getattr(API_SERVER, '{func}')(*args, **kwargs)"
        function = compile(code, "<string>", "exec")
        exec(function, globals())
