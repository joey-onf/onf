#!/bin/bash

declare -a pkgs=()


curl -o helm-v3.15.3-linux-amd64.tar.gz https://get.helm.sh/helm-v3.15.3-linux-amd64.tar.gz
curl -o 'helm-v3.5.2-linux-amd64.tar.gz' --url https://get.helm.sh/helm-v3.5.2-linux-amd64.tar.gz
