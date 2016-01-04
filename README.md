##Alba Caeli

Requirements (conda can be replaced by pip as well):

pip install flask
pip install flask-sqlalchemy
pip install sqlalchemy-migrate
pip install flask-login
pip install flask-wtf


Start locally by running:

(source activate flask...)

python db_create.py
python db_fill.py
python run.py

And log in with the username "user"


On pythonanywhere: workon myenv
