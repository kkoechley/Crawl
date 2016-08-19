from requests import session

payload = {
    'action': 'login',
    'username': USERNAME,
    'password': PASSWORD
}

with session() as c:
    c.post('http://example.com/login.php', data=payload)
    response = c.get('http://example.com/protected_page.php')
    print(response.headers)
    print(response.text)

    import requests
    from requests import session
    import httplib2
    from bs4 import BeautifulSoup

    http = httplib2.Http()
    from selenium import webdriver

    # driver = webdriver.Firefox()
    from selenium.common.exceptions import NoSuchAttributeException
    from selenium.webdriver.common.keys import Keys
    import re

    url = 'https://pulse.conviva.com/login/'
    user = {'username': 'ssargent@adobe.com',
            'password': ''}
    with session() as req:
        r = req.post(url, data=user)
        response = req.get('https://pulse.conviva.com/reports/15/')
        driver = webdriver.Chrome()
        driver.get('https://pulse.conviva.com/login/')
        title = driver.find_element_by_class_name('PulseLogo').text
        print(title)
        # print(response.headers)
        # print(response.text)
        with open("requests_results.html", "wb") as f:
            f.write(r.content)
            f.write(response.content)
            # print(r.content)


    def trade_spider(max_pages):
        page = 1
        while page <= max_pages:
            # body = {'username': 'ssargent@adobe.com', 'password': ''}
            # headers = {'Content-type': 'application/x-www-form-urlencoded'}
            # response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
            # headers = {'Cookie': response['set-cookie']}
            # url = "https://pulse.conviva.com/reports/15/"
            # response, content = http.request(url, 'GET', headers=headers)
            # print(r.cookies)
            # full_url = {'sessionid': r.cookies}
            # r = requests.post(url, data=full_url)
            # source_code = requests.get(r.content)
            # just get the code, no headers or anything
            plain_text = response.content
            # plain_text = r.text
            address = driver.find_element_by_xpath('/html/body/div[1]/div/div')
            # print(address.string)
            soup = BeautifulSoup(plain_text, "html.parser")
            for link in soup.findAll('h1', {'class': 'PageHeader'}):
                href = link.get('href')
                title = link.get('data-type')
                value = link.string  # just the text, not the HTML
                # print(href)
                # print(title)
                print(value)
                # print (r.cookies);
                # get_single_item_data(url)
            page += 1


    def get_single_item_data(item_url):
        source_code = requests.get(item_url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        for link in soup.findAll('a'):
            title = link.string  # just the text, not the HTML
            # print(link)
            # print(title)
            # href = link.get('href')
            # print(href)


    trade_spider(1)
