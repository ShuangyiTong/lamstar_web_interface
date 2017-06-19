import os, time
from multiprocessing import Process
from .models import NetworkType

class NetworkMgr:
    def __init__(self):

        try:
            os.system('rm -r main/temp')
            os.mkdir('main/temp')
        except:
            print('remove temp folder failed')

        # A dict of (running networks internal id : timestamp) 
        self.running_networks = {}
        # A dict of (timestamp : process object)
        self.running_processes = {}
        # To be joined, timestamp list
        self.to_be_joined = []

    def send_commands_by_script(self, commands):

        # script file name
        temp_script = commands[0][1] + '-' + str(time.time()).split('.')[0] + '.__script__'

        # generate script file
        with open('main/temp/' + temp_script, 'w') as f:
            for command in commands:
                f.write(command[2]+'\n')

        # shell command
        shell = NetworkType.objects.get(type_name=commands[0][0]).bin_path + ' main/temp/' + temp_script

        # create process with shell command
        p = Process(target=os.system, args=(shell,))
        p.start()
        timestamp = str(time.time())
        self.running_networks[commands[0][1]] = timestamp
        self.running_processes[timestamp] = p
        self.to_be_joined.append(timestamp)
        return

    # commands is a list of (type_name, internal id, command)
    # returns [status code, message]
    def send_commands(self, commands):

        exit_codes = []

        # group commands based on internal id
        internal_ids = set(map(lambda x:x[1], commands))
        grouped_commands = [[y for y in commands if y[1]==x] for x in internal_ids]

        # clear to be joined
        self.to_be_joined = []

        # start processes
        for same_network_command in grouped_commands:
            self.send_commands_by_script(same_network_command)

        # join processes
        for timestamp in self.to_be_joined:
            self.running_processes[timestamp].join()
            exit_codes.append(self.running_processes[timestamp].exitcode)
            # remove this process from running networks and processes
            del self.running_processes[timestamp]
            for key in list(self.running_networks.keys()):
                if self.running_networks[key] == timestamp:
                    del self.running_networks[key]

        # collect status
        status_lst = []
        for exit_code in exit_codes:
            print(exit_code)
            if exit_code != 0:
                status_lst.append(exit_code)

        # return msg
        if status_lst==[]:
            return [1, 'All messages have been processed successfully']
        else:
            return [0, 'exit code: ' + ' '.join(status_lst)]

netmgr = NetworkMgr()