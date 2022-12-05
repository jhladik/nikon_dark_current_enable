#
#    Copyright (C) 2022  Jakub Hladik
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import usb.core
import usb.util
import array


dev = usb.core.find(idVendor=0x04b0, idProduct=0x0428)
if dev is None:
    raise ValueError("Device not found")

dev.set_configuration()

rx_buff = array.array("B", b"\x00"*512)

# GetDeviceInfo
# ContainerLength=12    ContainerType=CommandBlock    Code=0x1001    TransactionID=0    Payload=None
dev.write(0x02, b"\x0c\x00\x00\x00\x01\x00\x01\x10\x00\x00\x00\x00", 100)
rx_len = dev.read(0x81, rx_buff, 400)
rx_len = dev.read(0x81, rx_buff, 400)

# OpenSession
# ContainerLength=16    ContainerType=CommandBlock    Code=0x1002    TransactionID=1    Payload=01000000
dev.write(0x02, b"\x10\x00\x00\x00\x01\x00\x02\x10\x01\x00\x00\x00\x01\x00\x00\x00", 100)
rx_len = dev.read(0x81, rx_buff, 400)

# ServiceModeStart
# ContainerLength=16    ContainerType=CommandBlock    Code=0xfc01    TransactionID=2    Payload=00000000 00000000 00000000
dev.write(0x02, b"\x18\x00\x00\x00\x01\x00\x01\xfc\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", 100)
rx_len = dev.read(0x81, rx_buff, 400)

# Get camera model
# ContainerLength=16    ContainerType=CommandBlock    Code=0xfe02    TransactionID=3    Payload=00000000 80000000 00000000
dev.write(0x02, b"\x18\x00\x00\x00\x01\x00\x02\xfe\x03\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00", 100)
rx_len = dev.read(0x81, rx_buff, 400)
rx_len = dev.read(0x81, rx_buff, 400)

# Turn compression off
# ContainerLength=16    ContainerType=CommandBlock    Code=0xfc46    TransactionID=4    Payload=01000000 00000000 00000000
dev.write(0x02, b"\x18\x00\x00\x00\x01\x00\x46\xfc\x04\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", 100)
rx_len = dev.read(0x81, rx_buff, 400)

# Turn overscan on (disables black clipping, hot pixel removal, etc)
# ContainerLength=16    ContainerType=CommandBlock    Code=0xfc44    TransactionID=5    Payload=01000000 00000000 00000000
dev.write(0x02, b"\x18\x00\x00\x00\x01\x00\x44\xfc\x05\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", 100)
rx_len = dev.read(0x81, rx_buff, 400)

# Write to RAM location 0x76210000 value 0x009c00000000 (likely setting bias point to 128 so that all left tail is
# preserved while the mean is as low as possible)
# ContainerLength=16    ContainerType=CommandBlock    Code=0xfd31    TransactionID=6    Payload=1c0d0000 04000000 00000000
dev.write(0x02, b"\x18\x00\x00\x00\x01\x00\x31\xfd\x06\x00\x00\x00\x76\x21\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00", 100)
# ContainerLength=16    ContainerType=DataBlock       Code=0xfd31    TransactionID=6    Payload=08000000
dev.write(0x02, b"\x12\x00\x00\x00\x02\x00\x31\xfd\x06\x00\x00\x00\x00\x9c\x00\x00\x00\x00", 100)
rx_len = dev.read(0x81, rx_buff, 400)

# ServiceModeStop
# ContainerLength=16    ContainerType=CommandBlock    Code=0xfc02    TransactionID=7    Payload=00000000 00000000 00000000
dev.write(0x02, b"\x18\x00\x00\x00\x01\x00\x02\xfc\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", 100)
rx_len = dev.read(0x81, rx_buff, 400)

# CloseSession
# ContainerLength=12    ContainerType=CommandBlock    Code=0x1003    TransactionID=8    Payload=None
dev.write(0x02, b"\x0c\x00\x00\x00\x01\x00\x03\x10\x08\x00\x00\x00", 100)
rx_len = dev.read(0x81, rx_buff, 400)