completed_developer_day_attendees.csv: completed.csv
	python3 just_developer_days.py < completed.csv > completed_developer_day_attendees.csv.out
	mv completed_developer_day_attendees.csv.out completed_developer_day_attendees.csv

completed.csv: sanitized.csv
	python3 just_completed.py < sanitized.csv > completed.csv.out
	mv completed.csv.out completed.csv

sanitized.csv: exported.csv
	python3 crunchbadges.py < exported.csv > sanitized.csv.out
	mv sanitized.csv.out sanitized.csv
