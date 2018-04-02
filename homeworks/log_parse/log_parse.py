# -*- encoding: utf-8 -*-
import collections
import re
import datetime
def parse(
    ignore_files=False,
    ignore_urls=[],
    start_at=None,
    stop_at=None,
    request_type=None,
    ignore_www=False,
    slow_queries=False
):

    counts=collections.Counter()
    times=collections.Counter()
    def get_time(string):
        try:
            request_date=re.search(r'^\[(?P<time>.*)\]', string)
            return datetime.datetime.strptime(request_date.group('time'), "%d/%b/%Y %H:%M:%S")
        except:
            return None
    def get_code_and_time(string):
        result=re.search(r'(?P<response_code>\d+) (?P<response_time>\d+)$',string)
        if result:
            return result.groups()
        else:
            return (None,None)
    def get_params(string):
        result=re.search(r'"(\w+) (.+) (.+)"', string)
        if result:
            return result.groups()
        else:
            return (None,None,None)
        
    file = open('log.log','r')
    text=file.readlines()
    file.close()
    
    for string in text:
        ignore=False
        request_date=get_time(string)
        response_code, response_time = get_code_and_time(string)

        requesttype, request, protocol = get_params(string)

        if request:
            scheme,host,path,query,fragment=re.search(r'(?P<scheme>\w+)://(?P<host>[^/]*)(?P<path>[^?]+)*(?P<query>\?[^#]+)*(?P<fragment>#\w+)*',request).groups()
            if ignore_files:
                if re.search(r'\.(\w+)$', path) and query is None and fragment is None:
                    ignore=True
            if request_type:
                if request_type != requesttype:
                    ignore=True
            if start_at:
                if get_time(start_at)>request_date:
                    ignore = True
            if stop_at:
                if get_time(stop_at)<request_date:
                    ignore = True
            for i in ignore_urls:
                if i == path:
                    ignore=True
                    break
            if ignore_www:
                host=re.search(r'(www.)*(?P<without_www>.+)',host).group('without_www')
        else:
            ignore = True
        if not ignore:
            times[host+path]+=int(response_time)
            counts[host+path]+=1
    for key,value in counts.items():
        times[key]//=counts[key]
    if slow_queries:
        return [i[1] for i in times.most_common(5)]
    else:
        return [i[1] for i in counts.most_common(5)]