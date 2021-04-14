if [ $1 == 'help' ]
then
    while read line; do echo $line; done < shooter.help
elif [ $1 == 'daily' ] || [ $1 == 'weekly' ] || [ $1 == 'monthly' ]
then
    python3 src/screenshot/fialda.py $1
elif [ $1 == '15m' ] || [ $1 == '1h' ] || [ $1 == '1d' ]
then
    python3 src/screenshot/fialda.py $1 $2
else
    echo Wrong commands
    fi
fi
