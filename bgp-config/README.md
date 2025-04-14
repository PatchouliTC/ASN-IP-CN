# 用于收取BGP全表的相关配置
- 适用于vultr云服务器,其他能摸全表BGP的可以自行修改
- 基于bird2配置

## vultr服务器需求
1. 建议选择亚洲地区服务器基准配置
2. 低于每月5刀的服务器不提供IPV4,如果确认自己网络/虚拟网络不存在稳定IPV6支持建议换成5刀版本
3. 开启BGP服务记得要求全表

## `bird.conf`变更字段
- `vultr_asn` vultr提供的随机asn
- `vultr_password` vultr提供的asn密码
- `vultr_machine_ipv4` vultr设备v4地址
- `vultr_machine_ipv6` vultr设备v6地址
- `machine_ipv4_route` vultr设备v4路由[可以访问vultr内部ASN地址的路由]
- `machine_ipv6_route` vultr设备v6路由[可以访问vultr内部ASN地址的路由]
- `NIC` vultr设备主网卡名