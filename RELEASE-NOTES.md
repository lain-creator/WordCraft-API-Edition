# WordCraft API Edition · PCB 专业术语优先翻译

版本 `0.11.0-api.20261028.2`，基于上游 v0.11.0，非上游官方发行版。

- 三个翻译按钮支持本机导入的 PCB 专业词库，最长词组优先、英文边界匹配、多义词按上下文判断。
- API 设置新增词库状态、JSON 导入及刷新，不依赖原网站。安装包不含个人术语数据或密钥。
- 检查已知的压合/press-fit 误译和原文未提及的附件声明；仍需人工复核，不改变无自动格式修复重试策略。
- 保留精确选区、表格取值、已有双语去重、原文档独立副本及字体/图片修复。

- WordCraft 使用独立仓库、源码包和 Mac / Win64 构建流程，不再与 GridCraft 混发。
- 保留自定义 API 设置：GPT / OpenAI、MiniMax、DeepSeek、Kimi、小米 MiMo、自定义兼容接口，支持 Chat Completions / Responses。
- 保留选区转英文、全文转英文、选区转中文，以及精确选区和表格取值、字体替代、图片裁剪和拉伸修复。
- 沿用应用标识和配置位置，不迁移或清除现有 API 设置。密钥不会进入安装包和源码；固定翻译网站调用已移除。

Mac Apple 芯片选 `macos-arm64.zip`；Windows 10/11 x64 选 `win64.zip`，完整解压运行，需要 [Visual C++ x64 运行库](https://aka.ms/vc14/vc_redist.x64.exe)。附项目源码 ZIP 与 SHA256。

WordCraft 已独立发布，本次不删除其他历史 Release。更新沿用原有配置目录，不更改用户文件或已有 API 配置；专业词库保存在用户本机，不包含在公开安装包中。

原有验证为模拟 API 与选区、字体、图片回归；没有真实付费 API 或 Windows 桌面实机验证。复杂排版、SVG、EXIF 旋转仍可能有限制。Mac 临时签名、未公证；Windows 未做发布者签名。
