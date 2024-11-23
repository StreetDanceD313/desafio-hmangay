import pika
from lxml import html
import json
import redis
from datetime import datetime
import pika.credentials

import requests

url_base = "http://appasp.sefaz.go.gov.br/Sintegra/Consulta/consultar.asp"
url_consulta = "http://appasp.sefaz.go.gov.br/Sintegra/Consulta/consultar.asp"

params = pika.URLParameters('amqp://teste:123456@localhost:5672/demo-vhost')
connection = pika.BlockingConnection(params)
channel = connection.channel()

r = redis.Redis(host='localhost', port=6379, password='Redis2024', db=0)


def scrap_process(ch, method, properties, body):
    response_base = requests.get(url_base)
    cookies = response_base.headers.get('set-cookie').join('; ')
    print(cookies)
    cnpj = str(body)

    content_body:str = (
        'rTipoDoc=2&' +
        'tDoc=' + cnpj + '&' +
        'tCCE=&' +
        'tCNPJ=&' +
        'tCPF=' + cnpj + '&' +
        'btCGC=Consultar&' +
        'zion.SystemAction=consultarSintegra()&' +
        'zion.OnSubmited= &' +
        'zion.FormElementPosted=zionFormID_1&' +
        'zionPostMethod= &' +
        'zionRichValidator=true')
    
    page = requests.post(url=url_consulta, data = content_body
                         , allow_redirects=True, stream=False, headers={
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'en-US,en;q=0.9',
        'Cache-Control' : 'max-age=0',
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Content-Length' : str(content_body.__len__()),
        'Connection' : 'keep-alive',
        'DNT' : '1',
        'Referer' : 'http://appasp.sefaz.go.gov.br/Sintegra/Consulta/default.html',
        'Upgrade-Insecure-Requests' : '1',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Cookie' : cookies
    })
    print(page.content)

    
    tree = html.fromstring(page.content)
    print(tree)
    results_from_query:list[str] = tree.xpath('//*[@class=\'col box\']/div/text()')
    print(results_from_query)

    if( results_from_query.__len__() > 0):
        join_result = ''
        for found in results_from_query:
            if(join_result != ''):
                join_result += ', '
            join_result = found
        r.set(body, join_result)
        print(join_result)
        
    print('end')
    
    

channel.basic_consume(queue='scrap', on_message_callback=scrap_process, auto_ack=True)
print('Started Consuming')
channel.start_consuming()
