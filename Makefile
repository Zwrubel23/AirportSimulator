
clean:
	# clear the contents of the SimResults, TicketLog, & FlightLog files from the last run
	> SimResults.txt
	> TicketLog.json
	> FlightLog.json

	# Add the initial brackets to the TicketLog and FlightLog files
	echo "[]" >> TicketLog.json
	echo "[]" >> FlightLog.json

test: 
	make clean

	# Run the file
	python3 Main.py

addlogs:
	git add FlightLog.json TicketLog.json SimResults.txt
