import urllib.request


class Loader(object):

    def __init__(self):
        pass

    @staticmethod
    def get_file(url):
        req = urllib.request.Request(url)

        ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:44.0) Gecko/20100101 Firefox/44.0'
        accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        accept_lang = 'en-US,en;q=0.5'

        req.add_header('User-Agent', ua)
        req.add_header('Accept', accept)
        req.add_header('Accept-Language', accept_lang)

        # gelbooru can raise HTTP 403 (Forbidden) error
        # when we try load pic without Referer
        try:
            page = urllib.request.urlopen(req, None, timeout=5)
        except urllib.error.HTTPError:
            print('403 ERROR')
            # send some food
            req.add_header('Referer', url)
            page = urllib.request.urlopen(req, None, timeout=5)

        page_text = page.read()

        return page_text

    def get_html(self, url):
        page_text = self.get_file(url)
        return page_text.decode('utf-8')
