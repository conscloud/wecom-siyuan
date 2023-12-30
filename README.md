# 简介

基于[mostlittlebee/chatgpt-on-wecom: 基于ChatGPT的企业微信聊天应用 (github.com)](https://github.com/mostlittlebee/chatgpt-on-wecom)及[muhanstudio/siyuan-wxbox: 一个简单但功能齐全的自制思源笔记微信收集箱 (github.com)](https://github.com/muhanstudio/siyuan-wxbox)做了简单修改，**满足自己的需求**。

基于企业微信的思源笔记收集箱，通过向企业微信应用发送文本、图片、定位自动在思源笔记中生成相应的笔记。已实现的特性如下：

- [x] **文本笔记**：接收发送给应用号的企业微信文本消息，创建一条文本笔记
- [x] **图片笔记**：接收发送给应用号的企业微信图片消息，创建一条图片笔记
- [x] **定位笔记**：接收发送给应用号的企业微信定位消息，创建一条关于位置的笔记
- [x] **链接笔记**：接收发送给应用号的企业链接信息或网址，创建一条关于链接笔记

**文本笔记：**

![image-20231230105628337](https://cdn.jsdelivr.net/gh/conscloud/picgotemp/imgplus/202312301056116.webp)

![image-20231230105758079](https://cdn.jsdelivr.net/gh/conscloud/picgotemp/imgplus/202312301057352.webp)

**图片笔记：**

![image-20231230110056652](https://cdn.jsdelivr.net/gh/conscloud/picgotemp/imgplus/202312301100923.webp)

![image-20231230110125372](https://cdn.jsdelivr.net/gh/conscloud/picgotemp/imgplus/202312301101964.webp)

**位置笔记**：

![](https://cdn.jsdelivr.net/gh/conscloud/picgotemp/imgplus/202312301102382.webp)

![image-20231230110333347](https://cdn.jsdelivr.net/gh/conscloud/picgotemp/imgplus/202312301103641.webp)

**链接笔记：**

![image-20231230110424760](https://cdn.jsdelivr.net/gh/conscloud/picgotemp/imgplus/202312301104018.webp)

![image-20231230110510982](https://cdn.jsdelivr.net/gh/conscloud/picgotemp/imgplus/202312301105239.webp)

![image-20231230110526366](https://cdn.jsdelivr.net/gh/conscloud/picgotemp/imgplus/202312301105622.webp)

# 更新日志

1、2023-12-30，初步通用

# 快速开始

## 准备

### 1. 部署思源笔记私有服务器

详见：[siyuan/README_zh_CN.md at master · siyuan-note/siyuan (github.com)](https://github.com/siyuan-note/siyuan/blob/master/README_zh_CN.md)

### 2.运行环境

支持 Linux、MacOS、Windows 系统（可在Linux服务器上长期运行)，同时需安装 `Python`。 
> 建议Python版本在 3.7.1~3.9.X 之间，3.10及以上版本在 MacOS 可用，其他系统上不确定能否正常运行。


1.克隆项目代码：

```bash
git clone https://github.com/conscloud/wecom-siyuan.git
cd wecom-siyuan/
```

2.安装所需核心依赖：

```bash
pip3 install flask
pip3 install wechatpy
pycryptodome
pip3 install --upgrade openai
```
## 配置

配置文件的模板在根目录的`config-template.json`中，需复制该模板创建最终生效的 `config.json` 文件：

```bash
cp config-template.json config.json
```

然后在`config.json`中填入配置，以下是对默认配置的说明，可根据需要进行自定义修改：

```bash
#config-template.json
{
  "conversation_max_tokens": "最大返回字符",
  "WECHAT_TOKEN": "企业微信 回调token",
  "WECHAT_ENCODING_AES_KEY":"企业微信 编码后的AES Key",
  "WECHAT_CORP_ID":"企业微信 企业ID",
  "Secret":"企业微信 应用Secret",
  "AppId":"企业微信 应用ID",
  "character_desc": "企业微信应用发送消息到思源笔记，自动创建笔记",
  "siyuan_urlmd" : "思源笔记笔记创建API地址，例如http://127.0.0.1:6806/api/filetree/createDocWithMd",
  "user_name": "微信用户名",
  "notebook" : "你的笔记本ID",
  "apitoken" : "你的思源笔记apitoken"
}
```

## 运行

### 1.本地运行

如果是开发机 **本地运行**，直接在项目根目录下执行：

```bash
python3 app.py
```


### 2.服务器部署

使用nohup命令在后台运行程序：

```bash
touch nohup.out                                   # 首次运行需要新建日志文件                     
nohup python3 app.py & tail -f nohup.out          # 在后台运行程序并通过日志输出二维码
```

