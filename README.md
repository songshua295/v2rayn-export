# v2rayn-export 🚀

一个用于从 V2RayN 客户端提取和转换配置信息的 Python 脚本。

## ✨ 功能

- 从 V2RayN 格式导出配置信息 📦
- 将配置转换为其他工具可用的格式 🔄
- 支持多种版本的导出流程 ⚙️

## 🛠 环境要求

- Python 3.x 🐍

## 📦 安装步骤

1. 克隆此仓库：
    ```bash
    git clone https://github.com/songshua295/v2rayn-export.git
    cd v2rayn-export
    ```

2. （可选）创建虚拟环境：
    ```bash
    python3 -m venv env
    source env/bin/activate  # Windows 使用 `env\Scripts\activate`
    ```

3. 安装所需依赖项（如有必要）：
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 使用方法

推荐使用v2版本python脚本，因为采用数据采用剪贴板，比来自数据库db的复制粘贴更加可靠。
注意⚠️：先测速和排序后再复制订阅会更好。

### 基本用法
运行脚本以从 V2RayN 中提取配置信息：
```bash
python FromV2rayN.py
```
或者使用另一版本：

```bash
python FromV2rayN-v2.py
```

## 📄 配置详情
请参阅 配置文件格式说明.md 以了解更多关于配置格式及脚本使用的详细说明。
