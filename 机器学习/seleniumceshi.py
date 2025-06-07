import os
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def run_chrome_automation():
    # 设置Chrome浏览器选项
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 无头模式，取消注释可启用
    chrome_options.add_argument("--start-maximized")  # 窗口最大化
    
    # 创建临时用户数据目录
    temp_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    
    # 指定Chrome驱动路径
    driver_path = r"D:\javaweb\demo\src\main\chromedriver\chromedriver.exe" 
    service = Service(driver_path)
    
    # 创建Chrome浏览器实例
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # 打开百度搜索页面
        driver.get("https://www.baidu.com")
        time.sleep(1)  # 等待页面加载

        # 1. 通过ID定位搜索框并输入"程允锋"
        search_box = driver.find_element(By.ID, "kw")
        search_box.send_keys("程允锋")
        driver.find_element(By.ID, "su").click()
        time.sleep(5)
        print("通过ID搜索结果:", driver.title)

        # 返回首页
        driver.get("https://www.baidu.com")
        time.sleep(1)

        # 2. 通过NAME定位搜索框并输入"程允锋"
        driver.find_element(By.NAME, "wd").send_keys("程允锋")
        driver.find_element(By.ID, "su").click()
        time.sleep(5)
        print("通过NAME搜索结果:", driver.title)

        # 返回首页
        driver.get("https://www.baidu.com")
        time.sleep(1)

        #3. 通过CLASS定位搜索框并输入"程允锋"
        driver.find_element(By.CLASS_NAME, "s_ipt").send_keys("程允锋")
        driver.find_element(By.ID, "su").click()
        time.sleep(5)
        print("通过CLASS搜索结果:", driver.title)

        # 其他定位方式示例（以百度页面元素为例）
        driver.get("https://www.baidu.com")
        time.sleep(1)

        #4. 通过TAG定位搜索框并输入"程允锋"
        inputs = driver.find_elements(By.TAG_NAME, "input")
        for input_elem in inputs:
            if input_elem.get_attribute("name") == "wd":
                input_elem.send_keys("程允锋")
                driver.find_element(By.ID, "su").click()
                break
        time.sleep(5)
        print("通过TAG搜索结果:", driver.title)

        #5. 通过LINK TEXT定位并点击"新闻"链接
        driver.get("https://www.baidu.com")
        driver.find_element(By.LINK_TEXT, "新闻").click()
        time.sleep(5)
        print("通过LINK TEXT跳转结果:", driver.title)

        #6. 通过PARTIAL LINK TEXT定位并点击"地"链接（地图）
        driver.get("https://www.baidu.com")
        driver.find_element(By.PARTIAL_LINK_TEXT, "地").click()
        time.sleep(5)
        print("通过PARTIAL LINK TEXT跳转结果:", driver.title)

        #7. 通过CSS SELECTOR定位搜索框并输入"程允锋"
        driver.get("https://www.baidu.com")
        driver.find_element(By.CSS_SELECTOR, "#kw").send_keys("程允锋")
        driver.find_element(By.CSS_SELECTOR, "#su").click()
        time.sleep(5)
        print("通过CSS SELECTOR搜索结果:", driver.title)

       # 8. 通过XPATH定位搜索框并输入"程允锋"
        driver.get("https://www.baidu.com")
        driver.find_element(By.XPATH, "//input[@id='kw']").send_keys("程允锋")
        driver.find_element(By.XPATH, "//input[@id='su']").click()
        time.sleep(5)
        print("通过XPATH搜索结果:", driver.title)

    except Exception as e:
        print(f"测试过程中发生错误: {e}")
    finally:
        # 关闭浏览器
        print("测试完成，关闭浏览器")
        driver.quit()
        
        # 清理临时目录
        try:
            if os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
                print(f"临时用户数据目录已删除: {temp_dir}")
        except Exception as e:
            print(f"清理临时目录时出错: {e}")

if __name__ == "__main__":
    run_chrome_automation()