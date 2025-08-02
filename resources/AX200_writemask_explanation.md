# AX200 PCIe Configuration Space Write Mask Explanation

## Overview

The `pcileech_cfgspace_writemask.coe` file has been updated to properly reflect the read/write permissions for an Intel AX200 WiFi 6 adapter. This file defines which bits in the PCIe configuration space can be written to (1) and which are read-only (0).

## Key Changes Made

### Standard PCIe Header (0x00-0x3F)

| Offset | Original | Updated | Description |
|--------|----------|---------|-------------|
| 0x00-0x03 | ffffffff | 0000ffc7 | Vendor/Device ID (RO), Command reg (partial RW) |
| 0x04-0x07 | ffffffff | 00000000 | Status reg (RO), Class/Rev ID (RO) |
| 0x08-0x0B | ffffffff | 00000000 | Cache line, latency, header type, BIST (RO) |
| 0x0C-0x0F | ffffffff | 00000000 | Reserved (RO) |
| 0x10-0x13 | ffffffff | fffffff0 | BAR0 (RW except lower 4 bits) |
| 0x14-0x1F | ffffffff | 00000000 | BAR1-5 (RO for AX200) |
| 0x20-0x2B | ffffffff | 00000000 | Cardbus CIS, Subsystem IDs (RO) |
| 0x2C-0x2F | ffffffff | 00000000 | Reserved (RO) |
| 0x30-0x33 | ffffffff | 000000ff | ROM BAR (enable bit writable) |
| 0x34-0x37 | ffffffff | 00000000 | Capabilities pointer (RO) |
| 0x38-0x3B | ffffffff | 000000ff | Interrupt Line (RW), Interrupt Pin (RO) |
| 0x3C-0x3F | ffffffff | 00000000 | Min_Gnt, Max_Lat (RO) |

### Extended Configuration Space (0x40-0xFFF)

- **0x40-0xBF**: All set to read-only (00000000)
- **0xC0-0xFF**: PCIe capabilities with limited write access
  - Power Management: Some control bits writable (0000ff00)
  - PCIe Capability: Device/Link control writable (0000ffff)
- **0x100-0xFFF**: All extended configuration space read-only

## Technical Rationale

### Read-Only Fields
- **Vendor/Device ID**: Hardware identification, never writable
- **Class Code**: Device type classification, fixed
- **Revision ID**: Hardware revision, fixed
- **Subsystem IDs**: Board-level identification, typically fixed
- **BAR Type Bits**: Memory/IO type and addressing mode, fixed

### Writable Fields
- **Command Register (0x04)**: 
  - Bits 0-2: I/O Space, Memory Space, Bus Master Enable
  - Bits 8-10: SERR# Enable, Fast Back-to-Back, Interrupt Disable
- **BAR0 (0x10)**: 
  - Upper 28 bits writable for base address
  - Lower 4 bits read-only (type=0x0C for 64-bit prefetchable)
- **Interrupt Line (0x3C)**: Software-assigned interrupt routing
- **ROM BAR Enable**: Bit 0 controls ROM visibility

### Limited Write Access
- **PCIe Capabilities**: Device and link control registers
- **Power Management**: Power state control bits

## Impact on AX200 Emulation

This write mask ensures:

1. **Realistic Behavior**: Matches real AX200 hardware behavior
2. **Security**: Prevents modification of critical identification fields
3. **Compatibility**: Allows necessary driver configuration
4. **Stability**: Protects fixed hardware characteristics

## Verification

To verify the write mask is working correctly:

1. **Read-only test**: Attempt to write to vendor ID (should fail)
2. **Writable test**: Modify command register (should succeed)
3. **BAR test**: Configure BAR0 base address (should work)
4. **Driver test**: Ensure AX200 drivers can configure the device

## Files Updated

- `ip/pcileech_cfgspace_writemask.coe` - Main write mask file
- `resources/AX200_cfgspace_writemask.coe` - AX200-specific backup

This configuration provides a realistic emulation of Intel AX200 hardware behavior while maintaining compatibility with PCILeech DMA research requirements.
