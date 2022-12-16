from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# path = 'C:\\Users\farma\Downloads\chromedriver'
# driver = webdriver.Chrome(path)
def AutoPost():
    df = pd.read_excel('article_websites.xlsx')

    Message = []
    websites =[]
    for i in range(len(df)):
        try:
            url = 'https://' + df.url[i] + '/'
            websites.append(df.url[i])
            driver.get(url)
            time.sleep(5)
            username = driver.find_element(By.NAME,'username')
            password = driver.find_element(By.NAME,'password')
            login = driver.find_element(By.XPATH, '//button[text()="Login"]')

            action = ActionChains(driver)
            action.send_keys_to_element(username,df.User[i]).perform()
            action.send_keys_to_element(password,df.Password[i]).perform()
            action.click(login).perform()
            time.sleep(10)

            driver.get(url + 'create-blog/')
            time.sleep(5)

            # blog_title = driver.find_element(By.XPATH,'//*[@id="blog_title"]')
            # blog_desc = driver.find_element(By.XPATH,'//*[@id="new-blog-desc"]')

            action = ActionChains(driver)
            blog_title = driver.find_element(By.XPATH,'//*[@id="blog_title"]') #.send_keys('This is an awesome blog title')
            blog_desc = driver.find_element(By.XPATH,'//*[@id="new-blog-desc"]') #.send_keys('This is an awesome blog description')
            blog_content = driver.find_element(By.XPATH,'//*[@name="blog_content"]')
            img_div = driver.find_element(By.XPATH,'//div[@data-block="thumdrop-zone"]')
            blog_image = driver.find_element(By.XPATH,"//input[@type='file']").send_keys('C://Users/farma/Downloads/light.jpg')
            blog_tag = driver.find_element(By.CLASS_NAME,'bootstrap-tagsinput')
            publish_btn = driver.find_element(By.XPATH, '//button[text()="Publish"]')

            action.send_keys_to_element(blog_title,"This is awesome post title").perform()
            action.send_keys_to_element(blog_desc,"This is an awesome blog description").perform()
            action.send_keys_to_element(blog_content,"This is an awesome blog content").perform()
            select_cat = Select(driver.find_element(By.ID,'blog_category'))
            select_cat.select_by_value('2')
            action.send_keys_to_element(blog_tag,"Trending").perform()

            action.click(publish_btn).perform()
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