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


disable_apt_news

# [EOF]
