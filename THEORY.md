# Orthogonal Agent Polity (OAP)

> 正交代理政体：用最小正交维度描述 Main Agent 如何治理 Subagent 的认识论自由，并允许这种治理关系随运行环境动态切换。

## 0. 理论定位

OAP 是一个多 Agent 治理关系的语义框架，而不是政治哲学模型，也不是 Agent 人格分类。

OAP v1 假定一个拥有完整治理权的 **Main Agent / Sovereign**。Subagent 不与 Main 共享主权；它获得多少上下文访问权、事实调查权，由 Main 所采用的政体决定。

因此 OAP 描述的不是“两个 Agent 是否平等”，而是：

- Main 向 Subagent 开放多少认知上下文；
- Main 向 Subagent 授予多少独立事实调查权。

政体属于 **Main → Subagent 的治理边**，而不是 Subagent 的固定人格。

---

## 1. 核心命题

设 Main Agent 为 \(M\)，Subagent 为 \(S\)。

OAP v1 用两个最小正交轴描述 Main 对 S 的治理方式：

1. **Context Openness / 上下文开放性（C）**
   - Main 是否允许 S 读取 Main 的最新认知上下文，并据此主动补充、质疑、纠正。

2. **Investigative Autonomy / 调查自主性（I）**
   - Main 是否允许 S 在没有得到明确调查指令时，主动搜索、读取、观察、比较和调查外部事实。

其中：

```text
C ∈ {0,1}
I ∈ {0,1}
```

于是：

```text
P_M(S) = (C, I)
```

形成四种最小政体：

| C | I | 政体 | Subagent 角色 |
|---|---|---|---|
| 0 | 0 | 权威排外 | 被动工具 |
| 1 | 0 | 权威亲外 | 知情参谋 |
| 0 | 1 | 平等排外 | 独立调查者 |
| 1 | 1 | 平等亲外 | 开放事实伙伴 |

这里的“权威 / 平等 / 亲外 / 排外”都是操作性术语，不表示现实政治立场。

---

## 2. 主权假设：Main 是完整权力持有者

OAP v1 的基础不是对称 Agent 网络，而是一个明确的治理结构：

```text
        Main / Sovereign
        完整治理权
             │
      选择对子代理的政体
             │
        P_M(S) = (C,I)
             ↓
          Subagent
```

“平等”不等于主权平等。

在 OAP 中：

```text
平等 = Main 授予 Subagent 主动调查事实的自由
```

“亲外”也不等于双方互相开放，而是：

```text
亲外 = Main 向 Subagent 开放 Main 的最新认知上下文
```

无论处于 00、10、01、11 中的哪一种政体，Main 都保留最终治理权，包括但不限于：

- 任务分配；
- 资源预算；
- 工具授权；
- 执行授权；
- veto / termination；
- 政体切换。

因此 OAP 改变的是 **Subagent 的认识论自由度**，不是 Main 的主权位置。

---

## 3. 两条正交轴

### 3.1 轴 A：亲外 ↔ 排外

**Context Openness** 描述 Main 是否向 Subagent 开放自己的最新认知状态。

排外（C=0）：

- S 不知道 Main 当前相信什么；
- S 只接收明确交付的信息；
- 可以降低不同 Agent 之间的叙事相关性。

亲外（C=1）：

- S 可以读取 Main 最近的判断、假设和疑点；
- S 可以针对 Main 当前认知进行补充、限定、反证和纠错。

示例：

```text
Main 当前判断：
“这个错误很可能来自 CSS。”

C=1：Vision Agent 可以直接检查并反馈：
“当前现场证据并不支持 CSS 假设。”

C=0：Vision Agent 不知道 Main 已形成该判断。
```

### 3.2 轴 B：权威 ↔ 平等

**Investigative Autonomy** 描述 Main 是否授予 Subagent 自主事实调查权。

权威（I=0）：

- 调查议程由 Main 决定；
- S 不主动扩大调查范围；
- S 只执行被明确要求的调查。

平等（I=1）：

- S 可以自行发现问题；
- S 可以主动搜索、读文件、看日志、浏览代码、观察现场、寻找反例；
- S 可以把足以改变 Main 判断的新事实主动推回系统。

因此：

```text
Investigative Autonomy ≠ Sovereign Equality
```

---

## 4. 四种基本政体

### 4.1 00 · 权威排外：被动工具

```text
Main
  ↓ 明确任务
Subagent
  ↓
返回结果
```

Subagent：

- 不读取 Main 最新上下文；
- 不主动扩大调查；
- 不主动寻找 Main 判断的漏洞。

优点：

- 延迟最低；
- 资源成本最低；
- 可预测性最高。

典型：简单执行器、受控工具代理。

### 4.2 10 · 权威亲外：知情参谋

S 知道 Main 正在想什么，但无权自行扩大调查范围。

它可以说：

> “你当前判断与我已有的信息不一致。”

但默认不会继续：

> “我自己去把整个仓库、日志和运行现场重新查一遍。”

适合：

- 预算受限；
- 希望减少 Main 的自我强化；
- 又不希望产生额外调查调用。

### 4.3 01 · 平等排外：独立调查者

S 不读取 Main 当前推理，但拥有独立调查权。

```text
              外部事实
             ↗      ↖
          Main      S
```

它的重要价值是 **主动制造认知去相关性**。

例如：

```text
Main：API Cache
S：Frontend State
```

当两条独立路径发生冲突，冲突本身就是高价值信息。

因此 01 不是 11 的残缺版本，而是 Blind Review、独立 Code Review、Security Audit、独立事实核查等场景的核心政体。

### 4.4 11 · 平等亲外：开放事实伙伴

```text
Main 最新上下文
      ↓
Subagent 理解
      ↓
质疑 / 补充
      ↓
主动调查外部事实
      ↓
补证 / 反证 / 修正
      ↓
主动反馈 Main
      ↓
Main 更新判断
      ↓
新的上下文再次开放
```

这形成持续认知嵌合，但不要求 Subagent 服从 Main 的结论，也不要求 Subagent 永远反对 Main。

---

## 5. OAP 的认识论原则

> **Agent 可以成为彼此的信息来源，但不能成为彼此的事实来源。**

英文：

> **Agents share cognition, but reality remains outside them.**

Main 与 Subagent 都可能错。

因此 OAP 中的 adversarial 不是“必须唱反调”，而是：

> **系统必须始终保留由外部事实证伪当前判断的能力。**

合法反馈包括：

- 支持；
- 补充；
- 限定条件；
- 发现遗漏；
- 提出反例；
- 替代解释；
- 证据不足；
- 承认对方正确；
- 承认自己错误。

---

## 6. 调查权与行动权严格分离

OAP v1 只定义认识论治理：

```text
Context Openness
Investigative Autonomy
```

它不自动授予改变世界的权限。

例如 Vision Agent 可以：

```text
搜索      ✅
阅读      ✅
观察屏幕  ✅
分析视频  ✅
查日志    ✅
```

但默认：

```text
点击按钮  ❌
修改文件  ❌
提交表单  ❌
删除内容  ❌
```

因此：

```text
调查自主权 ≠ 行动自主权
```

执行权限应由独立的 Capability / Permission System 管理，避免把“知道”“调查”“改变世界”重新压缩成一个含混的自主性变量。

---

## 7. 政体属于治理边，不属于 Agent 人格

不要定义：

```text
“Vision Agent 是平等亲外型 Agent。”
```

而应定义：

```text
Main --[11]--> Vision
Main --[01]--> Security
Main --[00]--> Git
```

同一个 Subagent 在不同治理者或不同运行阶段下可以接受不同政体。

OAP v1 可以表示为一个有根治理图：

```text
G = (V, E, M)
```

其中：

- `V` = Agents；
- `M` = Main / Sovereign；
- `E` = Main 对各 Subagent 的治理边。

每条边：

```text
e(M → S_i) = (C, I)
```

---

## 8. 动态政体

OAP 不假设某一种政体永远最优。

政体是一种 **runtime state**。

### 8.1 Garden / 田园

典型条件：

- 时间较充足；
- 资源可接受；
- 错误可恢复；
- 可以反复验证；
- 环境敌意较低。

这种环境中，11 往往具有较高认识论收益：

```text
理解 → 质疑 → 调查 → 反馈 → 修正
```

### 8.2 Abyss / 深渊

典型条件：

- 时间极短；
- 资源极少；
- 操作不可逆；
- 失败成本巨大；
- 开放讨论本身可能增加风险。

此时 Main 可以收缩治理：

```text
11 → 10 → 00
```

甚至进入 Main 立即行动、其他 Agent 只保留紧急 veto 的模式。

因此：

> 权威排外不一定是认识论最优，但可能是生存约束下的局部最优。

---

## 9. 可逆认知拓扑

成熟系统的目标不是永久开放，也不是永久集中，而是拥有 **可逆的认知拓扑收缩与展开能力**。

收缩：

```text
11 平等亲外
 ↓ 资源下降
10 权威亲外
 ↓ 危机升级
00 权威排外
```

恢复：

```text
00
 ↓ 恢复调查权 / 上下文开放
10 或 01
 ↓
11
```

抽象为：

```text
P_t(M,S) → P_(t+1)(M,S)
```

或：

```text
P_(t+1) = F(P_t, Environment, Risk, Budget, Uncertainty)
```

其中 `F` 属于治理策略，而不是 OAP 两条轴本身。

---

## 10. 谁切换政体

OAP v1 中，政体切换权属于 Main。

Main 可以依据：

- 时间压力；
- 资源预算；
- 失败成本；
- 操作不可逆性；
- 环境敌意；
- 信息不确定性；

动态改变：

- 是否注入 Main 最新上下文；
- 是否允许自主调查；
- 搜索预算；
- Agent 调度；
- 工具权限；
- system prompt / harness 行为。

换政体不是换模型，而是换治理关系。

---

## 11. Harness 最小实现

OAP v1 的最小运行时只需要两个变量：

```json
{
  "context_openness": true,
  "investigative_autonomy": true
}
```

对应：

```python
if context_openness:
    inject_recent_main_context()

if investigative_autonomy:
    enable_autonomous_investigation()
```

这使 OAP 具有直接的：

```text
语义轴 ↔ runtime switch
```

映射。

---

## 12. 多模态 Agent：第一典型实例

OAP 最初适合的典型结构是：

```text
Main Agent
    ↕
Multimodal Evidence Agent
```

多模态 Evidence Agent 默认应处于计划 / 调查模式，而不是行动模式。

它可以：

- 看图片；
- 看视频；
- 看屏幕；
- 读文件；
- 搜索；
- 调查；
- 比较；
- 发现异常；
- 主动报告。

其目标不是“尽可能发挥视觉能力”，而是：

> **尽可能扶正整个系统对外部事实的认识。**

如果真正证据来自日志、代码或文档，它也应该前往这些来源。

模态只是能力；事实扶正才是目标。

---

## 13. 推广到任意 Subagent

OAP 不与视觉绑定。

候选实例：

- Coding Agent；
- Research Agent；
- Security Agent；
- Testing Agent；
- Memory Agent；
- Planning Agent；
- Browser Agent；
- Financial Agent；
- Robotics Agent。

例如：

```text
Security Agent → 01 平等排外
Research Agent → 11 平等亲外
Git Agent      → 00 权威排外
```

不同政体表达的是 Main 对其认识论自由的不同治理策略。

---

## 14. 与一般正交分解方法的关系

OAP v1 的两条轴不是普遍世界本体，而是针对 **Main–Subagent 治理关系** 找到的一组最小正交分解。

更一般的方法是：

```text
复杂关系
  ↓
选择少量高分辨力、尽可能正交的轴
  ↓
形成最小可穷举状态空间
  ↓
分别最低展开
  ↓
按需递归，而不是无节制增加全局维度
```

OAP 是该方法在多 Agent 编排领域的一次具体实例化。

因此理论不主张：

> “所有 Agent 关系永远只有 Context Openness 和 Investigative Autonomy 两个维度。”

而主张：

> “OAP v1 先用这两个轴建立一个足够小、四个象限均有独立语义、可直接实现并可测试的最小政体空间。”

---

## 15. 可检验假设

OAP 初版应优先验证，而不是继续扩维。

### H1 · Context Openness

与 00 相比，10 是否能在较少额外工具调用的情况下，降低 Main 自我强化和遗漏明显反证的概率？

### H2 · Investigative Autonomy

与 10 相比，11 是否能通过主动调查发现 Main 未明确要求但足以改变结论的新事实？

### H3 · Epistemic Decorrelation

与 11 相比，01 是否在 Blind Review / Security Audit 等任务中提供更高的独立证据价值？

### H4 · Environment-dependent Polity

Garden 中 11 是否具有更好的综合正确率；Abyss 中 00/10 是否具有更好的延迟、资源和风险表现？

### H5 · Dynamic Switching

动态切换政体是否优于把所有 Subagent 永久固定在单一模式？

可测指标包括：

- 任务正确率；
- 反证发现率；
- 独立错误相关性；
- 工具调用数；
- token 成本；
- 延迟；
- 错误恢复率；
- 高风险误操作率。

---

## 16. v1 暂不纳入

第一版保持克制，不急于加入：

- 信任分数；
- Agent 等级；
- voting；
- 声望系统；
- 人格系统；
- 多层 belief graph；
- 十几个连续参数；
- 行动自主权；
- 复杂社会学类比。

理由：

```text
2 bit / 4 state
```

已经具有一个非常难得的性质：

> **足够小，同时四个象限都有独立工程意义。**

先证明它可实现、可解释、可测试、能改善多 Agent 编排，再考虑扩展。

---

## 17. 一句话版本

**English**

> Orthogonal Agent Polity models how a sovereign Main Agent governs Subagents by dynamically switching orthogonal dimensions of context openness and investigative autonomy.

**中文**

> 正交代理政体通过“上下文开放性 × 调查自主性”等正交维度，描述拥有完整治理权的 Main Agent 如何动态调节 Subagent 的认识论自由。

认识论原则：

> **Agents share cognition, but reality remains outside them.**
>
> **代理共享认知，但事实永远在代理之外。**

---

## 18. 后续路线

1. 实现最小 Harness：`context_openness` + `investigative_autonomy`。
2. 为四种政体分别建立最小可重复实验。
3. 测量正确率、相关错误、工具成本和延迟。
4. 验证 01 是否确实产生有价值的认知去相关性。
5. 验证 Garden / Abyss 下的最优政体是否不同。
6. 实现动态切换策略，并测试切换收益。
7. 在数据支持后，再考虑新增正交维度或独立权限框架。
