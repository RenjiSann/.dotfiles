#! /bin/sh

set -ex

if ! which gcovr ; then
    echo "No gcovr installed, aborting"
    exit 1
fi

# Print the coverage percentage
gcovr src/

test -d coverage/ && rm -rf coverage/
mkdir coverage/

# Use our "patched" gcovr that adapts the --cobertura option
# depending on the version used
GCOVR="./scripts/gcovr.sh"
${GCOVR} -o coverage/cobertura.xml
gcovr --xml-pretty --exclude-unreachable-branches --print-summary -o coverage.xml --root . ${CI_PROJECT_DIR}

#
gcovr --html-details -o coverage/coverage.html