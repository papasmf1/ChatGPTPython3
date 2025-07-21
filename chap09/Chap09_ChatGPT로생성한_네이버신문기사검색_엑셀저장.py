#Chap9_ChatGPT로생성한_네이버신문기사검색_엑셀파일.py
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# URL for Naver search results
url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%B0%98%EB%8F%84%EC%B2%B4'

# Make a request to the webpage
response = requests.get(url)
response.raise_for_status()  # Ensure we notice bad responses

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the news article titles (assuming they are within <a> tags with a specific class)
titles = soup.find_all('a', {'class': 'news_tit'})

# Extract the text from the titles
article_titles = [title.get_text() for title in titles]

# Create a new Excel workbook and select the active worksheet
wb = Workbook()
ws = wb.active

# Write the titles to the worksheet
ws.append(["Article Titles"])  # Add a header
for title in article_titles:
    ws.append([title])

# Save the workbook to the specified file path
file_path = 'news_titles.xlsx'
wb.save(file_path)

print(f"Saved the article titles to {file_path}")
