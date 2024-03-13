#! /bin/sh

# Print the coverage percentage
gcovr src/


mkdir cov_out/

# Use our "patched" gcovr that adapts the --cobertura option
# depending on the version used
GCOVR="./script/gcovr.sh"
${GCOVR} -o cov_out/cobertura.xml

#
gcovr --html-details -o cov_out/coverage.html