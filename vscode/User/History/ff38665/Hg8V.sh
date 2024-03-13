#! /bin/sh

# Use our "patched" gcovr (the cobertura )
GCOVR="./script/gcovr.sh"

# Print the coverage percentage
${GCOVR} src/

${GCOVR} -o cov_out/cobertura.xml

${GCOVR} --html-details -o cov_out/coverage.html