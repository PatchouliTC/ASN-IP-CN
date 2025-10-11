#!/bin/bash
# 自动下载并更新 asn_cn.conf
set -e

ZIP_URL="https://github.com/PatchouliTC/ASN-IP-CN/releases/latest/download/ASN-IP-Data.zip"
ZIP_FILE="ASN-IP-Data.zip"
CONF_FILE="asn_cn.conf"

# 下载最新的 zip 文件
curl -L "$ZIP_URL" -o "$ZIP_FILE"

# 解压出 asn_cn.conf 文件
unzip -o "$ZIP_FILE" -d "/tmp/asn-output"

if [ -f "$CONF_FILE" ]; then
    rm -f "$CONF_FILE"
fi

# 移动并覆盖到脚本所在目录
mv -f "/tmp/asn-output/$CONF_FILE" "$CONF_FILE"

# 清理下载的 zip 文件
rm -f "$ZIP_FILE"

# 清理 output 目录（只删除解压出来的文件，不删除 output 文件夹本身）
rm -rf /tmp/asn-output
