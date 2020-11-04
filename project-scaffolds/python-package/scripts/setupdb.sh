export FLASK_APP=cluedo.www
flask db init
flask db stamp head
flask db migrate -m "Initial migration."
flask db upgrade