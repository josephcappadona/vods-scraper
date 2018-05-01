#!/bin/bash

if [ -z "$2" ]
    then
        echo "Usage:  $0 PlAYLIST_NAME PlAYLIST_URL"
        exit 1
fi

NAME=$1
URL=$2
COMMAND='youtube-dl --write-description --write-info-json --write-sub --all-subs --sub-format "srt/best" --write-thumbnail --sleep-interval 1 --retries 30 -o "/media/serverhdd3/$NAME/%(playlist)s/%(title)s.%(ext)s" -f best -ciw "$URL"'

mkdir /media/serverhdd3/"$NAME"
echo '$COMMAND' > /media/serverhdd3/"$NAME"/readme.txt
eval $COMMAND
