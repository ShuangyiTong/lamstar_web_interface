from django.db import models

# Create your models here.

class NetworkType(models.Model):
    type_name = models.CharField(max_length=64, primary_key=True, unique=True)
    bin_path = models.CharField(max_length=64)
    cmd_lang = models.CharField(max_length=64)
    cmd_lang_def = models.CharField(max_length=256, null=True)
    tcp_ip_enabled = models.CharField(max_length=5)
    constructing_parameters = models.CharField(max_length=4096)
    

class Network(models.Model):
    internal_id = models.CharField(max_length=64, primary_key=True, unique=True)
    displayed_name = models.CharField(max_length=256, null=True)
    information = models.CharField(max_length=4096, null=True)
    network_type = models.ForeignKey(NetworkType, on_delete=models.CASCADE)
    created_date = models.DateTimeField()
    last_modified = models.DateTimeField()
    def update_by_dict(self, update_dict):

        # create update fields dict default
        update_fields = {}
        for field in update_dict['fields']:
            update_fields[field] = update_dict[field]
        obj, created = self.objects.update_or_create(
            internal_id = update_dict['internal_id'],
            defaults = update_fields,
        )

    
class NetworkLog(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    commands = models.CharField(max_length=65536)
    data_sets = models.CharField(max_length=4096)
    results = models.CharField(max_length=256)

class Database(models.Model):
    internal_id = models.CharField(max_length=64, primary_key=True, unique=True)
    displayed_name = models.CharField(max_length=256, null=True)
    database_type = models.CharField(max_length=64)
    comments = models.CharField(max_length=4096, null=True)
    num_tables = models.IntegerField()
    created_date = models.DateTimeField()
    last_modified = models.DateTimeField()

class Table(models.Model):
    database = models.ForeignKey(Database, on_delete=models.CASCADE)
    internal_id = models.CharField(max_length=64, primary_key=True, unique=True)
    table_name = models.CharField(max_length=256)
    created_date = models.DateTimeField()
    last_modified = models.DateTimeField()
    # first coloumn will be the primary unique key, separate by comma
    fields = models.CharField(max_length=4096)
