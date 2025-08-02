import re

write_protected_bits_PCIE = (
    "00000f00",  # 1
    "00000010",  # 2
    "ff7f0f00",  # 3
    "00000000",  # 4
    "cb0d00c0",  # 5
    "00000000",  # 6
    "0000ffff",  # 7
    "00000000",  # 8
    "00000000",  # 9
    "00000000",  # 10
    "ff7f0000",  # 11
    "00000000",  # 12
    "bfff2000",  # 13
)

write_protected_bits_PM = (
    "00000000",  # 1
    "00000000",  # 2
)

write_protected_bits_MSI = (
    "0000f104",  # 1
    "03000000",  # 2
    "00000000",  # 3
    "00000000",  # 4
    "00000000",  # 5
    "00000000",  # 6
    "00000000",  # 7
    "ffff0000",  # 8
)

write_protected_bits_MSIX = (
    "000000c0",  # 1
    "00000000",  # 2
    "00000000",  # 3
)

write_protected_bits_VPD = ("00000000",)

write_protected_bits_VSC = (
    "000000ff",  # 1
    "ffffffff",  # 2
    "00000000",  # 3
)

write_protected_bits_PTH = ("00000000",)

write_protected_bits_VSEC = (
    "00000000",  # 1
    "00000000",  # 2
    "ffffffff",  # 3
    "ffffffff",  # 4
)

write_protected_bits_AER = (
    "00000000",  # 1
    "31f0ff07",  # 2
    "31f0ff07",  # 3
    "31f0ff07",  # 4
    "c1f10000",  # 5
    "c1f10000",  # 6
    "40050000",  # 7
    "00000000",  # 8
    "00000000",  # 9
    "00000000",  # 10
    "00000000",  # 11
)

write_protected_bits_DSN = (
    "00000000",  # 1
    "00000000",  # 2
    "00000000",  # 3
)

write_protected_bits_LTR = (
    "00000000",  # 1
    "00000000",  # 2
)

write_protected_bits_L1PM = (
    "00000000",  # 1
    "00000000",  # 2
    "3f00ffe3",  # 3
    "fb000000",  # 4
)

write_protected_bits_PTM = (
    "00000000",  # 1
    "00000000",  # 2
    "00000000",  # 3
    "03ff0000",  # 4
)

CAPABILITY_NAMES = {
    0x01: "power management",
    0x02: "AGP",
    0x03: "VPD",
    0x04: "slot identification",
    0x05: "MSI",
    0x06: "compact PCI hot swap",
    0x07: "PCI-X",
    0x08: "hyper transport",
    0x09: "vendor specific",
    0x0A: "debug port",
    0x0B: "compact PCI central resource control",
    0x0C: "PCI hot plug",
    0x0D: "PCI bridge subsystem vendor ID",
    0x0E: "AGP 8x",
    0x0F: "secure device",
    0x10: "PCI express",
    0x11: "MSI-X",
    0x12: "SATA data/index configuration",
    0x13: "advanced features",
    0x14: "enhanced allocation",
    0x15: "flattening portal bridge",
}

EXTENDED_CAPABILITY_NAMES = {
    0x0001: "advanced error reporting",
    0x0002: "virtual channel",
    0x0003: "device serial number",
    0x0004: "power budgeting",
    0x0005: "root complex link declaration",
    0x0006: "root complex internal link control",
    0x0007: "root complex event collector endpoint association",
    0x0008: "multi-function virtual channel",
    0x0009: "virtual channel",
    0x000A: "root complex register block",
    0x000B: "vendor specific",
    0x000C: "configuration access correlation",
    0x000D: "access control services",
    0x000E: "alternative routing-ID interpretation",
    0x000F: "address translation services",
    0x0010: "single root IO virtualization",
    0x0011: "multi-root IO virtualization",
    0x0012: "multicast",
    0x0013: "page request interface",
    0x0014: "AMD reserved",
    0x0015: "resizable BAR",
    0x0016: "dynamic power allocation",
    0x0017: "TPH requester",
    0x0018: "latency tolerance reporting",
    0x0019: "secondary PCI express",
    0x001A: "protocol multiplexing",
    0x001B: "process address space ID",
    0x001C: "LN requester",
    0x001D: "downstream port containment",
    0x001E: "L1 PM substates",
    0x001F: "precision time measurement",
    0x0020: "M-PCIe",
    0x0021: "FRS queueing",
    0x0022: "Readyness time reporting",
    0x0023: "designated vendor specific",
    0x0024: "VF resizable BAR",
    0x0025: "data link feature",
    0x0026: "physical layer 16.0 GT/s",
    0x0027: "receiver lane margining",
    0x0028: "hierarchy ID",
    0x0029: "native PCIe enclosure management",
    0x002A: "physical layer 32.0 GT/s",
    0x002B: "alternate protocol",
    0x002C: "system firmware intermediary",
}

fixed_section = [
    "00000000",
    "470500f9",
    "00000000",
    "ffff0040",
    "f0ffffff",
    "ffffffff",
    "f0ffffff",
    "ffffffff",
    "f0ffffff",
    "f0ffffff",
    "00000000",
    "00000000",
    "01f8ffff",
    "00000000",
    "00000000",
    "ff000000",
]

writemask_dict = {
    "0x10": write_protected_bits_PCIE,
    "0x03": write_protected_bits_VPD,
    "0x01": write_protected_bits_PM,
    "0x05": write_protected_bits_MSI,
    "0x11": write_protected_bits_MSIX,
    "0x09": write_protected_bits_VSC,
    "0x00A": write_protected_bits_VSEC,
    "0x0001": write_protected_bits_AER,
    "0x0003": write_protected_bits_DSN,
    "0x0018": write_protected_bits_LTR,
    "0x001E": write_protected_bits_L1PM,
    "0x000B": write_protected_bits_PTM,
    "0x0017": write_protected_bits_PTH,
}


def read_cfg_space(file_path):
    # 初始化一个空字典来存储dword映射
    dword_map = {}
    # 打开指定路径的文件并读取内容
    with open(file_path, "r") as file:
        content = file.read()
        # 使用正则表达式查找所有8位的十六进制数
        dwords = re.findall(r"[0-9a-fA-F]{8}", content)
        # 遍历找到的dword并存储到字典中，最多存储1024个
        for index, dword in enumerate(dwords):
            if index < 1024:
                dword_map[index] = int(dword, 16)
    # 返回dword映射字典
    return dword_map


def locate_caps(dword_map):
    # 初始化一个空字典来存储能力
    capabilities = {}

    # 获取能力列表的起始位置
    start = dword_map[0x34 // 4] >> 24
    cap_location = start

    # 遍历能力列表，直到cap_location为0
    while cap_location != 0:
        cap_dword = dword_map[cap_location // 4]
        cap_id = (cap_dword >> 24) & 0xFF
        next_cap = (cap_dword >> 16) & 0xFF

        # 打印找到的能力ID和偏移量
        print(
            f"Found Cap ID: 0x{cap_id:02X}, Start offset: {hex(cap_location)}, Next cap offset: {hex(next_cap)}"
        )
        capabilities[f"0x{cap_id:02X}"] = cap_location
        cap_location = next_cap

    # 扩展能力的起始位置
    ext_cap_location = 0x100
    while ext_cap_location != 0:
        ext_cap_dword = dword_map[ext_cap_location // 4]

        # 将大端字节序转换为小端字节序
        ext_cap_dword_le = int.from_bytes(
            ext_cap_dword.to_bytes(4, byteorder="big"), byteorder="little"
        )
        ext_cap_id = ext_cap_dword_le & 0xFFFF
        next_ext_cap = (ext_cap_dword_le >> 20) & 0xFFF

        # 打印找到的扩展能力ID和偏移量
        print(
            f"Found Ext Cap ID: 0x{ext_cap_id:04X}, Start offset: {hex(ext_cap_location)}, Next cap offset: {hex(next_ext_cap)}"
        )
        capabilities[f"0x{ext_cap_id:04X}"] = ext_cap_location
        ext_cap_location = next_ext_cap

    # 返回能力字典
    return capabilities


def create_wrmask(dwords):
    # 创建一个与dwords长度相同的掩码列表，初始值为"ffffffff"
    return ["ffffffff" for _ in dwords]


def update_writemask(wr_mask, input, start_index):
    # 计算结束索引，确保不超过掩码列表的长度
    end_index = min(start_index + len(input), len(wr_mask))
    # 更新掩码列表中的部分值
    wr_mask[start_index:end_index] = input[: end_index - start_index]
    return wr_mask


def main(file_in, file_out):
    # 读取配置空间文件并转换为字典
    cfg_space = read_cfg_space(file_in)
    # 定位能力并返回能力字典
    caps = locate_caps(cfg_space)

    # 创建初始的写掩码
    wr_mask = create_wrmask(cfg_space)
    # 更新写掩码的固定部分
    wr_mask = update_writemask(wr_mask, fixed_section, 0)

    # 遍历能力字典并更新写掩码
    for cap_id, cap_start in caps.items():
        if cap_id not in writemask_dict:
            print(f"Skipping cap {cap_id} as no writemask defined")
            continue
        section = writemask_dict.get(cap_id)
        cap_start_index = cap_start // 4
        wr_mask = update_writemask(wr_mask, section, cap_start_index)

    # 写入更新后的写掩码到输出文件
    new_line_index = 0
    with open(file_out, "w") as f:
        f.write(f"; {format(new_line_index, 'X').zfill(2) + '00'}\n")
        for i in range(0, len(wr_mask), 4):
            f.write(",".join(wr_mask[i : i + 4]) + ",\n")
            if i >= 64 and (i) % 64 == 0:
                f.write("\n")
                new_line_index += 1
                f.write(f"; {format(new_line_index, 'X').zfill(2) + '00'}\n")


if __name__ == "__main__":
    main("./pcileech_cfgspace.coe", "pcileech_cfgspace_writemask.coe")
