# WordCraft API Edition

WordCraft 的独立第三方 API 定制版，基于上游 [storytold/wordcraft v0.11.0](https://github.com/storytold/wordcraft/tree/v0.11.0)，不是上游官方发行版。本仓库只发布 WordCraft，不包含 GridCraft 程序。

## 下载与安装

在本仓库的 [Releases](https://github.com/lain-creator/WordCraft-API-Edition/releases) 下载：

- Mac Apple 芯片：`WordCraft-…-macos-arm64.zip`，解压得到 `WordCraft.app`。
- Windows 10/11 x64：`WordCraft-…-win64.zip`，完整解压后运行 `WordCraft.exe`；需要 [Visual C++ x64 运行库](https://aka.ms/vc14/vc_redist.x64.exe)。

Mac 使用临时签名，未公证；Windows 未做发布者签名。Intel Mac 不适用 arm64 安装包。校验下载文件请使用同一 Release 的 `SHA256SUMS.txt`。

## API 翻译

“开始”功能区点击“API 设置”，自行填写服务商地址、模型 ID、API Key。支持 GPT / OpenAI、MiniMax、DeepSeek、Kimi、小米 MiMo 及自定义 OpenAI 兼容接口（Chat Completions / Responses）；不保证每家厂商所有专有协议都兼容。

三个翻译按钮：选区转英文、全文转英文、选区转中文。打开文件和框选不会发送内容；点击翻译才发送范围内候选文字，不发送图片或完整文档文件，生成独立 DOCX 副本。保留现有完整双语，不重复追加；模型输出仍需核对。固定网站调用已移除。

API Key 默认仅本次运行使用，可选保存在 Mac 钥匙串 / Windows 凭据管理器；不写入源码、文档或普通配置。连接测试可能产生少量费用，但不发送文档。默认 HTTPS，不跟随重定向；远程 HTTP 需明确允许。详见 [API 使用说明](wordcraft/docs/local-api-assistant.md)。

`0.11.0-api.20261028.2` 新增本机 PCB 术语库：按最长词组匹配、英文单词边界和语境优先使用专业表达，隔离已知错误词对，校验压合/press-fit 及无来源附件声明。API 设置可查看数量、刷新或导入 JSON。公开包不含个人词库；本机同步导入不会更改原始词库。

保留中文界面、UTF-8 正反选区及表格取值、中文字体替代、DOCX 正负裁剪及图片边缘拉伸修复。不捆绑微软字体。复杂排版、SVG 和 EXIF 旋转仍有限制；不是与 Microsoft Word 完全一致的替代品。现有回归使用本机模拟 API，没有真实付费 API 或 Windows 桌面实机验证。

## 独立发布与溯源

独立仓库首版编号 `0.11.0-api.20261028.1`，从原合仓库 WordCraft API 版 `0.11.0-wordcraft.20261027.2` 拆分，只调整仓库、说明和构建发布流程，不新增应用功能，也不改变应用标识或用户配置位置。电脑上的现有安装及设置不会因创建仓库而改变。

原始定制源码来自 [Gridcraft-API-access-version](https://github.com/lain-creator/Gridcraft-API-access-version) 提交 `d89187e1eb60b16eb4536892a6e4503ef09d2d2f` 的 `wordcraft/`、`craft-i18n/` 及相关许可文件；拆分时合仓库 HEAD 为 `b08152bd50fb682d9542d9fb036b049445f9d3ec`，WordCraft 目录未再变化。保留原作者、贡献者、NOTICE、ATTRIBUTION 和第三方许可，不将原作品归为本次定制原创。

新仓库的 Mac / Win64 下载验证成功后，将按用户要求删除旧 GridCraft 仓库中的 WordCraft Release 和安装包，旧下载链接不再可用；原 Git 标签及源代码历史保留用于溯源。后续 WordCraft 更新使用本独立仓库，不再与 GridCraft 混发。

## 从源码构建

安装 Rust 1.95.0 和平台原生构建工具：

```sh
export CRAFT_I18N_DIR="$PWD/craft-i18n"
export CRAFT_I18N_REQUIRED=1
cd wordcraft
cargo build --locked --release -p wordcraft
cargo xtask ci
```

`wordcraft/` 为完整应用源码；`craft-i18n/` 为共享翻译数据快照（其中可包含其他 Craft 应用的词条，不包含其应用源码）。所有 Cargo path 依赖位于 WordCraft 自身目录。公开 craft-libs 依赖锁定在 `17744430be327d0257496a6a31c8d38fe20a6756`，Cargo 自动获取；无需 GridCraft 仓库。

打包从仓库根目录执行：

```sh
python3 scripts/package.py --platform macos-arm64 --binary wordcraft/target/release/wordcraft --version 0.11.0-api.20261028.1 --output dist
python3 scripts/package.py --platform win64 --binary wordcraft/target/x86_64-pc-windows-msvc/release/wordcraft.exe --version 0.11.0-api.20261028.1 --output dist
```

GitHub Actions 的 `release.yml` 在 `v*-api.*` 标签推送后构建 Mac arm64 / Win64；两平台成功后发布 WordCraft 安装包、仅本项目源码和 SHA256。Mac 使用 macOS 15 Intel runner 的 Xcode SDK 交叉编译 arm64，避免 macOS 14 arm64 的排队/退役问题。手动运行默认只构建；填写已有 `release_tag` 可重新构建并发布该标签，不改写标签、不会删除或覆盖旧发布。

## 许可

WordCraft 及定制修改遵循 MIT / Apache-2.0（任选），完整许可、NOTICE 和素材归属见 `wordcraft/`。共享翻译及第三方依赖遵循各自目录的许可。品牌素材另有原项目条款，不因本次拆分改变。
