#! /bin/sh

set -ex

# Check presence of gcovr binary
if ! which gcovr ;
then
    echo "gcovr not found"
    exit 1
fi

# Check version
X=`gcovr --version | head -n 1`
case "$X" in
    gcovr\ [6-9].*|gcovr\ 5.[!0])
        echo "gcovr version >5.0 detected"
        PARAM="--cobertura"
        break ;;
    *)
        echo "gcovr version <=5.0 detected"
        PARAM="--xml"
        break ;;
esac

# Run Gcovr
exec gcovr ${PARAM} $@
