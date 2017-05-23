# what-to-do

# Local setup
Before running shell commands, set the `FLASK_APP` and `FLASK_DEBUG`
environment variables :

    export FLASK_APP=/path/to/manage.py
    export FLASK_DEBUG=1

Then setup the database (sqlite for local dev):

    flask db init
    flask db migrate
    flask db upgrade
    flask run

Then run the following commands to bootstrap your environment :

    git clone https://github.com/bweisel/what-to-do
    cd what-to-do
    pip install -r requirements.txt
    flask run
