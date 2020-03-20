# asana_task

# Документация

1. docker-compose up
2. docker ps
3. docker exec -t -i "id asana_task" bash
4. ./manage.py makemigrations
5. ./manage.py migrate
6. ./manage.py createsuperuser и создать логин и пароль
7. открыт в броузере 0.0.0.0.8000/admin

# как использовать админ панель первый раз

1. добавить токен доступа и активировать
![Иллюстрация к проекту](https://github.com/artush96/images/raw/master/token.png)
![Иллюстрация к проекту](https://github.com/artush96/images/raw/master/aktivacia_tokena.png)
2. добавить Команда (Team gid и Название команды нужно взять из сайта асана)
![Иллюстрация к проекту](https://github.com/artush96/images/raw/master/kamanda.png)
![Иллюстрация к проекту](https://github.com/artush96/images/raw/master/gid_i_name_kamandi.png)
3. перезагрузить Docker
4. открыт в броузере 0.0.0.0.8000 и кликать Get Users (добавляет все пользователи из каманды)
![Иллюстрация к проекту](https://github.com/artush96/images/raw/master/get_users.png)
5. дабавить, изменить и удалить проект
6. дабавить, изменить и удалить задачи









