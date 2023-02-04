#!/usr/bin/python3

#v0.5
############
#To-do List#
############
#Task;Status;Date;Validated?
#Initial build;Done;01-12-2021;Y
#Add argument-based selector;Done;02-12-2021;Y
#Basic error handling;Done;03-12-2021;Y
#Additional If logic;Done;10-12-2021;Y
#Logging capabilities;Done;02-03-2023;Y

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
#load Logging
import logging.handlers
import logging

########
# Vars #
########
tio = TenableIO() # [1] Grabs API Keys automatically from env
#tio = TenableIO('TIO_ACCESS_KEY', 'TIO_SECRET_KEY') #[2]
full_list = []
list_never_scanned = []
list_scanned = []
agent_count = None
key = 'last_scanned'
target_group = 265114 #REQUIRED! Group ID that contains not scanned agents.

#############
# Functions #
#############

def add_agent():
    print("Searching for Agents that never got scanned...")
    try:
        for agent in tio.agents.list(('groups', 'neq', '%s' % target_group)):
            full_list.append(agent)

        # Search for Agents that DO NOT have the dict key "last_scanned" (a.k.a. never got scanned) and dumps their IDs to a new list
        for i in full_list:
            if key not in tio.agents.details(i['id']):
                list_never_scanned.append(i)
            else:
                pass

        # Checks if any agent needs to be added to the unscanned agent group based on the previous step. If not, execution stops
        agent_count = len(list_never_scanned)
        if agent_count == 0:
            print("No Agent update required! Exiting...")
            exit()
        else:
            pass

        print("The following IDs never got scanned:")
        for i in list_never_scanned:
            print("Agent ID:", i['id'], "| Agent Name:", i['name'])

        # Adds every non-scanned agent to an agent group that gets scanned every day
        for x in list_never_scanned:
            print("Adding Agent", x['id'], "(",
                  x['name'], ")", "to group", target_group)
            tio.agent_groups.add_agent(target_group, x['id'])

    except:
        sys.exit("An error has ocurred attempting to add new Agents. Exiting...")


def delete_agent():
    # If an agent belongs to group "Unscanned" and key last_scanned exists, remove agent from group
    print("Searching for Agents that got scanned...")
    try:
        for agent in tio.agents.list(('groups', 'eq', '%s' % target_group)):
            if key in tio.agents.details(agent['id']):
                list_scanned.append(agent)
            else:
                pass

        # Checks if any agent needs to be removed from the unscanned agent group based on the previous step. If not, execution stops
        agent_count = len(list_scanned)
        if agent_count == 0:
            print("No Agent update required! Exiting...")
            exit()
        else:
            pass

        print("The following IDs got scanned already:")
        for i in list_scanned:
            print("Agent ID:", i['id'], "| Agent Name:", i['name'])

        # Deletes every scanned agent belonging to agent group Unscanned
        for i in list_scanned:
            print("Deleting Agent",
                  i['id'], "(", i['name'], ")", "from group", target_group)
            tio.agent_groups.delete_agent(target_group, i['id'])

    except:
        sys.exit("An error has ocurred attempting to delete Agents. Exiting...")

def setup_logging(log_level):
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler("script.log"),
            logging.StreamHandler()
        ])


def main():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--add', action='store_const',
                       help='Adds Nessus Agents to group for scanning', const=add_agent)
    group.add_argument('--delete', action='store_const',
                       help='Deletes Nessus Agents from group if already scanned', const=delete_agent)
    parser.add_argument('--log', choices=['debug', 'info', 'warning', 'error', 'critical'],
                        default='warning', help='Log level')

    args = parser.parse_args()
    log_level = getattr(logging, args.log.upper(), None)
    if not isinstance(log_level, int):
        parser.error("Invalid log level: %s" % args.log)
        sys.exit(1)

    setup_logging(log_level)

    if args.add:
        add_agent()
    elif args.delete:
        delete_agent()
    else:
        pass


main()
