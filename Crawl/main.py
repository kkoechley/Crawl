import time
import re
from selenium.common.exceptions import TimeoutException
import sys
sys.path.insert(0, '/Users/rutherfordle/PycharmProjects/')
import CrawlConnect

#Import WebDriver, page direct and credential from external directory CrawlConnect
driver = CrawlConnect.driver

ssai = '25843'
ssaiperc = '99.75'

green = "GREEN"
red = "RED"
buffCap = 5.0
vsfCap = 10.0
vstCap = 15.0
authnSDK = 70
authzSDK = 70
authnMVPD = 70
authzMVPD = 70
authzLatencyMax = 15000
sdkHoursBefore = 1
mvpdHoursBefore = 1
authnSDKRed = ''
authzSDKRed = ''
authnMVPDRed = ''
authzMVPDRed = ''
authLatMVPDRed= ''
sdkBreak = 'iOS'
mvpdBreak = 'WOW'

#driver = webdriver.Firefox()
from selenium.common.exceptions import NoSuchAttributeException
from selenium.webdriver.common.keys import Keys




driver.find_element_by_class_name("submit").click()
time.sleep(3)
delay = 3
try:
    conc = driver.find_element_by_xpath('//*[@id="w_0"]/div/div[4]').text
    buff = driver.find_element_by_xpath('//*[@id="w_1"]/div/div[4]').text
    buffRoku = driver.find_element_by_xpath('//*[@id="w_1"]/div/div[5]/table/tbody/tr[5]/td[2]/div').text
    vst = driver.find_element_by_xpath('//*[@id="w_3"]/div/div[5]/table/tbody/tr[1]/td[2]/div').text
    vstRoku = driver.find_element_by_xpath('//*[@id="w_3"]/div/div[5]/table/tbody/tr[5]/td[2]/div').text
    vsf = driver.find_element_by_xpath('//*[@id="w_5"]/div/div[4]').text
    vsfRoku = driver.find_element_by_xpath('//*[@id="w_5"]/div/div[5]/table/tbody/tr[5]/td[2]/div').text
    # buff = buff.strip("%","")
    from datetime import datetime
    from pytz import timezone
    driver.get('http://bucasit-build.corp.adobe.com/grafana/dashboard/db/adobe-pass?from=now-1h&to=now')
    time.sleep(3)

    graf = driver.find_element_by_class_name('singlestat-panel-value').text
    graf1 = driver.find_element_by_class_name('graph-legend-value').text
    #print(graf1)
    #print(graf)

    hr = "%H"
    day = "%Y-%m-%d"
    timeofday = datetime.now(timezone('US/Pacific'))
    hr = timeofday.strftime(hr)
    day = timeofday.strftime(day)
    hr = int(hr)
    hr1 = hr - sdkHoursBefore
    if hr == 0:
        hr = 01
        hr1 = 00
    #hr2 = hr + 1
    driver.get('http://sp-dc.adobepass.com/esm/v2/media-company/year/month/day/hour?sdk-type&proxy=Direct&requestor-id=NBCOlympics&media-company=NBC&start=' + str(day) +'T' + str(hr1) + ':00:00&end=' + str(day) +'T' + str(hr) + ':00:00&limit=1000')
    time.sleep(3)

    authnTotal = ''
    authzTotal = ''
    x = '1'
    plat = 'empty'
    authValue = True

    while (authValue == True):

        plat = driver.find_element_by_xpath('/html/body/table/tbody/tr['+ x +']/td[6]').text
        authnSucc = driver.find_element_by_xpath('/html/body/table/tbody/tr['+ x +']/td[10]').text
        authnPend = driver.find_element_by_xpath('/html/body/table/tbody/tr['+ x +']/td[11]').text
        authzSucc = driver.find_element_by_xpath('/html/body/table/tbody/tr['+ x +']/td[15]').text
        authzPend = driver.find_element_by_xpath('/html/body/table/tbody/tr['+ x +']/td[14]').text

        authnSucc = re.sub('[,]', '', authnSucc)
        authnPend = re.sub('[,]', '', authnPend)
        authzSucc = re.sub('[,]', '', authzSucc)
        authzPend = re.sub('[,]', '', authzPend)
        authnSucc = float(authnSucc)
        authnPend = float(authnPend)
        authzSucc = float(authzSucc)
        authzPend = float(authzPend)

        authnPerc = authnSucc/authnPend * 100 if authnPend != 0 else '0'
        authzPerc = authzSucc/authzPend * 100 if authzPend != 0 else '0'

        green if authnPerc >= authnSDK or authnPerc == '0' else red
        green if authzPerc >= authzSDK or authzPerc == '0' else red
        if authnPerc >= authnSDK or authnPerc == 0:
            authn = plat + ' ' + str(authnPerc) + '% ' + green
        else:
            authn = plat + ' ' + str(authnPerc) + '% ' + red
            authnSDKRed += plat + ' (' + str(authnSucc) + '/' + str(authnPend) + ') ' + str(authnPerc) + '% '
            authnSDKRed += red + '\n'

        authn += '\n'
        x = int(x)
        if (plat == sdkBreak):
            authn += '\n'

        x = str(x)
        authnTotal += authn

        if authzPerc >= authzSDK or authzPerc == 0:
            authz = plat + ' ' + str(authzPerc) + '% ' + green
        else:
            authz = plat + ' ' + str(authzPerc) + '% ' + red
            authzSDKRed += plat + ' (' + str(authzSucc) + '/' + str(authzPend) + ') ' + str(authzPerc) + '% '
            authzSDKRed += red + '\n'

        authz += '\n'
        x = int(x)
        if (plat == sdkBreak):
            authz += '\n'

        x = str(x)
        authzTotal += authz

        x = int(x)
        x += 1
        x = str(x)

        try:
            driver.find_element_by_xpath('/html/body/table/tbody/tr[' + x + ']/td[6]').text
            authValue = True
        except:
            authValue = False

    print('SDK Authentication')
    print(str(authnTotal))
    print('SDK Authorization')
    print(str(authzTotal))

    hr1 = hr - mvpdHoursBefore
    # hr2 = hr + 1
    driver.get(
        'http://sp-dc.adobepass.com/esm/v2/media-company/year/month/day/hour/proxy/mvpd?proxy=Direct&requestor-id=NBCOlympics&media-company=NBC&start=' + str(day) +'T' + str(hr1) + ':00:00&end=' + str(day) +'T' + str(hr) + ':00:00&limit=1000')
    time.sleep(3)

    authnTotal = ''
    authzTotal = ''
    authzLatTotal = ''
    x = '1'
    plat2 = 'empty'
    authValue = True

    while (authValue == True):

        plat2 = driver.find_element_by_xpath('/html/body/table/tbody/tr[' + x + ']/td[7]').text
        authnSucc = driver.find_element_by_xpath('/html/body/table/tbody/tr[' + x + ']/td[10]').text
        authnPend = driver.find_element_by_xpath('/html/body/table/tbody/tr[' + x + ']/td[11]').text
        authzSucc = driver.find_element_by_xpath('/html/body/table/tbody/tr[' + x + ']/td[15]').text
        authzAttempts = driver.find_element_by_xpath('/html/body/table/tbody/tr[' + x + ']/td[14]').text
        authzLatency = driver.find_element_by_xpath('/html/body/table/tbody/tr[' + x + ']/td[18]').text

        authnSucc = re.sub('[,]', '', authnSucc)
        authnPend = re.sub('[,]', '', authnPend)
        authzSucc = re.sub('[,]', '', authzSucc)
        authzAttempts = re.sub('[,]', '', authzAttempts)
        authzLatency = re.sub('[,]', '', authzLatency)
        authnSucc = float(authnSucc)
        authnPend = float(authnPend)
        authzSucc = float(authzSucc)
        authzAttempts = float(authzAttempts)
        authzLatency = float(authzLatency)

        authnPerc = authnSucc / authnPend * 100 if authnPend != 0 else '0'
        authzPerc = authzSucc / authzAttempts * 100 if authzAttempts != 0 else '0'
        authzLatencySec = authzLatency / authzAttempts if authzAttempts != 0 else '0'

        if authnPerc >= authnMVPD or authnPerc == 0:
            authn = plat2 + ' ' + str(authnPerc) + '% ' + green
        else:
            authn = plat2 + ' ' + str(authnPerc) + '% ' + red
            authnMVPDRed += plat2 + ' (' + str(authnSucc) + '/' + str(authnPend) + ') ' + str(authnPerc) + '% '
            authnMVPDRed += red + '\n'

        authn += '\n'
        x = int(x)
        if (plat2 == mvpdBreak):
            authn += '\n'

        x = str(x)
        authnTotal += authn

        if authzPerc >= authzMVPD or authzPerc == 0:
            authz = plat2 + ' ' + str(authzPerc) + '% ' + green
        else:
            authz = plat2 + ' ' + str(authzPerc) + '% ' + red
            authzMVPDRed += plat2 + ' (' + str(authzSucc) + '/' + str(authzPend) + ') ' + str(authzPerc) + '% '
            authzMVPDRed += red + '\n'

        authz += '\n'
        x = int(x)
        if (plat2 == mvpdBreak):
            authz += '\n'

        x = str(x)
        authzTotal += authz

        if authzLatencySec <= authzLatencyMax or authzLatencySec == '0':
            authzLat = plat2 + ' ' + str(authzLatencySec) + ' ' + green
        else:
            authzLat = plat2 + ' ' + str(authzLatencySec) + ' ' + red
            authLatMVPDRed += plat2 + ' (' + str(authzLatency) + '/' + str(authzAttempts) + ') ' + str(authzLatencySec) + ' '
            authLatMVPDRed += red + '\n'

        authzLat += '\n'
        x = int(x)
        if (plat2 == mvpdBreak):
            authzLat += '\n'

        x = str(x)
        authzLatTotal += authzLat

        x = int(x)
        x += 1
        x = str(x)

        try:
            driver.find_element_by_xpath('/html/body/table/tbody/tr[' + x + ']/td[7]').text
            authValue = True
        except:
            authValue = False

    print('MVPD Authentication')
    print(str(authnTotal))
    print('MVPD Authorization')
    print(str(authzTotal))
    print('MVPD Latency')
    print(str(authzLatTotal))
    print('\n')

    hr = "%H"
    min = "%M"
    timeofday = datetime.now(timezone('US/Eastern'))
    hr = timeofday.strftime(hr)
    min = timeofday.strftime(min)
    min = int(min)
    min -= (min % 15)
    if min == 0:
        min = '00'
    min = str(min)
    timeofday = hr + min
    timeofday = str(timeofday)
    #module unicodedata
    buff = re.sub('[%]', '', buff)
    buffRoku = re.sub('[%]', '', buffRoku)
    vsf = re.sub('[%]', '', vsf)
    vsfRoku = re.sub('[%]', '', vsfRoku)
    result = timeofday + ',' + graf + ',' + ssai + ',' + conc + ',rebuff=' + buff + '/' + buffRoku + ',vst=' + vst + ',' + '/' + vstRoku + ',vsf=' + vsf + '/' + vsfRoku
    result = result.replace(" ", "") + ',ssai_suc=' + ssaiperc

    buff = float(buff)
    buffRoku = float(buffRoku)
    vst = float(vst)
    vstRoku = float(vstRoku)
    vsf = float(vsf)
    vsfRoku = float(vsfRoku)
    if (buff <= buffCap):
        print('Rebuffering: ' + green)
    else:
        print('Rebuffering: ' + str(buff) + ' ' + red)
    if (buffRoku <= buffCap):
        print('Roku Rebuffering: ' + green)
    else:
        print('Roku Rebuffering: ' + str(buffRoku) + ' ' + red)
    if (vst <= vstCap):
        print('VST: ' + green)
    else:
        print('VST: ' + str(vst) + ' ' + red)
    if (vstRoku <= vstCap):
        print('VST Roku: ' + green)
    else:
        print('VST Roku: ' + str(vstRoku) + ' ' + red)
    if (vsf <= vsfCap):
        print('VSF: ' + green)
    else:
        print('VSF: ' + str(vsf) + ' ' + red)
    if (vsfRoku <= vstCap):
        print('VSF Roku: ' + green)
    else:
        print('VSF Roku: ' + str(vsfRoku) + ' ' + red)
    print(result + '\n')

    if authnSDKRed == '':
        authnSDKRed = green
    if authzSDKRed == '':
        authzSDKRed = green
    if authnMVPDRed == '':
        authnMVPDRed = green
    if authzMVPDRed == '':
        authzMVPDRed = green
    if authLatMVPDRed == '':
        authLatMVPDRed = green

    print('AuthnSDK = ' + authnSDKRed)
    print('AuthzSDK = ' + authzSDKRed)
    print('AuthnMVPD = ' + authnMVPDRed)
    print('AuthzMVPD = ' + authzMVPDRed)
    print('AuthLatency = ' + authLatMVPDRed)


except TimeoutException:
    print("Loading took too much time!")

#print(response.headers)
#print(response.text)
#with open("requests_results.html", "wb") as f:
    #f.write(r.content)
    #f.write(response.content)
    # print(r.content)
driver.quit();
    #driver2.quit();

