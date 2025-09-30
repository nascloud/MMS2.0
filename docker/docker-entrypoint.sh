#!/bin/bash
export LANG=C.UTF-8
export LC_ALL=C.UTF-8

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

# 创建 MosDNS 必需的规则文件目录和空文件
echo "创建 MosDNS 规则文件目录..."
mkdir -p /etc/mosdns/rules
mkdir -p ./custom

# 创建 MosDNS 配置中必需的规则文件（如果不存在）
echo "检查并创建必需的 MosDNS 规则文件..."
touch /etc/mosdns/rules/direct_domain.txt
touch /etc/mosdns/rules/proxy_domain.txt
touch /etc/mosdns/rules/reject_domain.txt
touch ./custom/direct.txt
touch ./custom/proxy.txt
touch ./custom/local_ptr.txt

echo "所有必需的 MosDNS 规则文件已准备就绪"

# 检查mosdns服务是否安装
if mosdns service status 2>&1 | grep -q "not installed"; then
    echo "MosDNS 服务未安装，正在安装..."
    mosdns service install -c /etc/mosdns/config.yaml -d /etc/mosdns || true
    # 启动服务
    echo "MosDNS 服务安装完毕，正在启动..."
    mosdns service start
else
    # 启动服务
    echo "MosDNS 服务已安装，正在启动..."
    mosdns service start
fi

# 检查运行状态并输出状态
if mosdns service status 2>&1 | grep -q "running"; then
    echo "MosDNS 服务已启动..."
else 
    echo "MosDNS 服务启动失败..."
fi    

# Wait a moment for mosdns to start
sleep 2

# Start mihomo in background
echo "Starting mihomo..."
mihomo -d /etc/mihomo &

# Wait a moment for mihomo to start
sleep 2

# Start packaged MMS2.0 executable
echo "Starting MMS2.0 application..."
/app/mms