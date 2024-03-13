#! /bin/sh

set -ex

if ! which gcovr ; then
    echo "No gcovr installed, aborting"
    exit 1
fi

# Print the coverage percentage
gcovr src/

test -d cov_out/ && rm -rf cov_out/
mkdir cov_out/

# Use our "patched" gcovr that adapts the --cobertura option
# depending on the version used
GCOVR="./scripts/gcovr.sh"
${GCOVR} -o cov_out/cobertura.xml

#
gcovr --html-details -o coverage/coverage.html