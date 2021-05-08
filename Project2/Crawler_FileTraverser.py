

import requests
import requests.exceptions
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque
import re
import sys
import os
import subprocess
import argparse
import urllib
import json
import pickle
import time
import bs4

def crawler(domain, ofile, mute):
    try:
        # a queue of urls to be crawled
        new_urls = deque([domain])
        # a set of urls that we have already crawled
        processed_urls = set()
        # a set of domains inside the target website
        local_urls = set()
        # a set of domains outside the target website
        foreign_urls = set()
        # a set of broken urls
        broken_urls = set()
        log=[]
        # process urls one by one until we exhaust the queue
        while len(new_urls):

            # move next url from the queue to the set of processed urls
            url = new_urls.popleft()
            processed_urls.add(url)
            # get url's content
            print("Processing %s" % url)
            if url not in log:
                log.append(url)
                try:
                    response = requests.head(url)
                except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
                    # add broken urls to it's own set, then continue
                    broken_urls.add(url)
                    continue

                if 'content-type' in response.headers:
                    content_type = response.headers['content-type']
                    if not 'text/html' in content_type:
                        continue

                try:
                    response = requests.get(url)
                except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
                    # add broken urls to it's own set, then continue
                    broken_urls.add(url)
                    continue
            else:
                break
            
            # extract base url to resolve relative links
            parts = urlsplit(url)
            base = "{0.netloc}".format(parts)
            strip_base = base.replace("www.", "")
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            path = url[:url.rfind('/')+1] if '/' in parts.path else url

            # create a beutiful soup for the html document
            soup = BeautifulSoup4(response.text, "lxml")

            for link in soup.find_all('a'):
                # extract link url from the anchor
                anchor = link.attrs["href"] if "href" in link.attrs else ''

                if anchor.startswith('/'):
                    local_link = base_url + anchor
                    local_urls.add(local_link)
                elif strip_base in anchor:
                    local_urls.add(anchor)
                elif not anchor.startswith('http'):
                    local_link = path + anchor
                    local_urls.add(local_link)
                else:
                    foreign_urls.add(anchor)

            for i in local_urls:
                if not i in new_urls and not i in processed_urls:
                    new_urls.append(i)

        print()
        if mute is False:
            if ofile is not None:
                return report_file(ofile, processed_urls, local_urls, foreign_urls, broken_urls)
            else:
                return report(processed_urls, local_urls, foreign_urls, broken_urls)
        else:
            if ofile is not None:
                return mute_report_file(ofile, local_urls)
            else:
                return mute_report(local_urls)
    
    except KeyboardInterrupt:
        parts = urlsplit(url)
        base = "{0.netloc}".format(parts)
        strip_base = base.replace("www.", "")
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        # create a beutiful soup for the html document
        soup =  BeautifulSoup(response.text, "lxml")

        for link in soup.find_all('a'):
            # extract link url from the anchor
            anchor = link.attrs["href"] if "href" in link.attrs else ''

            if anchor.startswith('/'):
                local_link = base_url + anchor
                local_urls.add(local_link)
            elif strip_base in anchor:
                local_urls.add(anchor)
            elif not anchor.startswith('http'):
                local_link = path + anchor
                local_urls.add(local_link)
            else:
                foreign_urls.add(anchor)

        for i in local_urls:
            if not i in new_urls and not i in processed_urls:
                new_urls.append(i)

    print()
    if mute is False:
        if ofile is not None:
            return report_file(ofile, processed_urls, local_urls, foreign_urls, broken_urls)
        else:
            return report(processed_urls, local_urls, foreign_urls, broken_urls)
    else:
        if ofile is not None:
            return mute_report_file(ofile, local_urls)
        else:
            return mute_report(local_urls)
        sys.exit()


def limit_crawler(domain, ofile, limit, mute):
    try:
        # a queue of urls to be crawled
        new_urls = deque([domain])
        # a set of urls that we have already crawled
        processed_urls = set()
        # a set of domains inside the target website
        limit_urls = set()
        # a set of domains outside the target website
        limit_urls = set()
        # a set of broken urls
        broken_urls = set()

        # process urls one by one until we exhaust the queue
        while len(new_urls):

            # move next url from the queue to the set of processed urls
            url = new_urls.popleft()
            processed_urls.add(url)
            # get url's content
            print("Processing %s" % url)
            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
                # add broken urls to it's own set, then continue
                broken_urls.add(url)
                continue

         # extract base url to resolve relative links
        parts = urlsplit(url)
        base = "{0.netloc}".format(parts)
        strip_base = base.replace("www.", "")
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        # create a beutiful soup for the html document
        soup = BeautifulSoup(response.text, "lxml")

        for link in soup.find_all('a'):
            # extract link url from the anchor
            anchor = link.attrs["href"] if "href" in link.attrs else ''
            print(anchor)

            if limit in anchor:
                limit_urls.add(anchor)
            else:
                pass

        for i in limit_urls:
            if not i in new_urls and not i in processed_urls:
                new_urls.append(i)

        print()
        if mute is False:
            if ofile is not None:
                return limit_report_file(limit, ofile, processed_urls, limit_urls, broken_urls)
            else:
                return limit_report(limit, processed_urls, limit_urls, broken_urls)
        else:
            if ofile is not None:
                return limit_mute_report_file(limit, ofile, limit_urls)
            else:
                return limit_mute_report(limit, limit_urls)

    except KeyboardInterrupt:
        sys.exit()


def limit_report_file(limit, ofile, processed_urls, limit_urls, broken_urls):
    with open(ofile, 'w') as f:
        print(
            "--------------------------------------------------------------------", file=f)
        print("All found URLs:", file=f)
        for i in processed_urls:
            print(i, file=f)
        print(
            "--------------------------------------------------------------------", file=f)
        print("All " + limit + "URLs:", file=f)
        for j in limit_urls:
            print(j, file=f)
        print(
            "--------------------------------------------------------------------", file=f)
        print("All broken URL's:", file=f)
        for z in broken_urls:
            print(z, file=f)


def limit_report(limit, processed_urls, limit_urls, broken_urls):
    print("--------------------------------------------------------------------")
    print("All found URLs:")
    for i in processed_urls:
        print(i)
    print("--------------------------------------------------------------------")
    print("All " + limit + " URLs:")
    for j in limit_urls:
        print(j)
    print("--------------------------------------------------------------------")
    print("All broken URL's:")
    for z in broken_urls:
        print(z)


def limit_mute_report_file(limit, ofile, limit_urls):
    with open(ofile, 'w') as f:
        print(
            "--------------------------------------------------------------------", file=f)
        print("All " + limit + " URLs:", file=f)
        for j in limit_urls:
            print(j, file=f)


def limit_mute_report(limit, limit_urls):
    print("--------------------------------------------------------------------")
    print("All " + limit + "URLs:")
    for i in limit_urls:
        print(i)

def report_file(ofile, processed_urls, local_urls, foreign_urls, broken_urls):
    with open(ofile, 'w') as f:
        print(
            "--------------------------------------------------------------------", file=f)
        print("All found URLs:", file=f)
        for i in processed_urls:
            print(i, file=f)
        print(
            "--------------------------------------------------------------------", file=f)
        print("All local URLs:", file=f)
        for j in local_urls:
            print(j, file=f)
        print(
            "--------------------------------------------------------------------", file=f)
        print("All foreign URLs:", file=f)
        for x in foreign_urls:
            print(x, file=f)
        print("--------------------------------------------------------------------", file=f)
        print("All broken URL's:", file=f)
        for z in broken_urls:
            print(z, file=f)


def report(processed_urls, local_urls, foreign_urls, broken_urls):
    print("--------------------------------------------------------------------")
    print("All found URLs:")
    for i in processed_urls:
        print(i)
    print("--------------------------------------------------------------------")
    print("All local URLs:")
    for j in local_urls:
        print(j)
    print("--------------------------------------------------------------------")
    print("All foreign URLs:")
    for x in foreign_urls:
        print(x)
    print("--------------------------------------------------------------------")
    print("All broken URL's:")
    for z in broken_urls:
        print(z)


def mute_report_file(ofile, local_urls):
    with open(ofile, 'w') as f:
        print(
            "--------------------------------------------------------------------", file=f)
        print("All local URLs:", file=f)
        for j in local_urls:
            print(j, file=f)


def mute_report(local_urls):
    print("--------------------------------------------------------------------")
    print("All local URLs:")
    for i in local_urls:
        print(i)


def main(argv):
    # define the program description
    text = 'A Python program that crawls a website and recursively checks links to map all internal and external links'
    # initiate the parser with a description
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument('--domain', '-d', required=True,
                        help='domain name of website you want to map. i.e. "https://scrapethissite.com"')
    parser.add_argument('--ofile', '-o',
                        help='define output file to save results of stdout. i.e. "test.txt"')
    parser.add_argument('--limit', '-l',
                        help='limit search to the given domain instead of the domain derived from the URL. i.e: "github.com"')
    parser.add_argument('--mute', '-m', action="store_true",
                        help='output only the URLs of pages within the domain that are not broken')
    parser.parse_args()

    # read arguments from the command line
    args = parser.parse_args()

    domain = args.domain
    ofile = args.ofile
    limit = args.limit
    mute = args.mute
    if domain:
        print("domain:", domain)
    if ofile:
        print("output file:", ofile)
    if limit:
        print("limit:", limit)
    if mute:
        print("mute:", mute)

    if limit is None:
        print()
        crawler(domain, ofile, mute)
        print()
    else:
        print()
        limit_crawler(domain, ofile, limit, mute)
        print()

def storing_data_json():
    a=open('test.txt')
    b=a.readlines()
    c=open('crawled_data.pickle','ab')
    data={}
    data['Crawled url']=[]
    for y in range(2,b.index('All foreign URLs:\n')-1):
        if '--' not in b[y] and 'All' not in b[y]:
            b[y]=b[y][:-1]
            data['Crawled url'].append(b[y])
    pickle.dump(data,c)

def search(search_term):
    db_file=open('crawled_data.pickle','rb')
    dict_m=pickle.load(db_file)
    out_data={}
    out_data['Results']=[]
    out_data['time_taken']=0
    out_data['Total Results']=0
    start=time.time()
    for g in dict_m['Crawled url']:
        if search_term.lower() in g:
            out_data['Results'].append(g)
    end=time.time()
    out_data['time_taken']=end-start
    out_data['Total Results']=len(out_data['Results'])
    print('Total Results :'+str(out_data['Total Results'])+'   '+'Time Taken : '+str(out_data['time_taken'])+' seconds'+'\n')
    json_data = json.dumps(out_data)
    return(json_data)

if __name__ == "__main__":
    dec=str(input('Crawl ? or Search (c :- crawl, s:- search) :'))
    if dec =='c':
        print('Crawling UNH Site once all Pages processed \nthey will be stored in crawled_data.pickle')
        main(sys.argv[1:])
        storing_data_json()
        print('Done')
    if dec=='s':
        search_term=str(input('Search : '))
        temp_term=search_term
        final_search=search_term
        out_search_term=''
        rq=0
        n=0
        n_2=0
        if '?q' in search_term:
            if "%20" in search_term:
                p=search_term[search_term.index('=')+1,search_term.index('&')]
                q=p.split('%20')
                final_search=''
                for g in q:
                    final_search+=g
            else:
                if '&num_results=' in search_term:
                    h=search_term.split('&num_results=')
                    print(h)
                    n=int(h[1])
                    rq=1
                if '&offset=' in search_term:
                    h=search_term.split('&offset=')
                    n_2=int(h[1])
                    rq=1
                if rq==1:
                    final_search=search_term[search_term.index('=')+1:search_term.index('&')]
                else:
                    h=search_term.split('=')
                    out_st=h[-1]
                    final_search=''
                    final_search=out_st

        search_term=final_search
        a=search(search_term)
        b=a.split(',')
        start=a.index('[')
        end=a.index(']')
        out=a[start+1:end]
        f_list=out.split(',')
        if rq==1:
            if n==0:
                n=len(f_list)
        time_taken=b[-2]
        if rq==1:
            f_list=f_list[n_2:n]
        if f_list==['']:
            st=-1
            en=0
            temp_s=''
            for x in range(-1,-len(temp_term),-1):
                if temp_term[x]=='/':
                    en=x
                    break
            for y in range(st,en,-1):
                temp_s+=temp_term[y]
            temp_s=temp_s[::-1]
            for y in os.listdir(temp_s):
                f_list.append(y)
            f_list.pop(0)
            print(f_list)
        else:
            print(f_list)

    