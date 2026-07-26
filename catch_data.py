import json
from getpass import getpass
from pathlib import Path

import requests


TOKEN_URL = "https://maimai.lxns.net/api/v0/oauth/token"
PLAYER_URL = "https://maimai.lxns.net/api/v0/user/maimai/player"
SCORES_URL = "https://maimai.lxns.net/api/v0/user/maimai/player/scores"


def get_access_token(client_id, client_secret, authorization_code):
    response = requests.post(
        TOKEN_URL,
        json={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": authorization_code,
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        },
        timeout=30,
    )
    if not response.ok:
        print("\n获取 Access Token 失败：")
        print(response.text)
        response.raise_for_status()

    result = response.json()

    access_token = result.get("access_token")

    # 兼容旧版接口的 data 包装
    if access_token is None and isinstance(result.get("data"), dict):
        access_token = result["data"].get("access_token")

    if not access_token:
        raise RuntimeError(
            "服务器响应中没有 access_token：\n"
            + json.dumps(result, ensure_ascii=False, indent=2)
        )

    return access_token


def fetch_data(url, access_token):
    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        timeout=30,
    )

    if not response.ok:
        print(f"\n请求失败：{url}")
        print(response.text)
        response.raise_for_status()

    return response.json()


def save_json(filename, data):
    Path(filename).write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main():
    print("=== LXNS maimai 数据获取工具 ===\n")

    client_id = input("Client ID: ").strip()
    client_secret = getpass("Client Secret（输入时不会显示）: ").strip()
    authorization_code = input("浏览器显示的授权码: ").strip()

    print("\n输入长度检查：")
    print("Client ID:", len(client_id))
    print("Client Secret:", len(client_secret))
    print("授权码:", len(authorization_code))

    access_token = get_access_token(
        client_id,
        client_secret,
        authorization_code,
    )

    print("\n授权成功，正在获取玩家资料……")
    player = fetch_data(PLAYER_URL, access_token)

    print("正在获取全部成绩……")
    scores = fetch_data(SCORES_URL, access_token)

    save_json("player.json", player)
    save_json("scores.json", scores)

    score_data = scores.get("data", scores) if isinstance(scores, dict) else scores

    print("\n获取完成：")
    print("  player.json：玩家资料")
    print("  scores.json：全部谱面成绩")

    if isinstance(score_data, list):
        print(f"  共 {len(score_data)} 条谱面成绩")


if __name__ == "__main__":
    main()