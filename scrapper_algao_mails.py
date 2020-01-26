import requests
import urllib.request
import time
import re
from bs4 import BeautifulSoup
#This is the site map, with all the links to the members pages
main_url = 'https://www.algao.org.uk/sitemap.xml'

response = requests.get(main_url)

main_url_html = BeautifulSoup(response.text, 'xml')

#All links in that site map
main_url_html_links =  main_url_html.findAll('loc')
#links in a list
links_list = list(main_url_html_links)
#At each link we convert it into string, and we delete part of the link, that is wrong
for i in range(len(links_list)):
    links_list[i] = str(links_list[i])
    links_list[i] = links_list[i][5:-6]
    print('link ' + str(i) + ' of ' + str(len(links_list)) + ' done')

#All the member pages links
members_urls = [s for s in links_list if "https://www.ww.algao.org.uk/membership" in s]

for h in range(len(members_urls)):
    members_urls[h] = members_urls[h][0:12] + members_urls[h][15:]
    print('member_url  ' + str(h) + ' of ' + str(len(members_urls)) + ' done')
mails = []


for f in range(len(members_urls)):
    #page of memeber f
    response_member = requests.get(members_urls[f])
    member_html = BeautifulSoup(response_member.text, 'html.parser')
    #all links of member page f
    member_html_links = member_html.find_all('a')
    #as string
    for h in range(len(member_html_links)):
        member_html_links[h] = str(member_html_links[h])
    #Mailtos
    mailtos = [s for s in member_html_links if "mailto" in s]
    #extract adresses
    for j in range(len(mailtos)):
        mailtos[j] = re.search('>(.*)<', mailtos[j]).group(1)
        mails.append(mailtos[j])
    print('mail   ' + str(f) + ' of ' + str(len(members_urls)) + ' done')
file = open("mails.txt", "w+")
for w in range(len(mails)):
    file.write(mails[w] + "\n")
    print('line   ' + str(w) + ' of ' + str(len(mails)) + ' done')
file.close
