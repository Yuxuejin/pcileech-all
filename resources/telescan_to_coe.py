#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script: TeleScan PE PCIE config space '.tlscan' to Vivado '.coe' file converter.

Args:
    1) source '.tlscan' file path.
    2) destination '.coe` file path.

Format:
https://docs.xilinx.com/r/en-US/ug896-vivado-ip/Using-a-COE-File
"""
import os
import sys
import datetime
import xml.etree.ElementTree


assert len(sys.argv) >= 2, 'Missing argument'
src_path = os.path.normpath(sys.argv[1])
# Default output to ip directory for PCILeech project
if len(sys.argv) >= 3:
    dst_path = os.path.normpath(sys.argv[2])
else:
    dst_path = os.path.normpath("ip/pcileech_cfgspace.coe")

# Load and parse the XML format '.tlscan' file
bs = xml.etree.ElementTree.parse(str(src_path)).find('.//bytes').text
# Make one 8,192 char long hex bytes string
bs = ''.join(bs.split())
assert len(bs) == 8192, f'Expected 8912 character (4096 hex byte) string, got {len(bs):,}!'

# Write out ".coe" file
with open(dst_path, 'w') as fp:
    fp.write(f'; Intel AX200 WiFi 6 PCIe Configuration Space\n')
    fp.write(f'; Converted from "{src_path}" on {datetime.datetime.now()}\n')
    fp.write(f'; Complete 4KB configuration space for accurate AX200 emulation\n')
    fp.write('memory_initialization_radix=16;\nmemory_initialization_vector=\n')

    for y in range(16):
        fp.write(f'\n; {(y * 256):04X}\n')

        for x in range(16):
            # Convert bytes to DWORDs with correct endianness
            dword1 = f"{bs[6:8]}{bs[4:6]}{bs[2:4]}{bs[0:2]}".upper()
            dword2 = f"{bs[14:16]}{bs[12:14]}{bs[10:12]}{bs[8:10]}".upper()
            dword3 = f"{bs[22:24]}{bs[20:22]}{bs[18:20]}{bs[16:18]}".upper()
            dword4 = f"{bs[30:32]}{bs[28:30]}{bs[26:28]}{bs[24:26]}".upper()
            fp.write(f'{dword1},{dword2},{dword3},{dword4},\n')
            bs = bs[32:]

    fp.write(';\n')
