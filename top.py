import requests
import re
import json
from requests.exceptions import RequestException
import time

#抓取首页
def get_one_page(url):
	try:
		headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
		}
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		return None

#正则提取
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
    	yield{
    		'index':item[0],
    		'image':item[1],
    		'title':item[2].strip(),
    		'actor':item[3].strip()[3:],
    		'time':item[4].strip()[5:],
    		'score':item[5] + item[6]   		
    	}
 

#写入文件
def write_to_file(content):
	with open('result.txt','a',encoding='utf-8') as f:
		f.write(json.dumps(content,ensure_ascii=False) + '\n')


#主函数
def main(offset):
	url = 'http://maoyan.com/board/4?offset=' + str(offset)
	html = get_one_page(url)
	for item in parse_one_page(html):
		print(item)
		write_to_file(item)

if __name__ == '__main__':
	for i in range(10):
		main(offset=i * 10)
		time.sleep(1)
