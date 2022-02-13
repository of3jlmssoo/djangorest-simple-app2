from django.db import models

# Create your models here.


class Chokinbako(models.Model):
    chokinbako_id = models.IntegerField(unique=True, null=False, blank=False)
    chokinbako_name = models.CharField(unique=True, null=False, blank=False, max_length=10)
    chokinbako_value = models.PositiveIntegerField(default=10000)


"""
python manage.py makemigrations chokin
python manage.py sqlmigrate chokin 0001
python manage.py migrate

python manage.py shell
from chokin.models import Chokinbako
Chokinbako.objects.all()

q=Chokinbako(chokinbako_id=1, chokinbako_name='box1', chokinbako_value=20000)
q.save()
q=Chokinbako(chokinbako_id=2, chokinbako_name='box2', chokinbako_value=0)
q.save()
q=Chokinbako(chokinbako_id=3, chokinbako_name='box3', chokinbako_value=10000)
q.save()


q = Chokinbako.objects.get(chokinbako_name='box1')
q.chokinbako_value
q.chokinbako_value=50000
q.save()


"""
