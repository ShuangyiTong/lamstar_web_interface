import traceback, os, random, string, time

from django.utils import timezone
from .models import NetworkType, Network, Database
from .dbmgr import dbmgr


# Internal processing functions

def process_new_nettype(request):
    name = request.GET.get('type_name')
    exe_path = request.GET.get('exe_path')
    lang = request.GET.get('cmd_lang')
    lang_def = request.GET.get('cmd_lang_def')
    tcp_ip = request.GET.get('tcp_ip')
    cons_para = request.GET.get('cons_para')
    try:
        newtype = NetworkType(type_name=name, bin_path=exe_path, cmd_lang=lang, cmd_lang_def=lang_def, 
                            tcp_ip_enabled=tcp_ip, constructing_parameters=cons_para)
        newtype.save()
    except:
        return traceback.format_exc()
    return 1

def process_new_database(request):
    name = request.GET.get('name')
    type_name = request.GET.get('type_name')
    comments = request.GET.get('comments')
    internal_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    time_string = timezone.now()

    # Interaction with dbmgr
    try:
        dbmgr.establish_connection(type_name, internal_id)
        status = dbmgr.commit(internal_id)
    except:
        return traceback.format_exc()
    if status[0] != 1:
        return status[1]

    # interaction with its own database
    try:
        newdatabase = Database(internal_id=internal_id, displayed_name=name, database_type=type_name, comments=comments,
                              created_date=time_string, last_modified=time_string, num_tables=0)
        newdatabase.save()
    except:
        return traceback.format_exc()
    return 'Successfully create new database'


def delete_network(internal_id):
    network_file = 'main/networks/' + internal_id + '.nn'
    if(os.path.isfile(network_file)):            
        try:
            os.remove(network_file)
        except:
            return 'falied'
    try:
        Network.objects.get(internal_id=internal_id).delete()
    except:
        return 'failed'
    return 'success'

def delete_database(internal_id):
    database_file = 'main/databases/' + internal_id + '.db'
    if(os.path.isfile(database_file)):
        try:
            os.remove(database_file)
        except:
            return 'failed'
    try:
        Database.objects.get(internal_id=internal_id).delete()
    except:
        return 'failed'
    return 'success'

def cmd_update(update_dict):
    if update_dict['category'] == 'db':
        # Check if some fields contains file data
        if update_dict['methology'] == 'indirect':
            for field in update_dict['fields']:
                try:
                    with open(update_dict[field], 'r') as f:
                        data = f.read()
                    update_dict[field] = data
                except:
                    pass

        if update_dict['model'] == 'Network':
            try:
                Network.update_by_dict(Network, update_dict)
            except:
                return traceback.format_exc()
            return 1

    return 'update dict format not recoganized'
