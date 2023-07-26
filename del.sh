
daydel=$(date +"%Y-%m-%d" -d "$2 day")

find save/$1 -type f -name "*$daydel*_*_.png" -exec rm -rf {} \;

