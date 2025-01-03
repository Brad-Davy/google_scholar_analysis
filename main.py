import requests
from bs4 import BeautifulSoup
from time import sleep
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.5
plt.rcParams['figure.autolayout'] = True
cm = 1/2.54

years = range(2010, 2024)
query = 'Python programming'

def determine_number_of_articles(query: str, start_year: str, end_year: str) -> int:
    # URL of the Google Scholar search results page
    url = f"https://scholar.google.co.uk/scholar?q={query}&hl=en&as_sdt=0%2C5&as_rr=1&as_vis=1&as_ylo={start_year}&as_yhi={end_year}"

    # Send a GET request to the URL
    response = requests.get(url)
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')

    total_results_text = soup.find('div', {'id': 'gs_ab_md'}).find('div').text
    total_results = total_results_text.split()[1].replace(',', '')
    return total_results

def determine_number_of_papers(query: str, start_year: str, end_year: str) -> list:
    number_of_papers = []

    for each_year in years:
        total_results = determine_number_of_articles(query, each_year, each_year+1)
        try:
            number_of_papers.append(int(total_results))
        except:
            number_of_papers.append(0)
        print(f"Number of articles on {query} in {each_year}: {total_results}")
        sleep(2)  # Sleep for 2 seconds to avoid getting blocked by Google
    return number_of_papers


with open('results.txt', 'r') as f:
    year = []
    number_of_papers = []
    content = f.read()
    for lines in content.split('\n'):
        data = lines.split(' ')
        number_of_papers.append(int(data[-1]))
        year.append(int(data[-2].split(':')[0]))

fig = plt.figure(figsize=(10*cm, 10*cm))
plt.yscale('log')
plt.xlabel('Year')
plt.ylabel('Number of papers using Python')
plt.scatter(year, number_of_papers, color='black', marker='o', s=10)
plt.savefig('python_papers.png', dpi=300)
plt.show()