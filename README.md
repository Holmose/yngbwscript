## 云南省干部在线学习学院 必修课学习脚本
运行后不需要手动切换视频进行观看，自动输入验证码进行验证
https://www.ynsgbzx.cn/

### 版本说明
新增选修课学习，在配置文件中添加即可。

### 使用说明
需要首先安装aibote
下载地址：http://www.aibote.net/download.html

python版本为：3.10.13

安装依赖
```bash
pip install -r requrements.txt
```

修改USERINFO.yaml用户名和密码，改为自己的，注意英文冒号后有空格
浏览器类型可以为chrome、edge
```
浏览器: "chrome"
```

edge和chrome会自动寻找浏览器路径，其他浏览器需要指定browserPath
如
```
浏览器: "C:\\Program Files\\Google\\Chrome\\Application"
```

USERINFO.yaml文件默认内容：
```
# 井号开头为注释
用户名: "testuser"
密码: "123456"
# 这里填写使用的浏览器
浏览器: "chrome"

# 这里填写本次学习的是选修还是必修
本次学习: "必修"

# 定时执行 8点1分和9点都会执行
定时执行: ["08:01", "09:00"]
```
意思为：用户名为testuser，密码为123456，浏览器使用chrome，学习必修课
若要学习选修，将必修改为选修即可，如下：
```
本次学习: "选修"
```

需要安装官方版本的chrome浏览器

然后启动运行
```
python web_bot.py
```

![1696237260467.png](https://img1.imgtp.com/2023/10/02/kjWxcxXm.png)
