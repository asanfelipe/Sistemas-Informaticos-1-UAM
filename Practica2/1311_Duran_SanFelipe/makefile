export PGUSER := alumnodb
export PGPASSWORD := alumnodb
export PGDATABASE := si1

reset_db:   
	dropdb si1
	createdb si1
	gunzip -c dump_v1.4.sql.gz | psql

enter_db:
	sudo -u postgres psql si1

run:
	python3 -m app
