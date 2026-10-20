---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: e09c99c604f0d83311533b7ae3d87258_024bfcdfcbd711f1b307525400393706
    ReservedCode1: FsUddDZdL+8o7rQcoh/D0C3wCzOYZ/i14Jx5C2WxpDwl9YGB7uwGH4dSKFUnA0GPVNQd6Z/NMpzxx45sko+1WREvEeW3lUfq+nleUHy2tD7AxlrUBjo9shX41hCJsImuT1+XStvlRQg9S3flcPt79UdMbGCYJTw9GnOwCEsvjg50ew0jm/1T29Ep6e8=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: e09c99c604f0d83311533b7ae3d87258_024bfcdfcbd711f1b307525400393706
    ReservedCode2: FsUddDZdL+8o7rQcoh/D0C3wCzOYZ/i14Jx5C2WxpDwl9YGB7uwGH4dSKFUnA0GPVNQd6Z/NMpzxx45sko+1WREvEeW3lUfq+nleUHy2tD7AxlrUBjo9shX41hCJsImuT1+XStvlRQg9S3flcPt79UdMbGCYJTw9GnOwCEsvjg50ew0jm/1T29Ep6e8=
---

# 桌面翻译组件

轻量级桌面翻译工具，支持 **中文 / 英文 / 日文 / 俄文** 互译，无需安装任何依赖。

## 功能特性

- 四语互译：中 ↔ 英 ↔ 日 ↔ 俄
- 自动语言检测（源语言选"自动检测"时）
- 翻译结果一键复制
- 窗口置顶模式（勾选"置顶"）
- `Ctrl + Enter` 快捷键翻译
- 免费翻译接口（MyMemory 为主、Google 兜底），无需 API Key

## 运行环境

| 项目 | 要求 |
|------|------|
| Python | 3.6+（仅标准库） |
| 系统 | Windows / macOS / Linux |
| 网络 | 需要联网访问翻译接口 |

## 快速开始

```bash
python desktop_translator.py
```

## 使用方式

1. 在输入框粘贴或输入文本
2. 选择源语言和目标语言
3. 点击「翻译」按钮或按 `Ctrl + Enter`
4. 点击「复制结果」将译文复制到剪贴板

## 技术细节

- GUI 框架：Tkinter（Python 内置）
- 翻译接口：MyMemory API（主）+ Google Translate API（兜底）
- 自动检测：正则匹配日文假名、俄文字母、中文字符、英文字母
- 单文件实现，零外部依赖

## 许可证

MIT License
*（内容由AI生成，仅供参考）*
