from automation9 import Automation9
from selenium import webdriver
import time
from guerrillamail import GuerrillaMailSession

auto = Automation9()

def bettingtalk_signup_new_account(username=None, email=None, password="!Admin987", mailSessionID=None):
    driver = webdriver.Chrome(executable_path=r"D:\01_software\chromedriver_win32\chromedriver.exe")
    driver.get("http://www.bettingtalk.com/forum/register.php")
    driver.find_element_by_id("email").send_keys(email)
    elem = driver.find_element_by_id("emailconfirm")
    elem.send_keys(email)
    elem.submit()
    
    import time
    time.sleep(10) # wait for verification email

    # click on signup link sent to email
    if mailSessionID is not None:
        time.sleep(2) # wait for verification email
        print("mailSessionID="+mailSessionID)
        subjectPattern = "verification code in Betting Talk - Sports betting forum and news"
        linkPattern = r'(?P<veri_link>http.*)">'
        link = auto.MAIL_get_verification_link(mailSessionID, subjectPattern, linkPattern)
        import requests
        if link is not None:
            r = requests.get(link)
            print(r.status_code)

    driver.find_element_by_id("regusername").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("passwordconfirm").send_keys(password)
    

if __name__ == "__main__":
    registerInfo = auto.generate_register_info()
##    registerInfo["email"] = "xawbaqya@sharklasers.com"
    registerInfo["email"] = "zejpctku@sharklasers.com"
##    registerInfo["mailSessionID"] = "jq1cuhoqbdu6j1ma2kb94v0pe3"
    print(registerInfo)
    bettingtalk_signup_new_account(**registerInfo)
