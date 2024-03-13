#! /bin/bash

for FOLDER in exo*
do
    pushd "$FOLDER"
    rm -rf 'alire/' 'bin/' 'config/' "share/*"
    popd
done