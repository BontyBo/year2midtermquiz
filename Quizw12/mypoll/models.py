from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    private = models.BooleanField(default=False)
    havecompany = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    
class Company(models.Model):
    code = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=64)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.name