# Foodgram - Вкус момента, разделяемый миром!

Foodgram – это продуктовый помощник. На этом сервисе авторизированные пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд. Для неавторизированных пользователей доступны просмотр рецептов и страниц авторов.

# Адрес: https://foodgram.servemp3.com/recipes/
# Админка: логин - admin, пароль - 123


![Logo](https://lh3.googleusercontent.com/u/0/drive-viewer/AITFw-wayWWs7IQpofSG-atrufty_vM5IN9lpOLSARM6ktwbIuMB9r5za4Y3k1WzlMdvw3FmN-VO1w8xVktBZ-uNaZI-W_Qk7A=w1920-h963)


## Стек технологий

**Клиент:**
React (JavaScript)

**Сервер:** Django (Django REST) + Python 3.9, nginx (веб-сервер), gunicorn (WSGI-сервер), PostgreSQL (база данных)

**Дополнительно:** Docker (контейнеризация)
## Развертывание

Как запустить проект на боевом сервере:

Установить на сервере docker и docker-compose.
Скопировать на сервер файлы docker-compose.yml и default.conf:

```bash
scp docker-compose.yml <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/docker-compose.yml
scp nginx.conf <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/nginx.conf
```
Добавить в Secrets на Github следующие данные:

```bash
DOCKER_PASSWORD= # Пароль от аккаунта на DockerHub
DOCKER_USERNAME= # Username в аккаунте на DockerHub
HOST= # IP удалённого сервера
SSH_KEY= # SSH-key компьютера, с которого будет происходить подключение к удалённому серверу
SSH_PASSPHRASE= # Если для ssh используется фраза-пароль
TELEGRAM_TO= # ID пользователя в Telegram
TELEGRAM_TOKEN= # Токен бота в Telegram
USER= # Логин на удалённом сервере
```
Выполнить команды:

```bash
git add .
git commit -m "Коммит"
git push
```
После этого будут запущены процессы workflow:

- проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest
- сборка и доставка докер-образа для контейнера web на Docker Hub
- автоматический деплой проекта на боевой сервер
- отправка уведомления в Telegram о том, что процесс деплоя успешно завершился
## Устанавливаем и настраиваем внешний NGINX
```bash
# Устанавливаем NGINX
sudo apt install nginx -y
# Запускаем
sudo systemctl start nginx
# Настраиваем firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
# Включаем firewall
sudo ufw enable
# Открываем конфигурационный файл NGINX
sudo nano /etc/nginx/sites-enabled/default
# Полностью удаляем из него все и пишем новые настройки

server {
    listen 80;
    foodgram.servemp3.com;
    
    location / {
        proxy_set_header HOST $host;
        proxy_pass http://127.0.0.1:9001;

    }
}

# Сохраняем изменения и выходим из редактора
# Проверяем корректность настроек
sudo nginx -t
# Запускаем NGINX
sudo systemctl start nginx
```
## Подключаем SSL сертификат
```bash
# Установка пакетного менеджера snap.
# У этого пакетного менеджера есть нужный вам пакет — certbot.
sudo apt install snapd
# Установка и обновление зависимостей для пакетного менеджера snap.
sudo snap install core; sudo snap refresh core
# При успешной установке зависимостей в терминале выведется:
# core 16-2.58.2 from Canonical✓ installed 

# Установка пакета certbot.
sudo snap install --classic certbot
# При успешной установке пакета в терминале выведется:
# certbot 2.3.0 from Certbot Project (certbot-eff✓) installed

# Создание ссылки на certbot в системной директории,
# чтобы у пользователя с правами администратора был доступ к этому пакету.
sudo ln -s /snap/bin/certbot /usr/bin/certbot

# Получаем сертификат и настраиваем NGINX следуя инструкциям
sudo certbot --nginx
# Перезапускаем NGINX
sudo systemctl reload nginx
```
## Импортируем ингредиенты в БД, и создаем учетку Админа

Переходим в директорию и выполняем команды:

```bash
cd foodgram
sudo docker compose -f docker-compose.production.yml exec backend bash
python manage.py import_csv data/ingredients.csv
python manage.py createsuperuser
```
## 🔗 Автор
Александр