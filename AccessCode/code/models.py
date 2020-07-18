# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class SmsContent(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    number = models.CharField(db_column='Number', max_length=255, blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=255)  # Field name made lowercase.
    time = models.DateTimeField(blank=True, null=True)
    simnum = models.CharField(db_column='Simnum', max_length=255, blank=True, null=True)  # Field name made lowercase.
    md5 = models.CharField(db_column='Md5', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        # 打印时触发此方法
        return 'id={},content={},time={},simnum={},md5={}'.format(self.id, self.content, self.time, self.simnum, self.md5)

    class Meta:
        managed = True
        db_table = 'sms_content'
