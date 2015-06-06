daily_report
===

懒惰改变世界。这是一个提醒并帮助你完成上个工作日的日报工作的工具（只适合本团队内部使用）。

## 依赖 ##

* Firefox >= 36
* Selenium >= 2.8.0
* Python 2.7

## 安装 ##

1. 安装 [Firefox](http://www.firefox.com.cn/download/) ；
2. 安装 Python 2.7（Mac 系统已自带）；
3. 打开 Firefox ，将 dependencies/selenium-ide-2.8.0 目录下拖动到 Firefox 窗口完成安装并退出 Firefox 。
4. 安装程序依赖的 selenium 模块 ：

``` sh
$ sudo pip install selenium
```

如果没有安装 pip ，先执行 dependencies/get-pip.py 安装 pip ：

``` sh
$ sudo python dependencies/get-pip.py
```

## 使用 ##

### 1. 配置 ###

``` python
repeat_flag = False			# 是否每天重复（除周末）
report_time = 8				# 如果每天重复，则每天提醒进行日报的时间（建议每天设为上午8点）
user_name = '****************'		# 域账户名
user_passwd = '****************'	# 域密码
task_index = 1                      # 要自动汇报的项目的序号（如果只有一个项目可以不用改）
default_msg = u"框架开发"		# 默认的工作描述
default_time = 10 			# 默认的工作时长
```

### 2. 执行 ###

``` python
$ python report.py
```

将自动打开 Firefox 登录日报系统记录上一工作日的工作。

在这个过程中，会弹出一个子项目选择框，需要你手动选择一个子项目。

完成后将自动填写工作描述和默认工作时长。填写完成后，有 5 秒的时间让你确认工作时长，之后将自动提交并关闭窗口。

## 温馨提示 ##

1. 只帮忙记录工作日的日报，其他时间请自行登录日报管理系统进行汇报。
2. 系统休眠状态下脚本将不会被执行。请修改系统的节能选项防止电脑进入休眠，并使用[锁屏](http://www.macx.cn/thread-2087596-1-1.html)取代休眠。
3. 只用作技术学习交流，请勿用于其他用途。

## TODO ##

* [ ] 解决模态窗口阻塞问题，自动选择项目。
* [ ] 先获取考勤记录，并根据考勤记录来设置工作时长；
* [ ] 终极目标：一次执行，完成整月的日报汇报。

