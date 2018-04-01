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
        months={"Jan":1,"Feb":2,'Mar':3,"Apr":4,'May':5,'Jun':6,'Jul':7,'Aug':8,"Sep":9,"Oct":10,'Nov':11,'Dec':12}
        request_date=re.search(r'(?P<day>\d+)/(?P<month>\w+)/(?P<year>\d+) (?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+)',string)
        if request_date:
            request_date=datetime.datetime(int(request_date.group('year')),months[request_date.group('month')],int(request_date.group('day')),int(request_date.group('hour')),
                                 int(request_date.group('minute')),int(request_date.group('second')))
            return request_date
        else:
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
                if '.' in path:
                    ingnore=True
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