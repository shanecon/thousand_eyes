#!/usr/bin/python
import getpass
import argparse
import sys
import pymongo
from ThousandEyesPY import ThousandEyesPY
from pprint import pprint

__author__ = ['shane@']
__version__ = "Oct 2016"

def get_api_token():
    """Get api token of the user to login with.

    Args: None

    Return:
      Tuple: (password)
    """
    password = getpass.getpass('Api Token: ')
    if len(password) > 6:
        return (password)
    else:
        print('Password entered is less than 8 characters long')
        get_api_token()

def alert_names(active_alerts):
    """Print out alert names or no alerts active

    Args: active_alerts from api

    Return:
      print active alerts or no alerts"""
    if active_alerts['alert']:
        for alert_1 in active_alerts['alert']:
            for alert_2 in alert_1['agents']:
                print alert_2['agentName']
                print alert_2['metricsAtStart']
    else:
        print "No Active Alerts"

def agent_list_out(agent_list_api):
    """ Print out agent list from thousand eyes.

    Args:  agent_list api call

    Return:
      Add output to mongodb thousand_eyes_agent
      print out agent_list api call results"""
    try:
    #  needs a mongodb instance running
        conn = pymongo.MongoClient('10.0.0.0', 27017)
    except pymongo.errors.ConnectionFailure, e:
        print "Could not connect to MongoDB: %s" % e
    db = conn.neteng
    db.drop_collection('thousand_eyes_agent')
    db.thousand_eyes_agent.insert(agent_list_api, check_keys=False)
    pprint(agent_list_api)

def bgp_list_out(bgp_list_api):
    """ Print out bgp list from thousand eyes.                                
                                                                                
    Args:  bgp_list api call                                                  
                                                                                
    Return:                                                                     
      Add output to mongodb thousand_eyes_agent                                 
      print out bgp_list api call results""" 
    try:
    #  needs a mongodb instance running                                         
        conn = pymongo.MongoClient('10.0.0.0', 27017)                        
    except pymongo.errors.ConnectionFailure, e:                                 
        print "Could not connect to MongoDB: %s" % e                            
    db = conn.neteng                                                            
    db.drop_collection('thousand_eyes_bgp')                                   
    db.thousand_eyes_bgp.insert(bgp_list_api, check_keys=False)             
    pprint(bgp_list_api)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Alert details')
    parser.add_argument('user',help='Enter Thousand eyes user name')
    parser.add_argument('-agent_list',help="Optional print out list of agents",
    action="store_true")
    parser.add_argument('-bgp_list',help="Option print out list of bgp agents",
    action="store_true")
    args = parser.parse_args()
    api_password = get_api_token()
    api = ThousandEyesPY(username=args.user, password=api_password)
    if args.agent_list:
        agent_list_api = api.agent_list()
        agent_list_out(agent_list_api)
    elif args.bgp_list:
        bgp_list_api = api.bgp_monitor_list()
        bgp_list_out(bgp_list_api)
    else:
        active_alerts = api.active_alerts()
        alert_names(active_alerts)
