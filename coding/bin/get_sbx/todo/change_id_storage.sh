#!/bin/bash

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
function __anonymous()
{
    cat <<EOT

** -----------------------------------------------------------------------
**       IAM: ${BASH_SOURCE[0]}
** change_id: Idc138a6bc178a80fa6bec0fcbfe1275a13f38ec1
** directory: .get/
** -----------------------------------------------------------------------

cd .get

[INVALID]
lrwxrwxrwx Idc138a6bc178a80fa6bec0fcbfe1275a13f38ec1 -> 34717

[EXISTS] - change_id/* contains content
-rw-r--r-- change_id/Idc138a6bc178a80fa6bec0fcbfe1275a13f38ec1

[MIA] - reverse mapping 
[[ ! -d gerrit_id/34717 ]]
# ls: cannot access 'gerrit_id/34717': No such file or directory
EOT

    return
}

__anonymous
unset __anonymous

# [EOF]
