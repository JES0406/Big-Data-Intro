import time
import requests

def download_page(url):
    response = requests.get(url)
    return response.text

urls = [
    "https://www.example.com",
    "https://www.python.org",
    "https://www.github.com",
    "https://www.stackoverflow.com",
]

if __name__ == '__main__':
    start_time = time.time()
    
    for url in urls:
        download_page(url)
    
    print(f"Sequential download took {time.time() - start_time:.2f} seconds")
