if [ $1 == 'help' ]
then
    while read line; do echo $line; done < shooter.help
elif [ $2 == 'daily' ] || [ $2 == 'weekly' ] || [ $2 == 'monthly' ]
then
    python3 src/screenshot/fialda.py $2
elif [ $2 == '15m' ] || [ $2 == '1h' ] || [ $2 == '1d' ]
then
    python3 src/screenshot/fialda.py $2 $3
else
    echo Wrong commands
fi