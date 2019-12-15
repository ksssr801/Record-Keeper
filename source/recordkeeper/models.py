from __future__ import unicode_literals
from django.db import models

class CommonAttrsModel(models.Model):
    created_at = models.DateTimeField(null=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Person(CommonAttrsModel):
    first_name = models.CharField(max_length=500, null=False)
    last_name = models.CharField(max_length=500, null=False)
    date_of_birth = models.IntegerField()
    gender = models.CharField(max_length=50)

    class Meta:
        unique_together = ('first_name', 'last_name')
        db_table = 'tbl_person'

class PersonStatus(CommonAttrsModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    status_text = models.CharField(max_length=500)

    class Meta:
        db_table = 'tbl_personstatus'

class FormulaFields(CommonAttrsModel):
    formula = models.TextField()
    column_number = models.IntegerField()

    class Meta:
        db_table = 'tbl_formulafields'
