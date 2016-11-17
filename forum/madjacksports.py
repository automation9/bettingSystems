import automation9
from captcha2 import CaptchaUpload
from guerrillamail import GuerrillaMailSession
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from PIL import Image   

def madjacksports_signup_new_account(username=None, email=None, password="!Admin987", mailSessionID=None):
    """
    mailSessionID: used for "Click on link to verify user"
    """
    driver = webdriver.Chrome(executable_path=r"D:\01_software\chromedriver_win32\chromedriver.exe")
    driver.get("http://www.madjacksports.com/forum/register.php")
    select = Select(driver.find_element_by_id('month')).select_by_value("02")
    select = Select(driver.find_element_by_id('day')).select_by_value("28")
    element = driver.find_element_by_id("year")
    element.send_keys("1988")
    element.submit()    # 'Proceed...'
    import time
    time.sleep(0.5)

    driver.find_element_by_id("regusername").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("passwordconfirm").send_keys(password)
    driver.find_element_by_id("email").send_keys(email)
    driver.find_element_by_id("emailconfirm").send_keys(email)
##    import time
##    time.sleep(2) # stop to solve catcha manually
    img = driver.find_element_by_id("imagereg")
    automation9.screenshot_captcha(driver, img, "captcha.png")
    captcha = CaptchaUpload("7db8a59bcb89211a9a94d6829239b239")
    captcha_value = captcha.solve("captcha.png").replace(" ","")
    print(captcha_value)
    driver.find_element_by_id("imageregt").send_keys(captcha_value)
    
    driver.find_element_by_id("cfield_7").send_keys("A")
    driver.find_element_by_id("cfield_6").send_keys(username)
    element = driver.find_element_by_id("cb_rules_agree")
    element.click()
    element.submit()
    import time
    time.sleep(10) # wait for verification email
    #{{The string you entered for the image verification did not match what was displayed.}}
    if "The string you entered for the image verification did not match what was displayed." in driver.page_source:
        return False

    # after signup then click on signup link send to email
    if mailSessionID is not None:
        time.sleep(2) # wait for verification email
        print("mailSessionID="+mailSessionID)
        subjectPattern = "Action Required to Activate Membership for MadJack Sports Forums"
        linkPattern = r'<a href="(?P<veri_link>.*a=act.*?)">'
        link = automation9.MAIL_get_verification_link(mailSessionID, subjectPattern, linkPattern)
        import requests
        r = requests.get(link)
        print(r.status_code)
        
    
    # if register successfully then store to local file
    with open("./forum_accounts.txt", "r+") as f:
        import datetime
        timestamp = ('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
        content = f.read()
        f.seek(0, 0)
        f.write(timestamp +"\t"+ email +"\t"+ "madjacksports" +"\n" + content)
    
if __name__ == "__main__":   
    registerInfo = automation9.generate_register_info()
##    registerInfo["email"] = "vaqrxqgv@sharklasers.com"
    print(registerInfo)
    madjacksports_signup_new_account(**registerInfo)
    
    
