# -*- makefile -*-

all: try

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
# vlan-args += --prefix 'XGS-PON-X'

# vlan-args += --cidr-count 4
vlan-args += --device    'enp3s01d'
vlan-args += --workflow  'A'

vlan-args += --comment 'onu SCOM000d01c7a'
vlan-args += --cidr '10.11.111.254/24'
vlan-args += --comment 'onu fSCOM00001c8d'
vlan-args += --cidr '10.22.222.254/32' 
vlan-args += --comment 'onu SCOM00019ab7d'
vlan-args += --cidr '10.33.333.254/24'
vlan-args += --comment 'onu SCOMa0301e8d'
vlan-args += --cidr '10.44.444.254/24'

# vlan-args += --cidr '10.54.42.254/24'
# vlan-args += --cidr '10.55.41.254/24'


## ERRS
# vlan-args += --cidr '10.22.500.254/32'
# vlan-args += --cidr '10.22.222.254/500'

#vlan-args += --subnet '11.111'
#vlan-args += --subnet '11.111'
#vlan-args += --subnet '22.222'
#vlan-args += --subnet '33.333'
#vlan-args += --subnet '44.444'

# vlan-args += --workflow DT
# vlan-args += --help
try:
	./vlan.py $(vlan-args)

# [EOF]
