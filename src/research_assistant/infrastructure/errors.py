"""异常体系：统一的错误类型。

为什么需要：
- 现在代码里异常混乱：ValueError/KeyError/裸 Exception 混用
- API 层无法区分「配置错误」「模型调用失败」「工具执行失败」，难做友好提示

设计：
- AppError：所有自定义异常的基类（带用户可读的 message）
- 具体错误继承 AppError，API 层按类型返回不同 HTTP 状态码
"""


# 应用异常基类：所有自定义异常继承它
class AppError(Exception):
    """应用级错误基类。

    属性:
        message: 用户可读的错误描述（可安全展示给用户）
        code: 错误码（可选，用于前端/日志分类）
    """

    def __init__(self, message: str, code: str = "app_error"):
        # 调用父类初始化（Exception 接受消息）
        super().__init__(message)
        # 保存用户可读消息
        self.message = message
        # 保存错误码（默认 app_error）
        self.code = code


# 配置错误：.env 缺 key、配置非法等
class ConfigError(AppError):
    """配置错误：环境变量缺失或非法。"""

    def __init__(self, message: str):
        # 配置错误固定错误码 config_error
        super().__init__(message, code="config_error")


# 模型调用错误：API 超时、限流、网络问题
class ModelError(AppError):
    """模型调用错误：DeepSeek API 相关失败。"""

    def __init__(self, message: str):
        super().__init__(message, code="model_error")


# 工具执行错误：自定义工具/内置工具执行失败
class ToolError(AppError):
    """工具执行错误：工具调用过程中的失败。"""

    def __init__(self, message: str):
        super().__init__(message, code="tool_error")


# 审批错误：人机回环相关（如 thread_id 找不到中断状态）
class ApprovalError(AppError):
    """审批错误：人机回环流程异常。"""

    def __init__(self, message: str):
        super().__init__(message, code="approval_error")