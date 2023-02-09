#!/usr/bin/python3

#v0.4
############
#To-do List#
############
#Task;Status;Date;Validated?
#Initial build;Done;01-12-2021;Y
#Add argument-based selector;Done;02-12-2021;Y
#Basic error handling;Done;03-12-2021;Y
#Additional If logic;Done;10-12-2021;Y
#Logging capabilities;N/A;xx-xx-xxxx;N

########
# Lib  #
########
#load dotenv lib
from dotenv import load_dotenv
load_dotenv() #Makes system environment variables available to the script. Needed in [1]. Else, use [2]
#load argparse lib
import argparse
#load tenable.io lib https://github.com/tenable/pyTenable
from tenable.io import TenableIO
#load sys module
import sys
########
# Vars #
########
tio = TenableIO() # [1] Grabs API Keys automatically from env
#tio = TenableIO('TIO_ACCESS_KEY', 'TIO_SECRET_KEY') # [2]
full_list = []
list_never_scanned = []
list_scanned = []
agent_count = None
key = 'last_scanned'
target_group = XXXXXX #REQUIRED! Group ID that contains not scanned agents.

#############
# Functions #
#############
def add_agent():
    print("Searching for Agents that never got scanned...")
    try:
        for agent in tio.agents.list(('groups','neq','%s' % target_group)):
            full_list.append(agent['id'])

        #Search for Agents that DO NOT have the dict key "last_scanned" (a.k.a. never got scanned) and dumps their IDs to a new list
        for i in full_list:
            if key not in tio.agents.details(i):
                list_never_scanned.append(i)
            else:
                pass

        #Checks if any agent needs to be added to the unscanned agent group based on the previous step. If not, execution stops
        agent_count = len(list_never_scanned)
        if agent_count == 0:
            print("No Agent update required! Exiting...")
            exit()
        else:
            pass

        print("The following IDs never got scanned:")
        for i in list_never_scanned:
            print(i)


        #Adds every non-scanned agent to an agent group that gets scanned every day
        for x in list_never_scanned:
            print("Adding Agent", x, "to group", target_group)
            tio.agent_groups.add_agent(target_group,x)


    except:
        sys.exit("An error has ocurred attempting to add new Agents. Exiting...")


def delete_agent():
#If an agent belongs to group "Unscanned" and key last_scanned exists, remove agent from group
    print("Searching for Agents that got scanned...")
    try:
        for agent in tio.agents.list(('groups','eq','%s' % target_group)):
            if key in tio.agents.details(agent['id']):
                list_scanned.append(agent['id'])
            else:
                pass

        #Checks if any agent needs to be removed from the unscanned agent group based on the previous step. If not, execution stops
        agent_count = len(list_scanned)
        if agent_count == 0:
            print("No Agent update required! Exiting...")
            exit()
        else:
            pass

        print("The following IDs got scanned already:")
        for i in list_scanned:
            print(i)

        #Deletes every scanned agent belonging to agent group Unscanned
        for i in list_scanned:
            print("Deleting Agent", i, "from group", target_group)
            tio.agent_groups.delete_agent(target_group,i)

    except:
        sys.exit("An error has ocurred attempting to delete Agents. Exiting...")

def main():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--add', action='store_const', help='Adds Nessus Agents to group for scanning', const=add_agent)
    group.add_argument('--delete', action='store_const', help='Deletes Nessus Agents from group if already scanned', const=delete_agent)

    args = parser.parse_args()
    if args.add:
        add_agent()
    elif args.delete:
        delete_agent()
    else:
        pass

main()
