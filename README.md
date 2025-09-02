## 框架目录结构
```
# 框架目录结构
├────.auth/
├────.gitignore
├────config/  配置文件层，存放整个项目需要用到的配置项
│    ├────__init__.py
│    ├────allure_config/
│    │    ├────http_server.exe  生成的一个http服务，用于放在allure报告压缩包里面，在windows环境下不安装allure也能打开查看报告
│    │    ├────logo.svg   当前部门或者项目logo，用于替换allure报告里面的logo。注意：代码里面无替换，是手动在lib/allure里面替换的
│    │    └────双击打开Allure报告.bat    一个用于在windows环境下不安装allure也能打开查看报告bat文件
│    ├────global_vars.py   全局变量，用于保存测试过程中变量，方便调用
│    ├────path_config.py    项目路径配置文件，注意：目录名称更改，需要更改配置文件
│    └────settings.py    项目配置文件，用于保存一些配置数据
└────utils/   公共模块，将一些公共函数、方法以及通用操作进行封装
│    ├────__init__.py
│    ├────assertion_utils/   接口断言的处理
│    │    ├────__init__.py
│    │    ├────assert_control.py
│    │    └────assert_function.py
│    ├────base_utils/   playwright基类，包括UI和API
│    │    ├────__init__.py
│    │    ├────base_page.py   基类，定义项目所需的基础方法，对playwright一些常用的页面进行二次封装，提高项目的代码重用性
│    │    ├────base_request.py  基类，定义项目所需的基础方法，对playwright的接口进行二次封装
│    │    └────request_control.py 请求playwright的接口进行再次封装，包括请求前数据处理，请求时日志记录，请求后断言，数据提取
│    ├────data_utils/   处理数据的一些方法
│    │    ├────__init__.py
│    │    ├────data_handle.py
│    │    ├────eval_data_handle.py
│    │    ├────extract_data_handle.py
│    │    └────faker_handle.py
│    ├────database_utils/  数据库处理
│    │    ├────__init__.py
│    │    └────mysql_handle.py
│    ├────files_utils/  文件处理
│    │    ├────__init__.py
│    │    ├────files_handle.py
│    │    └────yaml_handle.py
│    ├────logger_utils/  日志处理
│    │    ├────__init__.py
│    │    └────loguru_log.py
│    ├────models.py   模型类
│    ├────notify_utils/   通知处理
│    │    ├────__init__.py
│    │    ├────dingding_bot.py
│    │    ├────wechat_bot.py
│    │    └────yagmail_bot.py
│    ├────report_utils/  报告处理
│    │    ├────__init__.py
│    │    ├────allure_handle.py
│    │    ├────get_results_handle.py
│    │    ├────platform_handle.py
│    │    └────send_result_handle.py
│    └────tools/  其他工具类
│    │    ├────__init__.py
│    │    ├────func_handle.py
│    │    ├────generate_project_tree.py
│    │    ├────http_server.py
│    │    └────time_handle.py
├────lib/  保存第三方包，例如：[allure-2.22.0]
├────files/  用于存放测试过程中所需要的测试文件
├────outputs/  测试报告，日志，图片保存的路径
│    ├────image/ 用于管理生成的图片
│    ├────log/ 用于管理生成的日志
│    └────report/  测试报告层，用于管理生成的测试报告
├────interfaces/  接口池，保存测试过程中需要调用的接口
├────pages/     page_object，页面对象层，也是PO的核心层，继承BasePage，管理页面元素以及操作元素的方法（将操作元素的动作写成方法）
├────testcases/  测试用例层，用于管理测试用例，这里会用到单元测试框架：Pytest， 涉及到conftest.py的使用
├────conftest.py  Pytest 测试框架中用于定义可重用的测试夹具（fixtures）
├────dockerfile   使用docker部署框架的文件
├────dockerfile2 使用docker部署框架的文件
├────Pipfile  pipenv管理框架所需的依赖包
├────Pipfile.lock  pipenv管理框架所需的依赖包
├────pytest.ini  pytest的配置文件
├────README.md
├────requirements.txt   管理框架所有的依赖包及对应版本
├────run.py  批量执行测试用例的主程序
```


## 依赖库
```
pytest = "*"
loguru = "*"
pytest-rerunfailures = "*"
faker = "*"
yagmail = "*"
allure-pytest = "*"
pytest-playwright = "*"
jsonpath = "*"
pyyaml = "*"
pymysql = "*"
sshtunnel = "*"
pipreqs = "*"
pytest-ordering = "*"
pathvalidate = "*"
pycryptodome = "*"
```



### 安装python
本地电脑搭建好 python环境3.9。包括allure测试报告所需的java环境（安装jdk）。


### 安装依赖包
#### 使用pipenv管理依赖包
1) 安装pipenv
```
# 建议在项目根目录下执行命令安装
pip install pipenv
```

2) 使用pipenv管理安装环境依赖包：pipenv install （必须在项目根目录下执行）
```
   注意：使用pipenv install会自动安装Pipfile里面的依赖包，该依赖包仅安装在虚拟环境里，不安装在测试机。
```

###  安装playwright浏览器驱动
```
playwright install   # 安装浏览器驱动
```


#### 运行
```
  > python run.py  (默认在test环境运行测试用例, 报告采用allure)
  > python run.py -m demo 在test环境仅运行打了标记demo用例， 默认报告采用allure
  > python run.py -env live 在live环境运行测试用例
  > python run.py -env=test 在test环境运行测试用例
  > python run.py -browser chromium  (使用chrome浏览器运行测试用例)
  > python run.py -env test  -report no -browser chromium  -mode headless 在test环境，使用谷歌无头浏览器运行用例，并且生成allure html report
```

注意：
- 如果pycharm.interpreter拥有了框架所需的所有依赖包，可以通过pycharm直接在`run.py`中右键运行
