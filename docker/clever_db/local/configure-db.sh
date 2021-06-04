#!/bin/bash

export STATUS=1
i=0

while [[ $STATUS -ne 0 ]] && [[ $i -lt 60 ]]; do
	i=$i+1
	/opt/mssql-tools/bin/sqlcmd -t 1 -U sa -P "!Strongpass12345" -Q "select 1" >> /dev/null    
	STATUS=$?
done

if [ $STATUS -ne 0 ]; then 
	echo "Error: MSSQL SERVER took more than thirty seconds to start up."
	exit 1
fi

echo "======= MSSQL SERVER STARTED ========" | tee -a ./config.log
# Run the setup script to create the DB and the schema in the DB
# echo $SA_PASSWORD
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "!Strongpass12345" -d master -i setup.sql

echo "======= MSSQL CONFIG COMPLETE =======" | tee -a ./config.log