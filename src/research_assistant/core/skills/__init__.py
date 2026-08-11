"""技能包：按类别组织的技能源目录。

技能 = SKILL.md 文件（frontmatter: name/description + 正文工作流），
agent 按需加载（渐进式披露，省 token）。

结构：
- skills/          技能源根目录（agent 的 skills 参数指向这里）
  - research/      研究类技能（文献综述、论文总结…）
  - writing/       写作类技能（报告、备忘…）
  - coding/        代码类技能（调试、重构…）

新增技能：在对应类别目录下新建子目录 + SKILL.md。
"""

# 导入 pathlib 的 Path：定位技能目录的绝对路径
from pathlib import Path

# 技能源根目录的绝对路径（不依赖启动目录，用 __file__ 推导）
# 结构：core/skills/__init__.py → parent=core/skills → /skills = 技能源根
SKILLS_DIR = str(Path(__file__).parent / "skills")

# 技能包公共出口
__all__ = ["SKILLS_DIR"]