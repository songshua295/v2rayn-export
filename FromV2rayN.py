# 功能说明： win版本v2rayn的订阅以及节点导出脚本，可以配合其他工具同步到服务器上，以此来实现一个url多端同步配置。此脚本不具备同步功能
# win v2rayn下载直达地址： https://github.com/2dust/v2rayN/releases/download/6.60/v2rayN-With-Core.zip
# 使用说明： v2rayn中先对订阅节点配置后，测速后再使用该脚本，需要注意指定配置yaml文件。
# 同一级目录下写好配置文件，文件名称： 配置.yaml，路径为v2rayn的配置db数据库路径
# db路径: "C:/Users/xxx/Documents/tools/fq/v2rayN-With-Core/guiConfigs/guiNDB.db"
# 需要安装的相关库：pyyaml、csv、pyyaml等
# 配置.yaml 内容
# db路径: "C:/Users/xxx/Documents/tools/fq/v2rayN-With-Core/guiConfigs/guiNDB.db"
# ftp_server: ip
# ftp_user: ftp用户名
# ftp_password: ftp密码
# local_file_path: 节点.txt 本地的节点txt文件路径，默认不修改
# remote_file_name: 节点.txt 可以选择性修改
import yaml
import sqlite3
import csv
from urllib.parse import quote
from urllib.parse import quote_plus
import base64
from ftplib import FTP

# 读取 YAML 配置文件
with open('配置.yaml', 'r', encoding='utf8') as file:
    config = yaml.safe_load(file)

db_path = config['db路径']



def getSubscriptions(db_path):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查询 Subitem 表的 remarks 和 url 字段
    query_subitem = "SELECT remarks, url FROM Subitem"
    cursor.execute(query_subitem)

    results_subitem = cursor.fetchall()

    # 订阅链接处理
    with open('订阅.csv', 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['remarks', 'url'])
        for row in results_subitem:
            writer.writerow(row)

    # 关闭数据库连接
    conn.close()


def getNodes(db_path):

    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查询 ProfileItem 表的记录
    query_profile_item ="""
    SELECT p.indexId, p.configType, p.configVersion, p.address, p.port, p.id, p.alterId, p.security, p.network,
           p.remarks, p.headerType, p.requestHost, p.path, p.streamSecurity, p.allowInsecure, p.subid, p.isSub,
           p.flow, p.sni, p.alpn, p.coreType, p.preSocksPort, p.fingerprint, p.displayLog, p.publicKey, p.shortId, p.spiderX
    FROM ProfileItem p
    JOIN ProfileExItem pe ON p.indexId = pe.IndexId
    WHERE pe.delay > 0 AND pe.delay < 500
    ORDER BY pe.delay ASC;
    """
    cursor.execute(query_profile_item)

    results_profile_item = cursor.fetchall()

    # 定义 configType 的映射
    config_type_mapping = {
        1: 'vmess',
        3: 'ss',
        5: 'vless',
        6: 'trojan',
        7: 'hysteria2'
    }


    # 将结果进行处理并写入文件
    with open('节点.txt', 'w', encoding='utf8') as file:
        for row in results_profile_item:
            indexId, configType, configVersion, address, port, id, alterId, security, network, remarks, headerType, requestHost, path, streamSecurity, allowInsecure, subid, isSub, flow, sni, alpn, coreType, preSocksPort, fingerprint, displayLog, publicKey, shortId, spiderX = row
            if configType in config_type_mapping:
                config_type = config_type_mapping[configType]                    
            else:
                continue
            # 针对ss协议做额外字段调整
            if configType==3:
                securityAndId = base64.b64encode((security + ':' + id).encode()).decode()
                base_url = f'{config_type}://{securityAndId}@{address}:{port}'
            else:
                base_url = f'{config_type}://{id}@{address}:{port}'
            params = []
            if configVersion:
                encoded_value = quote_plus(str(configVersion))
                params.append(f'configVersion={encoded_value}')
            if network:
                # 针对trojan协议调整
                if config_type=='trojan':
                    encoded_value = quote_plus(str(network))
                    params.append(f'type={encoded_value}')
                else:
                    encoded_value = quote_plus(str(network))
                    params.append(f'network={encoded_value}')
            if headerType:
                encoded_value = quote_plus(str(headerType))
                params.append(f'headerType={encoded_value}')
            if requestHost:
                encoded_value = quote_plus(str(requestHost))
                params.append(f'requestHost={encoded_value}')
            if path:
                encoded_value = quote_plus(str(path))
                params.append(f'path={encoded_value}')
            # 别的协议是这个
            if streamSecurity:
                encoded_value = quote_plus(str(streamSecurity))
                params.append(f'security={encoded_value}')
            # ss协议是这个字段
            if security:
                encoded_value = quote_plus(str(security))
                params.append(f'security={encoded_value}')
            if allowInsecure:
                # encoded_value = quote_plus(str(allowInsecure))
                if allowInsecure=='true':
                    encoded_value='1'
                else:
                    encoded_value='0'
                params.append(f'allowInsecure={encoded_value}')
            if subid:
                encoded_value = quote_plus(str(subid))
                params.append(f'subid={encoded_value}')
            if isSub:
                encoded_value = quote_plus(str(isSub))
                params.append(f'insecure={encoded_value}')
            if flow:
                encoded_value = quote_plus(str(flow))
                params.append(f'flow={encoded_value}')
            if sni:
                encoded_value = quote_plus(str(sni))
                params.append(f'sni={encoded_value}')
            if alpn:
                encoded_value = quote_plus(str(alpn))
                params.append(f'alpn={encoded_value}')
            if coreType:
                encoded_value = quote_plus(str(coreType))
                params.append(f'coreType={encoded_value}')
            if preSocksPort:
                encoded_value = quote_plus(str(preSocksPort))
                params.append(f'preSocksPort={encoded_value}')
            if fingerprint:
                encoded_value = quote_plus(str(fingerprint))
                params.append(f'fp={encoded_value}')
            if publicKey:
                encoded_value = quote_plus(str(publicKey))
                params.append(f'pbk={encoded_value}')
            if shortId:
                encoded_value = quote_plus(str(shortId))
                params.append(f'sid={encoded_value}')
            if spiderX:
                encoded_value = quote_plus(str(spiderX))
                params.append(f'spx={encoded_value}')
            if remarks:
                encoded_value = quote_plus(str(remarks))
                params.append(f'#{encoded_value}')
            if params:
                full_url = base_url + '?' + '&'.join(params)
                file.write(full_url + '\n')

    # 关闭数据库连接
    conn.close()

# 取前100个延迟最低的节点
def limit100(file_path):
    with open(file_path, 'r', encoding='utf-8') as in_file:
        lines = [next(in_file) for _ in range(100)]
    with open('limit100.txt', 'w', encoding='utf-8') as out_file:
        out_file.writelines(lines)

def putOnFtp():
    # 读取 YAML 配置文件
    with open('配置.yaml', 'r', encoding='utf8') as file:
        config = yaml.safe_load(file)

    ftp_server = config['ftp_server']
    ftp_user = config['ftp_user']
    ftp_password = config['ftp_password']
    # 要上传的文件路径
    local_file_path = config['local_file_path']
    # 上传到 FTP 服务器后的文件名
    remote_file_name = config['remote_file_name']

    try:
        # 连接到 FTP 服务器，并设置主动模式
        ftp = FTP(ftp_server)
        ftp.login(ftp_user, ftp_password)
        ftp.set_pasv(False)
        print(f"成功登录到 FTP 服务器 {ftp_server}，并设置为主动模式")

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

# main
if __name__ == "__main__":
    getSubscriptions(db_path) #订阅导出
    getNodes(db_path)   #节点导出
    limit100("节点.txt")#延迟最低的100个
    putOnFtp()