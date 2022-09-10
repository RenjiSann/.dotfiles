#! /bin/sh

SRC="$(pwd)/vimrc"
DEST="${HOME}/.vimrc"
if [ -L "${DEST}" ]; then
	rm "${DEST}"
fi
ln -sfv -T "${SRC}" "${DEST}"


SRC="$(pwd)/vim"
DEST="${HOME}/.vim"
if [ -L "${DEST}" ]; then
	rm "${DEST}"
fi
ln -sfv -T "${SRC}" "${DEST}"
