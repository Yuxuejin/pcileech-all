# pcileech-wifi
pcileech-fpga with wireless card emulation

# wifi adapter, but not really
![screenshot](https://i.imgur.com/kL8ozgs.png)

# Usage
This firmware was created for researching purposes only.

# Original project by ekknod based on Ulf Frisk pcileech-fpga project
Original project can be found from https://github.com/ekknod/pcileech-wifi

# Anti-Cheats
This project was created to test current top Anti-Cheats against FPGA approach with minimal effort / knowledge.  

It work on VANGUARD on specific AMD motherboard (no idea why, vanilla firmware or others firmware are blocked here).
Otherwise, VANGUARD block it on 99% of motherboards, when the real device is not blocked.
The real device is blocked without wifi connection tho.


Faceit dosn't have technology to differenciate between the real device and the rogue cloned firmware.
They have decided to totally block this device based on his vid/pid or configuration space.

Blocking an orignal and legal wifi card. Good job to FACEIT.
They also block original and legal capture card like Avermedia GC573.
Good job again.


Credit : ekknod, Ulf Frisk


Update : detected by drvscan as 12/07/2024 :-) I let you figure out alone
drvscan will detect 99% of lazy firmware. this one was a lazy project (aroun 25min to get it done "right")


# 待办清单

配置空间优化
[ ] 分析真实无线网卡的完整配置空间结构（可使用Linux的lspci -xxxx命令）
[ ] 修改src/pcileech_fifo.sv中的配置空间启用选项（将rw[203]设置为1'b0）
[ ] 在ip/pcileech_cfgspace.coe中完善配置空间内容，确保与真实设备一致
[ ] 实现配置空间中的厂商特定扩展区域
设备标识改进
[ ] 收集多个常见无线网卡的VID/PID组合
[ ] 在pcileech_pcie_cfg_a7.sv中实现动态设备ID机制
[ ] 添加设备ID轮换逻辑，避免被固定黑名单阻止
[ ] 确保设备类型、子系统ID等配置与选定的设备ID匹配
设备序列号(DSN)优化
[ ] 修改src/pcileech_pcie_cfg_a7.sv中的DSN生成逻辑
[ ] 实现基于随机算法或特定规则的DSN生成
[ ] 确保生成的DSN符合真实设备的格式规范
PCIe功能完善
[ ] 实现完整的中断处理机制
[ ] 完善PCIe电源管理功能
[ ] 添加MSI/MSI-X中断支持
[ ] 实现PCIe高级错误报告(AER)功能
[ ] 确保PCIe链路训练过程符合规范
BAR(基址寄存器)配置优化
[ ] 分析真实设备的BAR配置
[ ] 在PCIe配置向导中调整BAR大小和类型
[ ] 确保BAR内存映射行为与真实设备一致
[ ] 实现BAR空间的基本读写响应功能
设备行为模拟
[ ] 实现基本的设备初始化序列
[ ] 添加对标准命令集的响应逻辑
[ ] 模拟设备固件版本信息
[ ] 实现基本的设备状态寄存器
防检测机制
[ ] 分析drvscan的--scanpci --advanced测试内容
[ ] 实现针对PCI功能测试的合规响应
[ ] 添加对设备配置空间访问的监控机制
[ ] 实现对异常访问模式的检测和应对
固件更新机制
[ ] 实现模拟的固件更新接口
[ ] 添加固件版本查询功能
[ ] 模拟固件更新过程的状态转换
[ ] 实现固件校验和验证机制