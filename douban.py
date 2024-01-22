
"""
创建一个浏览器驱动
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from time import sleep
import pandas as pd
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# 指定Edge浏览器驱动的位置
edge_driver_path = r"D:\jupyter\网络数据爬取\MicrosoftWebDriver.exe"


edge_options = Options()
edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
edge_options.add_experimental_option("useAutomationExtension", False)
edge_options.add_argument("--headless")
edge_options.add_argument("--disable-gpu")
# 创建并启动Edge浏览器服务对象
service = Service(edge_driver_path)
bro = webdriver.Edge(options=edge_options, service=service)

# 注入JS脚本以绕过webdriver检测
bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """
})
keyword = input('管理咨询')
url = f'https://search.douban.com/book/subject_search?search_text={keyword}&cat=1001/'
bro.get(url)
data = []

"""这里确定翻页数量"""
for m in range(120):
    try:

        """
        开始获取信息
        """
        bro.switch_to.window(bro.window_handles[-1])
        print(bro.current_url)
        title_elements = WebDriverWait(bro, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item-root")))
        for title_element in title_elements:
            con = []
            """获取书名"""
            try:
                title = title_element.find_element(By.CLASS_NAME, "title").text
                #print(title)
                con.append(title)
            except:
                con.append(' ')

            """获取评分"""

            try:
                rate = title_element.find_element(By.CLASS_NAME, "rating_nums").text
                #print(rate)
                con.append(rate)
            except:
                con.append(' ')

            """获取评分人数"""

            try:
                pl = title_element.find_element(By.CLASS_NAME, "pl").text
                #print(pl)
                con.append(pl)
            except:
                con.append(' ')

            """获取作者等详情信息"""

            try:
                abstract = title_element.find_element(By.CLASS_NAME, "abstract").text.split('/')

                """获取日期信息"""
                try:
                    r = 0
                    for item in abstract:
                        if '-' in item:
                            con.append(item)
                            abstract.remove(item)
                            #print('日期',item)
                            r+=1
                            break
                    if r==0:
                        con.append(' ')     
                except:
                    pass

                """获取价格信息"""
                try:
                    j = 0
                    for item in abstract:
                        if '元' in item:
                            con.append(item.replace('元',''))
                            abstract.remove(item)
                            #print('价格',item)
                            j +=1
                            break
                    if j==0:
                        con.append(' ')             
                except:
                    pass

                """获取出版社信息"""
                try:
                    c = 0
                    for item in abstract:
                        if '出版社' in item:
                            con.append(item)
                            abstract.remove(item)
                            #print('出版社',item)
                            c +=1
                            break
                    if c ==0:
                        con.append(' ') 
                except:
                    pass

                """获取作者信息"""

                try:
                    my_list = abstract
                    text = ','.join(my_list)
                    con.append(text)
                    #print('作者',text)
                except:
                    con.append(' ')

            except:
                pass

            data.append(con)    
            #print(len(data))
            """
            记录文件表
            """
            df = pd.DataFrame(data, columns=['书名', '评分', '评分人数', '日期', '价格', '出版社', '作者'])
            df.to_excel(f'{keyword}书籍信息收集表.xlsx', index=False)
        print(f'{keyword}第{m+1}页数据获取完毕')

        """翻页"""

        nextbutton = WebDriverWait(bro, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='next']")))
        action = ActionChains(bro)
        action.move_to_element(nextbutton).click().perform()
        sleep(2)
    except:
        pass

