# MMS (Mihomo + MosDNS + Sync) Docker 镜像
FROM debian:bookworm-slim

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV APP_DIR=/app
ENV MOSDNS_DIR=/etc/mosdns
ENV MIHOMO_DIR=/etc/mihomo

# 安装必要的依赖
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    gzip \
    python3 \
    python3-pip \
    procps \
    inotify-tools \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
RUN pip3 install --upgrade pip --break-system-packages && \
    pip3 install --no-cache-dir --break-system-packages requests pyyaml watchdog

# 创建应用目录和默认配置目录
RUN mkdir -p $APP_DIR /etc/mosdns/rules /etc/mihomo /default-configs

# 下载并安装最新版 mihomo (amd64)
RUN set -e && \
    echo "Getting latest mihomo release..." && \
    LATEST_MIHOMO=$(curl -s "https://api.github.com/repos/MetaCubeX/mihomo/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/' | head -1) && \
    echo "Latest mihomo version: $LATEST_MIHOMO" && \
    if [ -z "$LATEST_MIHOMO" ]; then echo "Failed to get latest version"; exit 1; fi && \
    echo "Getting download URL for linux-amd64..." && \
    DOWNLOAD_URL=$(curl -s "https://api.github.com/repos/MetaCubeX/mihomo/releases/latest" | grep '"browser_download_url":' | grep 'linux-amd64' | sed -E 's/.*"([^"]+)".*/\1/' | head -1) && \
    echo "Downloading from: $DOWNLOAD_URL" && \
    if [ -z "$DOWNLOAD_URL" ]; then echo "Failed to get download URL"; exit 1; fi && \
    FILENAME=$(basename "$DOWNLOAD_URL") && \
    echo "Downloaded filename: $FILENAME" && \
    curl -L --fail --retry 3 --retry-delay 5 -o "$FILENAME" "$DOWNLOAD_URL" && \
    if echo "$FILENAME" | grep -q '\.gz$'; then \
        gunzip "$FILENAME" && \
        EXTRACTED_FILE=$(echo "$FILENAME" | sed 's/\.gz$//'); \
    elif echo "$FILENAME" | grep -q '\.zip$'; then \
        unzip "$FILENAME" && \
        EXTRACTED_FILE="mihomo-linux-amd64"; \
    else \
        EXTRACTED_FILE="$FILENAME"; \
    fi && \
    echo "Extracted file: $EXTRACTED_FILE" && \
    chmod +x "$EXTRACTED_FILE" && \
    mv "$EXTRACTED_FILE" /usr/local/bin/mihomo && \
    rm -f "$FILENAME" && \
    echo "mihomo installed successfully"

# 下载并安装最新版 mosdns (amd64)
RUN set -e && \
    echo "Getting latest mosdns release..." && \
    LATEST_MOSDNS=$(curl -s "https://api.github.com/repos/IrineSistiana/mosdns/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/' | head -1) && \
    echo "Latest mosdns version: $LATEST_MOSDNS" && \
    if [ -z "$LATEST_MOSDNS" ]; then echo "Failed to get latest version"; exit 1; fi && \
    echo "Getting download URL for linux-amd64..." && \
    DOWNLOAD_URL=$(curl -s "https://api.github.com/repos/IrineSistiana/mosdns/releases/latest" | grep '"browser_download_url":' | grep 'linux-amd64' | sed -E 's/.*"([^"]+)".*/\1/' | head -1) && \
    echo "Downloading from: $DOWNLOAD_URL" && \
    if [ -z "$DOWNLOAD_URL" ]; then echo "Failed to get download URL"; exit 1; fi && \
    FILENAME=$(basename "$DOWNLOAD_URL") && \
    echo "Downloaded filename: $FILENAME" && \
    curl -L --fail --retry 3 --retry-delay 5 -o "$FILENAME" "$DOWNLOAD_URL" && \
    if echo "$FILENAME" | grep -q '\.gz$'; then \
        gunzip "$FILENAME" && \
        EXTRACTED_FILE=$(echo "$FILENAME" | sed 's/\.gz$//'); \
    elif echo "$FILENAME" | grep -q '\.zip$'; then \
        unzip "$FILENAME" && \
        EXTRACTED_FILE="mosdns"; \
    else \
        EXTRACTED_FILE="$FILENAME"; \
    fi && \
    echo "Extracted file: $EXTRACTED_FILE" && \
    chmod +x "$EXTRACTED_FILE" && \
    mv "$EXTRACTED_FILE" /usr/local/bin/mosdns && \
    rm -f "$FILENAME" *.md *.yaml LICENSE 2>/dev/null || true && \
    echo "mosdns installed successfully"

# 复制配置文件到默认配置目录
COPY ./docker/config.yaml $APP_DIR/config
COPY ./docker/mihomo.yaml /default-configs/
COPY ./docker/mosdns.yaml /default-configs/

# 复制源代码文件
COPY ./mihomo_sync/ $APP_DIR/mihomo_sync/
COPY ./main.py $APP_DIR/

# 复制脚本文件
COPY ./docker/docker-entrypoint.sh $APP_DIR/

# 设置文件权限
RUN chmod +x $APP_DIR/docker-entrypoint.sh

# 暴露端口
# 53: MosDNS DNS服务
# 1053: Mihomo DNS服务（备用）
# 7890: Mihomo 混合端口
# 7891: Mihomo SOCKS代理
# 7892: Mihomo HTTP代理  
# 9090: Mihomo 控制面板
EXPOSE 53/tcp 53/udp
EXPOSE 1053/tcp 1053/udp
EXPOSE 7890 7891 7892 9090

# 设置工作目录
WORKDIR $APP_DIR

# 设置启动命令
CMD ["/bin/bash", "/app/docker-entrypoint.sh"]