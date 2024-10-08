#!/bin/bash

script_name=$1
init_flag=$2
number_of_jobs=$3
input_file=$4

usage() {
    echo -e "Usage:\n$0 <script name> --init <number of processes to be run> <input_file>\n$0 <script name>"
    exit 1
}

if [ "$init_flag" = "--init" ] && [ $# -eq 4 ]; then
    mkdir -p "$script_name"
    mkdir -p "$script_name"/logs
    split -n l/"$number_of_jobs" "$input_file" "$script_name"/x
else
    usage
fi

for split_path in "$script_name"/x??;
do
    f=${split_path: -3:3}
    rye run pypy3 "$script_name".py -p --file "$split_path" > "$script_name"/logs/"$f".log 2>&1 &
done
