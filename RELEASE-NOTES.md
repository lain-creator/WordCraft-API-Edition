# WordCraft API Edition · 独立仓库首版

版本 `0.11.0-api.20261028.1`，基于上游 v0.11.0；从原 WordCraft API 版 `0.11.0-wordcraft.20261027.2` 独立发布，非上游官方发行版。

- WordCraft 使用独立仓库、源码包和 Mac / Win64 构建流程，不再与 GridCraft 混发。
- 保留自定义 API 设置：GPT / OpenAI、MiniMax、DeepSeek、Kimi、小米 MiMo、自定义兼容接口，支持 Chat Completions / Responses。
- 保留选区转英文、全文转英文、选区转中文，以及精确选区和表格取值、字体替代、图片裁剪和拉伸修复；本次不新增应用功能。
- 沿用应用标识和配置位置，不迁移或清除现有 API 设置。密钥不会进入安装包和源码；固定翻译网站调用已移除。

Mac Apple 芯片选 `macos-arm64.zip`；Windows 10/11 x64 选 `win64.zip`，完整解压运行，需要 [Visual C++ x64 运行库](https://aka.ms/vc14/vc_redist.x64.exe)。附项目源码 ZIP 与 SHA256。

新下载校验成功后，按用户要求删除旧 GridCraft 仓库里的 WordCraft Release 和附件，使旧下载链接失效；保留原源码标签和 Git 历史。仓库迁移不覆盖电脑上的安装版，不更改用户文件或 API 配置。

原有验证为模拟 API 与选区、字体、图片回归；没有真实付费 API 或 Windows 桌面实机验证。复杂排版、SVG、EXIF 旋转仍可能有限制。Mac 临时签名、未公证；Windows 未做发布者签名。
