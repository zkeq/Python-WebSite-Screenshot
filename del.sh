
daydel=$(date +"%Y-%m-%d" -d "$1 day")

find save/$0 -type f -name "*$daydel*.png" -exec rm -rf {} \; 

