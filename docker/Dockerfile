# 第一阶段：构建和打包 Python 项目
FROM python:3.11-slim AS builder

ENV APP_DIR=/app
WORKDIR $APP_DIR

# 安装依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    gzip \
    procps \
    inotify-tools \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
RUN pip install --upgrade pip && \
    pip install httpx pyyaml requests watchdog python-json-logger pyinstaller

# 复制源码
COPY ./main.py $APP_DIR/
COPY ./mihomo_sync/ $APP_DIR/mihomo_sync/

# 打包为单一可执行文件
RUN pyinstaller --onefile --name mms main.py

# 第二阶段：精简运行环境
FROM debian:bookworm-slim

ENV APP_DIR=/app
WORKDIR $APP_DIR

# 安装必要运行依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    gzip \
    procps \
    inotify-tools \
    && rm -rf /var/lib/apt/lists/*

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
    rm -rf "$FILENAME" *.md *.yaml LICENSE __MACOSX 2>/dev/null || true && \
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
    rm -rf "$FILENAME" *.md *.yaml LICENSE __MACOSX 2>/dev/null || true && \
    echo "mosdns installed successfully"

# 复制配置文件到默认配置目录
COPY ./docker/config.yaml $APP_DIR/config/
COPY ./docker/mihomo.yaml /default-configs/
COPY ./docker/mosdns.yaml /default-configs/

# 复制脚本文件
COPY ./docker/docker-entrypoint.sh $APP_DIR/
RUN chmod +x $APP_DIR/docker-entrypoint.sh

# 只复制打包后的可执行文件
COPY --from=builder /app/dist/mms $APP_DIR/mms
RUN chmod +x $APP_DIR/mms

# 暴露端口
EXPOSE 53/tcp 53/udp
EXPOSE 1053/tcp 1053/udp
EXPOSE 7890 7891 7892 9090

# 设置工作目录
WORKDIR $APP_DIR

# 设置启动命令（用打包后的可执行文件）
CMD ["/bin/bash", "/app/docker-entrypoint.sh"]