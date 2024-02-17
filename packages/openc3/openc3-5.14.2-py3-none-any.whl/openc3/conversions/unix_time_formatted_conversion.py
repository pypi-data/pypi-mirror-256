# Copyright 2023 OpenC3, Inc.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addums as found in the LICENSE.txt
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# This file may also be used under the terms of a commercial license
# if purchased from OpenC3, Inc.


from openc3.conversions.unix_time_conversion import UnixTimeConversion
from openc3.utilities.time import formatted


# Converts a unix format time: Epoch Jan 1 1970, seconds and microseconds,
# into a formatted string.
class UnixTimeFormattedConversion(UnixTimeConversion):
    # Initializes converted_type to :STRING and converted_bit_size to 0
    #
    # @param seconds_item_name [String] The telemetry item in the packet which
    #   represents the number of seconds since the UNIX time epoch
    # @param microseconds_item_name [String] The telemetry item in the packet
    #   which represents microseconds
    def __init__(self, seconds_item_name, microseconds_item_name=None):
        super().__init__(seconds_item_name, microseconds_item_name)
        self.converted_type = "STRING"
        self.converted_bit_size = 0

    # @param (see Conversion#call)
    # @return [String] Formatted packet time
    def call(self, value, packet, buffer):
        return formatted(super().call(value, packet, buffer))

    # @return [String] The name of the class followed by the time conversion
    def __str__(self):
        result = f"UnixTimeFormattedConversion {self.seconds_item_name}"
        if self.microseconds_item_name:
            result += f" {self.microseconds_item_name}"
        return result
