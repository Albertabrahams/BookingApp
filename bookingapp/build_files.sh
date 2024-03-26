 echo "BUILD START"
 python3.8.9 -m pip install -r requirements.txt
 python3.8.9 manage.py collectstatic --noinput --clear
 echo "BUILD END"