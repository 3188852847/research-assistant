"""人机回环（Human-in-the-Loop）子系统。

对外只暴露两个函数：
- check_interrupts：检查结果是否有待审批操作
- resume：用用户决策恢复执行
"""

# 从 manager 模块导出两个函数（import 方只需 from core.human_in_the_loop import ...）
from research_assistant.core.human_in_the_loop.manager import check_interrupts, resume