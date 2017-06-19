import json, os, traceback

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse

from .models import Network, NetworkLog, NetworkType, Database, Table
from .networkmgr import netmgr
from .cmdpool import cmd_pool
from .internal import process_new_nettype, process_new_database, delete_network, delete_database
from .dbmgr import active_connections, close_connection

# utility functions

def sizeof_fmt(num, suffix='B'):
    for unit in [' ',' Ki',' Mi',' Gi',' Ti',' Pi',' Ei',' Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, ' Yi', suffix)

# AJAX request 

def ajax_NewTypeOfNetwork(request):
    success = process_new_nettype(request)
    info = {
        'success' : success
    }
    return JsonResponse(info)

def ajax_RequestNetworkTypeInfo(request):
    requested_type = request.GET.get("type_name")
    parameters = (get_object_or_404(NetworkType, type_name=requested_type)).constructing_parameters.split(',')
    context = {'parameters' : parameters}
    return render(request, 'main/div/create_network_form.html', context)

def ajax_CreateNetwork(request):

    # Command name
    cmd_dict = {'cmd' : 'newnet'}

    # Necessary names
    cmd_dict['type_name'] = request.GET.get('type_name')
    cmd_dict['save_name'] = request.GET.get('name')

    # Extract number of network creation arguments
    argc = int(request.GET.get('argc'))
    cmd_dict['argc'] = argc
    for i in range(argc):
        key = 'arg' + str(i).strip()
        key_in_request = 'param_' + str(i).strip()
        cmd_dict[key] = request.GET.get(key_in_request)

    # Determine if command is immediate
    if request.GET.get("to_queue")=='on':
        status = cmd_pool.queue_command(to_queue=True, cmd_dict=cmd_dict)
    else:
        status = cmd_pool.queue_command(to_queue=False, cmd_dict=cmd_dict)

    # retuen a json status message
    info = {
        'status' : status
    }
    return JsonResponse(info)

def ajax_CreateDatabase(request):
    status = process_new_database(request)
    info = {
        'status' : status
    }
    return JsonResponse(info)

def ajax_NetworkDetailsDashboard(request):
    request_id = request.GET.get('internal_id')
    json_data = (get_object_or_404(Network, internal_id=request_id)).information
    if json_data != None:
        json_dict = json.loads(json_data)
    else:
        json_dict = {
            'Error' : 'Network information is empty, if the network was just created, press "refresh status" to get information',
        }

    try:
        network_file = 'main/networks/' + request_id + '.nn'
        size = sizeof_fmt(os.stat(network_file).st_size)
    except:
        size = 'Network file not found!'

    context = {
        'json_dict' : json_dict,
        'internal_id' : request_id,
        'size' : size,
    }
    return render(request, 'main/div/network_details_dashboard.html', context)

def ajax_DatabaseDetails(request):
    request_id = request.GET.get('internal_id')
    q_database = get_object_or_404(Database, internal_id=request_id)

    try:
        dbfile = 'main/databases/' + request_id + '.db'
        size = sizeof_fmt(os.stat(dbfile).st_size)
    except:
        size = 'Database file not found!'

    context = {
        'database' : q_database,
        'size' : size,
    }
    return render(request, 'main/div/database_details.html', context)

def ajax_RefreshNetworkInfo(request):
    cmd_dict = { 
        'cmd': 'refresh-status',
        'internal_id': request.GET.get('internal_id')
    }
    status = cmd_pool.queue_command(to_queue=False, cmd_dict=cmd_dict)
    return ajax_NetworkDetailsDashboard(request)

def ajax_DeleteNetwork(request):
    internal_id = request.GET.get('internal_id')
    status = delete_network(internal_id)
    info = {
        'status' : status
    }
    return JsonResponse(info)

def ajax_DeleteDB(request):
    internal_id = request.GET.get('internal_id')
    status = delete_database(internal_id)
    info = {
        'status' : status,
    }
    return JsonResponse(info)

def ajax_CloseDB(request):
    internal_id = request.GET.get('internal_id')
    try:
        status = close_connection(internal_id)
    except:
        status = 'failed'

    if status[0] == 1:
        status = 'success'
    else:
        status = 'failed'
        
    info = {'status' : status}
    return JsonResponse(info)

def ajax_TableList(request):
    internal_id = request.GET.get('internal_id')
    q_database = get_object_or_404(Database, internal_id=internal_id)
    all_tables = Table.objects.filter(database__exact=q_database)
    context = {
        'all_tables' : all_tables,
        'db_id' : q_database.internal_id,
    }
    return render(request, 'main/div/table_list_browsing.html', context)

# html response

def DashboardView(request):
    all_networks = Network.objects.all()
    context = {
        'all_networks' : all_networks,
        'running_networks' : netmgr.running_networks,
        'all_network_types' : NetworkType.objects.all()
    }
    return render(request, 'main/dashboard.html', context)

def GeneralSettingView(request):
    context = {}
    return render(request, 'main/general_settings.html', context)

def NettypeSettingsView(request):
    context = {'all_network_types' : NetworkType.objects.all()}
    return render(request, 'main/nettype_settings.html', context)

def DatabasesBrowsingView(request):
    all_databases = Database.objects.all()
    active_databases = active_connections()

    context = {
        'all_databases' : all_databases,
        'active_connections' : active_databases
    }
    return render(request, 'main/databases_browsing.html', context)