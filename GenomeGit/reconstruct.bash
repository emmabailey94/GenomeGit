#!bin/bash

cd $1
source="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

python ${source}/reconstruct_parser_v2.py $2
