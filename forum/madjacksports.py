import automation9
##from guerrillamail import GuerrillaMailSession
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from PIL import Image

def get_captcha(driver, element, path):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    driver.save_screenshot(path)

    import time
    time.sleep(10) # stop to solve catcha manually

    # uses PIL library to open image in memory
    image = Image.open(path)

    left = location['x']
    top = location['y'] + 140
    right = location['x'] + size['width']
    bottom = location['y'] + size['height'] + 140

    image = image.crop((left, top, right, bottom))  # defines crop points
    image.save(path, 'jpeg')  # saves new cropped image

def get_captcha2(driver, elem, path):
    from selenium.webdriver import ActionChains
##    elem = driver.find_element_by_css_selector("#imagecpt")
    action_chain = ActionChains(driver)
    action_chain.move_to_element(elem)
    action_chain.perform()
    loc, size = elem.location_once_scrolled_into_view, elem.size
    left, top = loc['x'], loc['y']
    width, height = size['width'], size['height']
    box = (int(left), int(top), int(left + width), int(top + height))
##    screenshot = driver.get_screenshot_as_base64()
##    img = Image.open(StringIO(base64.b64decode(screenshot)))
    driver.save_screenshot(path)
    image = Image.open(path)

    captcha = image.crop(box)
    captcha.save(path, 'PNG')   

def generate_register_info():
    _username = automation9.random_username()
    _mailSession = automation9.custom_guerrilla_mail_session(username=_username)
    _email_address = _mailSession.email_address
    return {
        'email': _email_address,
        'username': _username,
        'password': "!Admin987",
        'mailSession' : _mailSession,
        }
    
##    automation9.get_guerrilla_mail_session()
##    email = n   
##    username = 
##    password = "!Admin987"
    
    return asession

def signup_new_account(**kwargs):
    driver = webdriver.Chrome(executable_path=r"D:\01_software\chromedriver_win32\chromedriver.exe")
    driver.get("http://www.madjacksports.com/forum/register.php")
    select = Select(driver.find_element_by_id('month')).select_by_value("02")
    select = Select(driver.find_element_by_id('day')).select_by_value("28")
    element = driver.find_element_by_id("year")
    element.send_keys("1988")
    element.submit()    # 'Proceed...'
    import time
    time.sleep(0.5)

    driver.find_element_by_id("regusername").send_keys(kwargs['username'])
    driver.find_element_by_id("password").send_keys(kwargs['password'])
    driver.find_element_by_id("passwordconfirm").send_keys(kwargs['password'])
    driver.find_element_by_id("email").send_keys(kwargs['email'])
    driver.find_element_by_id("emailconfirm").send_keys(kwargs['email'])
    import time
    time.sleep(2) # stop to solve catcha manually
    img = driver.find_element_by_id("imagereg")
    automation9.get_captcha(driver, img, "captcha.png")
    
    driver.find_element_by_id("cfield_7").send_keys("A")
    element = driver.find_element_by_id("cb_rules_agree")
    element.click()
    element.submit()

    # after signup then click on signup link send to email
    # if register successfully then store to local file
    
if __name__ == "__main__":
####    registerInfo = generate_register_info()
####    print(registerInfo)
##    registerInfo = {'password': '!Admin987', 'email': 'GaryNatcher138@guerrillamailblock.com', 'username': 'GaryNatcher138'}
##    signup_new_account(**registerInfo)

##    from captcha2upload.captcha2upload import CaptchaUpload
##    import captcha2upload
    from captcha2upload.captcha2upload import *
    captcha = CaptchaUpload("7db8a59bcb89211a9a94d6829239b239")
    print(captcha.getbalance())
    
