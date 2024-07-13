#to install requirements 

pip install -r requirements. txt

cd ../front_end 

npm install



#to run celery worker from root folder

celery -A app.celery_instance worker -l info -P solo



#to run celery beat from root folder

celery -A app.celery_instance beat --max-interval 1 -l info

