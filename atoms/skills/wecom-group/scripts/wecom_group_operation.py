import requests
import json
import sys
import argparse
import os


class WeComApp:
    def __init__(self, corpid, secret, timeout=20):
        self.corpid = corpid
        self.secret = secret
        self.timeout = timeout
        self.access_token = self._get_access_token()

    def _request_json(self, method, url, payload=None):
        try:
            if method.lower() == "get":
                resp = requests.get(url, timeout=self.timeout)
            else:
                resp = requests.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise RuntimeError(f"HTTP 请求失败: {e}") from e
        except ValueError as e:
            raise RuntimeError(f"接口返回不是合法 JSON: {e}") from e

    def _get_access_token(self):
        """获取企业微信访问令牌"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corpid}&corpsecret={self.secret}"
        data = self._request_json("get", url)
        if data.get("errcode") == 0:
            return data.get("access_token")
        raise RuntimeError(f"获取 Token 失败: {data}")
    def create_group(self, name, owner, userlist, chatid=None):
        """创建群聊会话"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/appchat/create?access_token={self.access_token}"
        payload = {
            "name": name,
            "owner": owner,
            "userlist": userlist,
        }
        if chatid:
            payload["chatid"] = chatid

        res_data = self._request_json("post", url, payload)
        return {
            "ok": res_data.get("errcode") == 0,
            "action": "create",
            "chatid": res_data.get("chatid"),
            "response": res_data,
        }
    def send_message(self, chatid, content):
        """向群聊发送文本消息"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token={self.access_token}"
        payload = {
            "chatid": chatid,
            "msgtype": "text",
            "text": {
                "content": content,
            },
        }
        res_data = self._request_json("post", url, payload)
        return {
            "ok": res_data.get("errcode") == 0,
            "action": "send",
            "chatid": chatid,
            "response": res_data,
        }


def output_result(result, json_output=False):
    if json_output:
        print(json.dumps(result, ensure_ascii=False))
        return

    if result.get("ok"):
        action = result.get("action")
        if action == "create":
            print(f"✅ 群聊创建成功! ChatID: {result.get('chatid')}")
        elif action == "send":
            print("✅ 消息发送成功!")
        elif action == "create_and_send":
            print(f"✅ 群聊创建成功并已发送首条消息! ChatID: {result.get('chatid')}")
    else:
        print(f"❌ 操作失败: {result.get('response')}")


def output_error(message, json_output=False, response=None):
    result = {
        "ok": False,
        "error": message,
    }
    if response is not None:
        result["response"] = response

    if json_output:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"❌ {message}")
        if response is not None:
            print(response)


def main():
    parser = argparse.ArgumentParser(description="企业微信自建应用创建群聊及发信工具")

    parser.add_argument("--id", default=os.getenv("WECOM_CORPID"), help="企业ID (CorpID)，默认读取 WECOM_CORPID")
    parser.add_argument("--secret", default=os.getenv("WECOM_GROUP_HELPER_SECRET"), help="自建应用 Secret，默认读取 WECOM_GROUP_HELPER_SECRET")
    parser.add_argument("--json-output", action="store_true", help="以 JSON 形式输出结果，适合自动化/agent 调用")
    parser.add_argument("--timeout", type=int, default=20, help="HTTP 请求超时时间（秒）")

    subparsers = parser.add_subparsers(dest="command", help="操作命令")

    create_parser = subparsers.add_parser("create", help="创建新群聊")
    create_parser.add_argument("--name", required=True, help="群名称")
    create_parser.add_argument("--owner", required=True, help="群主 UserID")
    create_parser.add_argument("--users", required=True, help="成员 UserID，多个用逗号隔开")
    create_parser.add_argument("--chatid", help="自定义群 ID（可选）")
    create_parser.add_argument("--msg", help="创建后发送的首条消息（可选）")

    send_parser = subparsers.add_parser("send", help="向现有群发消息")
    send_parser.add_argument("--chatid", required=True, help="目标群聊的 ChatID")
    send_parser.add_argument("--msg", required=True, help="消息内容")
    args = parser.parse_args()

    if not args.id or not args.secret:
        output_error("缺少企业微信凭据，请通过 --id/--secret 或环境变量 WECOM_CORPID/WECOM_GROUP_HELPER_SECRET 提供", args.json_output)
        sys.exit(1)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        app = WeComApp(args.id, args.secret, timeout=args.timeout)

        if args.command == "create":
            user_list = [user.strip() for user in args.users.split(",") if user.strip()]
            if not user_list:
                output_error("--users 不能为空", args.json_output)
                sys.exit(1)

            create_result = app.create_group(args.name, args.owner, user_list, args.chatid)
            if not create_result.get("ok"):
                output_result(create_result, args.json_output)
                sys.exit(1)

            if args.msg:
                send_result = app.send_message(create_result.get("chatid"), args.msg)
                combined_result = {
                    "ok": send_result.get("ok"),
                    "action": "create_and_send",
                    "chatid": create_result.get("chatid"),
                    "create": create_result,
                    "send": send_result,
                    "response": {
                        "create": create_result.get("response"),
                        "send": send_result.get("response"),
                    },
                }
                output_result(combined_result, args.json_output)
                sys.exit(0 if combined_result.get("ok") else 1)

            output_result(create_result, args.json_output)
            sys.exit(0)

        if args.command == "send":
            send_result = app.send_message(args.chatid, args.msg)
            output_result(send_result, args.json_output)
            sys.exit(0 if send_result.get("ok") else 1)

    except Exception as e:
        output_error(str(e), args.json_output)
        sys.exit(1)


if __name__ == "__main__":
    main()