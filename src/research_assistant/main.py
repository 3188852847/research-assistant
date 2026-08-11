"""命令行对话入口：运行本文件即可与主 agent 对话。

启动方式：uv run python -m research_assistant.main
"""

# 导入构建 agent 的函数（agent.py 里定义的）
from research_assistant.agent import build_agent


# 主对话循环函数
def main() -> None:
    # 构建 agent（读取配置、组装模型+工具）
    # 如果 .env 没配好 key，这里会抛 ValueError 并打印中文引导（config.py 的功劳）
    agent = build_agent()

    # 打印欢迎语，说明退出方式
    print("research-assistant 已启动。输入问题开始对话，输入 exit 或 quit 退出。")

    # 无限循环：一直等待用户输入，直到用户退出
    while True:
        # input() 等待用户在终端输入一行文字并回车
        # 提示符 "你 > " 告诉用户该输入了
        user_input = input("你 > ")

        # 检查是否是退出命令
        # strip() 去掉首尾空白字符，这样 "exit " 也能正确识别
        if user_input.strip().lower() in ("exit", "quit"):
            # 用户要退出，打印告别语
            print("再见！")
            # break 跳出 while 循环，程序结束
            break

        # 跳过空输入（直接按回车不提问，避免白调一次模型）
        if not user_input.strip():
            # continue 回到 while 开头，重新等待输入
            continue

        # 调用 agent，把用户输入作为一条 user 消息传进去
        # invoke 返回一个结果对象，里面包含多轮消息
        result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})

        # 取结果里的最后一条消息，就是 agent 的最终回复
        # result["messages"] 是一个消息列表，[-1] 表示最后一个元素
        # .content 是消息的文本内容
        final_answer = result["messages"][-1].content

        # 打印 agent 的回复，前面加个 "agent > " 前缀区分是谁在说话
        print(f"agent > {final_answer}")


# Python 的入口约定：
# 只有直接运行本文件时（python -m research_assistant.main），__name__ 才是 "__main__"
# 被其他模块 import 时 __name__ 是模块名，不会执行下面的代码
# 这样既可以直接跑，也可以被测试程序安全导入
if __name__ == "__main__":
    # 调用主函数，启动对话循环
    main()