#!/bin/bash

export NAME=$1
export URL=$2
export COMMAND='youtube-dl --write-description --write-info-json --write-sub --all-subs --sub-format "srt/best" --write-thumbnail --sleep-interval 1 --retries 30 -o "/media/serverhdd3/$NAME/%(playlist)s/%(title)s.%(ext)s" -f best -ciw "$URL"'

mkdir /media/serverhdd3/"$NAME"
echo '$COMMAND' > /media/serverhdd3/"$NAME"/readme.txt
eval $COMMAND
