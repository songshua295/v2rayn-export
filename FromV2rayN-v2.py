# 由于之前的似乎能够直接导入到v2rayn，但是安卓端的v2rayNG似乎对格式更加严格。所以还是直接从v2rayN种直接复制会更加符合要求。
# 功能： 
# 1. 先在v2rayn中复制节点，然后运行此脚本，将剪贴板中的节点发送到FTP服务器中。
# 2. 获取v2rayn中的订阅地址上传到ftp服务器中

from ftplib import FTP
import yaml
import pyperclip
from urllib.parse import unquote
import sqlite3
import csv

# 从配置文件中加载变量参数
with open('配置.yaml', 'r', encoding='utf8') as file:
    config = yaml.safe_load(file)

ftp_server = config['ftp_server']
ftp_user = config['ftp_user']
ftp_password = config['ftp_password']
# 要上传的文件路径
local_file_path = config['local_file_path']
# 上传到 FTP 服务器后的文件名
remote_file_name = config['remote_file_name']
limit100_file_name = config['limit100_file_name']
db_path=config['db路径']

def putOnFtp(ftp_server,ftp_user,ftp_password,local_file_path,remote_file_name):
    # 读取 YAML 配置文件


    try:
        # 连接到 FTP 服务器，并设置主动模式
        ftp = FTP(ftp_server)
        ftp.login(ftp_user, ftp_password)
        ftp.set_pasv(False)
        print(f"成功登录到 FTP 服务器 {ftp_server}[主动模式]")

        # 切换到目标目录，如果目录不存在可以根据需要创建
        ftp.cwd("/")

        # 打开本地文件以二进制模式读取
        with open(local_file_path, "rb") as file:
            # 上传文件
            ftp.storbinary(f"STOR {remote_file_name}", file)
        print(f"成功上传文件 {local_file_path} 到 FTP 服务器")

        # 关闭 FTP 连接
        ftp.quit()
    except Exception as e:
        print(f"发生错误：{e}")

def getClip(local_file_path):
    # 获取剪贴板内容
    clipboard_content = pyperclip.paste()
     # 进行 URL 解码
    clipboard_content = unquote(clipboard_content)
    print(clipboard_content)

     # 定义要过滤的关键字
    keywords = ['流量', '过期', '官网', '落地', '回国', '本站', '用户', '若', '续费', '邮箱', '订阅','重置','到期','距离','购买','送永久']
    # 过滤行
    filtered_lines = [line for line in clipboard_content.split('\n') if not any(keyword in line for keyword in keywords)]
    filtered_content = '\n'.join(filtered_lines)
    filtered_content=filtered_content.replace('\n\n','\n')

    # 创建文件，如果文件已存在，将覆盖原有内容
    with open(local_file_path, 'w', encoding='utf-8') as file:
        file.write(filtered_content)

    print(f'剪贴板内容已输出到 {local_file_path} 文件中。')

def getLimit100():
    try:
        lines = []
        with open(local_file_path, 'r', encoding='utf-8') as file:
            for _ in range(100):
                line = file.readline()
                if not line:
                    break
                lines.append(line)
        with open(limit100_file_name, 'w', encoding='utf-8') as limit_file:
            limit_file.writelines(lines)
        print(f'前 100 行已输出到 {limit100_file_name} 文件中。')
    except Exception as e:
        print(f"获取前 100 行时发生错误：{e}")

# 从v2rayn配置db中获取订阅链接
def getSubscriptions(db_path):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查询 Subitem 表的 remarks 和 url 字段
    query_subitem = "SELECT remarks, url FROM Subitem"
    cursor.execute(query_subitem)

    results_subitem = cursor.fetchall()
    sub_file_path='订阅.txt'
    # 订阅链接处理
    with open(sub_file_path, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['remarks', 'url'])
        for row in results_subitem:
            writer.writerow(row)
    # 关闭数据库连接
    conn.close()
    putOnFtp(ftp_server,ftp_user,ftp_password,sub_file_path,sub_file_path)

if __name__=="__main__":
    # 节点获取
    getClip(local_file_path)
    # 节点上传ftp
    putOnFtp(ftp_server,ftp_user,ftp_password,local_file_path,remote_file_name)

    # 获取前 100 行并保存到新文件,并上传到ftp
    getLimit100()
    putOnFtp(ftp_server, ftp_user, ftp_password, limit100_file_name, f'{limit100_file_name}')

    # 订阅上传FTP 
    getSubscriptions(db_path)




