from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--username', type=str, required=True,  help='username')
parser.add_argument('--pwd', type=str, required=True,  help='pwd')
args = parser.parse_args()

#url = "https://24h.pchome.com.tw/prod/DGBJG9-A900B51SM?fq=/S/DGBJG9"
url = "https://24h.pchome.com.tw/prod/DGBJGB-1900AZWIA?fq=/S/DGBJGB"


options = webdriver.ChromeOptions()
prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            }
}
options.add_experimental_option('prefs', prefs) 
options.add_argument("disable-infobars") 
options.add_argument("--headless")  # 不開啟實體瀏覽器背景執行


driver = webdriver.Chrome()
driver.get(url)

# Get Product Name

product_name = driver.find_element(By.ID,"NickContainer")

print(product_name.text)


# Get Product Price

product_price = driver.find_element(By.ID, "PriceTotal")
print(product_price.text)

# Add Product to Cart

try:
    add_to_cart_btn = WebDriverWait(driver, 1, 0.5).until(EC.presence_of_element_located((By.XPATH, "//li[@Id='ButtonContainer']//button//span[text()='購物車']")))
    #add_to_cart_btn = driver.find_element(By.XPATH, "//li[@Id='ButtonContainer']//button//span[text()='購物車']")
    btn_Is_Exist = True
    print('可以購買!')
    loop_start = True
    loop_Max = 1

except:
    print('還不能購買! 重新整理!')
    btn_Is_Exist = False
    loop_start = True
    loop_Max = 20

loop_cnt=0
while loop_start:
        loop_cnt+=1
        if loop_cnt > loop_Max:
            print("林北不買了! 看!")
            break

        if btn_Is_Exist:
            add_to_cart_btn.click()
            # Go to Cart List
            link_to_cart = driver.find_element(By.XPATH, "//a[@class='cart']")
            print(link_to_cart.get_attribute('href'))
            # link_to_cart.click()
            driver.get(link_to_cart.get_attribute('href'))
            driver.implicitly_wait(10)
            # Login
            element = driver.find_element(By.ID,"loginAcc")
            element.send_keys(args.username) # Input Your Account
            element = driver.find_element(By.ID,"loginPwd")
            element.send_keys(args.pwd) # Input Your Psw
            element = driver.find_element(By.ID, "btnLogin")
            element.click()
            driver.implicitly_wait(10)
            # press the pipay_btn
            pipay_btn = driver.find_element(By.XPATH, "//li[@class='PI']//a[@title='Pi 拍錢包']") 
            pipay_btn.click()
            driver.implicitly_wait(3)
            # press the popup window to countinue
            continue_btn = driver.find_element(By.XPATH, "//a[@id='btnSubmit']")
            print(continue_btn.text)
            continue_btn.click()
            driver.implicitly_wait(5)
            # How to deal with unexpect pop up window ????
            # Issue not solve
            # check if the pop up windows is shown
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present(),
                'Timed out waiting for PA creation ' +
                'confirmation popup to appear. ')
                alert = driver.switch_to.alert
                alert.accept()
                print("alert accepted")
                driver.implicitly_wait(5)
            except TimeoutException:
                print("no alert")
            # Confirm personal infomation
            # press confirm btn
            confirm_btn = driver.find_element(By.XPATH, "//a[@id='btnSubmit']")
            print(confirm_btn.text)
            confirm_btn.click()
            driver.implicitly_wait(5)
            # Generator An Purchase QRCode
            qrcode_url = driver.find_element(By.XPATH,"//div[@class='open_info']/a").get_attribute('href')
            print(qrcode_url)
            driver.get(qrcode_url)
        else:
            driver.implicitly_wait(5)
            print('Refresh this page '+ str(loop_cnt))
            driver.refresh()
            time.sleep(1)
else:
        input("press enter to finish this thread")
        driver.quit()