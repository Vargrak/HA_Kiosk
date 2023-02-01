#Lilith Ernst
#Version 2-1-2023
#Free to Use and Distribute, No Warranty is Provided

#Uses Firefox
#Continuously starts a kiosk instance of firefox to load a home assistant webpage
#This is only meant to run on linux

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, os

def firefox_defines():
    global driver
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.privatebrowsing.autostart", True)
    options = webdriver.FirefoxOptions()
    options.add_argument("-kiosk")
    driver = webdriver.Firefox(executable_path="/usr/bin/geckodriver", firefox_profile=profile, options=options)

def ha_webpage():
    driver.get(ha_url)
    username_get()
    password_get()

def username_get():
    global username
    try:
        username = driver.find_element("xpath", "//*[@id='username']")
        username.clear()
        username.send_keys(ha_user)
    except:
        username_get()

def password_get():
    global password
    try:
        password = driver.find_element("xpath", "//*[@id='password']")
        password.clear()
        password.send_keys(ha_pass)
        password.send_keys(Keys.RETURN)
    except:
        password_get()
        
def check_if_ha_server_up():
    global ha_ip
    return os.system(f"ping -q -c 1 -W 3000 {ha_ip}") == 0
        
def check_if_still_logged_in():
    global disconnected
    global ping
    
    print("Checking...")
    print(f"Status: Disconnected:{disconnected}, Ping:{ping}")
    print(f"{os.system(f'ping -q -c 1 -W 3000 {ha_ip}')}")
    
    ping = check_if_ha_server_up()
    if (ping and not disconnected):
        print(f"Connected")
        try:
            driver.find_elements_by_xpath("//*[contains(text(), 'Terminal')]")
            if (not ha_ip in driver.current_url or "auth" in driver.current_url): #If you are having problems
                raise Exception("Not on page!")
            
        except:
            print("Not logged in!")
            
            try:
                driver.close()
            except:
                pass
            
            firefox_defines()
            ha_webpage()
            
    
    elif (not disconnected and not ping):
        print(f"Disconnected")
        disconnected = True
        
    elif (disconnected and ping):
        print(f"Reconnected")
        disconnected = False
        
        try:
            driver.close()
        except:
            pass
        
        firefox_defines()
        ha_webpage()
        
        
def main_run():
    global ping, disconnected
    global ha_url, ha_pass, ha_user, ha_ip
    
    #Must set all of these to work.
    ha_url = "" #Browser URL of home assistant.    Ex: "http://192.168.1.50:8123/"
    ha_user = "" #Username to log in with.         Ex: "Bob"
    ha_pass = "" #Password for the account.        Ex: "1234pass"
    ha_ip = "" #IP for the home assistant server.  Ex: "192.168.1.50"
    
    disconnected = False
    ping = check_if_ha_server_up()
    
    firefox_defines() #Starts firefox and puts it into kiosk mode
    ha_webpage() #Attempts to log in
    
    while True:
        time.sleep(10) #Time in seconds before it checks if disconncted, logged out, or not on the HA page
        check_if_still_logged_in()

if __name__ == '__main__':
    main_run()

