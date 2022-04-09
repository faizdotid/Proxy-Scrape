from secrets import choice
import requests
import re

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'})

def split_only_domain(url):
    domain = url[0].split("/")[2]
    return domain

class Scrape:
    
    def __init__(self, url, regex):
        self.url = url
        self.regex = regex
        self.proxies = []
    
    def make_request(self):
        for u in self.url:
            try:
                resp = session.get(u, timeout=70)
                resp.raise_for_status()
                self.parse_body(resp.text)
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError):
                pass

    def parse_body(self, body):
        try:
            proxies = re.findall(self.regex, body)
            if proxies:
                for proxy in proxies:
                    self.proxies.append(proxy)
            else:
                pass
        except Exception as e:
            print(e)

    def __str__(self):
        redup = set(self.proxies)
        with open('proxies.txt', 'a') as f:
                f.write('\n'.join(redup)+'\n')
        return "Successfully scraped {} proxies from {}".format(str(len(redup)), split_only_domain(self.url))


class Main(Scrape):
    
    def __init__(self, option="All"):
        self.option = option
        self.default_regex = r'\d+\.\d+\.\d+\.\d+:\d{1,5}'
        self.config_proxy = {
            1: ["https://www.proxy-list.download/api/v1/get?type=http", "https://www.proxy-list.download/api/v1/get?type=https", "https://www.proxy-list.download/api/v1/get?type=socks4", "https://www.proxy-list.download/api/v1/get?type=socks5"],
            2: ["https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt", "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt", "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt", "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt"],
            3: ["https://free-proxy-list.net/", "https://www.us-proxy.org/", "https://www.socks-proxy.net/", "https://free-proxy-list.net/uk-proxy.html", "https://www.sslproxies.org/", "https://free-proxy-list.net/anonymous-proxy.html"],
            4: ["https://spys.me/proxy.txt"],
            5: ["https://api.proxyscrape.com/?request=getproxies&proxytype=all&country=all&ssl=all&anonymity=all"],
        }

    def run(self):
        if self.option == "All":    
            print("Maybe it will take a few minutes to scrape all proxies")
            for k, v in self.config_proxy.items():
                Scrape.__init__(self, v, self.default_regex)
                self.make_request()
                print(self)
        else:
            v = self.config_proxy[int(self.option)]
            Scrape.__init__(self, v, self.default_regex)
            self.make_request()
            print(self)

def main():
    print("""


██████╗░██████╗░░█████╗░██╗░░██╗██╗░░░██╗░░░░░░░██████╗░█████╗░██████╗░░█████╗░██████╗░███████╗
██╔══██╗██╔══██╗██╔══██╗╚██╗██╔╝╚██╗░██╔╝░░░░░░██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝
██████╔╝██████╔╝██║░░██║░╚███╔╝░░╚████╔╝░█████╗╚█████╗░██║░░╚═╝██████╔╝███████║██████╔╝█████╗░░
██╔═══╝░██╔══██╗██║░░██║░██╔██╗░░░╚██╔╝░░╚════╝░╚═══██╗██║░░██╗██╔══██╗██╔══██║██╔═══╝░██╔══╝░░
██║░░░░░██║░░██║╚█████╔╝██╔╝╚██╗░░░██║░░░░░░░░░██████╔╝╚█████╔╝██║░░██║██║░░██║██║░░░░░███████╗
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░░░░░░░╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚══════╝


1. Proxy-List.Download
2. Github
3. Free-Proxy-List.net
4. Spys.me
5. Proxyscrape
6. All
""")
    choice = input("Enter your choice: ")
    if choice == "6":
        Main().run()
    elif re.search(r'^[1-5]$', choice):
        Main(choice).run()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
