custom-scripts/linux/clear-migrations.sh
mysql -p < custom-scripts/linux/reset-database.sql
python manage.py makemigrations
python manage.py migrate