import random, string, time
from django.utils import timezone

from .networkmgr import netmgr
from .internal import cmd_update
from .models import NetworkType, Network

delimiter = ' wan'

def create_network(param_dict, immediate):

    # Extract dict data binding to stack variables
    save_name = param_dict.get('save_name')
    type_name = param_dict.get('type_name')

    # Extract network creation argument
    argc = param_dict.get('argc')
    commands = []
    newcommand = 'newnet '
    for i in range(argc):
        newcommand += (param_dict.get('arg' + str(i)) + " ")
    newcommand += delimiter

    # We give a special internal_id for this kind of operation to identify what kind of network
    temp_id = ''.join(str(ord(c)) for c in type_name)

    # append create command to command list, for details see .networkmgr.py
    commands.append([type_name, temp_id, newcommand])

    # Detailed explanation see http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
    internal_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(25))

    # append save command
    newcommand = ('savenet main/networks/' + internal_id + ".nn " + delimiter)
    commands.append([type_name, temp_id, newcommand])

    time_string = timezone.now()

    # create update model dictionaries
    update_dict = {
        'category' : 'db',
        'model' : 'Network',
        'internal_id' : internal_id,
        'methology' : 'direct',
        'fields' : ['displayed_name', 'network_type', 'created_date', 'last_modified'],
        'displayed_name' : save_name,
        'network_type' : NetworkType.objects.get(type_name=type_name),
        'created_date' : time_string,
        'last_modified' : time_string
    }

    # send this command if this is immediate operation, else return command list
    if immediate:
        status = netmgr.send_commands(commands)
        if status[0]==1:
            if cmd_update(update_dict)==1:
                return 'Successfully created new netowrk with id - ' + internal_id
            else:
                return 'Network created but DB update unknown error'
        else:
            return status[1]
    else:
        return [commands, [update_dict]]

def refresh_status(cmd_dict, immediate):
    commands = []

    # required parameters
    internal_id = cmd_dict['internal_id']
    type_name = Network.objects.get(internal_id=internal_id).network_type.type_name

    # readnet
    newcommand = 'readnet main/networks/' + internal_id + '.nn' + delimiter
    commands.append([type_name, internal_id, newcommand])

    return_file = 'main/temp/' + internal_id + '-' + str(time.time()).split('.')[0] + '__response__.json'
    newcommand = 'status-json ' + return_file + delimiter
    commands.append([type_name, internal_id, newcommand])

    update_dict = {
        'category' : 'db',
        'model' : 'Network',
        'internal_id' : internal_id,
        'methology' : 'indirect',
        'fields' : ['information'],
        'information' : return_file
    }

    if immediate:
        status = netmgr.send_commands(commands)
        # if successful
        if status[0] == 1:
            if cmd_update(update_dict)==1:
                return 1
            else:
                return 'Information retrived but DB update unknown error'
        # not successful
        else:
            return 'Error in send commands'
    else:
        return [commands, [update_dict]]


def interp(cmd_dict, immediate):
    cmd = cmd_dict.get('cmd')
    if cmd=='newnet':
        return create_network(cmd_dict, immediate)
    if cmd=='refresh-status':
        return refresh_status(cmd_dict, immediate)

    return "Unknown command"

class CmdPool:
    def __init__(self):
        self.pool = []
    def queue_command(self, to_queue=True, cmd_dict=None):
        if cmd_dict.get('cmd')==None:
            return 'No command found in passing dict, command ignored'
        elif to_queue:
            self.pool.append(cmd_dict)
            return 'Added to queue'
        else:
            return interp(cmd_dict, True)

cmd_pool = CmdPool()