"""CLI 对话入口：备用调试入口（Web 形态下保留，方便快速测试）。

启动方式：uv run python -m research_assistant.core.cli
"""

# 导入构建 agent 的函数
# 注意路径：agent.py 已迁移到 core/ 下，import 路径相应更新
from research_assistant.core.agent import build_agent
# 导入进度可视化（presenters 层）
from research_assistant.core.presenters import stream_with_progress

# 主对话循环函数（与原 main.py 逻辑一致）
def main() -> None:
    # 构建 agent（读取配置、组装模型+工具）
    # 如果 .env 没配好 key，这里会抛 ValueError 并打印中文引导（config.py 的功劳）
    agent = build_agent()

    # 打印欢迎语，说明退出方式
    print("research-assistant CLI 已启动。输入问题开始对话，输入 exit 或 quit 退出。")

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

        # 调用 agent 并实时显示思考过程（stream 流式 + 进度可视化）
        # 每次 event 翻译成一行进度打印，用户能看到 agent 在干什么
        last_content = ""
        for line in stream_with_progress(
                agent,
                {"messages": [{"role": "user", "content": user_input}]},
                {"configurable": {"thread_id": "cli"}},  # CLI 用固定会话 ID（简单起见）
        ):
            # 进度行直接打印（带缩进区分于正式回复）
            print(f"  {line}")

        # 进度流里没有返回最终回复，需要再取一次
        # 用 invoke 拿最终结果（stream 只是展示过程，结果仍要 invoke）
        # 注意：这里会再调一次模型？不——CLI 场景简化为：
        # 进度可视化后，重新 invoke 拿最终回复（简单可靠，代价是重复一次）
        # invoke 必须带和 stream 相同的 config（checkpointer 需要 thread_id）
        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config={"configurable": {"thread_id": "cli"}},
        )
        final_answer = result["messages"][-1].content
        print(f"agent > {final_answer}")


# Python 的入口约定：直接运行本文件时 __name__ 才是 "__main__"
if __name__ == "__main__":
    # 调用主函数，启动对话循环
    main()