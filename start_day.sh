#! /usr/bin/env bash
set -eu
die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "1 argument required, $# provided"

DAY=$1
[[ $DAY =~ ^[0-9]+$ ]] || die "Day must be an integer, $DAY provided"
FOLDER_NAME="day_$DAY"
[ -d  $FOLDER_NAME ] && die "Directory $FOLDER_NAME already exists"

mkdir "$FOLDER_NAME"
cp ./template/* "$FOLDER_NAME"
echo "created $FOLDER_NAME"
