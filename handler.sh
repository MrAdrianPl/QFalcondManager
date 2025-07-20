#!/bin/bash
PARAM=$1

if [ "$PARAM" = "--setup" ]; then 
    "$APPDIR/usr/bin/python3" "$APPDIR/usr/src/qfsetup.py"
elif [ "$PARAM" = "--version" ]; then 
    echo $CAPPVERSION
elif [ "$PARAM" = "--help" ]; then
    echo "--setup sets profiles folder and grants correct permissions to it"
    echo "--version displays version"
    echo "--help will display this prompt"
    echo "no parameters will start profile manager"
else 
    "$APPDIR/usr/bin/python3" "$APPDIR/usr/src/qfmain.py"
fi