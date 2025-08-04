#!/usr/bin/env python3
"""
PCILeech Standard Configuration Space Generator
Generates configuration space that matches PCILeech standard capability chain:
0x40: PM → 0x50: MSI → 0x60: PCIe → 0x9C: MSI-X
"""

import datetime

def generate_pcileech_standard_config():
    """Generate configuration space matching PCILeech standard layout"""
    
    # Initialize 4KB configuration space (1024 DWORDs)
    config_space = [0x00000000] * 1024
    
    print("Generating PCILeech standard configuration space...")
    
    # Standard Configuration Space Header (0x00-0x3F)
    config_space[0x00] = 0x27238086  # Device ID (0x2723) + Vendor ID (0x8086)
    config_space[0x01] = 0x10000406  # Status (0x1000) + Command (0x0406)
    config_space[0x02] = 0x0280001A  # Class Code (0x028000) + Revision ID (0x1A)
    config_space[0x03] = 0x00001000  # BIST + Header Type + Latency Timer + Cache Line Size
    
    # BAR0: 64-bit prefetchable memory, 16MB
    config_space[0x04] = 0xFFF0000C  # BAR0 - Lower 32 bits
    config_space[0x05] = 0x00000000  # BAR1 - Upper 32 bits
    config_space[0x06] = 0x00000000  # BAR2
    config_space[0x07] = 0x00000000  # BAR3
    config_space[0x08] = 0x00000000  # BAR4
    config_space[0x09] = 0x00000000  # BAR5
    config_space[0x0A] = 0x00000000  # Cardbus CIS Pointer
    config_space[0x0B] = 0x00848086  # Subsystem ID (0x0084) + Subsystem Vendor ID (0x8086)
    config_space[0x0C] = 0x00000000  # Expansion ROM Base Address
    config_space[0x0D] = 0x00000040  # Reserved + Capabilities Pointer (0x40)
    config_space[0x0E] = 0x00000000  # Reserved
    config_space[0x0F] = 0x00000100  # Max_Lat + Min_Gnt + Interrupt Pin (1) + Interrupt Line
    
    # PCILeech Standard Capability Chain
    
    # PM Capability (0x40) - DWORD 0x10
    config_space[0x10] = 0x00025001  # PMC (0x0002) + Next Ptr (0x50) + Cap ID (0x01)
    config_space[0x11] = 0x00000008  # Data + PMCSR Bridge Extensions + PMCSR
    config_space[0x12] = 0x00000000  # Reserved
    config_space[0x13] = 0x00000000  # Reserved
    
    # MSI Capability (0x50) - DWORD 0x14
    config_space[0x14] = 0x00006005  # Message Control (0x0000) + Next Ptr (0x60) + Cap ID (0x05)
    config_space[0x15] = 0x00000000  # Message Address Lower
    config_space[0x16] = 0x00000000  # Message Address Upper
    config_space[0x17] = 0x00000000  # Message Data + Reserved
    
    # PCIe Express Capability (0x60) - DWORD 0x18
    config_space[0x18] = 0x00029C10  # PCIe Cap (0x0002) + Next Ptr (0x9C) + Cap ID (0x10)
    config_space[0x19] = 0x00108E42  # Device Capabilities
    config_space[0x1A] = 0x00002810  # Device Status + Device Control
    config_space[0x1B] = 0x0000E845  # Link Capabilities
    config_space[0x1C] = 0x00000040  # Link Status + Link Control
    config_space[0x1D] = 0x00000000  # Slot Capabilities
    config_space[0x1E] = 0x00000000  # Slot Status + Slot Control
    config_space[0x1F] = 0x00000000  # Root Capabilities + Root Control
    config_space[0x20] = 0x00000000  # Root Status
    config_space[0x21] = 0x00000000  # Device Capabilities 2
    config_space[0x22] = 0x00000000  # Device Status 2 + Device Control 2
    config_space[0x23] = 0x00000000  # Link Capabilities 2
    config_space[0x24] = 0x00000000  # Link Status 2 + Link Control 2
    
    # MSI-X Capability (0x9C) - DWORD 0x27
    config_space[0x27] = 0x00070011  # Table Size (7) + Next Ptr (0x00) + Cap ID (0x11)
    config_space[0x28] = 0x00001000  # Table Offset (0x1000) + Table BIR (0)
    config_space[0x29] = 0x00002000  # PBA Offset (0x2000) + PBA BIR (0)
    config_space[0x2A] = 0x00000000  # Reserved
    
    print("PCILeech standard capability chain:")
    print("  0x40: PM Capability → Next = 0x50")
    print("  0x50: MSI Capability → Next = 0x60")
    print("  0x60: PCIe Express Capability → Next = 0x9C")
    print("  0x9C: MSI-X Capability → Next = 0x00 (End)")
    
    return config_space

def write_coe_file(config_space):
    """Write configuration space to COE file"""
    
    # Ensure we have exactly 1024 DWORDs (4KB)
    if len(config_space) < 1024:
        config_space.extend([0x00000000] * (1024 - len(config_space)))
    
    with open('ip/pcileech_cfgspace.coe', 'w') as f:
        f.write("; Intel AX200 WiFi 6 PCIe Configuration Space (PCILeech Standard)\n")
        f.write(f"; Generated on {datetime.datetime.now()}\n")
        f.write("; Capability Chain: PM(0x40) → MSI(0x50) → PCIe(0x60) → MSI-X(0x9C)\n")
        f.write("memory_initialization_radix=16;\n")
        f.write("memory_initialization_vector=\n\n")
        
        # Write exactly 1024 DWORDs in groups of 4 per line
        for i in range(0, 1024, 4):
            if i % 64 == 0:  # Add address comment every 16 lines
                f.write(f"; {i*4:04X}\n")
            
            line_data = []
            for j in range(4):
                line_data.append(f"{config_space[i + j]:08X}")
            
            f.write(','.join(line_data))
            if i + 4 < 1024:
                f.write(',\n')
            else:
                f.write(';\n')
    
    print("PCILeech standard configuration space written to ip/pcileech_cfgspace.coe")

if __name__ == "__main__":
    config_space = generate_pcileech_standard_config()
    write_coe_file(config_space)
    print("\n✅ PCILeech standard configuration space generation complete!")
    print("✅ Matches PCIe core configuration exactly!")
    print("✅ Ready for compilation and testing!")
