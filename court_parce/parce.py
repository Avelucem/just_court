import os
import threading
from queue import Queue
from bs4 import BeautifulSoup

import requests


court_number = input('Введите код суда:')
last_number = input('Введите код последенего автораспреедления:')
s = requests.Session()
try:
    open(os.path.abspath('dbcase/db_%s.txt' % court_number), 'r', encoding = 'utf-8')
except:
    f = open(os.path.abspath('dbcase/db_%s.txt' % court_number), 'w', encoding='utf-8')
    x = open(os.path.abspath('dbcase/db_stealth_%s.txt' % court_number), 'w', encoding='utf-8')
    y = open(os.path.abspath('download/text_%s.txt' % court_number), 'w', encoding='utf-8')
    f.close()
    x.close()
    y.close()

f_read = open(os.path.abspath('dbcase/db_%s.txt' % court_number), 'r', encoding = 'utf-8')
url_logs = "http://court.gov.ua/logs.php"
empty_url_str = '<h1>Звіти про автоматизований розподіл по справі №:  від 01.01.1970 </h1>'

class Downloader(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
            # Получаем url из очереди
            url = self.queue.get()
            # Скачиваем файл
            self.court(url)
            # Отправляем сигнал о том, что задача завершена
            self.queue.task_done()
    def court(self, url):
        inspector = s.get(url)
        inspector_soup = BeautifulSoup(inspector.content, 'lxml')
        DID = inspector_soup.find(id='did').next_element.split('_')[0]
        header_info = '%s' % inspector_soup.find_all('h1')[-1]
        if header_info != empty_url_str:
            if DID != u'0':
                text_read = open(os.path.abspath('download/text_%s.txt' % court_number), 'a+', encoding='utf-8')
                cookies = {
                    'PHPSESSID': 'dhbol7btr9pfup7s9jh0n0i1b0',
                }
                headers = {
                    'Host': 'court.gov.ua',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                    'Accept': 'text/plain, */*; q=0.01',
                    'Accept-Language': 'ru,en-US;q=0.7,en;q=0.3',
                    'Referer': 'https://court.gov.ua/log_documents/%s/%s/' % (url[0], court_number),
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'max-age=0',
                }
                data = {"doc_ver": "54_2",
                        "did": DID,
                        "ddid": "%s" % court_number}
                response = requests.post('https://court.gov.ua/logs.php', headers=headers, data=data, cookies=cookies)
                prepped = response.text
                text_read.write(url)
                text_read.write(';')
                text_read.write(DID)
                text_read.write(';')
                for index in prepped.split('\r\n')[1:5]:
                    text_read.write(index)
                    text_read.write(';')
                text_read.write('\n')
                text_read.close()
                print('niceeeeeeeeeeeeeeeeeee %s'% url)
            else:
                f = open(os.path.abspath('dbcase/db_stealth_%s.txt' % court_number), 'a+', encoding='utf-8')
                f.write(url.split('/')[-3])
                f.write(';')
                f.write(header_info)
                f.write('\n')
                f.close()
                print('not very nice %s' % url)
        print(url)

def main(urls):
    queue = Queue()
    # Запускаем потом и очередь
    for i in range(20):
        t = Downloader(queue)
        t.setDaemon(True)
        t.start()
    # Даем очереди нужные нам ссылки для скачивания
    for url in urls:
        queue.put(url)
    # Ждем завершения работы очереди
    queue.join()

list_urls = int(last_number)
court_num = int(court_number)

if __name__ == "__main__":
    urls = []
    for links in list(range(list_urls+1, list_urls+1000000)):
        urls.append('http://court.gov.ua/log_documents/%s/%s/' % (links, court_num))
    main(urls)