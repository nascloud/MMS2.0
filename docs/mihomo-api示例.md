请求http://127.0.0.1:9090/rules

```
GET /rules HTTP/1.1
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Authorization: Bearer mihomo666
Connection: keep-alive
DNT: 1
Host: 127.0.0.1:9090
Referer: http://127.0.0.1:9090/ui/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0
sec-ch-ua: "Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

响应

```
{
    "rules": [
        {
            "type": "AND",
            "payload": "((DstPort,443) \u0026\u0026 (Network,udp))",
            "proxy": "REJECT",
            "size": -1
        },
        {
            "type": "AND",
            "payload": "((SrcIPCIDR,192.168.50.0/24) \u0026\u0026 (IPCIDR,192.168.50.0/24))",
            "proxy": "DIRECT",
            "size": -1
        },
        {
            "type": "IPCIDR",
            "payload": "192.168.50.0/24",
            "proxy": "🏠 Home",
            "size": -1
        },
        {
            "type": "DomainSuffix",
            "payload": "adobe.io",
            "proxy": "REJECT",
            "size": -1
        },
        {
            "type": "DomainSuffix",
            "payload": "xn--ngstr-lra8j.com",
            "proxy": "📧 谷歌服务",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "private_domain",
            "proxy": "🎯 本机直连",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "direct_domain",
            "proxy": "🎯 本机直连",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "proxy_domain",
            "proxy": "🚀 节点选择",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "talkatone_ad",
            "proxy": "REJECT",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "talkatone_proxy",
            "proxy": "🇺🇸 美国|Auto",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "networktest",
            "proxy": "📈 网络测试",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "spotify_domain",
            "proxy": "🇸🇬 新加坡|Auto",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "ai_domain_cn",
            "proxy": "🎯 本机直连",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "ai_domain",
            "proxy": "🤖 人工智能",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "ai_domain_!cn",
            "proxy": "🤖 人工智能",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "github_domain",
            "proxy": "🚀 节点选择",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "twitter_domain",
            "proxy": "🚀 节点选择",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "youtube_domain",
            "proxy": "📧 谷歌服务",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "google_domain",
            "proxy": "📧 谷歌服务",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "telegram_domain",
            "proxy": "📲 电报消息",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "netflix_domain",
            "proxy": "📹 海外视频",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "bahamut_domain",
            "proxy": "📹 海外视频",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "bilibili_domain",
            "proxy": "📺 哔哩哔哩",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "cn_domain",
            "proxy": "🎯 本机直连",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "geolocation-!cn",
            "proxy": "🚀 节点选择",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "private_ip",
            "proxy": "🎯 本机直连",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "netflix_ip",
            "proxy": "📹 海外视频",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "telegram_ip",
            "proxy": "📲 电报消息",
            "size": -1
        },
        {
            "type": "RuleSet",
            "payload": "cn_ip",
            "proxy": "🎯 本机直连",
            "size": -1
        },
        {
            "type": "Match",
            "payload": "",
            "proxy": "🐟 漏网之鱼",
            "size": -1
        }
    ]
}
```

请求 http://127.0.0.1:9090/providers/rules

```
GET /providers/rules HTTP/1.1
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Authorization: Bearer mihomo666
Connection: keep-alive
DNT: 1
Host: 127.0.0.1:9090
Referer: http://127.0.0.1:9090/ui/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0
sec-ch-ua: "Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

响应

```
{
    "providers": {
        "ai_domain": {
            "behavior": "Domain",
            "format": "TextRule",
            "name": "ai_domain",
            "ruleCount": 4,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-25T11:56:00.2058302+08:00"
        },
        "ai_domain_!cn": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "ai_domain_!cn",
            "ruleCount": 70,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.3669791+08:00"
        },
        "ai_domain_cn": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "ai_domain_cn",
            "ruleCount": 29,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.3767915+08:00"
        },
        "bahamut_domain": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "bahamut_domain",
            "ruleCount": 5,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.3438803+08:00"
        },
        "bilibili_domain": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "bilibili_domain",
            "ruleCount": 50,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.2964858+08:00"
        },
        "biliintl_domain": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "biliintl_domain",
            "ruleCount": 11,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.3773061+08:00"
        },
        "cn_domain": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "cn_domain",
            "ruleCount": 116951,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.6028995+08:00"
        },
        "cn_ip": {
            "behavior": "IPCIDR",
            "format": "MrsRule",
            "name": "cn_ip",
            "ruleCount": 19273,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.5512052+08:00"
        },
        "direct_domain": {
            "behavior": "Domain",
            "format": "TextRule",
            "name": "direct_domain",
            "ruleCount": 17,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.3893074+08:00"
        },
        "fakeip-filter": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "fakeip-filter",
            "ruleCount": 114,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.3767915+08:00"
        },
        "geolocation-!cn": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "geolocation-!cn",
            "ruleCount": 31365,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.5874082+08:00"
        },
        "github_domain": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "github_domain",
            "ruleCount": 29,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.3245188+08:00"
        },
        "google_domain": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "google_domain",
            "ruleCount": 1092,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.4358789+08:00"
        },
        "google_ip": {
            "behavior": "IPCIDR",
            "format": "MrsRule",
            "name": "google_ip",
            "ruleCount": 4335,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.3449222+08:00"
        },
        "netflix_domain": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "netflix_domain",
            "ruleCount": 24,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.3669791+08:00"
        },
        "netflix_ip": {
            "behavior": "IPCIDR",
            "format": "MrsRule",
            "name": "netflix_ip",
            "ruleCount": 78,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.3438803+08:00"
        },
        "networktest": {
            "behavior": "Classical",
            "format": "TextRule",
            "name": "networktest",
            "ruleCount": 1,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.8371554+08:00"
        },
        "pixiv_domain": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "pixiv_domain",
            "ruleCount": 11,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.4358789+08:00"
        },
        "private_domain": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "private_domain",
            "ruleCount": 131,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T15:52:33.8998566+08:00"
        },
        "private_ip": {
            "behavior": "IPCIDR",
            "format": "MrsRule",
            "name": "private_ip",
            "ruleCount": 18,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T15:52:10.0188839+08:00"
        },
        "proxy_domain": {
            "behavior": "Domain",
            "format": "TextRule",
            "name": "proxy_domain",
            "ruleCount": 18,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.3066823+08:00"
        },
        "spotify_domain": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "spotify_domain",
            "ruleCount": 22,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.4490567+08:00"
        },
        "talkatone_ad": {
            "behavior": "Classical",
            "format": "TextRule",
            "name": "talkatone_ad",
            "ruleCount": 10,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.472536+08:00"
        },
        "talkatone_proxy": {
            "behavior": "Classical",
            "format": "TextRule",
            "name": "talkatone_proxy",
            "ruleCount": 14,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.3433523+08:00"
        },
        "telegram_domain": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "telegram_domain",
            "ruleCount": 19,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.3557294+08:00"
        },
        "telegram_ip": {
            "behavior": "IPCIDR",
            "format": "MrsRule",
            "name": "telegram_ip",
            "ruleCount": 12,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.4210694+08:00"
        },
        "twitter_domain": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "twitter_domain",
            "ruleCount": 24,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.4210694+08:00"
        },
        "twitter_ip": {
            "behavior": "IPCIDR",
            "format": "MrsRule",
            "name": "twitter_ip",
            "ruleCount": 21,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.3245188+08:00"
        },
        "youtube_domain": {
            "behavior": "Domain",
            "format": "MrsRule",
            "name": "youtube_domain",
            "ruleCount": 176,
            "type": "Rule",
            "vehicleType": "HTTP",
            "updatedAt": "2025-09-24T14:30:46.4079836+08:00"
        }
    }
}
```

请求http://127.0.0.1:9090/proxies

```
GET /proxies HTTP/1.1
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Authorization: Bearer mihomo666
Connection: keep-alive
DNT: 1
Host: 127.0.0.1:9090
Referer: http://127.0.0.1:9090/ui/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0
sec-ch-ua: "Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

响应

```
{
    "proxies": {
        "COMPATIBLE": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {},
            "history": [],
            "id": "1f0991b6-ecba-6125-95ad-bb4d183b62e3",
            "interface": "",
            "mptcp": false,
            "name": "COMPATIBLE",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Compatible",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "DIRECT": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {},
            "history": [],
            "id": "1f0991b6-ecbb-6572-8c9c-97f560202e10",
            "interface": "",
            "mptcp": false,
            "name": "DIRECT",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Direct",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "GLOBAL": {
            "alive": true,
            "all": [
                "DIRECT",
                "REJECT",
                "🚀 节点选择",
                "♻️ Auto",
                "🤖 人工智能",
                "📲 电报消息",
                "📹 海外视频",
                "📧 谷歌服务",
                "📺 哔哩哔哩",
                "📈 网络测试",
                "🐟 漏网之鱼",
                "🛠️ 手动选择",
                "🇭🇰 香港|Auto",
                "🇹🇼 台湾|Auto",
                "🇸🇬 新加坡|Auto",
                "🇯🇵 日本|Auto",
                "🇺🇸 美国|Auto",
                "🏠 Home",
                "🎯 本机直连"
            ],
            "dialer-proxy": "",
            "extra": {},
            "hidden": false,
            "history": [],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "GLOBAL",
            "now": "DIRECT",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "",
            "tfo": false,
            "type": "Selector",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "Home|ss": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-24T15:52:34.1615756+08:00",
                            "delay": 182
                        },
                        {
                            "time": "2025-09-24T20:42:36.2412948+08:00",
                            "delay": 217
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-24T15:52:34.1615756+08:00",
                    "delay": 182
                },
                {
                    "time": "2025-09-24T20:42:36.2412948+08:00",
                    "delay": 217
                }
            ],
            "id": "1f0991b6-ecba-6125-8db8-3585576d5519",
            "interface": "",
            "mptcp": false,
            "name": "Home|ss",
            "routing-mark": 0,
            "smux": true,
            "tfo": false,
            "type": "Shadowsocks",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "Home|vmess": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-24T15:52:35.1065162+08:00",
                            "delay": 297
                        },
                        {
                            "time": "2025-09-24T20:42:36.3440639+08:00",
                            "delay": 188
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-24T15:52:35.1065162+08:00",
                    "delay": 297
                },
                {
                    "time": "2025-09-24T20:42:36.3440639+08:00",
                    "delay": 188
                }
            ],
            "id": "1f0991b6-ecbb-6572-a8e2-1f4824c6b7de",
            "interface": "",
            "mptcp": false,
            "name": "Home|vmess",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Vmess",
            "udp": false,
            "uot": true,
            "xudp": false
        },
        "Home|vmess-tls": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-24T15:52:33.9690209+08:00",
                            "delay": 175
                        },
                        {
                            "time": "2025-09-24T20:42:36.4670294+08:00",
                            "delay": 212
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-24T15:52:33.9690209+08:00",
                    "delay": 175
                },
                {
                    "time": "2025-09-24T20:42:36.4670294+08:00",
                    "delay": 212
                }
            ],
            "id": "1f0991b6-ecbb-6572-8b7f-b2f7e7912cb3",
            "interface": "",
            "mptcp": false,
            "name": "Home|vmess-tls",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Vmess",
            "udp": false,
            "uot": true,
            "xudp": false
        },
        "PASS": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {},
            "history": [],
            "id": "1f0991b6-ecbb-6572-aba0-c2e6657ca15e",
            "interface": "",
            "mptcp": false,
            "name": "PASS",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Pass",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "REJECT": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {},
            "history": [],
            "id": "1f0991b6-ecbb-6572-8e74-970e1ada6d1e",
            "interface": "",
            "mptcp": false,
            "name": "REJECT",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Reject",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "REJECT-DROP": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {},
            "history": [],
            "id": "1f0991b6-ecbb-6572-80dc-18c248a629ec",
            "interface": "",
            "mptcp": false,
            "name": "REJECT-DROP",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "RejectDrop",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "ali-hk": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:40.0124906+08:00",
                            "delay": 46
                        },
                        {
                            "time": "2025-09-25T09:57:36.6419624+08:00",
                            "delay": 61
                        },
                        {
                            "time": "2025-09-25T10:02:36.244802+08:00",
                            "delay": 49
                        },
                        {
                            "time": "2025-09-25T10:07:36.5092425+08:00",
                            "delay": 46
                        },
                        {
                            "time": "2025-09-25T10:12:36.3117724+08:00",
                            "delay": 70
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:40.0124906+08:00",
                    "delay": 46
                },
                {
                    "time": "2025-09-25T09:57:36.6419624+08:00",
                    "delay": 61
                },
                {
                    "time": "2025-09-25T10:02:36.244802+08:00",
                    "delay": 49
                },
                {
                    "time": "2025-09-25T10:07:36.5092425+08:00",
                    "delay": 46
                },
                {
                    "time": "2025-09-25T10:12:36.3117724+08:00",
                    "delay": 70
                }
            ],
            "id": "1f099b54-1f2e-6998-9516-db224e893870",
            "interface": "",
            "mptcp": false,
            "name": "ali-hk",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Vless",
            "udp": false,
            "uot": true,
            "xudp": true
        },
        "ali-hk-relay": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:40.2466807+08:00",
                            "delay": 98
                        },
                        {
                            "time": "2025-09-25T09:57:36.4166853+08:00",
                            "delay": 91
                        },
                        {
                            "time": "2025-09-25T10:02:36.4127117+08:00",
                            "delay": 92
                        },
                        {
                            "time": "2025-09-25T10:07:36.3590513+08:00",
                            "delay": 85
                        },
                        {
                            "time": "2025-09-25T10:12:36.4328896+08:00",
                            "delay": 101
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:40.2466807+08:00",
                    "delay": 98
                },
                {
                    "time": "2025-09-25T09:57:36.4166853+08:00",
                    "delay": 91
                },
                {
                    "time": "2025-09-25T10:02:36.4127117+08:00",
                    "delay": 92
                },
                {
                    "time": "2025-09-25T10:07:36.3590513+08:00",
                    "delay": 85
                },
                {
                    "time": "2025-09-25T10:12:36.4328896+08:00",
                    "delay": 101
                }
            ],
            "id": "1f099b54-1f2f-6dc8-9f3e-1e1878d52efe",
            "interface": "",
            "mptcp": false,
            "name": "ali-hk-relay",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Shadowsocks",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "claw-sg": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:40.1477765+08:00",
                            "delay": 89
                        },
                        {
                            "time": "2025-09-25T09:57:37.1464738+08:00",
                            "delay": 105
                        },
                        {
                            "time": "2025-09-25T10:02:36.3730141+08:00",
                            "delay": 92
                        },
                        {
                            "time": "2025-09-25T10:07:36.3135242+08:00",
                            "delay": 80
                        },
                        {
                            "time": "2025-09-25T10:12:36.3133778+08:00",
                            "delay": 80
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:40.1477765+08:00",
                    "delay": 89
                },
                {
                    "time": "2025-09-25T09:57:37.1464738+08:00",
                    "delay": 105
                },
                {
                    "time": "2025-09-25T10:02:36.3730141+08:00",
                    "delay": 92
                },
                {
                    "time": "2025-09-25T10:07:36.3135242+08:00",
                    "delay": 80
                },
                {
                    "time": "2025-09-25T10:12:36.3133778+08:00",
                    "delay": 80
                }
            ],
            "id": "1f099b54-1f2f-6dc8-b3ff-e397b1450100",
            "interface": "",
            "mptcp": false,
            "name": "claw-sg",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Vless",
            "udp": false,
            "uot": true,
            "xudp": true
        },
        "claw-sg-relay": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:40.6060188+08:00",
                            "delay": 134
                        },
                        {
                            "time": "2025-09-25T09:57:36.9982043+08:00",
                            "delay": 134
                        },
                        {
                            "time": "2025-09-25T10:02:36.7838505+08:00",
                            "delay": 131
                        },
                        {
                            "time": "2025-09-25T10:07:36.912859+08:00",
                            "delay": 127
                        },
                        {
                            "time": "2025-09-25T10:12:36.7611329+08:00",
                            "delay": 122
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:40.6060188+08:00",
                    "delay": 134
                },
                {
                    "time": "2025-09-25T09:57:36.9982043+08:00",
                    "delay": 134
                },
                {
                    "time": "2025-09-25T10:02:36.7838505+08:00",
                    "delay": 131
                },
                {
                    "time": "2025-09-25T10:07:36.912859+08:00",
                    "delay": 127
                },
                {
                    "time": "2025-09-25T10:12:36.7611329+08:00",
                    "delay": 122
                }
            ],
            "id": "1f099b54-1f2f-6dc8-aa84-0f46b510e16e",
            "interface": "",
            "mptcp": false,
            "name": "claw-sg-relay",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Shadowsocks",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "claw-sg2": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:43.0634463+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:39.4576745+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:39.2740966+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:39.416306+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:39.4427935+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:43.0634463+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:39.4576745+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:39.2740966+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:39.416306+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:39.4427935+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f2f-6dc8-bd30-ccc71d3dbaa3",
            "interface": "",
            "mptcp": false,
            "name": "claw-sg2",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Vless",
            "udp": false,
            "uot": true,
            "xudp": true
        },
        "claw-sg2-relay": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:40.3251116+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:36.6331134+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:36.5346327+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:36.6683952+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:36.5016056+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:40.3251116+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:36.6331134+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:36.5346327+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:36.6683952+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:36.5016056+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f2f-6dc8-b6db-c8118abd2c43",
            "interface": "",
            "mptcp": false,
            "name": "claw-sg2-relay",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Shadowsocks",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "dmit-us": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.104375+08:00",
                            "delay": 170
                        },
                        {
                            "time": "2025-09-25T09:57:37.4674348+08:00",
                            "delay": 163
                        },
                        {
                            "time": "2025-09-25T10:02:37.2573215+08:00",
                            "delay": 166
                        },
                        {
                            "time": "2025-09-25T10:07:37.5050047+08:00",
                            "delay": 167
                        },
                        {
                            "time": "2025-09-25T10:12:37.3027181+08:00",
                            "delay": 170
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.104375+08:00",
                    "delay": 170
                },
                {
                    "time": "2025-09-25T09:57:37.4674348+08:00",
                    "delay": 163
                },
                {
                    "time": "2025-09-25T10:02:37.2573215+08:00",
                    "delay": 166
                },
                {
                    "time": "2025-09-25T10:07:37.5050047+08:00",
                    "delay": 167
                },
                {
                    "time": "2025-09-25T10:12:37.3027181+08:00",
                    "delay": 170
                }
            ],
            "id": "1f099b54-1f2f-6dc8-a11f-e656abc187f1",
            "interface": "",
            "mptcp": false,
            "name": "dmit-us",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Vless",
            "udp": false,
            "uot": true,
            "xudp": true
        },
        "dmit-us-relay": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.2587727+08:00",
                            "delay": 196
                        },
                        {
                            "time": "2025-09-25T09:57:37.6175075+08:00",
                            "delay": 202
                        },
                        {
                            "time": "2025-09-25T10:02:37.4150588+08:00",
                            "delay": 187
                        },
                        {
                            "time": "2025-09-25T10:07:37.6510391+08:00",
                            "delay": 222
                        },
                        {
                            "time": "2025-09-25T10:12:37.4143035+08:00",
                            "delay": 196
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.2587727+08:00",
                    "delay": 196
                },
                {
                    "time": "2025-09-25T09:57:37.6175075+08:00",
                    "delay": 202
                },
                {
                    "time": "2025-09-25T10:02:37.4150588+08:00",
                    "delay": 187
                },
                {
                    "time": "2025-09-25T10:07:37.6510391+08:00",
                    "delay": 222
                },
                {
                    "time": "2025-09-25T10:12:37.4143035+08:00",
                    "delay": 196
                }
            ],
            "id": "1f099b54-1f2f-6dc8-b8cf-bda7eb3b5162",
            "interface": "",
            "mptcp": false,
            "name": "dmit-us-relay",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Shadowsocks",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "net-hk": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.5212775+08:00",
                            "delay": 197
                        },
                        {
                            "time": "2025-09-25T09:57:39.3622606+08:00",
                            "delay": 1407
                        },
                        {
                            "time": "2025-09-25T10:02:37.5908564+08:00",
                            "delay": 197
                        },
                        {
                            "time": "2025-09-25T10:07:38.1902798+08:00",
                            "delay": 312
                        },
                        {
                            "time": "2025-09-25T10:12:37.5310322+08:00",
                            "delay": 192
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.5212775+08:00",
                    "delay": 197
                },
                {
                    "time": "2025-09-25T09:57:39.3622606+08:00",
                    "delay": 1407
                },
                {
                    "time": "2025-09-25T10:02:37.5908564+08:00",
                    "delay": 197
                },
                {
                    "time": "2025-09-25T10:07:38.1902798+08:00",
                    "delay": 312
                },
                {
                    "time": "2025-09-25T10:12:37.5310322+08:00",
                    "delay": 192
                }
            ],
            "id": "1f099b54-1f2f-6dc8-8c3c-55f534bbf487",
            "interface": "",
            "mptcp": false,
            "name": "net-hk",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Vless",
            "udp": false,
            "uot": true,
            "xudp": true
        },
        "net-hk-relay": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.1726007+08:00",
                            "delay": 131
                        },
                        {
                            "time": "2025-09-25T09:57:37.912686+08:00",
                            "delay": 263
                        },
                        {
                            "time": "2025-09-25T10:02:37.3598631+08:00",
                            "delay": 133
                        },
                        {
                            "time": "2025-09-25T10:07:37.9096785+08:00",
                            "delay": 272
                        },
                        {
                            "time": "2025-09-25T10:12:37.2589573+08:00",
                            "delay": 144
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.1726007+08:00",
                    "delay": 131
                },
                {
                    "time": "2025-09-25T09:57:37.912686+08:00",
                    "delay": 263
                },
                {
                    "time": "2025-09-25T10:02:37.3598631+08:00",
                    "delay": 133
                },
                {
                    "time": "2025-09-25T10:07:37.9096785+08:00",
                    "delay": 272
                },
                {
                    "time": "2025-09-25T10:12:37.2589573+08:00",
                    "delay": 144
                }
            ],
            "id": "1f099b54-1f2f-6dc8-8864-afb75c8fd523",
            "interface": "",
            "mptcp": false,
            "name": "net-hk-relay",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Shadowsocks",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "silicloud-us": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.5297012+08:00",
                            "delay": 183
                        },
                        {
                            "time": "2025-09-25T09:57:38.9046445+08:00",
                            "delay": 178
                        },
                        {
                            "time": "2025-09-25T10:02:37.5703324+08:00",
                            "delay": 180
                        },
                        {
                            "time": "2025-09-25T10:07:37.7881808+08:00",
                            "delay": 175
                        },
                        {
                            "time": "2025-09-25T10:12:37.5426115+08:00",
                            "delay": 171
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.5297012+08:00",
                    "delay": 183
                },
                {
                    "time": "2025-09-25T09:57:38.9046445+08:00",
                    "delay": 178
                },
                {
                    "time": "2025-09-25T10:02:37.5703324+08:00",
                    "delay": 180
                },
                {
                    "time": "2025-09-25T10:07:37.7881808+08:00",
                    "delay": 175
                },
                {
                    "time": "2025-09-25T10:12:37.5426115+08:00",
                    "delay": 171
                }
            ],
            "id": "1f099b54-1f2f-6dc8-a85b-675304fe1c15",
            "interface": "",
            "mptcp": false,
            "name": "silicloud-us",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Vless",
            "udp": false,
            "uot": true,
            "xudp": true
        },
        "silicloud-us-relay": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.7299605+08:00",
                            "delay": 220
                        },
                        {
                            "time": "2025-09-25T09:57:38.4775879+08:00",
                            "delay": 248
                        },
                        {
                            "time": "2025-09-25T10:02:37.7588051+08:00",
                            "delay": 219
                        },
                        {
                            "time": "2025-09-25T10:07:38.0060636+08:00",
                            "delay": 225
                        },
                        {
                            "time": "2025-09-25T10:12:38.0944018+08:00",
                            "delay": 232
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.7299605+08:00",
                    "delay": 220
                },
                {
                    "time": "2025-09-25T09:57:38.4775879+08:00",
                    "delay": 248
                },
                {
                    "time": "2025-09-25T10:02:37.7588051+08:00",
                    "delay": 219
                },
                {
                    "time": "2025-09-25T10:07:38.0060636+08:00",
                    "delay": 225
                },
                {
                    "time": "2025-09-25T10:12:38.0944018+08:00",
                    "delay": 232
                }
            ],
            "id": "1f099b54-1f2f-6dc8-9ae4-eb2f9afdd441",
            "interface": "",
            "mptcp": false,
            "name": "silicloud-us-relay",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Shadowsocks",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "vps-jp": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.1705303+08:00",
                            "delay": 804
                        },
                        {
                            "time": "2025-09-25T09:57:36.4631322+08:00",
                            "delay": 110
                        },
                        {
                            "time": "2025-09-25T10:02:36.4933838+08:00",
                            "delay": 121
                        },
                        {
                            "time": "2025-09-25T10:07:37.4602642+08:00",
                            "delay": 111
                        },
                        {
                            "time": "2025-09-25T10:12:36.4750146+08:00",
                            "delay": 123
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.1705303+08:00",
                    "delay": 804
                },
                {
                    "time": "2025-09-25T09:57:36.4631322+08:00",
                    "delay": 110
                },
                {
                    "time": "2025-09-25T10:02:36.4933838+08:00",
                    "delay": 121
                },
                {
                    "time": "2025-09-25T10:07:37.4602642+08:00",
                    "delay": 111
                },
                {
                    "time": "2025-09-25T10:12:36.4750146+08:00",
                    "delay": 123
                }
            ],
            "id": "1f099b54-1f2f-6dc8-b22b-78f4e70fec7e",
            "interface": "",
            "mptcp": false,
            "name": "vps-jp",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Vless",
            "udp": false,
            "uot": true,
            "xudp": true
        },
        "vps-jp-relay": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:40.4740557+08:00",
                            "delay": 165
                        },
                        {
                            "time": "2025-09-25T09:57:37.2103223+08:00",
                            "delay": 176
                        },
                        {
                            "time": "2025-09-25T10:02:36.6339406+08:00",
                            "delay": 157
                        },
                        {
                            "time": "2025-09-25T10:07:36.6589751+08:00",
                            "delay": 159
                        },
                        {
                            "time": "2025-09-25T10:12:37.266993+08:00",
                            "delay": 160
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:40.4740557+08:00",
                    "delay": 165
                },
                {
                    "time": "2025-09-25T09:57:37.2103223+08:00",
                    "delay": 176
                },
                {
                    "time": "2025-09-25T10:02:36.6339406+08:00",
                    "delay": 157
                },
                {
                    "time": "2025-09-25T10:07:36.6589751+08:00",
                    "delay": 159
                },
                {
                    "time": "2025-09-25T10:12:37.266993+08:00",
                    "delay": 160
                }
            ],
            "id": "1f099b54-1f2f-6dc8-916d-4e491f980d27",
            "interface": "",
            "mptcp": false,
            "name": "vps-jp-relay",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Shadowsocks",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "wawo-hk": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.9925014+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:38.2138993+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:38.2143414+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:38.2571239+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:38.2431065+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.9925014+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:38.2138993+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:38.2143414+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:38.2571239+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:38.2431065+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f2f-6dc8-9c98-62502a226548",
            "interface": "",
            "mptcp": false,
            "name": "wawo-hk",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Vless",
            "udp": false,
            "uot": true,
            "xudp": true
        },
        "wawo-hk-relay": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:39.9671138+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:36.3580132+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:36.1672613+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:37.201428+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:36.1824793+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:39.9671138+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:36.3580132+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:36.1672613+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:37.201428+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:36.1824793+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f2f-6dc8-8253-86e3b291d95e",
            "interface": "",
            "mptcp": false,
            "name": "wawo-hk-relay",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Shadowsocks",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "zgo-us": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:43.6858321+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:39.9953641+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:39.5648939+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:40.0374794+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:39.5987589+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:43.6858321+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:39.9953641+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:39.5648939+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:40.0374794+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:39.5987589+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f2f-6dc8-bf6f-6886745f7e01",
            "interface": "",
            "mptcp": false,
            "name": "zgo-us",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Vless",
            "udp": false,
            "uot": true,
            "xudp": true
        },
        "zgo-us-relay": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.357524+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:37.4431619+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:37.0382991+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:37.7030555+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:37.4910459+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.357524+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:37.4431619+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:37.0382991+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:37.7030555+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:37.4910459+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f2f-6dc8-8d9c-102fdaca5b1a",
            "interface": "",
            "mptcp": false,
            "name": "zgo-us-relay",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Shadowsocks",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "♻️ Auto": {
            "alive": true,
            "all": [
                "🇯🇵 日本|Auto",
                "🇭🇰 香港|Auto",
                "🇹🇼 台湾|Auto",
                "🇸🇬 新加坡|Auto",
                "🇺🇸 美国|Auto"
            ],
            "dialer-proxy": "",
            "expectedStatus": "*",
            "extra": {},
            "fixed": "",
            "hidden": false,
            "history": [],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "♻️ Auto",
            "now": "🇯🇵 日本|Auto",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "https://www.apple.com/library/test/success.html",
            "tfo": false,
            "type": "Fallback",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "🇭🇰 [Any]HK 01": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:43.1473834+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:40.2705849+08:00",
                            "delay": 404
                        },
                        {
                            "time": "2025-09-25T10:02:41.9058844+08:00",
                            "delay": 621
                        },
                        {
                            "time": "2025-09-25T10:07:42.5056444+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:40.7866689+08:00",
                            "delay": 613
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:43.1473834+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:40.2705849+08:00",
                    "delay": 404
                },
                {
                    "time": "2025-09-25T10:02:41.9058844+08:00",
                    "delay": 621
                },
                {
                    "time": "2025-09-25T10:07:42.5056444+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:40.7866689+08:00",
                    "delay": 613
                }
            ],
            "id": "1f099b54-1f2f-6dc8-840c-2f1d2c656384",
            "interface": "",
            "mptcp": false,
            "name": "🇭🇰 [Any]HK 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "AnyTLS",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇭🇰 [Any]HK 02": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.6797184+08:00",
                            "delay": 99
                        },
                        {
                            "time": "2025-09-25T09:57:37.9701437+08:00",
                            "delay": 99
                        },
                        {
                            "time": "2025-09-25T10:02:37.7608223+08:00",
                            "delay": 99
                        },
                        {
                            "time": "2025-09-25T10:07:38.1477485+08:00",
                            "delay": 98
                        },
                        {
                            "time": "2025-09-25T10:12:37.702251+08:00",
                            "delay": 101
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.6797184+08:00",
                    "delay": 99
                },
                {
                    "time": "2025-09-25T09:57:37.9701437+08:00",
                    "delay": 99
                },
                {
                    "time": "2025-09-25T10:02:37.7608223+08:00",
                    "delay": 99
                },
                {
                    "time": "2025-09-25T10:07:38.1477485+08:00",
                    "delay": 98
                },
                {
                    "time": "2025-09-25T10:12:37.702251+08:00",
                    "delay": 101
                }
            ],
            "id": "1f099b54-1f2f-6dc8-bf69-8cb6a1e05b5c",
            "interface": "",
            "mptcp": false,
            "name": "🇭🇰 [Any]HK 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "AnyTLS",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇭🇰 [Any]HK 03": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.9834528+08:00",
                            "delay": 149
                        },
                        {
                            "time": "2025-09-25T09:57:38.3410361+08:00",
                            "delay": 127
                        },
                        {
                            "time": "2025-09-25T10:02:38.1753779+08:00",
                            "delay": 141
                        },
                        {
                            "time": "2025-09-25T10:07:38.3350742+08:00",
                            "delay": 142
                        },
                        {
                            "time": "2025-09-25T10:12:38.0541041+08:00",
                            "delay": 124
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.9834528+08:00",
                    "delay": 149
                },
                {
                    "time": "2025-09-25T09:57:38.3410361+08:00",
                    "delay": 127
                },
                {
                    "time": "2025-09-25T10:02:38.1753779+08:00",
                    "delay": 141
                },
                {
                    "time": "2025-09-25T10:07:38.3350742+08:00",
                    "delay": 142
                },
                {
                    "time": "2025-09-25T10:12:38.0541041+08:00",
                    "delay": 124
                }
            ],
            "id": "1f099b54-1f2f-6dc8-815b-3a020987eff3",
            "interface": "",
            "mptcp": false,
            "name": "🇭🇰 [Any]HK 03",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "AnyTLS",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇭🇰 [Any]HK 04": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.5501825+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:38.4435003+08:00",
                            "delay": 96
                        },
                        {
                            "time": "2025-09-25T10:02:37.833073+08:00",
                            "delay": 69
                        },
                        {
                            "time": "2025-09-25T10:07:38.2303284+08:00",
                            "delay": 97
                        },
                        {
                            "time": "2025-09-25T10:12:38.0070777+08:00",
                            "delay": 90
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.5501825+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:38.4435003+08:00",
                    "delay": 96
                },
                {
                    "time": "2025-09-25T10:02:37.833073+08:00",
                    "delay": 69
                },
                {
                    "time": "2025-09-25T10:07:38.2303284+08:00",
                    "delay": 97
                },
                {
                    "time": "2025-09-25T10:12:38.0070777+08:00",
                    "delay": 90
                }
            ],
            "id": "1f099b54-1f2f-6dc8-b42f-f5d799107f7f",
            "interface": "",
            "mptcp": false,
            "name": "🇭🇰 [Any]HK 04",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "AnyTLS",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇭🇰 [Hy2]HK 01": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.7958648+08:00",
                            "delay": 53
                        },
                        {
                            "time": "2025-09-25T09:57:38.3011666+08:00",
                            "delay": 51
                        },
                        {
                            "time": "2025-09-25T10:02:38.0485692+08:00",
                            "delay": 171
                        },
                        {
                            "time": "2025-09-25T10:07:38.2327644+08:00",
                            "delay": 62
                        },
                        {
                            "time": "2025-09-25T10:12:37.8445653+08:00",
                            "delay": 69
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.7958648+08:00",
                    "delay": 53
                },
                {
                    "time": "2025-09-25T09:57:38.3011666+08:00",
                    "delay": 51
                },
                {
                    "time": "2025-09-25T10:02:38.0485692+08:00",
                    "delay": 171
                },
                {
                    "time": "2025-09-25T10:07:38.2327644+08:00",
                    "delay": 62
                },
                {
                    "time": "2025-09-25T10:12:37.8445653+08:00",
                    "delay": 69
                }
            ],
            "id": "1f099b54-1f2f-6dc8-812e-2bed1afa5fea",
            "interface": "",
            "mptcp": false,
            "name": "🇭🇰 [Hy2]HK 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Hysteria2",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "🇭🇰 [Hy2]HK 02": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.8055028+08:00",
                            "delay": 54
                        },
                        {
                            "time": "2025-09-25T09:57:38.8596875+08:00",
                            "delay": 51
                        },
                        {
                            "time": "2025-09-25T10:02:37.8448567+08:00",
                            "delay": 49
                        },
                        {
                            "time": "2025-09-25T10:07:38.2821209+08:00",
                            "delay": 60
                        },
                        {
                            "time": "2025-09-25T10:12:37.8024938+08:00",
                            "delay": 44
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.8055028+08:00",
                    "delay": 54
                },
                {
                    "time": "2025-09-25T09:57:38.8596875+08:00",
                    "delay": 51
                },
                {
                    "time": "2025-09-25T10:02:37.8448567+08:00",
                    "delay": 49
                },
                {
                    "time": "2025-09-25T10:07:38.2821209+08:00",
                    "delay": 60
                },
                {
                    "time": "2025-09-25T10:12:37.8024938+08:00",
                    "delay": 44
                }
            ],
            "id": "1f099b54-1f2f-6dc8-80b4-db0e8e3741dc",
            "interface": "",
            "mptcp": false,
            "name": "🇭🇰 [Hy2]HK 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Hysteria2",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "🇭🇰 [Hy2]HK 03": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:42.085101+08:00",
                            "delay": 101
                        },
                        {
                            "time": "2025-09-25T09:57:38.8827413+08:00",
                            "delay": 96
                        },
                        {
                            "time": "2025-09-25T10:02:38.355331+08:00",
                            "delay": 194
                        },
                        {
                            "time": "2025-09-25T10:07:38.6582183+08:00",
                            "delay": 106
                        },
                        {
                            "time": "2025-09-25T10:12:38.2331327+08:00",
                            "delay": 97
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:42.085101+08:00",
                    "delay": 101
                },
                {
                    "time": "2025-09-25T09:57:38.8827413+08:00",
                    "delay": 96
                },
                {
                    "time": "2025-09-25T10:02:38.355331+08:00",
                    "delay": 194
                },
                {
                    "time": "2025-09-25T10:07:38.6582183+08:00",
                    "delay": 106
                },
                {
                    "time": "2025-09-25T10:12:38.2331327+08:00",
                    "delay": 97
                }
            ],
            "id": "1f099b54-1f2f-6dc8-98d3-771a941c496c",
            "interface": "",
            "mptcp": false,
            "name": "🇭🇰 [Hy2]HK 03",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Hysteria2",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "🇭🇰 [IPv6]HK 01": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.6797184+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:38.341554+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:37.7608223+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:38.1902798+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:37.8030358+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.6797184+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:38.341554+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:37.7608223+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:38.1902798+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:37.8030358+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f2f-6dc8-ad69-2936e3877d3c",
            "interface": "",
            "mptcp": false,
            "name": "🇭🇰 [IPv6]HK 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇭🇰 [IPv6]HK 02": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.680232+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:38.341554+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:37.7615269+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:38.1902798+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:37.8035756+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.680232+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:38.341554+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:37.7615269+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:38.1902798+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:37.8035756+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f31-620b-88b8-a97263f17899",
            "interface": "",
            "mptcp": false,
            "name": "🇭🇰 [IPv6]HK 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇭🇰 [三网]HK 01": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:41.9736902+08:00",
                            "delay": 64
                        },
                        {
                            "time": "2025-09-25T09:57:38.6732753+08:00",
                            "delay": 77
                        },
                        {
                            "time": "2025-09-25T10:02:38.1277937+08:00",
                            "delay": 72
                        },
                        {
                            "time": "2025-09-25T10:07:38.8722028+08:00",
                            "delay": 99
                        },
                        {
                            "time": "2025-09-25T10:12:38.1517729+08:00",
                            "delay": 70
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:41.9736902+08:00",
                    "delay": 64
                },
                {
                    "time": "2025-09-25T09:57:38.6732753+08:00",
                    "delay": 77
                },
                {
                    "time": "2025-09-25T10:02:38.1277937+08:00",
                    "delay": 72
                },
                {
                    "time": "2025-09-25T10:07:38.8722028+08:00",
                    "delay": 99
                },
                {
                    "time": "2025-09-25T10:12:38.1517729+08:00",
                    "delay": 70
                }
            ],
            "id": "1f099b54-1f31-620b-a9be-40464a9b3b09",
            "interface": "",
            "mptcp": false,
            "name": "🇭🇰 [三网]HK 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇭🇰 [三网]HK 03": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:42.1412897+08:00",
                            "delay": 101
                        },
                        {
                            "time": "2025-09-25T09:57:38.8376018+08:00",
                            "delay": 105
                        },
                        {
                            "time": "2025-09-25T10:02:38.0235277+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:38.3401492+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:38.1833153+08:00",
                            "delay": 93
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:42.1412897+08:00",
                    "delay": 101
                },
                {
                    "time": "2025-09-25T09:57:38.8376018+08:00",
                    "delay": 105
                },
                {
                    "time": "2025-09-25T10:02:38.0235277+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:38.3401492+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:38.1833153+08:00",
                    "delay": 93
                }
            ],
            "id": "1f099b54-1f31-620b-b426-58057059306c",
            "interface": "",
            "mptcp": false,
            "name": "🇭🇰 [三网]HK 03",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇭🇰 [三网]HK 04": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:42.4826745+08:00",
                            "delay": 93
                        },
                        {
                            "time": "2025-09-25T09:57:39.0555068+08:00",
                            "delay": 96
                        },
                        {
                            "time": "2025-09-25T10:02:38.23877+08:00",
                            "delay": 92
                        },
                        {
                            "time": "2025-09-25T10:07:38.8398123+08:00",
                            "delay": 92
                        },
                        {
                            "time": "2025-09-25T10:12:38.4323285+08:00",
                            "delay": 95
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:42.4826745+08:00",
                    "delay": 93
                },
                {
                    "time": "2025-09-25T09:57:39.0555068+08:00",
                    "delay": 96
                },
                {
                    "time": "2025-09-25T10:02:38.23877+08:00",
                    "delay": 92
                },
                {
                    "time": "2025-09-25T10:07:38.8398123+08:00",
                    "delay": 92
                },
                {
                    "time": "2025-09-25T10:12:38.4323285+08:00",
                    "delay": 95
                }
            ],
            "id": "1f099b54-1f31-620b-aba5-4e9053587ea1",
            "interface": "",
            "mptcp": false,
            "name": "🇭🇰 [三网]HK 04",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇭🇰 [移动]HK 02": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:42.1544623+08:00",
                            "delay": 73
                        },
                        {
                            "time": "2025-09-25T09:57:39.0277486+08:00",
                            "delay": 76
                        },
                        {
                            "time": "2025-09-25T10:02:43.0240136+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:38.5854754+08:00",
                            "delay": 70
                        },
                        {
                            "time": "2025-09-25T10:12:38.3980193+08:00",
                            "delay": 77
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:42.1544623+08:00",
                    "delay": 73
                },
                {
                    "time": "2025-09-25T09:57:39.0277486+08:00",
                    "delay": 76
                },
                {
                    "time": "2025-09-25T10:02:43.0240136+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:38.5854754+08:00",
                    "delay": 70
                },
                {
                    "time": "2025-09-25T10:12:38.3980193+08:00",
                    "delay": 77
                }
            ],
            "id": "1f099b54-1f31-620b-9a0c-a0034c2f2b6f",
            "interface": "",
            "mptcp": false,
            "name": "🇭🇰 [移动]HK 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇭🇰 香港|Auto": {
            "alive": true,
            "all": [
                "wawo-hk",
                "wawo-hk-relay",
                "ali-hk",
                "ali-hk-relay",
                "net-hk",
                "net-hk-relay",
                "🇭🇰 [Any]HK 01",
                "🇭🇰 [Any]HK 02",
                "🇭🇰 [Any]HK 03",
                "🇭🇰 [Any]HK 04",
                "🇭🇰 [Hy2]HK 01",
                "🇭🇰 [Hy2]HK 02",
                "🇭🇰 [Hy2]HK 03",
                "🇭🇰 [IPv6]HK 01",
                "🇭🇰 [IPv6]HK 02",
                "🇭🇰 [三网]HK 01",
                "🇭🇰 [三网]HK 03",
                "🇭🇰 [三网]HK 04",
                "🇭🇰 [移动]HK 02"
            ],
            "dialer-proxy": "",
            "expectedStatus": "*",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-24T15:52:34.3731789+08:00",
                            "delay": 290
                        }
                    ]
                }
            },
            "fixed": "",
            "hidden": false,
            "history": [
                {
                    "time": "2025-09-24T15:52:34.3731789+08:00",
                    "delay": 290
                }
            ],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "🇭🇰 香港|Auto",
            "now": "ali-hk",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "https://www.apple.com/library/test/success.html",
            "tfo": false,
            "type": "Fallback",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "🇯🇵 [Any]JP 01": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:42.3993342+08:00",
                            "delay": 88
                        },
                        {
                            "time": "2025-09-25T09:57:39.3048977+08:00",
                            "delay": 93
                        },
                        {
                            "time": "2025-09-25T10:02:38.2112509+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:38.6098815+08:00",
                            "delay": 66
                        },
                        {
                            "time": "2025-09-25T10:12:38.4587341+08:00",
                            "delay": 69
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:42.3993342+08:00",
                    "delay": 88
                },
                {
                    "time": "2025-09-25T09:57:39.3048977+08:00",
                    "delay": 93
                },
                {
                    "time": "2025-09-25T10:02:38.2112509+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:38.6098815+08:00",
                    "delay": 66
                },
                {
                    "time": "2025-09-25T10:12:38.4587341+08:00",
                    "delay": 69
                }
            ],
            "id": "1f099b54-1f31-620b-ab40-1bac6d9add3e",
            "interface": "",
            "mptcp": false,
            "name": "🇯🇵 [Any]JP 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "AnyTLS",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇯🇵 [Any]JP 02": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:42.4772002+08:00",
                            "delay": 102
                        },
                        {
                            "time": "2025-09-25T09:57:39.3307916+08:00",
                            "delay": 93
                        },
                        {
                            "time": "2025-09-25T10:02:38.2707886+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:38.4969661+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:38.5600518+08:00",
                            "delay": 76
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:42.4772002+08:00",
                    "delay": 102
                },
                {
                    "time": "2025-09-25T09:57:39.3307916+08:00",
                    "delay": 93
                },
                {
                    "time": "2025-09-25T10:02:38.2707886+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:38.4969661+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:38.5600518+08:00",
                    "delay": 76
                }
            ],
            "id": "1f099b54-1f31-620b-ae6f-77521b91c9c1",
            "interface": "",
            "mptcp": false,
            "name": "🇯🇵 [Any]JP 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "AnyTLS",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇯🇵 [Any]JP 03": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:42.4357678+08:00",
                            "delay": 88
                        },
                        {
                            "time": "2025-09-25T09:57:39.2373846+08:00",
                            "delay": 68
                        },
                        {
                            "time": "2025-09-25T10:02:39.5694024+08:00",
                            "delay": 809
                        },
                        {
                            "time": "2025-09-25T10:07:39.8158202+08:00",
                            "delay": 76
                        },
                        {
                            "time": "2025-09-25T10:12:38.5551242+08:00",
                            "delay": 72
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:42.4357678+08:00",
                    "delay": 88
                },
                {
                    "time": "2025-09-25T09:57:39.2373846+08:00",
                    "delay": 68
                },
                {
                    "time": "2025-09-25T10:02:39.5694024+08:00",
                    "delay": 809
                },
                {
                    "time": "2025-09-25T10:07:39.8158202+08:00",
                    "delay": 76
                },
                {
                    "time": "2025-09-25T10:12:38.5551242+08:00",
                    "delay": 72
                }
            ],
            "id": "1f099b54-1f31-620b-a518-028214f24f6a",
            "interface": "",
            "mptcp": false,
            "name": "🇯🇵 [Any]JP 03",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "AnyTLS",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇯🇵 [Hy2]JP 01": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:42.6430185+08:00",
                            "delay": 85
                        },
                        {
                            "time": "2025-09-25T09:57:39.3622606+08:00",
                            "delay": 99
                        },
                        {
                            "time": "2025-09-25T10:02:38.6056928+08:00",
                            "delay": 84
                        },
                        {
                            "time": "2025-09-25T10:07:38.9779206+08:00",
                            "delay": 82
                        },
                        {
                            "time": "2025-09-25T10:12:38.6626715+08:00",
                            "delay": 82
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:42.6430185+08:00",
                    "delay": 85
                },
                {
                    "time": "2025-09-25T09:57:39.3622606+08:00",
                    "delay": 99
                },
                {
                    "time": "2025-09-25T10:02:38.6056928+08:00",
                    "delay": 84
                },
                {
                    "time": "2025-09-25T10:07:38.9779206+08:00",
                    "delay": 82
                },
                {
                    "time": "2025-09-25T10:12:38.6626715+08:00",
                    "delay": 82
                }
            ],
            "id": "1f099b54-1f31-620b-8be2-9ee746786f31",
            "interface": "",
            "mptcp": false,
            "name": "🇯🇵 [Hy2]JP 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Hysteria2",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "🇯🇵 [Hy2]JP 02": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:42.5536314+08:00",
                            "delay": 79
                        },
                        {
                            "time": "2025-09-25T09:57:39.3715975+08:00",
                            "delay": 66
                        },
                        {
                            "time": "2025-09-25T10:02:38.5751396+08:00",
                            "delay": 74
                        },
                        {
                            "time": "2025-09-25T10:07:39.0265315+08:00",
                            "delay": 83
                        },
                        {
                            "time": "2025-09-25T10:12:38.7789759+08:00",
                            "delay": 71
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:42.5536314+08:00",
                    "delay": 79
                },
                {
                    "time": "2025-09-25T09:57:39.3715975+08:00",
                    "delay": 66
                },
                {
                    "time": "2025-09-25T10:02:38.5751396+08:00",
                    "delay": 74
                },
                {
                    "time": "2025-09-25T10:07:39.0265315+08:00",
                    "delay": 83
                },
                {
                    "time": "2025-09-25T10:12:38.7789759+08:00",
                    "delay": 71
                }
            ],
            "id": "1f099b54-1f31-620b-b193-f0ae525c5790",
            "interface": "",
            "mptcp": false,
            "name": "🇯🇵 [Hy2]JP 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Hysteria2",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "🇯🇵 [IPv6]JP 01": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:42.1552286+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:39.0555068+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:38.2392907+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:38.6104255+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:38.3985619+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:42.1552286+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:39.0555068+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:38.2392907+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:38.6104255+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:38.3985619+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f31-620b-a730-f20773eec1ba",
            "interface": "",
            "mptcp": false,
            "name": "🇯🇵 [IPv6]JP 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇯🇵 [IPv6]JP 02": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:42.1552286+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:39.0562675+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:38.2392907+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:38.610957+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:38.3990975+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:42.1552286+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:39.0562675+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:38.2392907+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:38.610957+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:38.3990975+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f31-620b-aeff-4b76e0b448c4",
            "interface": "",
            "mptcp": false,
            "name": "🇯🇵 [IPv6]JP 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇯🇵 [三网]JP 01": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:42.9174949+08:00",
                            "delay": 169
                        },
                        {
                            "time": "2025-09-25T09:57:40.540563+08:00",
                            "delay": 161
                        },
                        {
                            "time": "2025-09-25T10:02:39.2012503+08:00",
                            "delay": 202
                        },
                        {
                            "time": "2025-09-25T10:07:39.4714851+08:00",
                            "delay": 158
                        },
                        {
                            "time": "2025-09-25T10:12:39.5374025+08:00",
                            "delay": 169
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:42.9174949+08:00",
                    "delay": 169
                },
                {
                    "time": "2025-09-25T09:57:40.540563+08:00",
                    "delay": 161
                },
                {
                    "time": "2025-09-25T10:02:39.2012503+08:00",
                    "delay": 202
                },
                {
                    "time": "2025-09-25T10:07:39.4714851+08:00",
                    "delay": 158
                },
                {
                    "time": "2025-09-25T10:12:39.5374025+08:00",
                    "delay": 169
                }
            ],
            "id": "1f099b54-1f31-620b-8da9-8235088225d2",
            "interface": "",
            "mptcp": false,
            "name": "🇯🇵 [三网]JP 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇯🇵 [移动]JP 02": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:42.9887053+08:00",
                            "delay": 120
                        },
                        {
                            "time": "2025-09-25T09:57:39.7882221+08:00",
                            "delay": 115
                        },
                        {
                            "time": "2025-09-25T10:02:38.8164842+08:00",
                            "delay": 117
                        },
                        {
                            "time": "2025-09-25T10:07:39.2275583+08:00",
                            "delay": 118
                        },
                        {
                            "time": "2025-09-25T10:12:39.0212323+08:00",
                            "delay": 135
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:42.9887053+08:00",
                    "delay": 120
                },
                {
                    "time": "2025-09-25T09:57:39.7882221+08:00",
                    "delay": 115
                },
                {
                    "time": "2025-09-25T10:02:38.8164842+08:00",
                    "delay": 117
                },
                {
                    "time": "2025-09-25T10:07:39.2275583+08:00",
                    "delay": 118
                },
                {
                    "time": "2025-09-25T10:12:39.0212323+08:00",
                    "delay": 135
                }
            ],
            "id": "1f099b54-1f31-620b-8a2f-1d44a66777f6",
            "interface": "",
            "mptcp": false,
            "name": "🇯🇵 [移动]JP 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇯🇵 日本|Auto": {
            "alive": true,
            "all": [
                "vps-jp",
                "vps-jp-relay",
                "🇯🇵 [Any]JP 01",
                "🇯🇵 [Any]JP 02",
                "🇯🇵 [Any]JP 03",
                "🇯🇵 [Hy2]JP 01",
                "🇯🇵 [Hy2]JP 02",
                "🇯🇵 [IPv6]JP 01",
                "🇯🇵 [IPv6]JP 02",
                "🇯🇵 [三网]JP 01",
                "🇯🇵 [移动]JP 02"
            ],
            "dialer-proxy": "",
            "expectedStatus": "*",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-24T15:52:35.0896596+08:00",
                            "delay": 1051
                        }
                    ]
                }
            },
            "fixed": "🇯🇵日本｜三网BGP｜3x",
            "hidden": false,
            "history": [
                {
                    "time": "2025-09-24T15:52:35.0896596+08:00",
                    "delay": 1051
                }
            ],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "🇯🇵 日本|Auto",
            "now": "vps-jp",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "https://www.apple.com/library/test/success.html",
            "tfo": false,
            "type": "Fallback",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "🇸🇬 [Any]SG 01": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:43.4828649+08:00",
                            "delay": 193
                        },
                        {
                            "time": "2025-09-25T09:57:40.1725807+08:00",
                            "delay": 199
                        },
                        {
                            "time": "2025-09-25T10:02:39.3557777+08:00",
                            "delay": 200
                        },
                        {
                            "time": "2025-09-25T10:07:39.4703861+08:00",
                            "delay": 114
                        },
                        {
                            "time": "2025-09-25T10:12:39.3319943+08:00",
                            "delay": 196
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:43.4828649+08:00",
                    "delay": 193
                },
                {
                    "time": "2025-09-25T09:57:40.1725807+08:00",
                    "delay": 199
                },
                {
                    "time": "2025-09-25T10:02:39.3557777+08:00",
                    "delay": 200
                },
                {
                    "time": "2025-09-25T10:07:39.4703861+08:00",
                    "delay": 114
                },
                {
                    "time": "2025-09-25T10:12:39.3319943+08:00",
                    "delay": 196
                }
            ],
            "id": "1f099b54-1f31-620b-9678-8b79fa59bc24",
            "interface": "",
            "mptcp": false,
            "name": "🇸🇬 [Any]SG 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "AnyTLS",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇸🇬 [Any]SG 02": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:43.5076518+08:00",
                            "delay": 428
                        },
                        {
                            "time": "2025-09-25T09:57:39.978074+08:00",
                            "delay": 140
                        },
                        {
                            "time": "2025-09-25T10:02:38.6882203+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:39.0193266+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:39.2761277+08:00",
                            "delay": 147
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:43.5076518+08:00",
                    "delay": 428
                },
                {
                    "time": "2025-09-25T09:57:39.978074+08:00",
                    "delay": 140
                },
                {
                    "time": "2025-09-25T10:02:38.6882203+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:39.0193266+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:39.2761277+08:00",
                    "delay": 147
                }
            ],
            "id": "1f099b54-1f31-620b-9146-1ff8b8a90897",
            "interface": "",
            "mptcp": false,
            "name": "🇸🇬 [Any]SG 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "AnyTLS",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇸🇬 [IPv6]SG 01": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:42.4832124+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:39.3622606+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:38.6056928+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:38.9779206+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:38.5605969+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:42.4832124+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:39.3622606+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:38.6056928+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:38.9779206+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:38.5605969+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f31-620b-92b3-4419ad5e85c3",
            "interface": "",
            "mptcp": false,
            "name": "🇸🇬 [IPv6]SG 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇸🇬 [IPv6]SG 02": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:42.4837554+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:39.3627779+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:38.6056928+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:38.9779206+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:38.5605969+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:42.4837554+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:39.3627779+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:38.6056928+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:38.9779206+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:38.5605969+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f31-620b-a0b0-d8cc51cbf707",
            "interface": "",
            "mptcp": false,
            "name": "🇸🇬 [IPv6]SG 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇸🇬 [三网]SG 01": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:43.2617032+08:00",
                            "delay": 382
                        },
                        {
                            "time": "2025-09-25T09:57:39.8994109+08:00",
                            "delay": 125
                        },
                        {
                            "time": "2025-09-25T10:02:39.0322371+08:00",
                            "delay": 96
                        },
                        {
                            "time": "2025-09-25T10:07:39.4672484+08:00",
                            "delay": 128
                        },
                        {
                            "time": "2025-09-25T10:12:39.0321304+08:00",
                            "delay": 94
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:43.2617032+08:00",
                    "delay": 382
                },
                {
                    "time": "2025-09-25T09:57:39.8994109+08:00",
                    "delay": 125
                },
                {
                    "time": "2025-09-25T10:02:39.0322371+08:00",
                    "delay": 96
                },
                {
                    "time": "2025-09-25T10:07:39.4672484+08:00",
                    "delay": 128
                },
                {
                    "time": "2025-09-25T10:12:39.0321304+08:00",
                    "delay": 94
                }
            ],
            "id": "1f099b54-1f31-620b-b0a2-af49ee0ce38c",
            "interface": "",
            "mptcp": false,
            "name": "🇸🇬 [三网]SG 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇸🇬 [移动]SG 02": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:43.3409728+08:00",
                            "delay": 425
                        },
                        {
                            "time": "2025-09-25T09:57:39.8615801+08:00",
                            "delay": 104
                        },
                        {
                            "time": "2025-09-25T10:02:39.1200252+08:00",
                            "delay": 99
                        },
                        {
                            "time": "2025-09-25T10:07:39.6430402+08:00",
                            "delay": 106
                        },
                        {
                            "time": "2025-09-25T10:12:39.157927+08:00",
                            "delay": 102
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:43.3409728+08:00",
                    "delay": 425
                },
                {
                    "time": "2025-09-25T09:57:39.8615801+08:00",
                    "delay": 104
                },
                {
                    "time": "2025-09-25T10:02:39.1200252+08:00",
                    "delay": 99
                },
                {
                    "time": "2025-09-25T10:07:39.6430402+08:00",
                    "delay": 106
                },
                {
                    "time": "2025-09-25T10:12:39.157927+08:00",
                    "delay": 102
                }
            ],
            "id": "1f099b54-1f31-620b-8cfe-784e58cd5a8a",
            "interface": "",
            "mptcp": false,
            "name": "🇸🇬 [移动]SG 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇸🇬 新加坡|Auto": {
            "alive": true,
            "all": [
                "claw-sg",
                "claw-sg-relay",
                "claw-sg2",
                "claw-sg2-relay",
                "🇸🇬 [Any]SG 01",
                "🇸🇬 [Any]SG 02",
                "🇸🇬 [IPv6]SG 01",
                "🇸🇬 [IPv6]SG 02",
                "🇸🇬 [三网]SG 01",
                "🇸🇬 [移动]SG 02"
            ],
            "dialer-proxy": "",
            "expectedStatus": "*",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-24T15:52:34.3586192+08:00",
                            "delay": 287
                        }
                    ]
                }
            },
            "fixed": "🇸🇬新加坡｜三网IEPL专线1️⃣｜3x",
            "hidden": false,
            "history": [
                {
                    "time": "2025-09-24T15:52:34.3586192+08:00",
                    "delay": 287
                }
            ],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "🇸🇬 新加坡|Auto",
            "now": "claw-sg",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "https://www.apple.com/library/test/success.html",
            "tfo": false,
            "type": "Fallback",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "🇹🇼 [Any]TW 01": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:44.687437+08:00",
                            "delay": 187
                        },
                        {
                            "time": "2025-09-25T09:57:41.9802313+08:00",
                            "delay": 698
                        },
                        {
                            "time": "2025-09-25T10:02:42.3708988+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:39.1657069+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:39.7368014+08:00",
                            "delay": 199
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:44.687437+08:00",
                    "delay": 187
                },
                {
                    "time": "2025-09-25T09:57:41.9802313+08:00",
                    "delay": 698
                },
                {
                    "time": "2025-09-25T10:02:42.3708988+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:39.1657069+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:39.7368014+08:00",
                    "delay": 199
                }
            ],
            "id": "1f099b54-1f31-620b-afd8-1eb7fbea79f0",
            "interface": "",
            "mptcp": false,
            "name": "🇹🇼 [Any]TW 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "AnyTLS",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇹🇼 [Any]TW 02": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:43.6943114+08:00",
                            "delay": 159
                        },
                        {
                            "time": "2025-09-25T09:57:40.3572224+08:00",
                            "delay": 174
                        },
                        {
                            "time": "2025-09-25T10:02:40.1632509+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:42.5872407+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:42.4017659+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:43.6943114+08:00",
                    "delay": 159
                },
                {
                    "time": "2025-09-25T09:57:40.3572224+08:00",
                    "delay": 174
                },
                {
                    "time": "2025-09-25T10:02:40.1632509+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:42.5872407+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:42.4017659+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f31-620b-94f1-df2255170d72",
            "interface": "",
            "mptcp": false,
            "name": "🇹🇼 [Any]TW 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "AnyTLS",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇹🇼 [Hy2]TW 01": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:46.403205+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:44.7885639+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:42.5410868+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:40.3749835+08:00",
                            "delay": 96
                        },
                        {
                            "time": "2025-09-25T10:12:39.8101958+08:00",
                            "delay": 89
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:46.403205+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:44.7885639+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:42.5410868+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:40.3749835+08:00",
                    "delay": 96
                },
                {
                    "time": "2025-09-25T10:12:39.8101958+08:00",
                    "delay": 89
                }
            ],
            "id": "1f099b54-1f31-620b-b965-d31b8be7cead",
            "interface": "",
            "mptcp": false,
            "name": "🇹🇼 [Hy2]TW 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Hysteria2",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "🇹🇼 [IPv6]TW 01": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:43.0634463+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:39.8615801+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:39.2017693+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:39.4168696+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:39.1590887+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:43.0634463+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:39.8615801+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:39.2017693+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:39.4168696+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:39.1590887+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f31-620b-89bf-808366630d89",
            "interface": "",
            "mptcp": false,
            "name": "🇹🇼 [IPv6]TW 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇹🇼 [IPv6]TW 02": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:43.0634463+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:39.8615801+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:39.2017693+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:39.4174049+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:39.1596351+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:43.0634463+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:39.8615801+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:39.2017693+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:39.4174049+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:39.1596351+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f32-65cb-a4ce-95c4ed952b4b",
            "interface": "",
            "mptcp": false,
            "name": "🇹🇼 [IPv6]TW 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇹🇼 [三网]TW 01": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:46.6277433+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:43.4996018+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:42.9506621+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:43.0533396+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:42.7920911+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:46.6277433+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:43.4996018+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:42.9506621+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:43.0533396+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:42.7920911+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f32-6638-82ae-c467af454fc5",
            "interface": "",
            "mptcp": false,
            "name": "🇹🇼 [三网]TW 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇹🇼 [三网]TW 02": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:48.148106+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:44.9003868+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:44.2749536+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:44.4686099+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:44.2772074+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:48.148106+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:44.9003868+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:44.2749536+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:44.4686099+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:44.2772074+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f32-6638-8a02-ed304f4947f4",
            "interface": "",
            "mptcp": false,
            "name": "🇹🇼 [三网]TW 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇹🇼 台湾|Auto": {
            "alive": true,
            "all": [
                "🇹🇼 [Any]TW 01",
                "🇹🇼 [Any]TW 02",
                "🇹🇼 [Hy2]TW 01",
                "🇹🇼 [IPv6]TW 01",
                "🇹🇼 [IPv6]TW 02",
                "🇹🇼 [三网]TW 01",
                "🇹🇼 [三网]TW 02"
            ],
            "dialer-proxy": "",
            "expectedStatus": "*",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-24T15:52:34.2990037+08:00",
                            "delay": 267
                        }
                    ]
                }
            },
            "fixed": "",
            "hidden": false,
            "history": [
                {
                    "time": "2025-09-24T15:52:34.2990037+08:00",
                    "delay": 267
                }
            ],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "🇹🇼 台湾|Auto",
            "now": "🇹🇼 [Any]TW 01",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "https://www.apple.com/library/test/success.html",
            "tfo": false,
            "type": "Fallback",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "🇺🇸 [Any]US 01": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:44.3335293+08:00",
                            "delay": 226
                        },
                        {
                            "time": "2025-09-25T09:57:40.9499515+08:00",
                            "delay": 208
                        },
                        {
                            "time": "2025-09-25T10:02:39.4898815+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:39.6198796+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:40.2060999+08:00",
                            "delay": 175
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:44.3335293+08:00",
                    "delay": 226
                },
                {
                    "time": "2025-09-25T09:57:40.9499515+08:00",
                    "delay": 208
                },
                {
                    "time": "2025-09-25T10:02:39.4898815+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:39.6198796+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:40.2060999+08:00",
                    "delay": 175
                }
            ],
            "id": "1f099b54-1f32-6638-af6f-cb6983afde02",
            "interface": "",
            "mptcp": false,
            "name": "🇺🇸 [Any]US 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "AnyTLS",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇺🇸 [Any]US 02": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:44.272609+08:00",
                            "delay": 205
                        },
                        {
                            "time": "2025-09-25T09:57:41.0027813+08:00",
                            "delay": 222
                        },
                        {
                            "time": "2025-09-25T10:02:39.6769275+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:39.6306191+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:40.5532614+08:00",
                            "delay": 259
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:44.272609+08:00",
                    "delay": 205
                },
                {
                    "time": "2025-09-25T09:57:41.0027813+08:00",
                    "delay": 222
                },
                {
                    "time": "2025-09-25T10:02:39.6769275+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:39.6306191+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:40.5532614+08:00",
                    "delay": 259
                }
            ],
            "id": "1f099b54-1f32-6638-bc9b-8ccaf818f56f",
            "interface": "",
            "mptcp": false,
            "name": "🇺🇸 [Any]US 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "AnyTLS",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇺🇸 [Hy2]US 01": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:44.6995348+08:00",
                            "delay": 258
                        },
                        {
                            "time": "2025-09-25T09:57:40.9472227+08:00",
                            "delay": 243
                        },
                        {
                            "time": "2025-09-25T10:02:40.8699071+08:00",
                            "delay": 264
                        },
                        {
                            "time": "2025-09-25T10:07:40.9089677+08:00",
                            "delay": 255
                        },
                        {
                            "time": "2025-09-25T10:12:40.7778046+08:00",
                            "delay": 248
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:44.6995348+08:00",
                    "delay": 258
                },
                {
                    "time": "2025-09-25T09:57:40.9472227+08:00",
                    "delay": 243
                },
                {
                    "time": "2025-09-25T10:02:40.8699071+08:00",
                    "delay": 264
                },
                {
                    "time": "2025-09-25T10:07:40.9089677+08:00",
                    "delay": 255
                },
                {
                    "time": "2025-09-25T10:12:40.7778046+08:00",
                    "delay": 248
                }
            ],
            "id": "1f099b54-1f32-6638-8e0d-2547f9129847",
            "interface": "",
            "mptcp": false,
            "name": "🇺🇸 [Hy2]US 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Hysteria2",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "🇺🇸 [Hy2]US 02": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:44.4030619+08:00",
                            "delay": 176
                        },
                        {
                            "time": "2025-09-25T09:57:40.8522735+08:00",
                            "delay": 170
                        },
                        {
                            "time": "2025-09-25T10:02:40.389196+08:00",
                            "delay": 162
                        },
                        {
                            "time": "2025-09-25T10:07:40.4870093+08:00",
                            "delay": 174
                        },
                        {
                            "time": "2025-09-25T10:12:40.5960737+08:00",
                            "delay": 206
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:44.4030619+08:00",
                    "delay": 176
                },
                {
                    "time": "2025-09-25T09:57:40.8522735+08:00",
                    "delay": 170
                },
                {
                    "time": "2025-09-25T10:02:40.389196+08:00",
                    "delay": 162
                },
                {
                    "time": "2025-09-25T10:07:40.4870093+08:00",
                    "delay": 174
                },
                {
                    "time": "2025-09-25T10:12:40.5960737+08:00",
                    "delay": 206
                }
            ],
            "id": "1f099b54-1f32-6638-ab5b-769d1da2ee3a",
            "interface": "",
            "mptcp": false,
            "name": "🇺🇸 [Hy2]US 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Hysteria2",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "🇺🇸 [Hy2]US 03": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:44.6447094+08:00",
                            "delay": 189
                        },
                        {
                            "time": "2025-09-25T09:57:40.9170512+08:00",
                            "delay": 183
                        },
                        {
                            "time": "2025-09-25T10:02:40.6894707+08:00",
                            "delay": 191
                        },
                        {
                            "time": "2025-09-25T10:07:40.5784313+08:00",
                            "delay": 184
                        },
                        {
                            "time": "2025-09-25T10:12:40.7181177+08:00",
                            "delay": 192
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:44.6447094+08:00",
                    "delay": 189
                },
                {
                    "time": "2025-09-25T09:57:40.9170512+08:00",
                    "delay": 183
                },
                {
                    "time": "2025-09-25T10:02:40.6894707+08:00",
                    "delay": 191
                },
                {
                    "time": "2025-09-25T10:07:40.5784313+08:00",
                    "delay": 184
                },
                {
                    "time": "2025-09-25T10:12:40.7181177+08:00",
                    "delay": 192
                }
            ],
            "id": "1f099b54-1f32-6638-a924-0b7f127f3acb",
            "interface": "",
            "mptcp": false,
            "name": "🇺🇸 [Hy2]US 03",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Hysteria2",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "🇺🇸 [IPv6]US 01": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:43.6943114+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:40.5416484+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:40.1632509+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:39.8163569+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:39.8107308+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:43.6943114+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:40.5416484+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:40.1632509+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:39.8163569+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:39.8107308+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f32-6638-af4a-3671df62093d",
            "interface": "",
            "mptcp": false,
            "name": "🇺🇸 [IPv6]US 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇺🇸 [IPv6]US 02": {
            "alive": false,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": false,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:43.6948322+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T09:57:40.5421719+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:02:40.1632509+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:07:39.8163569+08:00",
                            "delay": 0
                        },
                        {
                            "time": "2025-09-25T10:12:39.8107308+08:00",
                            "delay": 0
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:43.6948322+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T09:57:40.5421719+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:02:40.1632509+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:07:39.8163569+08:00",
                    "delay": 0
                },
                {
                    "time": "2025-09-25T10:12:39.8107308+08:00",
                    "delay": 0
                }
            ],
            "id": "1f099b54-1f32-6638-9150-9964e7953786",
            "interface": "",
            "mptcp": false,
            "name": "🇺🇸 [IPv6]US 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇺🇸 [三网]US 01": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:47.7338994+08:00",
                            "delay": 273
                        },
                        {
                            "time": "2025-09-25T09:57:42.4162806+08:00",
                            "delay": 270
                        },
                        {
                            "time": "2025-09-25T10:02:41.4639716+08:00",
                            "delay": 276
                        },
                        {
                            "time": "2025-09-25T10:07:41.1830195+08:00",
                            "delay": 272
                        },
                        {
                            "time": "2025-09-25T10:12:41.3863558+08:00",
                            "delay": 357
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:47.7338994+08:00",
                    "delay": 273
                },
                {
                    "time": "2025-09-25T09:57:42.4162806+08:00",
                    "delay": 270
                },
                {
                    "time": "2025-09-25T10:02:41.4639716+08:00",
                    "delay": 276
                },
                {
                    "time": "2025-09-25T10:07:41.1830195+08:00",
                    "delay": 272
                },
                {
                    "time": "2025-09-25T10:12:41.3863558+08:00",
                    "delay": 357
                }
            ],
            "id": "1f099b54-1f32-6638-aa18-30fb37ad4e53",
            "interface": "",
            "mptcp": false,
            "name": "🇺🇸 [三网]US 01",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇺🇸 [移动]US 02": {
            "alive": true,
            "dialer-proxy": "",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-25T09:54:45.3289705+08:00",
                            "delay": 219
                        },
                        {
                            "time": "2025-09-25T09:57:41.8948383+08:00",
                            "delay": 213
                        },
                        {
                            "time": "2025-09-25T10:02:41.4469304+08:00",
                            "delay": 222
                        },
                        {
                            "time": "2025-09-25T10:07:41.1255637+08:00",
                            "delay": 260
                        },
                        {
                            "time": "2025-09-25T10:12:41.2688392+08:00",
                            "delay": 216
                        }
                    ]
                }
            },
            "history": [
                {
                    "time": "2025-09-25T09:54:45.3289705+08:00",
                    "delay": 219
                },
                {
                    "time": "2025-09-25T09:57:41.8948383+08:00",
                    "delay": 213
                },
                {
                    "time": "2025-09-25T10:02:41.4469304+08:00",
                    "delay": 222
                },
                {
                    "time": "2025-09-25T10:07:41.1255637+08:00",
                    "delay": 260
                },
                {
                    "time": "2025-09-25T10:12:41.2688392+08:00",
                    "delay": 216
                }
            ],
            "id": "1f099b54-1f32-6638-95f5-631f25aa99d0",
            "interface": "",
            "mptcp": false,
            "name": "🇺🇸 [移动]US 02",
            "routing-mark": 0,
            "smux": false,
            "tfo": false,
            "type": "Trojan",
            "udp": true,
            "uot": true,
            "xudp": false
        },
        "🇺🇸 美国|Auto": {
            "alive": true,
            "all": [
                "dmit-us",
                "dmit-us-relay",
                "silicloud-us",
                "silicloud-us-relay",
                "zgo-us",
                "zgo-us-relay",
                "🇺🇸 [Any]US 01",
                "🇺🇸 [Any]US 02",
                "🇺🇸 [Hy2]US 01",
                "🇺🇸 [Hy2]US 02",
                "🇺🇸 [Hy2]US 03",
                "🇺🇸 [IPv6]US 01",
                "🇺🇸 [IPv6]US 02",
                "🇺🇸 [三网]US 01",
                "🇺🇸 [移动]US 02"
            ],
            "dialer-proxy": "",
            "expectedStatus": "*",
            "extra": {
                "https://www.apple.com/library/test/success.html": {
                    "alive": true,
                    "history": [
                        {
                            "time": "2025-09-24T15:52:35.3546564+08:00",
                            "delay": 268
                        }
                    ]
                }
            },
            "fixed": "dmit-us-relay",
            "hidden": false,
            "history": [
                {
                    "time": "2025-09-24T15:52:35.3546564+08:00",
                    "delay": 268
                }
            ],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "🇺🇸 美国|Auto",
            "now": "dmit-us-relay",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "https://www.apple.com/library/test/success.html",
            "tfo": false,
            "type": "Fallback",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "🎯 本机直连": {
            "alive": true,
            "all": [
                "DIRECT"
            ],
            "dialer-proxy": "",
            "extra": {},
            "hidden": false,
            "history": [],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "🎯 本机直连",
            "now": "DIRECT",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "",
            "tfo": false,
            "type": "Selector",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "🏠 Home": {
            "alive": true,
            "all": [
                "Home|ss",
                "Home|vmess",
                "Home|vmess-tls"
            ],
            "dialer-proxy": "",
            "expectedStatus": "*",
            "extra": {},
            "fixed": "",
            "hidden": false,
            "history": [],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "🏠 Home",
            "now": "Home|ss",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "https://www.apple.com/library/test/success.html",
            "tfo": false,
            "type": "Fallback",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "🐟 漏网之鱼": {
            "alive": true,
            "all": [
                "🎯 本机直连",
                "🚀 节点选择",
                "🇯🇵 日本|Auto",
                "🇭🇰 香港|Auto",
                "🇹🇼 台湾|Auto",
                "🇸🇬 新加坡|Auto",
                "🇺🇸 美国|Auto",
                "🛠️ 手动选择"
            ],
            "dialer-proxy": "",
            "extra": {},
            "hidden": false,
            "history": [],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "🐟 漏网之鱼",
            "now": "🚀 节点选择",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "",
            "tfo": false,
            "type": "Selector",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "📈 网络测试": {
            "alive": true,
            "all": [
                "🎯 本机直连",
                "🚀 节点选择",
                "🇯🇵 日本|Auto",
                "🇭🇰 香港|Auto",
                "🇹🇼 台湾|Auto",
                "🇸🇬 新加坡|Auto",
                "🇺🇸 美国|Auto",
                "🛠️ 手动选择"
            ],
            "dialer-proxy": "",
            "extra": {},
            "hidden": false,
            "history": [],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "📈 网络测试",
            "now": "🎯 本机直连",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "",
            "tfo": false,
            "type": "Selector",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "📧 谷歌服务": {
            "alive": true,
            "all": [
                "🚀 节点选择",
                "🇯🇵 日本|Auto",
                "🇭🇰 香港|Auto",
                "🇹🇼 台湾|Auto",
                "🇸🇬 新加坡|Auto",
                "🇺🇸 美国|Auto",
                "🎯 本机直连",
                "🛠️ 手动选择"
            ],
            "dialer-proxy": "",
            "extra": {},
            "hidden": false,
            "history": [],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "📧 谷歌服务",
            "now": "🇺🇸 美国|Auto",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "",
            "tfo": false,
            "type": "Selector",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "📲 电报消息": {
            "alive": true,
            "all": [
                "🚀 节点选择",
                "🇯🇵 日本|Auto",
                "🇭🇰 香港|Auto",
                "🇹🇼 台湾|Auto",
                "🇸🇬 新加坡|Auto",
                "🇺🇸 美国|Auto",
                "🎯 本机直连",
                "🛠️ 手动选择"
            ],
            "dialer-proxy": "",
            "extra": {},
            "hidden": false,
            "history": [],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "📲 电报消息",
            "now": "🚀 节点选择",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "",
            "tfo": false,
            "type": "Selector",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "📹 海外视频": {
            "alive": true,
            "all": [
                "🚀 节点选择",
                "🇯🇵 日本|Auto",
                "🇭🇰 香港|Auto",
                "🇹🇼 台湾|Auto",
                "🇸🇬 新加坡|Auto",
                "🇺🇸 美国|Auto",
                "🎯 本机直连",
                "🛠️ 手动选择"
            ],
            "dialer-proxy": "",
            "extra": {},
            "hidden": false,
            "history": [],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "📹 海外视频",
            "now": "🚀 节点选择",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "",
            "tfo": false,
            "type": "Selector",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "📺 哔哩哔哩": {
            "alive": true,
            "all": [
                "🎯 本机直连",
                "🚀 节点选择",
                "🇯🇵 日本|Auto",
                "🇭🇰 香港|Auto",
                "🇹🇼 台湾|Auto",
                "🇸🇬 新加坡|Auto",
                "🇺🇸 美国|Auto",
                "🛠️ 手动选择"
            ],
            "dialer-proxy": "",
            "extra": {},
            "hidden": false,
            "history": [],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "📺 哔哩哔哩",
            "now": "🎯 本机直连",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "",
            "tfo": false,
            "type": "Selector",
            "udp": true,
            "uot": false,
            "xudp": false
        },
        "🚀 节点选择": {
            "alive": true,
            "all": [
                "♻️ Auto",
                "🇯🇵 日本|Auto",
                "🇭🇰 香港|Auto",
                "🇹🇼 台湾|Auto",
                "🇸🇬 新加坡|Auto",
                "🇺🇸 美国|Auto",
                "🎯 本机直连"
            ],
            "dialer-proxy": "",
            "extra": {},
            "hidden": false,
            "history": [],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "🚀 节点选择",
            "now": "🇭🇰 香港|Auto",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "",
            "tfo": false,
            "type": "Selector",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "🛠️ 手动选择": {
            "alive": true,
            "all": [
                "vps-jp",
                "vps-jp-relay",
                "wawo-hk",
                "wawo-hk-relay",
                "Home|ss",
                "Home|vmess",
                "Home|vmess-tls",
                "ali-hk",
                "ali-hk-relay",
                "claw-sg",
                "claw-sg-relay",
                "claw-sg2",
                "claw-sg2-relay",
                "dmit-us",
                "dmit-us-relay",
                "net-hk",
                "net-hk-relay",
                "silicloud-us",
                "silicloud-us-relay",
                "zgo-us",
                "zgo-us-relay",
                "🇭🇰 [Any]HK 01",
                "🇭🇰 [Any]HK 02",
                "🇭🇰 [Any]HK 03",
                "🇭🇰 [Any]HK 04",
                "🇭🇰 [Hy2]HK 01",
                "🇭🇰 [Hy2]HK 02",
                "🇭🇰 [Hy2]HK 03",
                "🇭🇰 [IPv6]HK 01",
                "🇭🇰 [IPv6]HK 02",
                "🇭🇰 [三网]HK 01",
                "🇭🇰 [三网]HK 03",
                "🇭🇰 [三网]HK 04",
                "🇭🇰 [移动]HK 02",
                "🇯🇵 [Any]JP 01",
                "🇯🇵 [Any]JP 02",
                "🇯🇵 [Any]JP 03",
                "🇯🇵 [Hy2]JP 01",
                "🇯🇵 [Hy2]JP 02",
                "🇯🇵 [IPv6]JP 01",
                "🇯🇵 [IPv6]JP 02",
                "🇯🇵 [三网]JP 01",
                "🇯🇵 [移动]JP 02",
                "🇸🇬 [Any]SG 01",
                "🇸🇬 [Any]SG 02",
                "🇸🇬 [IPv6]SG 01",
                "🇸🇬 [IPv6]SG 02",
                "🇸🇬 [三网]SG 01",
                "🇸🇬 [移动]SG 02",
                "🇹🇼 [Any]TW 01",
                "🇹🇼 [Any]TW 02",
                "🇹🇼 [Hy2]TW 01",
                "🇹🇼 [IPv6]TW 01",
                "🇹🇼 [IPv6]TW 02",
                "🇹🇼 [三网]TW 01",
                "🇹🇼 [三网]TW 02",
                "🇺🇸 [Any]US 01",
                "🇺🇸 [Any]US 02",
                "🇺🇸 [Hy2]US 01",
                "🇺🇸 [Hy2]US 02",
                "🇺🇸 [Hy2]US 03",
                "🇺🇸 [IPv6]US 01",
                "🇺🇸 [IPv6]US 02",
                "🇺🇸 [三网]US 01",
                "🇺🇸 [移动]US 02"
            ],
            "dialer-proxy": "",
            "expectedStatus": "*",
            "extra": {},
            "fixed": "dmit-us-relay",
            "hidden": false,
            "history": [],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "🛠️ 手动选择",
            "now": "dmit-us-relay",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "https://www.apple.com/library/test/success.html",
            "tfo": false,
            "type": "Fallback",
            "udp": false,
            "uot": false,
            "xudp": false
        },
        "🤖 人工智能": {
            "alive": true,
            "all": [
                "🚀 节点选择",
                "🇯🇵 日本|Auto",
                "🇭🇰 香港|Auto",
                "🇹🇼 台湾|Auto",
                "🇸🇬 新加坡|Auto",
                "🇺🇸 美国|Auto",
                "🎯 本机直连",
                "🛠️ 手动选择"
            ],
            "dialer-proxy": "",
            "extra": {},
            "hidden": false,
            "history": [],
            "icon": "",
            "interface": "",
            "mptcp": false,
            "name": "🤖 人工智能",
            "now": "🇺🇸 美国|Auto",
            "routing-mark": 0,
            "smux": false,
            "testUrl": "",
            "tfo": false,
            "type": "Selector",
            "udp": false,
            "uot": false,
            "xudp": false
        }
    }
}
```
