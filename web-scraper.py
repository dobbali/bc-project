class UrlCheck():
    """
    Takes list of urls and gives if the url is returning any results or not

    Attributes
    ----------
    report_type : list
        list with urls
    """

    def __init__(self):

        self.USER_AGENT = 'User-agent'
        self.ACCEPT = 'Accept'
        self.ACCEPT_ENCODING = 'Accept-Encoding'
        self.ACCEPT_LANGUAGE = 'Accept-language'
        self.CONNECTION = 'Connection'

        self.CONNECTION_DEFAULT = "keep-alive"
        self.ACCEPT_ENCODING_DEFAULT = "utf-8"
        self.ACCEPT_LANGUAGE_DEFAULT = 'en-us,en;q=0.5'

        self.USER_AGENT_MAC_FIREFOX = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/45.0.2"

        self.HEADER_FIREFOX_MAC = {self.USER_AGENT: self.USER_AGENT_MAC_FIREFOX,
            self.ACCEPT: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                self.ACCEPT_ENCODING: self.ACCEPT_ENCODING_DEFAULT,
                   self.ACCEPT_LANGUAGE: self.ACCEPT_LANGUAGE_DEFAULT,
                        self.CONNECTION: self.CONNECTION_DEFAULT}

        self.HEADER_CHROME_WINDOWS = {self.USER_AGENT: "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
            self.ACCEPT: "application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
                self.ACCEPT_ENCODING: self.ACCEPT_ENCODING_DEFAULT,
                    self.ACCEPT_LANGUAGE: self.ACCEPT_LANGUAGE_DEFAULT,
                        self.CONNECTION: self.CONNECTION_DEFAULT}

        self.USER_HEADERS = [self.HEADER_FIREFOX_MAC, self.HEADER_CHROME_WINDOWS]
        #self.path = path


    # Random User-Agent string
    def get_random_header(self):
        return self.USER_HEADERS[randint(0,(len(self.USER_HEADERS)-1))]

    # Opener with random header settings
    def get_random_opener(self):
        opener = urllib.request.build_opener()
        randomHeader = self.get_random_header()
        opener.addheaders = [(self.USER_AGENT,randomHeader[self.USER_AGENT]),
                             (self.ACCEPT,randomHeader[self.ACCEPT])
                             ,(self.ACCEPT_ENCODING,randomHeader[self.ACCEPT_ENCODING])
                             , (self.ACCEPT_LANGUAGE, randomHeader[self.ACCEPT_LANGUAGE])
                             ,(self.CONNECTION,randomHeader[self.CONNECTION])
                             ]
        return opener

    def get_request(self, url):
        try:
            resp= requests.get(url, self.get_random_header())
        except Exception as e:
            print(e)
            resp = "failed"
        return resp

    def get_count(self, resp):


        # time.sleep(random.uniform(delay_min, delay_max))
        cities = []
        states = []
        try:
            if resp.status_code == 404:
                count = 0
                return count
            soup = BeautifulSoup(resp.text, 'lxml')
            for val,  in zip(soup.findAll("h2"), soup.findAll("li", { "class" : "search-result-tagline__item" })): 
                cities.append(val.text)
                states.append(states.text)

        except Exception as e:
            print(e)
            print(resp)
            count = "re check"
        return  (cities, states)
    
    
if __name__ == "__main__":
    uc = UrlCheck()
    all_target_urls = []
    for page_num in range(1, 11):
        new_url = "https://www.niche.com/places-to-live/search/best-outdoors-cities/" + "?page="+str(page_num)
        all_target_urls.append(new_url)
        
    cities_list_html = []
    states_list_html = []
    for url in all_target_urls:
        resp = uc.get_request(url)
        soup = BeautifulSoup(resp.text, 'lxml')
        cities_list_html.append(soup.findAll("h2"))
        states_list_html.append(soup.findAll("li", { "class" : "search-result-tagline__item" }))
        
    cities = [city.text for cities_list in cities_list_html for city in cities_list]
    states = [state.text for states_list in states_list_html for state in states_list]

    regex = re.compile(r'[a-zA-Z].+')
    states = list(filter(regex.search, states))

    top_outdoor_activities = pd.DataFrame.from_dict({'city':cities,  'state':states}).reset_index().rename(columns {"index":"rank"})
    top_outdoor_activities["rank"] = top_outdoor_activities["rank"] + 1
    top_outdoor_activities["state"] = top_outdoor_activities.state.str.replace("City in ","")
    top_outdoor_activities.to_csv("top_outdoor_activity_location.csv")