import time
import threading
import requests

def download_page(url):
    response = requests.get(url)
    return response.text

def download_pages_threading(urls):
    threads = []
    
    for url in urls:
        thread = threading.Thread(target=download_page, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

urls = [
    "https://www.example.com",
    "https://www.python.org",
    "https://www.github.com",
    "https://www.stackoverflow.com",
]

if __name__ == '__main__':
    start_time = time.time()
    
    download_pages_threading(urls)
    
    print(f"Threaded download took {time.time() - start_time:.2f} seconds")
