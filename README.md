# what-to-do

## Local setup
Clone the repo and install the dependencies

    git clone https://github.com/bweisel/what-to-do
    cd what-to-do
    pip install -r requirements.txt

Set some required environment variables:

    export FLASK_APP=/path/to/manage.py
    export SECRET_KEY=this-is-the-local-key
    export FLASK_DEBUG=1

Then setup the database (sqlite for local dev):

    flask db init
    flask db migrate
    flask db upgrade

Then run the server:

    flask run
