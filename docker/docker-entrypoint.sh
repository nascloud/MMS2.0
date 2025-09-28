#!/bin/bash

# 检查并复制 mosdns 配置文件
if [ ! -f /etc/mosdns/config.yaml ]; then
    echo "警告: 未找到 /etc/mosdns/config.yaml，正在从默认配置复制..."
    mkdir -p /etc/mosdns
    cp /default-configs/mosdns.yaml /etc/mosdns/config.yaml
    echo "已复制 MosDNS 配置文件，请根据需要修改 /etc/mosdns/config.yaml"
else
    echo "找到 MosDNS 配置文件: /etc/mosdns/config.yaml"
fi

# 检查并复制 mihomo 配置文件
if [ ! -f /etc/mihomo/config.yaml ]; then
    echo "警告: 未找到 /etc/mihomo/config.yaml，正在从默认配置复制..."
    mkdir -p /etc/mihomo
    cp /default-configs/mihomo.yaml /etc/mihomo/config.yaml
    echo "已复制 Mihomo 配置文件，请根据需要修改 /etc/mihomo/config.yaml"
else
    echo "找到 Mihomo 配置文件: /etc/mihomo/config.yaml"
fi

# Start mosdns in background
echo "Starting mosdns..."
mosdns start -c /etc/mosdns/config.yaml -d /etc/mosdns &

# Wait a moment for mosdns to start
sleep 2

# Start mihomo in background
echo "Starting mihomo..."
mihomo -d /etc/mihomo &

# Wait a moment for mihomo to start
sleep 2

# Start MMS2.0 Python application
echo "Starting MMS2.0 application..."
python main.py