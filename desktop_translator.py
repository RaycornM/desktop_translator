# -*- coding: utf-8 -*-
"""
桌面翻译组件 - 支持 中/英/日/俄 互译
运行: python desktop_translator.py
依赖: 仅 Python 标准库 + 网络
"""

import json
import queue
import re
import threading
import tkinter as tk
from tkinter import ttk
from urllib.parse import quote
from urllib.request import urlopen, Request

LANGS = [
    ("auto", "自动检测"),
    ("zh-CN", "中文"),
    ("en", "英文"),
    ("ja", "日文"),
    ("ru", "俄文"),
]

MYMEMORY = "https://api.mymemory.translated.net/get?q={text}&langpair={src}|{tgt}"
GOOGLE = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={src}&tl={tgt}&dt=t&q={text}"


def detect_lang(text):
    if re.search(r"[\u3040-\u30ff\u4e00-\u9fff\uff66-\uff9f]", text) and re.search(r"[ぁ-んァ-ヶ]", text):
        return "ja"
    if re.search(r"[\u0400-\u04FF]", text):
        return "ru"
    if re.search(r"[一-龥]", text):
        return "zh-CN"
    if re.search(r"[A-Za-z]", text):
        return "en"
    return "en"


def _get(url, timeout=15):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", "ignore"))


def translate(text, src, tgt):
    if not text.strip():
        return ""
    if src == "auto":
        src = detect_lang(text)
    if src == tgt:
        return text
    try:
        data = _get(MYMEMORY.format(text=quote(text[:4500]), src=src, tgt=tgt))
        result = (data.get("responseData") or {}).get("translatedText", "")
        if result and data.get("responseStatus") == 200:
            return result.replace("&#39;", "'")
    except Exception:
        pass
    data = _get(GOOGLE.format(src=src, tgt=tgt, text=quote(text[:4500])))
    return "".join(seg[0] for seg in data[0] if seg and seg[0])


class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.q = queue.Queue()
        root.title("桌面翻译 · 中英日俄")
        root.geometry("520x460")
        root.minsize(440, 380)

        top = ttk.Frame(root, padding=8)
        top.pack(fill="x")
        ttk.Label(top, text="源语言").pack(side="left")
        self.src_var = tk.StringVar(value="auto")
        ttk.Combobox(top, textvariable=self.src_var, values=[f"{c}|{n}" for c, n in LANGS],
                     state="readonly", width=10).pack(side="left", padx=4)
        ttk.Label(top, text="→ 目标").pack(side="left", padx=(12, 0))
        self.tgt_var = tk.StringVar(value="zh-CN|中文")
        ttk.Combobox(top, textvariable=self.tgt_var, values=[f"{c}|{n}" for c, n in LANGS],
                     state="readonly", width=10).pack(side="left", padx=4)
        self.topmost = tk.BooleanVar(value=False)
        ttk.Checkbutton(top, text="置顶", variable=self.topmost,
                        command=self._toggle_topmost).pack(side="right")

        ttk.Label(root, text="输入文本").pack(anchor="w", padx=10)
        self.src_text = tk.Text(root, height=7, font=("Microsoft YaHei UI", 11))
        self.src_text.pack(fill="x", padx=10)
        self.src_text.bind("<Control-Return>", lambda e: self.do_translate())

        btns = ttk.Frame(root, padding=(10, 6))
        btns.pack(fill="x")
        ttk.Button(btns, text="翻 译 (Ctrl+Enter)", command=self.do_translate).pack(side="left")
        ttk.Button(btns, text="复制结果", command=self.copy_result).pack(side="left", padx=6)
        ttk.Button(btns, text="清空", command=self.clear_all).pack(side="left")

        ttk.Label(root, text="翻译结果").pack(anchor="w", padx=10)
        self.dst_text = tk.Text(root, height=8, font=("Microsoft YaHei UI", 11),
                                state="disabled", wrap="word")
        self.dst_text.pack(fill="both", expand=True, padx=10, pady=(2, 10))

        self.status = tk.StringVar(value="就绪 · 点翻译或按 Ctrl+Enter")
        ttk.Label(root, textvariable=self.status, anchor="w").pack(fill="x", padx=10, pady=(0, 6))

        self.root.after(100, self._drain_queue)

    def _toggle_topmost(self):
        self.root.attributes("-topmost", self.topmost.get())

    def _code(self, var):
        return var.get().split("|")[0]

    def _name(self, var):
        return var.get().split("|")[1] if "|" in var.get() else var.get()

    def do_translate(self):
        text = self.src_text.get("1.0", "end-1c").strip()
        if not text:
            self.status.set("输入点东西再翻吧")
            return
        src, tgt = self._code(self.src_var), self._code(self.tgt_var)
        self.status.set(f"翻译中… {self._name(self.src_var)} → {self._name(self.tgt_var)}")
        self.root.config(cursor="watch")
        threading.Thread(target=self._work, args=(text, src, tgt), daemon=True).start()

    def _work(self, text, src, tgt):
        try:
            result = translate(text, src, tgt)
            self.q.put(("ok", result))
        except Exception as exc:
            self.q.put(("err", str(exc)))

    def _drain_queue(self):
        try:
            while True:
                kind, payload = self.q.get_nowait()
                self.root.config(cursor="")
                if kind == "ok":
                    self.dst_text.config(state="normal")
                    self.dst_text.delete("1.0", "end")
                    self.dst_text.insert("1.0", payload)
                    self.dst_text.config(state="disabled")
                    self.status.set("完成")
                else:
                    self.status.set(f"翻译失败: {payload[:80]}")
        except queue.Empty:
            pass
        self.root.after(100, self._drain_queue)

    def copy_result(self):
        text = self.dst_text.get("1.0", "end-1c").strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.status.set("已复制到剪贴板")

    def clear_all(self):
        self.src_text.delete("1.0", "end")
        self.dst_text.config(state="normal")
        self.dst_text.delete("1.0", "end")
        self.dst_text.config(state="disabled")
        self.status.set("已清空")


if __name__ == "__main__":
    root = tk.Tk()
    TranslatorApp(root)
    root.mainloop()
