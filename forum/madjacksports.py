import automation9
from captcha2 import CaptchaUpload
from guerrillamail import GuerrillaMailSession
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from PIL import Image   

def generate_register_info():
    _username = automation9.random_username()
    _mailSession = automation9.custom_guerrilla_mail_session(username=_username)
    _email_address = _mailSession.email_address
    return {
        'email': _email_address,
        'username': _username,
        'password': "!Admin987",
        'mailSessionID' : _mailSession.session_id,
        }

def get_verification_link(mailSessionID=None, subjectPattern=None, linkPattern=r"", mailService="Guerrilla"):
    import re
    if mailService == "Guerrilla":
        from guerrillamail import GuerrillaMailSession
        _mailSession = GuerrillaMailSession(mailSessionID)
        for mail in _mailSession.get_email_list():
            print("============")
            print(mail.guid)
            if subjectPattern in mail.subject:
                fetch_mail = _mailSession.get_email(mail.guid)
                body = fetch_mail.body
                m = re.search(linkPattern, body)
                if m:
                    link = m.group('veri_link')
                    print("LINK FOUND: "+link)
                    return link
    return 

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
        print("mailSessionID="+mailSessionID)
        subjectPattern = "Action Required to Activate Membership for MadJack Sports Forums"
        linkPattern = r'<a href="(?P<veri_link>.*a=act.*?)">'
        link = get_verification_link(mailSessionID, subjectPattern, linkPattern)
        print("LINK="+link)
        time.sleep(2) # wait for verification email
        import requests
        r = requests.get(link)
        print(r.status_code)
        
    
    # if register successfully then store to local file
    with open("./emails.txt", "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(email + "\t" + "madjacksports" +"\n" + content)
    
if __name__ == "__main__":
######    registerInfo = generate_register_info()
######    print(registerInfo)
####    registerInfo = {'password': '!Admin987', 'email': 'GaryNatcher138@guerrillamailblock.com', 'username': 'GaryNatcher138'}
####    signup_new_account(**registerInfo)
##
####    from captcha2upload.captcha2upload import CaptchaUpload
####    import captcha2upload
##    captcha = CaptchaUpload("7db8a59bcb89211a9a94d6829239b239")
##    print(captcha.solve("captcha.png").replace(" ",""))
##    print(captcha.getbalance())
    
    registerInfo = generate_register_info()
##    registerInfo["email"] = "vaqrxqgv@sharklasers.com"
    print(registerInfo)
    madjacksports_signup_new_account(**registerInfo)

##    with open("./mailBody.txt", "r+") as rf:
##        import re
##        content = rf.read()
##        print(content)
##        linkPattern = r'^<a href="(?P<veri_link>.*a=act.*?)">'
##        m = re.search(linkPattern, content)
##        if m:
##            print("FOUND")
##            print(m.group('veri_link'))


    

##    text = 'http://www.madjacksports.com/forum/register.php?a=act&amp;u=493869&amp;i=0b7b61158e71772fa7e53da3dcfe11316c82d83c">http://www.madjacksports.com/forum/register.php?a=act&amp;u=493869&amp;i=0b7b61158e71772fa7e53da3dcfe11316c82d83c</a>'
##    pattern = r'^<a href="(?P<veri_link>.*?)">'
##    get_verification_link(mailSessionID, subjectPattern, linkPattern=r"")
    
##    aSession = GuerrillaMailSession("9qf5f8ffjrv40t824k2b1kq0i3")
##    print(aSession.email_timestamp)
##    get_verification_link(aSession, "", "")
    
    
