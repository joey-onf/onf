#!/bin/bash

## -----------------------------------------------------------------------
## https://askubuntu.com/questions/1452519/what-are-the-services-apt-news-and-esm-cache-and-how-do-i-disable-them
## -----------------------------------------------------------------------
function disable_apt_news()
{
    sudo systemctl mask apt-news.service
    sudo systemctl mask esm-cache.service
    return
}

##----------------##
##---]  MAIN  [---##
##----------------##
readarray -t version < <(lsb_release -sr 2>/dev/null)

case "${version[*]}" in
    *'18.04'*) disable_apt_news ;;
    *)
        echo "[SKIP] $0"
        echo '[SKIP] Update services are only disabled for legacy 18.04 install'
        ;;
esac

# [EOF]
