"""
	A Command-Line Interface to Twitter's REST API and Streaming API.
	-----------------------------------------------------------------
	
	Run this command line script with any Twitter endpoint.  The json-formatted
	response is printed to the console.  The script works with both Streaming API and
	REST API endpoints.

	IMPORTANT: Before using this script, you must enter your Twitter application's OAuth
	credentials in TwitterAPI/credentials.txt.  Log into http://dev.twitter.com to create
	your application.
	
	Examples:

	::
	
		python -u -m TwitterAPI.cli -endpoint search/tweets -parameters q=zzz
		python -u -m TwitterAPI.cli -endpoint statuses/filter -parameters track=zzz
		
	These examples print the raw json response.  You can also print one or more fields
	from the response, for instance the tweet 'text' field, like this:
	
	::
	
		python -u -m TwitterAPI.cli -endpoint statuses/filter -parameters track=zzz -fields text
		
	Documentation for all Twitter endpoints is located at:
		 https://dev.twitter.com/docs/api/1.1
"""

__author__ = "Jonas Geduldig"
__date__ = "June 7, 2013"
__license__ = "MIT"

import argparse
import codecs
import json
import sys
import urllib
import os
import re
#import pyglet
#from ttp import ttp
from .TwitterOAuth import TwitterOAuth
from .TwitterAPI import TwitterAPI


def _search(name, obj):
    """Breadth-first search for name in the JSON response and return value."""
    q = []
    q.append(obj)
    while q:
        obj = q.pop(0)
        if hasattr(obj, '__iter__'):
            isdict = isinstance(obj, dict)
            if isdict and name in obj:
                return obj[name]
            for k in obj:
                q.append(obj[k] if isdict else k)
    else:
        return None


def _to_dict(param_list):
    """Convert a list of key=value to dict[key]=value"""
    if param_list:
        return {
            name: value for (
                name,
                value) in [
                param.split('=') for param in param_list]}
    else:
        return None


if __name__ == '__main__':
    # print UTF-8 to the console
    p = ttp.Parser()	
    try:
        # python 3
        sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
    except:
        # python 2
        sys.stdout = codecs.getwriter('utf8')(sys.stdout)

    parser = argparse.ArgumentParser(
        description='Request any Twitter Streaming or REST API endpoint')
    parser.add_argument(
        '-oauth',
        metavar='FILENAME',
        type=str,
        help='file containing OAuth credentials')
    parser.add_argument(
        '-endpoint',
        metavar='ENDPOINT',
        type=str,
        help='Twitter endpoint',
        required=True)
    parser.add_argument(
        '-parameters',
        metavar='NAME_VALUE',
        type=str,
        help='parameter NAME=VALUE',
        nargs='+')
    parser.add_argument(
        '-fields',
        metavar='NAME',
        type=str,
        help='print a top-level field in the json response',
        nargs='+')
    parser.add_argument(
        '-indent',
        metavar='SPACES',
        type=int,
        help='number of spaces to indent json output',
        default=None)
    args = parser.parse_args()

    try:
        params = _to_dict(args.parameters)
        oauth = TwitterOAuth.read_file(args.oauth)

        api = TwitterAPI(
            oauth.consumer_key,
            oauth.consumer_secret,
            oauth.access_token_key,
            oauth.access_token_secret)
        response = api.request(args.endpoint, params)

        for item in response.get_iterator():
            if 'message' in item:
                print('ERROR %s: %s' % (item['code'], item['message']))
            elif not args.fields:
                print(json.dumps(item, ensure_ascii='False', indent=args.indent))  
            else:
                for name in args.fields:
                    value = _search(name, item)
                    if value:
                        #print('%s: %s' % (name, value))
						#removing characters creating problem in PHP
						value1=re.sub('/','', value)
						#result=p.parse(value,html=False);
						#value1=re.sub('[^A-Za-z0-9]+', ' ', value)
						print('%s: %s' % (name, value))
						value1 = re.sub("(?P<url>https?://[^\s]+)", '', value)
						value2=re.sub('/','', value1)
						print('Playing: %s' % (value2))
						os.system("mplayer {TTS URL}"+urllib.quote_plus(value2)+"{remaining url}")

    except KeyboardInterrupt:
        print('\nTerminated by user')

    except Exception as e:
        print('*** STOPPED %s' % str(e))
