import requests
import urllib.request
import time
import re
from bs4 import BeautifulSoup
#open csv file
file = open("algao_members.csv", "w+")
file.write("member_name,member_role,member_mail\n")


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
    print('link ' + str(i+1) + ' of ' + str(len(links_list)) + ' done')

#All the member pages links
members_urls = [s for s in links_list if "https://www.ww.algao.org.uk/membership" in s]

for h in range(len(members_urls)):
    members_urls[h] = members_urls[h][0:12] + members_urls[h][15:]
    print('member_url  ' + str(h+1) + ' of ' + str(len(members_urls)) + ' done')
names = []
rols = []
mails = []



for f in range(len(members_urls)):
    #Delayer of requestes to avoid problems
    t0 = time.time()
    response_member = requests.get(names_urls[f])
    response_delay = time.time() - t0
    print(response_delay)
    print("sec")
    time.sleep(response_delay)
    member_html = BeautifulSoup(response_member.text, 'html.parser')
    #all links of member page f
    member_html_links = member_html.find_all('a')
    #All divs
    member_html_divs = member_html.find_all('div')

    # divs as string
    for h in range(len(member_html_divs)):
        member_html_divs[h] = str(member_html_divs[h])

    #links as string
    for h in range(len(member_html_links)):
        member_html_links[h] = str(member_html_links[h])

    #Extract name
    names = [s for s in member_html_divs if "field-user-name" in s]
    if len(names) == 0:
        member_name = ["no name"]
    else:
        member_name = re.search('content">(.*)</div', names[-1]).group(1)
        member_name = member_name[:-7]

    #extract role
    roles = [s for s in member_html_divs if "field-user-role" in s]
    if len(roles) == 0:
        member_role = ["no rol"]
    else:
        member_role = re.search('content">(.*)</div', roles[-1]).group(1)
        member_role = member_role[:-7]

    #extract mailto
    mailtos = [s for s in member_html_links if "mailto" in s]
    if len(mailtos) == 0:
        member_mail = ["no mail"]
    else:
        member_mail = re.search('>(.*)<', mailtos[0]).group(1)




    #save data on file
    file.write(str(member_name) + "," + str(member_role) + "," + str(member_mail) + "\n")

    print('member   ' + str(f+1) + ' of ' + str(len(members_urls)) + ' done')
file.close
