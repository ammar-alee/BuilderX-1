import requests

INDEX_URL = "https://builderx.io/app/"


def get_resource(url):
    return requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
    ).text


def find_links(source):
    


def main():
    html = get_resource(INDEX_URL)
    print(html)


if __name__ == "__main__":
    main()
