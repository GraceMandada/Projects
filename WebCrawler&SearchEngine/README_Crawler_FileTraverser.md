Steps to run the script :

Code 1 : Crawler_FileTraverser.py

1) If UNH site isn't crawled yet then crawl by pressing 'c' after running the software. Once crawling is done the crawler will stop. Incase you see same website pages being repeated simply press ctrl+c.
command: >python Crawler_FileTraverser.py -d http://newhaven.edu/ -o text.txt

Once crawled a txt file called 'test.txt' and a pickle file will be made. Txt file will consist of all crawled local and foreign pages.
pickle file will consist of all links so you dont need to crawl the site again.

2) Once UNH site is scraped ,run the script once again and now press 's' to search.

3) Simply type keyword to search for. Incase of a File you want to traverse ensure folder is in same directory
   as of the source code and simply write the domain of website followed by /foldername. For example to traverse
   through folder named 'Practice Questions' simply write 'https://www.newhaven.edu/Practice Questions' and the
   script will traverse through this folder.

How the script is made :

1) I used some basic python Libraries like bs4,requests,urllib,json etc.First the script visits the main page
   of the website and then deques the domain.
2) The script fetches all 'href' links found on the src code on the page and puts them inside a set of links 
   to be crawled.
3) Script maintains a record of visited and non-visited pages all the time.
4) In order to ensure that no non-working page is included script always sends a request and waits for [200]
   response code which means the webpage is up and working and can be crawled.
5) Once crawled the script makes a report of working(home/foreign) pages and broken links.
6) Then it uses this report to create a binary file with all crawled(working) links which can be used in future.  

