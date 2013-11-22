#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import httplib
import urllib

class BadRequest(httplib.HTTPException):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
        
    def __str__(self):
        return 'state code: %s, reason: %s' % (self.code, self.msg)
        
class DNSApiError(Exception):
    def __init__(self, code, message):
        self.code = int(code)
        self.message = message
    
    def __unicode__(self):
        return u'code: %s, message: %s' % (self.code, self.message)
        
    def __str__(self):
        return self.__unicode__().encode('utf-8')

class DictObject(dict):
    def __init__(self, d):
        dict.__init__(self, d)
    
    def __getattr__(self, attr):
        if attr in self:
            ret = self[attr]
            if type(ret) is dict:
                return DictObject(ret)
            elif type(ret) is list:
                for idx, item in enumerate(ret):
                    if type(item) is dict:
                        ret[idx] = DictObject(item)
            return ret
        
def _post(method, **kwargs):
    assert kwargs and \
            all([key in kwargs for key in ('login_email', 'login_password')])
    kwargs['format'] = 'json'   # only support json response.
    
    utf8 = lambda u: u.encode('utf-8') if type(u) is unicode else str(u)
    kwargs = dict([(utf8(key), utf8(val)) for key, val in kwargs.items()])
    body = urllib.urlencode(kwargs)
    headers = {
            'User-Agent': 'dnspod api/0.0.1a (hi@darkbull.net)',
            'Host': 'dnsapi.cn',
        }
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Content-Length'] = str(len(body))
    
    conn = httplib.HTTPSConnection('dnsapi.cn')
    if not method.startswith('/'):
        method = '/' + method
    conn.request('POST', method, body = body, headers = headers)
    resp = conn.getresponse()
    stat, reason, html = (resp.status, resp.reason, resp.read())
    conn.close()
    if stat != 200:
        raise BadRequest(stat, reason)
    ret = DictObject(json.loads(html))
    stat = ret.status
    if int(stat.code) != 1:
        raise DNSApiError(stat.code, stat.message)
    return ret
    
class DNSApi(object):
    def __init__(self, email, passwd):
        self.email = email
        self.passwd = passwd
        self._attrs = [ ]
        
    def __getattr__(self, attr):
        self._attrs.append(attr)
        return self
        
    def __call__(self, **kwargs):
        kwargs['login_email'] = self.email
        kwargs['login_password'] = self.passwd
        m = '.'.join(self._attrs)
        self._attrs = [ ]
        return _post(m, **kwargs)
        
if __name__ == '__main__':
    pass
    # api = DNSApi('email', 'pwd')
    # ret = api.Domain.List()
    # for domain in ret.domains:
        # print domain.name, domain.id
    
    # ret = api.Record.List(domain_id = 1739879)
    # for record in ret.records:
        # print record.id, record.name, record.value, record.line.encode('utf-8')
    
    # print api.Record.Ddns(domain_id = 1739879, record_id = 12900354, sub_domain = 'www', record_line = u'默认')
    
    # print ret.status.message
    
