#!/usr/bin/python
# -*- coding: utf-8 -*-
import io,os,sys,time,random,thread,string,calendar

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

reload(sys)
sys.setdefaultencoding('utf8')

repeat_flag = False			# 是否每天重复（除周末）
report_time = 8				# 如果每天重复，则每天打开日报的时间（建议每天设为上午8点）
user_name = '****************'		# 域账户名
user_passwd = '****************'	# 域密码
task_index = 1                          # 要自动汇报的项目的序号（如果只有一个项目可以不用改）
default_msg = u"框架开发"		# 默认的工作描述
default_time = 10 			# 默认的工作时长


def report():
    print '开始写日报...'
    driver = webdriver.Firefox() # Get local session of firefox
    driver.get("http://timesheetv2.paic.com.cn/timesheet/")
    driver.delete_all_cookies()
    time.sleep(3)

    # 登录
    driver.find_element_by_id("j_username").clear()
    driver.find_element_by_id("j_username").send_keys(user_name)
    driver.find_element_by_id("j_password").clear()
    driver.find_element_by_id("j_password").send_keys(user_passwd)
    driver.find_element_by_name("Submit").click()   

    # 修改时间为上个工作日。
    driver.switch_to_frame("menuContent")
    cur_handle = driver.current_window_handle
    wait = WebDriverWait(driver, 20)
    wait.until(lambda driver: driver.find_element_by_id("workDate_trigger").is_displayed())   
    driver.find_element_by_id("workDate_trigger").click()
    cur_year = time.strftime('%y',time.localtime(time.time()))
    year = string.atoi(cur_year)
    cur_mon = time.strftime('%m',time.localtime(time.time()))
    mon = string.atoi(cur_mon)
    cur_date = time.strftime('%d',time.localtime(time.time()))
    date = string.atoi(cur_date)
    cur_day = time.strftime('%a',time.localtime(time.time()))    

    # 计算上个工作日的日期
    last_month = False
    if cur_day != 'Mon':  # 对于非周一，上个工作日为1天前
        if date == 1:
            mon = mon-1
            last_month = True
            date = calendar.monthrange(year, mon)[1]
        else:
            date = date-1           
    else:  # 对于周一，上个工作日为3天前
        if date <= 3:
            mon = mon-1
            last_month = True
            date = calendar.monthrange(year, mon)[1]-3+date
        else:
            date = date-3

    if last_month:  # 点击上一个月
        btns = driver.find_element_by_class_name("headrow").find_elements_by_class_name("button")
        for btn in btns:
            if btn.text == '‹':
                btn.click()
    
    # 选择上个工作日
    daysrows = driver.find_element_by_class_name("calendar").find_elements_by_class_name("daysrow")
    done_choose = False
    for daysrow in daysrows:
        days = daysrow.find_elements_by_class_name("day")
        for day in days:
            if day.text == "%d" % date:
                ActionChains(driver).click(day).perform()
                try:
                    alert = driver.switch_to_alert()
                    alert.accept()
                    done_choose = True
                    break
                except:
                    print 'no alerts display'
            if done_choose:
                break
        if done_choose:
            break

    time.sleep(5)

    # 增加一条记录
    driver.switch_to_window(cur_handle)
    driver.switch_to_frame("menuContent")
    driver.find_element_by_id("projAdd").click()

    wait.until(lambda driver: driver.find_element_by_id("projectWorkTimes[0].projectId").is_displayed())

    # 点击项目选择列表，进入选择下拉框。
    task_option = driver.find_element_by_id("projectWorkTimes[0].projectId").find_elements_by_tag_name('option')[task_index]
    task_option.click()

    # 自动填写其他内容
    driver.find_element_by_id("projectWorkTimes[0].remark").clear()
    driver.find_element_by_id("projectWorkTimes[0].remark").send_keys(default_msg)
    driver.find_element_by_id("projectWorkTimes[0].costHours").clear()
    driver.find_element_by_id("projectWorkTimes[0].costHours").send_keys(default_time)
    print "即将在 5 秒后提交，请确认昨天的工作时长。"
    time.sleep(10)

    # 提交日报并关闭 Firefox
    driver.find_element_by_id("submmit").click()
    driver.close()
    print '日报提交完成！'

    
def main():
    global time_interval
    bRunning = 0
    cur_time = -1
    last_time = -1

    if not repeat_flag:
        report()
    else:
        print "等待记日报时间（每天 %d 点）..." % report_time
        while True:
            cur_day = time.strftime('%a',time.localtime(time.time()))
            cur_time = time.strftime('%Y%m%d-%H',time.localtime(time.time()))
            last_date = last_time.split('-')[0]
            cur_date = cur_time.split('-')[0]
            if bRunning == 0 and cur_day not in ('Sat', 'Sun') and cmp(last_date, cur_date) != 0 and int(cur_time.split('-')[1]) == report_time:
                bRunning = 1
                last_time = cur_time
                report()
                bRunning = 0
            time.sleep(1800)            
        
if __name__ == "__main__":
    main()
