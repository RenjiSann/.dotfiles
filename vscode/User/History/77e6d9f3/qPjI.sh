#! /bin/bash

for FOLDER in exo*
do
    pushd "$FOLDER"
    rm -rf 'alire/' 'obj/' 'bin/' 'config/' "share/*"
    popd
done