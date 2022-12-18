from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.implicitly_wait(5)

# path = 'C:\\Users\farma\Downloads\chromedriver'
# driver = webdriver.Chrome(path)
def AutoPost():
    df = pd.read_excel('a.xlsx')
    title = "Quis autem vel eum iure reprehenderit"
    description = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium"
    image = 'C://Users/farma/Downloads/light.jpg'

    # All html inside single quotes
    content = '<h1>Yi Zeng</h1> <a href="https://google.com">Link</a> Post' 

    Message = []
    websites =[]
    sites = []
    link = []
    for i in range(18,19):
        try:
            url = df.url[i]
            websites.append(df.url[i])
            driver.get(url)
            #loggin
            time.sleep(5)
            try:
                username =driver.find_element(By.NAME,"username")
            except:
                username =driver.find_element(By.XPATH,'//*[@id="login"]/div[2]/label[1]/input')
            try:
                password = driver.find_element(By.NAME,"password")
            except:
                password =driver.find_element(By.XPATH,'//*[@id="login"]/div[2]/label[2]/input')

            time.sleep(5)
            driver.execute_script("arguments[0].scrollIntoView(true);", username)

            action = ActionChains(driver)
            action.click(username).perform()
            action.send_keys(df.User[i]).perform()

            time.sleep(0.5)
            action.click(password).perform()
            action.send_keys(df.Password[i]).perform()
            time.sleep(0.5)

            try:
                login = driver.find_element(By.XPATH, '//button[text()="Login"]')
            except:
                login = driver.find_element(By.XPATH, '//div[contains(@class,"login")]//button[@type="submit"]')
            action.click(login).perform()

            time.sleep(10)

            #New Blog Post Link
            post_url = "https://" + url.split('/')[2] + "/create-blog/"
            driver.get(post_url)
            time.sleep(5)

            # Blog Title
            action = ActionChains(driver)
            blog_title = driver.find_element(By.XPATH,'//*[@id="blog_title"]') #.send_keys('This is an awesome blog title')
            action.send_keys_to_element(blog_title,title).perform()


            #Blog Description
            blog_desc=""
            try:
                blog_desc = driver.find_element(By.XPATH,'//*[@id="new-blog-desc"]') #.send_keys('This is an awesome blog description')
            except:
                pass
           
            if blog_desc is not None:
                action.send_keys_to_element(blog_desc,description).perform()

           #Blog Image
            driver.find_element(By.XPATH,"//input[@type='file']").send_keys(image)
            
            
            #Blog Category
            category_element = driver.find_element(By.ID,'blog_category')
            select_cat = Select(category_element)
            select_cat.select_by_value('2')

            driver.execute_script("arguments[0].scrollIntoView(true);", category_element)

            #Blog Tag Element
            try:
                blog_tag = driver.find_element(By.CLASS_NAME,'bootstrap-tagsinput')
            except:
                blog_tag = driver.find_element(By.NAME,'blog_tags')
            #Blog Tag
            action.click(blog_tag).perform()
            action.send_keys("#Trending").perform()

            #Blog Content
            try:
                blog_content = driver.find_element(By.XPATH,'//*[@name="blog_content"]')
                action.click(blog_content).perform()
                driver.execute_script(f"tinyMCE.activeEditor.setContent('{content}')")
                 
            except:
                # driver.find_element(By.ID,'blog_ifr').click()
                # action.send_keys(content).perform()
                cframe = driver.find_element(By.ID,'blog_ifr')
                action.click(cframe).perform()
                driver.execute_script(f"tinyMCE.activeEditor.setContent('{content}')")

            # ===== Publish Button =====
            action = ActionChains(driver)
            try:
                pbtn = driver.find_element(By.CLASS_NAME,'btn btn-main setting-panel-mdbtn')
                print("Published: classname")
            except:
                try:
                    pbtn =driver.find_element(By.XPATH, '//button[contains(text(),"Publish")]')
                    print("published: contains publish")
                except:
                    pbtn =driver.find_element(By.XPATH, '//*[@id="insert-blog"]/div[3]/button') 
                    print("published: insert-blog id")
            
            driver.execute_script("arguments[0].scrollIntoView(true);", pbtn)
            action.click(pbtn).perform()
            time.sleep(30)
            url = driver.current_url
            sites.append(df.url[i])
            if url:
                Message.append(f"{url}")
                link.append(f"Published: {url}")
            else:
                Message.append(f"Posted: Link Unavailable")
        except Exception as e:
            Message.append(str(e)[0:120])


        res = {"Website": websites,"Message/Update":Message}
        res_df = pd.DataFrame(res)
        res_df.to_excel('file.xlsx')
        report = {"Website":sites,"Url":link}
        report_df = pd.DataFrame(report)
        report_df.to_excel("Link_Report.xlsx")
    driver.quit()

if __name__ == "__main__":
    AutoPost()