# onf/voltha

vlan.py - A helper script used to generate vlan and dhcp configs for XGSPON testing.

```
./vlan.py                       \
  --device 'enp3s01d'           \
  --workflow  'A'               \
  --comment 'onu SCOM000d01c7a' \
  --cidr '10.11.111.254/24'

# [ACT]: onu SCOM000d041c7a
ip link add link enp3s01d name enp3s01d.11 type vlan id 11
ip link set enp3s01d.11 up
ip link add link enp3s01d.11 name enp3s01d.11.111 type vlan id 111
ip link set enp3s01d.11.111 up
ip addr add 10.11.111.254/24 dev enp3s01d.11.111
# [FIN]: onu SCOM000d01c7a
```
