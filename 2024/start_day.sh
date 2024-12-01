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
SOLUTION_NAME="p$DAY.py"
[ -d  $FOLDER_NAME ] && die "Directory $FOLDER_NAME already exists"

mkdir "$FOLDER_NAME"
touch $FOLDER_NAME/example.txt
cp template/solution.py $FOLDER_NAME/$SOLUTION_NAME
echo "created $FOLDER_NAME"
