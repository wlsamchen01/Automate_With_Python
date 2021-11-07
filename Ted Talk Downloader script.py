import requests  # for getting content of the TED Talk page
from bs4 import BeautifulSoup  # web scraping
import re  # regular expression pattern matching
import sys  # for argument parsing

# Exception Handling
# This part is added so that we can pass in the url when we run the script
# in terminal
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    sys.exit("Error: Please enter the TED Talk URL")


# url = "https://www.ted.com/talks/jia_jiang_what_i_learned_from_100_days_of_rejection"


r = requests.get(url)

print("Download about to start")

# use BeautifulSoup to create a "soup" of the content we got from requests
soup = BeautifulSoup(r.content, features="lxml")

# We want to find out the location of the mp4
# when we inspect the page, the mp4 is located inside a script tag labelled
# "talkPage.init"
for val in soup.findAll("script"):
    if (re.search("talkPage.init", str(val))) is not None:
        result = str(val)


# extract the mp4 from the result string
result_mp4 = re.search("(?P<url>https?://[^\s]+)(mp4)", result).group("url")


mp4_url = result_mp4.split('"')[0]


file_name = mp4_url.split("/")[len(mp4_url.split("/")) - 1].split("?")[0]


print("Downloading video from ... " + mp4_url)
print("Storing video in ..." + file_name)


# Download the mp4

r = requests.get(mp4_url)

with open(file_name, "wb") as f:
    f.write(r.content)

print("Download Process is finished")
