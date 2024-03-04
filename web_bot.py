#-*- coding: utf8 -*-
import time
import base64
import ddddocr
import sys
import re
import os
import lxml
from bs4 import BeautifulSoup
import yaml

# 1. 导入 WebBotMain 类
from AiBot import WebBotMain

with open('USERINFO.yaml',encoding='utf-8') as file1:
    data = yaml.load(file1,Loader=yaml.FullLoader)#读取yaml文件
    print(data)

USERNAME = data["用户名"]
PASSWORD = data["密码"]
BROWSER = data["浏览器"]
LEARNED = data["本次学习"]
CRONTAB_TIME = data["定时执行"]

# 2. 自定义一个脚本类，继承 WebBotMain
class CustomWebScript(WebBotMain):
    # 3. 设置等待参数
    # 3.1 设置等待时间
    wait_timeout = 3
    # 3.2 设置重试间隔时长
    interval_timeout = 0.5

    # 4. 设置日志等级
    log_level = "INFO"  # "DEBUG"

    # 5. 设置方法超时是否抛出异常
    raise_err = False  # True

    # 定义OCR识别
    ocr = ddddocr.DdddOcr()

    # 今日未学个数
    unlearned = 0

    # 今日总学分数
    total_core = 10

    def oneday_watch(self):
        # 打开主页
        self.goto("https://www.ynsgbzx.cn/index.aspx")
        home_page_id = self.get_current_page_id()

        while True:
            try:
                time.sleep(self.wait_timeout)
                if self.get_element_text('//*[@id="go"]') == '退出系统':
                    print("登录成功！")
                    break
                # 清空输入框
                self.clear_element('//*[@id="LoginView1_Login1_UserName"]')
                self.clear_element('//*[@id="LoginView1_Login1_Password"]')
                self.clear_element('//*[@id="LoginView1_Login1_txtValidate"]')

                self.send_keys('//*[@id="LoginView1_Login1_UserName"]', USERNAME)
                self.send_keys('//*[@id="LoginView1_Login1_Password"]', PASSWORD)

                # 获取登录验证码
                check_code = self.image_check('//*[@id="ImageCheck"]')
                print('识别出的验证码为：' + check_code)
                # 填入验证码
                self.send_keys('//*[@id="LoginView1_Login1_txtValidate"]', check_code)

                # 点击登录
                self.click_element('//*[@id="LoginView1_Login1_LoginButton"]')
                time.sleep(self.wait_timeout)

                if self.click_alert(True):
                    print("点击确定!")
                    time.sleep(self.wait_timeout)
                    
            except Exception as e:
                print("出现错误，等待 %s %ss" % (e, self.wait_timeout))
                time.sleep(self.wait_timeout)

        # 点击个人空间
        time.sleep(self.wait_timeout)
        print('点击个人空间')
        self.click_element('//*[@id="navbar"]/ul[1]/li[6]/a')
        time.sleep(self.wait_timeout)

        if LEARNED != "选修":
            # 必修课学习
            try:
                page_message = self.get_element_text('//*[@id="MyCourseList1_AspNetPager1"]/div[1]')
                total_page = re.findall(r'共(\d+)页', page_message)[0]
                print("一共有", total_page, "页", "，课件数：", re.findall(r'课件数：(\d+)', page_message)[0])
            except:
                print("没有找到必修课！")
                return
        else:
            # 选修课学习
            print("切换选修课")
            try:
                self.click_element('//*[@id="lbxx"]')
                time.sleep(self.wait_timeout)
                page_message = self.get_element_text('//*[@id="MyCourseList4_AspNetPager1"]/div[1]')
                total_page = re.findall(r'共(\d+)页', page_message)[0]
                print("一共有", total_page, "页", "，课件数：", re.findall(r'课件数：(\d+)', page_message)[0])
            except:
                print("没有找到必修课！")
                return
            
        # 获取左边考核标准
        message = self.get_element_text('//*[@id="collapseone"]')
        print()
        print("-"*10)
        print(message)
        print("-"*10)
        print()

        # 获取学习分数
        mark_message = self.get_element_text('//*[@id="form1"]/div[7]/div/div[2]/div[1]/div/div[2]/p[4]/mark')
        learned = re.findall(r'(\d+\.\d+)分', mark_message)
        if learned and LEARNED != "选修":
            print('已经学习：%s分！' % learned[0])
            if float(learned[0])>=self.total_core:
                print('今日分数已学满！')
                return
            else:
                print('今日分数未满，开始学习！')
                self.unlearned = self.total_core - float(learned[0])
        elif LEARNED == "选修":
            print("选修课开始学习！")
        
        for batch in range(int(total_page)):
            print("开始学习第", batch+1, "页！")
            self.extract_url()

            time.sleep(self.wait_timeout)
            self.switch_to_page(home_page_id)
            time.sleep(self.wait_timeout)
            if LEARNED != "选修":
                self.click_element('//*[@id="MyCourseList1_AspNetPager1"]/div[2]/a[last()]')
            else:
                self.click_element('//*[@id="MyCourseList4_AspNetPager1"]/div[2]/a[last()]')
            time.sleep(self.wait_timeout)
        if LEARNED != "选修":
            print("今日学习完成！")
        else:
            print("选修课已经学习完成！")
        return


    # 6. 重写方法，编写脚本
    # 注意：此方法是脚本执行入口
    def script_main(self):
        # 6. API 演示
        # 注意：Python 版本支持的 Api 与 Nodejs 基本相同
        # 教程中仅演示部分 Api，更多 Api 请自行探索，所有 Api 均包含详细的参数要求和返回值，请自行查看。

        init_count = 0
        while True:
            time_now = time.strftime("%H:%M", time.localtime())  # 刷新
            if time_now in CRONTAB_TIME:
                self.oneday_watch()
                init_count += 1
                print("已经持续执行{}天！".format(init_count))
            elif init_count == 0:
                self.oneday_watch()
                init_count += 1
                print("已经持续执行{}天！".format(init_count))
            for char in '|/-\\':
                print(f"等待中 {char}", end="\r")
                time.sleep(0.3)

    # 验证码识别
    def image_check(self, xpath:str) -> str:
        # 截屏验证码
        image_base64 = self.save_screenshot(xpath)
        # 解码图片
        img_bytes = base64.b64decode(image_base64)
        # 识别验证码
        check_code = self.ocr.classification(img_bytes)
        
        return check_code
    
    # 获取每页的链接开始观看
    def extract_url(self):
        outer_html = self.get_element_outer_html('//*[@id="form1"]/div[7]/div/div[2]/div[2]/div[3]/div/div[1]/table/tbody')
        soup = BeautifulSoup(outer_html,'lxml')
        link_titles = soup.select('.yx-common-link')
        process = soup.select('.progress-bar-warning')
        for i,v in enumerate(process):
            temp = v.text.strip()
            if temp == '100%':
                continue
            else:
                print("开始学习：", link_titles[i].text.strip())
                course_id = re.findall('id=(\d+)', link_titles[i]['href'])[0]

                url = 'https://www.ynsgbzx.cn/play/play.aspx?course_id=' + course_id
                self.watch_video(link_titles[i].text.strip(), url)
                if LEARNED != "选修":
                    self.unlearned -= 1
                    print("当前分数：%s" % (self.total_core - self.unlearned))
                    if (self.unlearned<=0):
                        print("今日分数已学满！")
                        return
                print("开始播放下一个视频！")
                print("----------\n")
                time.sleep(self.wait_timeout*2)

    # 观看每个视频
    def watch_video(self,title, url):
        print("开始学习：%s" % title)
        self.new_page(url)
        time.sleep(self.wait_timeout)

        while True:
            # 识别验证码
            check_code = self.image_check('//*[@id="ImageCheck"]')
            self.clear_element('//*[@id="validanswer"]')
            print('识别出的验证码为：' + check_code)
            self.send_keys('//*[@id="validanswer"]', check_code)

            # 点击登录
            self.click_element('//*[@id="btnvalidanswer"]')
            time.sleep(self.wait_timeout)
            if self.click_alert(True):
                print("验证码错误!")
                time.sleep(self.wait_timeout)
            else:
                print("验证码正确")
                break

        time.sleep(self.wait_timeout)
        self.switch_to_frame('//*[@id="ifr"]')
        self.switch_to_frame('//*[@id="mainFrame"]')

        # 获取未看时间点
        unwatch_images = self.get_element_text('//*[@id="lnode"]')
        # 未学时间点：1-602-14,16-25,27-32,34-41,43-50,52-54分钟
        # 未学时间点：1-1203-7,9-20,22-32,34-40,42-43分钟
        # 未学时间点：7-14,16-46,50-50分钟
        # 未学时间点：46-73分钟
        unwatch = re.findall(r'点：(\d+)', unwatch_images)
        if unwatch:
            # 计算秒数
            time_point = (int(unwatch[0])-1) * 60
            print("检测到未看时间点，跳转到 %s 秒" % time_point)
            # 跳转到未看时间点
            self.execute_script("document.querySelector('video').currentTime=%s;" % time_point)                

        while True:
            try:
                time.sleep(2)
                # 总共时长
                total_time = self.execute_script("document.querySelector('video').duration;")

                if total_time:
                    total_time = float(total_time)
                # 实时监听进度
                curent_time = self.execute_script("document.querySelector('video').currentTime;")

                if curent_time == "0":
                    # 视频卡住
                    print("检测到视频卡住，点击恢复！")
                    self.click_element('//*[@id="container_display"]')

                if curent_time:
                    curent_time = float(curent_time)

                total_iterations = 100
                temp_iter = (curent_time / total_time) * 100
                width = os.get_terminal_size().columns
                self.print_progress_bar(iteration=temp_iter, total=total_iterations, prefix='进度:', suffix='完成', length=50)

                if total_time - 4 <= curent_time:
                    print("播放结束！")
                    self.switch_to_frame('//*[@id="ifr"]')
                    self.switch_to_main_frame()
                    time.sleep(6)
                    print("关闭当前页面！")
                    self.close_current_page()
                    break
            except Exception as e:
                print("出现错误，等待 %s %ss" % (e, self.wait_timeout))
                time.sleep(self.wait_timeout)
        
    def print_progress_bar(self, iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
        # Print a new line when progress is complete
        if iteration == total:
            print()


# 7. 执行脚本，Pycharm 中，直接右键执行
if __name__ == '__main__':
    # 启动脚本，监听 9999 号端口
    # 默认使用 Chrome 浏览器

    # local=True 时，是本地运行脚本，会自动启动 WebDriver.exe 驱动；
    # 在远端部署脚本时，请设置 local=False，手动启动 WebDriver.exe，启动 WebDriver.exe 时需指定远端 IP 或端口号；

    # 如本地部署脚本，需要传递 WebDriver 启动参数时，参考下面方式，如不需传递启动参数，则忽略：
    driver_params = {
        "browserName": BROWSER,
        "debugPort": 0,
        "userDataDir": "./UserData",
        "browserPath": None,
        "argument": None,
    }
    CustomWebScript.execute(9999, local=True, driver_params=driver_params)
