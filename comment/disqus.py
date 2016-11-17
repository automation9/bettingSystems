from automation9 import Automation9
from selenium import webdriver
import time
from guerrillamail import GuerrillaMailSession
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# https://mailsac.com/
# http://www.yopmail.com/en/add-domain.php
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/

auto = Automation9()

def MAIL_get_verification_link(self, mailSessionID=None, subjectPattern=None, linkPattern=r"", mailService="Guerrilla"):
    import re
    if mailService == "Guerrilla":
        _mailSession = GuerrillaMailSession(mailSessionID)
        while True:
            for mail in _mailSession.get_email_list():
                if subjectPattern in mail.subject:
                    fetch_mail = _mailSession.get_email(mail.guid)
                    body = fetch_mail.body
                    print(body)
                    m = re.search(linkPattern, body)
                    if m:
                        link = m.group('veri_link')
                        print("LINK FOUND: "+link)
                        return link
            time.sleep(2)
    return None

def disqus_signup_new_account(username=None, email=None, password="!Admin987", mailSessionID=None, webDriverOption=False, bDeleteAllCookies=False):
    if webDriverOption == True:
        from selenium.webdriver.chrome.options import Options
        options = webdriver.ChromeOptions() 
        options.add_argument(r"user-data-dir=C:\Users\loan nguyen\AppData\Local\Google\Chrome\User Data\Default") #Path to your chrome profile
    ##    w = webdriver.Chrome(executable_path="C:\\Users\\chromedriver.exe", chrome_options=options)
    ##    userProfile= "C:\Users\loan nguyen\AppData\Local\Google\Chrome\User Data\Default"
        driver = webdriver.Chrome(executable_path=r"D:\01_software\chromedriver_win32\chromedriver.exe", chrome_options=options)
    else:
        driver = webdriver.Chrome(executable_path=r"D:\01_software\chromedriver_win32\chromedriver.exe")
        
    if bDeleteAllCookies == True:
        print("Delete cookies")
        driver.delete_all_cookies()
        time.sleep(10)
        
    driver.get("https://disqus.com/profile/signup/")
    ### logout from previous account
    if "Nice! Your account has been created." in driver.page_source:
        driver.find_element_by_link_text("I want to comment on sites").click()
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.title_is("Recommended Discussions · Disqus"))
        driver.find_element_by_class_name("dropdown").click()
        wait = WebDriverWait(driver, 20)
        logout_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT,'Log Out')))
        logout_link.click()
        driver.get("https://disqus.com/profile/signup/")
        
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.ID,'display-name-input')))
    driver.find_element_by_id("display-name-input").send_keys(username)
    driver.find_element_by_id("email-input").send_keys(email)
    driver.find_element_by_id("password-input").send_keys(password)
    driver.find_element_by_class_name("submit").click()

    time.sleep(2)
    if "We couldn't create your account. Please check what you've entered." in driver.page_source:
        username_elem = driver.find_element_by_id("display-name-input")
        username_elem.clear()
        username_elem.send_keys(username)
        email_elem = driver.find_element_by_id("email-input")
        email_elem.clear()
        email_elem.send_keys(email)
        password_elem = driver.find_element_by_id("password-input")
        password_elem.clear()
        password_elem.send_keys(password)
        ### manually solve recaptcha
##        driver.find_element_by_class_name("recaptcha-checkbox-checkmark").click()
        recaptcha_checkbox_elem = driver.find_element_by_xpath("//*[@role='presentation']")
        recaptcha_checkbox_elem.click()
        time.sleep(18)
        driver.find_element_by_class_name("submit").click()
        
    #
    driver.find_element_by_link_text("I want to comment on sites").click()

    # choose 3 channel to follow
    driver.get("https://disqus.com/home/explore/channels/sports/")

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'btn-follow')))
    follow_button_list = driver.find_elements_by_class_name("btn-follow")
##    wait.until("//button[contains(text(),'Follow')]")

    
    for i, follow in enumerate(follow_button_list):
        if i < 3:
            # http://stackoverflow.com/questions/11908249/debugging-element-is-not-clickable-at-point-error
            # http://stackoverflow.com/questions/36449732/selenium-python-element-is-not-clickable-at-point
            follow.send_keys("\n")
    time.sleep(1)
    # http://stackoverflow.com/questions/12323403/how-do-i-find-an-element-that-contains-specific-text-in-selenium-webdriver-pyth
    driver.find_element_by_xpath('//button[contains(text(),"Continue »")]').click()

    # verify email
    time.sleep(30) # wait for verification email
    if mailSessionID is not None:
        print("mailSessionID="+mailSessionID)
        subjectPattern = "Verify your email now, prevent stuck comments"
        linkPattern = r'<a href="(?P<veri_link>.*disqus*?)">'
        link = MAIL_get_verification_link(mailSessionID, subjectPattern, linkPattern)
        import requests
        if link is not None:
            r = requests.get(link)
            print(r.status_code)
    
    # if register successfully then store to local file
    with open("./comment_accounts.txt", "r+") as f:
        import datetime
        timestamp = ('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
        content = f.read()
        f.seek(0, 0)
        f.write(timestamp +"\t"+ email +"\t"+ "disqus" +"\n" + content)

    print("PLEASE TO REMEMBER TO VERIFY YOUR ACCOUT WITH PROVIDED EMAIL")
        
def googleSearch_for_disqus_forums(search_term_list, api_key, cse_id):
    from googleapiclient.discovery import build
    import pprint

    my_api_key = api_key
    my_cse_id = cse_id
    _base_term = '"disqus.com/home/forum"'

    # http://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search
    # https://developers.google.com/custom-search/json-api/v1/reference/cse/list
    def google_search(search_term, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
##        if res['items']:
        if "items" in res.keys():
            return res['items']
        return None

    # http://stackoverflow.com/questions/14543555/how-to-use-daterestrict-parameter-in-custom-search-api
    for term in search_term_list:
        search_term = _base_term + " " + term
        results = google_search(
##            search_term, my_api_key, my_cse_id, num=10, dateRestrict="d30", exactTerms="disqus_thread")
            search_term, my_api_key, my_cse_id, num=10, dateRestrict="m2")

##        if results:
##            for result in results:
##    ##            pprint.pprint(result)
##                link = result["link"]
##                print(link + "\t" + term)
##            
##            with open("./comment_communities.txt", "r+") as f:
##                import datetime
##                timestamp = ('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
##                content = f.read()
##                f.seek(0, 0)
##                f.write(timestamp +"\t"+ link +"\t"+ term.replace(" ","_") +"\n" + content)

        if results:
            for result in results:
    ##            pprint.pprint(result)
                link = result["link"]
                print(link + "\t" + term)
                import datetime
                timestamp = ('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
                new_content = timestamp +"\t"+ link +"\t"+ term.replace(" ","_") +"\n"
                
            with open("./comment_communities.txt", "r+") as f:
                old_content = f.read()
                f.seek(0, 0)
                f.write(new_content + content)

        
def do_spam_message_to_communities(site_list):
    pass

def do_spam_message_to_disqus_channel(username, password, channelURL):
    pass

def do_spam_message_to_disqus_forums(account, message, forumList):
    
    for forum in forumList():
        print(forum)
    pass
    
    

if __name__ == "__main__":
    # signup new account
    registerInfo = auto.generate_register_info()
    registerInfo["mailSessionID"] = None
    registerInfo["email"] = "ducthinhdt+1@gmail.com"
    registerInfo["webDriverOption"] = True
    registerInfo["bDeleteAllCookies"] = True
    print(registerInfo)
    disqus_signup_new_account(**registerInfo)


####    # search for website user google search api
##    search_term_list = [
####        "wnba", # no result
####        "nbl", # no result
##        "nhl",
####        "mlb", # no result
##        "ncaab",
##        "soccer",
##        "ncaaf",
##        "nfl",
##        "horse racing",
##        "football",
##        "basketball",
##        "sports",
####        "sports forcast", # no result
####        "sports predict" # no result
####        "bookie", # no result
##        "bet",
##        ]
####    search_for_disqus_sites(search_term_list, "AIzaSyDDIt9z51U2Ve34HAh8D5YNz-qzkGoyQZU", "007396311541146120664:0wvkwarjy7k") # niko
##    googleSearch_for_disqus_forums(search_term_list, "AIzaSyAE8xTk6zAQFYhQpz9ATMGUDcI34FN5KAw", "010427325042688803347:vzs1sd6l0ta") # sqt

