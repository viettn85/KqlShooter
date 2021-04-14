if [ $1 == 'help' ]
then
    while read line; do echo $line; done < kqls.help
elif [ $1 == "screenshot" ]
then
    python3 src/screenshot/vnd.py $2
fi
