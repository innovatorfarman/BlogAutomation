from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# path = 'C:\\Users\farma\Downloads\chromedriver'
# driver = webdriver.Chrome(path)
def AutoPost():
    df = pd.read_excel('a.xlsx')
    title = "Quis autem vel eum iure reprehenderit"
    description = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium"
    content ="Lorem ipsum dolor <a href='#'>sit</a> amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"

    Message = []
    websites =[]
    for i in range(28,len(df)):
        try:
            url = df.url[i]
            websites.append(df.url[i])
            driver.get(url)
            driver.implicitly_wait(15)
            #loggin
            username = driver.find_element(By.NAME,'username')
            password = driver.find_element(By.NAME,'password')
            try:
                login = driver.find_element(By.XPATH, '//button[text()="Login"]')
            except:
                login = driver.find_element(By.XPATH, '//div[contains(@class,"login")]//button[@type="submit"]')
            time.sleep(1)
            action = ActionChains(driver)
            action.click(username).perform()
            action.send_keys(df.User[i]).perform()
            time.sleep(0.5)
            action.click(password).perform()
            action.send_keys(df.Password[i]).perform()
            time.sleep(0.5)
            action.click(login).perform()
            time.sleep(10)

            #New Blog Post Link
            post_url = "https://"+url.split('/')[2] + "/create-blog/"
            driver.get(post_url)
            time.sleep(5)

            # Title and description element
            action = ActionChains(driver)
            blog_title = driver.find_element(By.XPATH,'//*[@id="blog_title"]') #.send_keys('This is an awesome blog title')
            blog_desc=""
            try:
                blog_desc = driver.find_element(By.XPATH,'//*[@id="new-blog-desc"]') #.send_keys('This is an awesome blog description')
            except:
                print("No Description")
           
           #Blog Image
            driver.find_element(By.XPATH,"//input[@type='file']").send_keys('C://Users/farma/Downloads/light.jpg')
            
            #Blog Tag Element
            blog_tag = driver.find_element(By.CLASS_NAME,'bootstrap-tagsinput')

            action.send_keys_to_element(blog_title,title).perform()
            if blog_desc is not None:
                action.send_keys_to_element(blog_desc,description).perform()
            
            #Blog Category
            select_cat = Select(driver.find_element(By.ID,'blog_category'))
            select_cat.select_by_value('2')

            #Blog Tag
            action.send_keys_to_element(blog_tag,"#Trending").perform()

            #Blog Content
            try:
                blog_content = driver.find_element(By.XPATH,'//*[@name="blog_content"]')
                action.send_keys_to_element(blog_content,content).perform()  
            except:
                driver.find_element(By.ID,'blog_ifr').click()
                action.send_keys(content).perform()

            # ===== Publish Button =====
            action = ActionChains(driver)
            try:
                pbtn = driver.find_element(By.CLASS_NAME,'btn btn-main setting-panel-mdbtn')
                print("pbtn: classname")
            except:
                try:
                    pbtn =driver.find_element(By.XPATH, '//button[contains(text(),"Publish")]')
                    print("pbtn: contains publish")
                except:
                    pbtn =driver.find_element(By.XPATH, '//*[@id="insert-blog"]/div[3]/button') 
                    print("pbtn: insert-blog id")

            action.click(pbtn).perform()
            time.sleep(15)
            url = driver.current_url
            if url:
                Message.append(f"{url}")
            else:
                Message.append(f"Posted: Link Unavailable")
        except Exception as e:
            Message.append(str(e)[0:200])


        res = {"Website": websites,"Message/Update":Message}
        res_df = pd.DataFrame(res)
        res_df.to_csv(f'file.csv')

if __name__ == "__main__":
    AutoPost()