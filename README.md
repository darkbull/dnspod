dnspod.cn接口的python封装, 具体api列表,请参考:https://www.dnspod.cn/docs/index.html

调用示例: 

api = DNSApi('email', 'pwd')
# 获取自己在dnspod的域名列表
ret = api.Domain.List()
for domain in ret.domains:
    print domain.name, domain.id
ret = api.Record.List(domain_id = 1739879)
for record in ret.records:
    print record.id, record.name, record.value, record.line.encode('utf-8')
