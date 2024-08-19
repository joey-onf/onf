# Broadband AMI Installer

## Intent

Given a base ubuntu image scripts in the ami/ directory will install
packages and configure resources creating an ED2 instance that will
be usable as a Broadband build node for jenkins.

## Hierarchy

| subdir | description |
| ------ | ----------- |
| ami/      | Scripts used to configure packages or system resources       |
| packages/ | A list of OS packages to install                             |
| users/    | Scripts used to create users and assign uid/guid for jenkins |




