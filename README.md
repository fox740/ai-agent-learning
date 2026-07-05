# 我建议你的学习路线（16周）

注意：

不是按照知识点。

而是按照**能力成长**。

---

# 第一阶段（2周）

## 目标

建立AI开发基础。

不是Agent。

### 学什么

Python（工程化部分）

只学：

- 项目结构
- logging
- config
- requirements
- typing
- dataclass

Linux

Git

Docker

FastAPI

只需要：

- GET
- POST
- UploadFile
- StreamingResponse

数据库：

SQLite即可。

不用一开始学Redis。

---

## 为什么？

因为：

以后所有Agent：

都是：

```text
上传文件

↓

调用模型

↓

返回结果
```

FastAPI一定会。

---

## 项目

不要做Agent。

做：

AI Chat

要求：

- 能聊天
- 能流式输出
- Docker启动
- GitHub

完成即可。

---

# 第二阶段（2周）

## 目标

真正理解LLM。

这里千万不要看几十节Transformer。

只需要：

理解：

```text
Tokenizer

Embedding

Attention

Prompt

Temperature

Top-p

Function Calling
```

能够回答：

为什么：

ChatGPT能聊天。

为什么：

Embedding能检索。

就够。

---

## 项目

把AI Chat升级：

支持：

上传PDF。

不用RAG。

只是上传。

解析。

总结。

---

# 第三阶段（3周）

开始真正学RAG。

这时候：

做你的第一个简历项目。

例如：

论文问答。

需要学习：

Chunk

Embedding

FAISS

Retriever

Prompt

Citation

做到：

```text
PDF

↓

Chunk

↓

Embedding

↓

FAISS

↓

LLM

↓

回答
```

做到这里。

已经可以投很多：

AI应用开发。

---

# 第四阶段（3周）

开始Agent。

重点：

不要学10个框架。

只学：

LangGraph。

理解：

State

Node

Edge

Memory

Workflow

然后：

Tool Calling。

例如：

天气。

计算器。

SQL。

Browser。

---

## 项目

论文分析Agent。

要求：

上传论文。

Agent：

总结。

提创新。

找不足。

输出Review。

这是第二个简历项目。

---

# 第五阶段（2周）

开始MCP。

为什么？

因为：

现在很多公司都在问。

学习：

Client

Server

Tool

自己写：

Weather MCP。

SQL MCP。

不用复杂。

---

# 第六阶段（4周）

开始：

真正改项目。

不是继续学。

例如：

论文Agent。

升级：

支持：

多论文。

多Agent。

历史记录。

权限。

引用。

部署。

Docker。

Github Action。

---

# 为什么我一直强调不要学太多？

因为：

现在很多人：

```text
LangChain

CrewAI

AutoGen

LlamaIndex

Semantic Kernel

PydanticAI

OpenAI SDK

Haystack

Flowise

......
```

全都会一点。

结果：

没有一个项目。

企业：

根本不关心。

---

# 我希望你的GitHub最后只有4个项目

而不是：

30个Demo。

例如：

## Project1

AI Chat

⭐⭐

练手。

---

## Project2（简历）

论文RAG。

⭐⭐⭐⭐⭐

企业喜欢。

---

## Project3（简历）

论文Agent。

⭐⭐⭐⭐⭐

企业喜欢。

---

## Project4（毕业前）

ECG AI Agent。

⭐⭐⭐⭐⭐⭐

别人没有。

---

# 关于500 AI Agent Projects

**我的建议是：**

不要现在打开那个仓库就开始做。

而是：

等第三阶段以后。

因为：

到时候：

你已经知道：

什么叫：

Prompt。

什么叫：

Embedding。

什么叫：

Tool。

这时候：

那个仓库会变成：

参考答案。

不是：

复制对象。

---

# 最后，我给你一个建议（这是结合你的背景给出的，不是通用建议）

**不要把目标定成"学Agent"。**

把目标定成：

> **2026年10月前，GitHub有2个高质量项目，简历能讲30分钟，每一行代码自己都能解释。**

对于实习来说，这比"学了50个框架"价值高得多。

---

## 如果是我来带你（也是我认为最适合你的方案）

我甚至不会让你自己到处找教程，而是会制定一条**唯一主线**：

**FastAPI → OpenAI/Qwen API → RAG → LangGraph → MCP → 企业级论文 Agent**

每一步都围绕**同一个项目**不断升级，而不是每学一个知识点就换一个 Demo。

这样有三个好处：

- **最快**：不会在无关技术上花时间。
- **最扎实**：每学一个知识点都马上用到，不容易忘。
- **最适合简历**：最后得到的是一个不断演进的企业级项目，而不是一堆互不相关的小 Demo。

**我认为这是目前最符合你目标（AI Agent 实习 + 两个高质量简历项目）的路线。**
