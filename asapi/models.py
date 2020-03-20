import json
import requests
from django.db import models


class ASUser(models.Model):
    as_user_gid = models.BigIntegerField()
    name = models.CharField(max_length=50, db_index=True, verbose_name='Пользовател')

    class Meta:
        verbose_name = 'Пользовател'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name




class Team(models.Model):
    team_gid = models.IntegerField()
    title = models.CharField(max_length=50, db_index=True, verbose_name='Название команды')
    member_list = models.ManyToManyField('ASUser', verbose_name='Список участников')

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команди'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        team_user_list = base_url + 'teams/' + str(self.team_gid) + '/users'
        r = requests.get(team_user_list, headers=headers)
        data = json.loads(r.text)
        team_list = []
        for t in data['data']:
            team_list.append(t['gid'])
        super(Team, self).save(*args, **kwargs)
        user = ASUser.objects.filter(as_user_gid__in=team_list)
        self.member_list.add(*user)


class Project(models.Model):
    project_gid = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, db_index=True, verbose_name='Имя проекта')
    member_list = models.ManyToManyField('ASUser', verbose_name='Список участников')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекти'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            pj = Project.objects.get(id=self.id)
            if pj is not None:
                options = {
                    "data": {
                        "archived": "false",
                        "color": "light-green",
                        "default_view": "list",
                        "name": self.name
                    }
                }
                requests.put(project_list_url + str(self.project_gid), headers=headers_1, json=options)
        except:
            options = {
                "data": {
                    "archived": "false",
                    "color": "light-green",
                    "default_view": "list",
                    "name": self.name,
                    "workspace": "1166632925114028"
                }
            }
            requests.post(project_list_url, headers=headers_1, json=options)
            r = requests.get(project_list_url, headers=headers)
            data = json.loads(r.text)
            project_list = []
            for p in data['data']:
                project_list.append(p['gid'])
            try:
                p_gid = project_list[-1]
            except:
                p_gid = 1
            self.project_gid = p_gid

        super(Project, self).save(*args, **kwargs)
        user = ASUser.objects.filter(id__in=self.member_list.all())
        self.member_list.add(*user)

    def delete(self, *args, **kwargs):
        requests.delete(project_list_url + str(self.project_gid), headers=headers, json=options_delete)
        super(Project, self).delete(*args, **kwargs)


class Tasks(models.Model):
    task_gid = models.IntegerField(blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='Проект')
    description = models.TextField(max_length=5000, verbose_name='Описание задачи')
    task_completion = models.DateField(verbose_name='Дата завершения')
    performer = models.ForeignKey('ASUser', on_delete=models.CASCADE, verbose_name='Назначенный исполнитель')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        try:
            tk = Tasks.objects.get(id=self.id)
            if tk is not None:
                options = {
                    "data": {
                        "completed": "false",
                        "assignee": str(self.performer.as_user_gid),
                        "due_on": str(self.task_completion),
                        "name": "Django Task-updated",
                        "notes": self.description
                    }
                }
                requests.put(task_url + str(self.task_gid), headers=headers_1, json=options)
        except:
            options = {
                "data": {
                    "completed": "false",
                    "assignee": str(self.performer.as_user_gid),
                    "due_on": str(self.task_completion),
                    "name": "Django Task",
                    "notes": self.description,
                    "projects": [
                        str(self.project.project_gid)
                    ],
                    "workspace": "1166632925114028"
                }
            }
            requests.post(task_url, headers=headers_1, json=options)
            r = requests.get(project_list_url + str(self.project.project_gid) + '/tasks', headers=headers)
            data = json.loads(r.text)
            task_list = []
            for t in data['data']:
                task_list.append(t['gid'])
            try:
                t_gid = task_list[0]
            except:
                t_gid = 1
            self.task_gid = t_gid

        super(Tasks, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        requests.delete(task_url + str(self.task_gid), headers=headers, json=options_delete)
        super(Tasks, self).delete(*args, **kwargs)


class AccesToken(models.Model):
    token = models.CharField(max_length=50, verbose_name='Токен доступа')
    active_token = models.BooleanField(verbose_name='Активный токен')

    class Meta:
        verbose_name = 'Токен доступа'
        verbose_name_plural = 'Токени доступа'

    def __str__(self):
        return self.token


base_url = 'https://app.asana.com/api/1.0/'
task_url = base_url + 'tasks/'
project_list_url = base_url + 'projects/'

try:
    token = AccesToken.objects.get(active_token=True)
    bearerToken = 'Bearer ' + token.token
except:
    token = ''
    bearerToken = 'Bearer ' + token

headers = {
    'Content-Type': 'application/json',
    'Authorization': bearerToken,
}

headers_1 = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': bearerToken,
}

options_delete = {
    "data": {}
}
