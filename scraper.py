import requests
from bs4 import BeautifulSoup
import re   #rejex  

root_url = "http://github.com"
website = requests.get(root_url + "/trending/python?since=daily&spoken_language_code=en")

parser = BeautifulSoup(website.content, "html.parser")  #we pass in the website content and we specify that we want an html parser

trending_repos = parser.find_all("article", class_="Box-row")  #in bueatiful soup, the find all method takes the 1.nameoftag ("div","a","p") and 2.DictionaryOfAttributes: dictionaty to specify the attributes that the tag must have.
#In BeautifulSoup, the class_ parameter is used to search for tags based on their CSS class. It is not a predefined keyword in Python; rather, it is a specific parameter name chosen by BeautifulSoup to avoid clashing with the reserved word class in Python.
for repo in trending_repos:
    repo_header = repo.find("h2").find("a")     #looking at the github website inspected we see the element with the data we looking for lies within the Box-row->h2->a, because we retrieving the links
    repo_name = "".join(repo_header.text.split())
    #explaining the line above: 
#     repo_header.text: This gets the text content of the repo_header tag. It might contain leading, trailing, or multiple consecutive whitespaces.
# split(): This method is called on the text to split it into a list of words. The default behavior of split() is to split the string at whitespace characters.
# "".join(...): This joins the list of words back into a single string with an empty string ("") as a separator. This effectively removes any extra whitespace between the words.
    repo_link = root_url + repo_header["href"]  #accessing the href attributes
    print(repo_name, end = "\n")
    print(repo_link, end = "\n")

    repo_stars = repo.find("a", href=repo_header["href"] + "/stargazers").text.strip()
    print(f"{repo_stars} stars", end="\n")  #formatting
    repo_forks =repo.find("svg", class_="octicon-repo-forked").find_parent().text.strip()

    print(f"{repo_forks} forks", end="\n")
    repo_stars_today_element = repo.find(text=re.compile("stars today"))        #re used to create a rejex 
    repo_stars_today = 0 if repo_stars_today_element is None else repo_stars_today_element.text.strip().split()[0]
    print(f"{repo_stars_today} stars today", end="\n"*2)

#explaining lines 27-30
# re.compile("stars today"): This creates a regular expression pattern that matches the literal text "stars today". The compile function is used to compile the regular expression pattern for efficiency.
# repo.find(text=...): This searches for a string in the text content of the repo element that matches the specified regular expression pattern. It returns the first matching text element found.
# So, repo_stars_today_element will be the BeautifulSoup element containing the text "stars today" if it is found within the repo element. If no such text is found, repo_stars_today_element will be None.

#Handles the case where repo_stars_today_element is None. If it is not None, it extracts the text content, removes leading and trailing whitespaces with .strip(), and then splits the text (assuming it's a number followed by "stars today") to get the numeric part. If repo_stars_today_element is None, it sets repo_stars_today to 0. This way, the code gracefully handles the case where "stars today" information is not present.