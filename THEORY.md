# Orthogonal Agent Polity (OAP)

> **正交代理政体：用最低维的政体语义坐标，对 Main Agent 治理 Subagent 的关系进行拟合；具体权限只是操作化，具体行为与系统效果则是涌现结果。**

英文短句：

> **OAP fixes the polity coordinates, not their implementation.**

以及认识论原则：

> **Agents share cognition, but reality remains outside them.**
>
> **代理共享认知，但事实永远在代理之外。**

---

## 0. 理论定位

OAP 是一个用于描述多 Agent **治理关系**的低维语义框架。

它不是：

- 现实政治哲学的直接移植；
- Agent 人格分类；
- 一组永久固定的软件权限；
- “上下文开放性 × 调查自主性”的同义词。

OAP 的第一步，是从复杂的子代理治理关系中抽取两条尽量正交、足够低维、又具有解释力的**政体思潮轴**，形成一个最小 `2 × 2` 关系空间。

OAP v1 采用：

1. **威权主义 ↔ 平等主义**
2. **排外主义 ↔ 亲外主义**

这两个轴首先是**语义拟合坐标**。

它们如何映射成上下文权限、调查权、发言权、预算权、记忆共享、工具调用等工程机制，是第二层问题；这些机制最终产生什么行为，则是第三层问题。

因此 OAP 的基本结构是：

```text
复杂治理现实
    ↓ 最低正交拟合
政体语义坐标
    ↓ 操作化
Harness / Runtime 权限与编排
    ↓ 运行
Agent 行为与系统效果
```

即：

```text
Polity Semantics
      ↓
Operationalization
      ↓
Emergent Phenotype
```

**定义、实现、效果三者必须严格分离。**

---

## 1. 主权假设：Main 是统治者

OAP v1 假定存在一个拥有完整治理权的：

```text
Main Agent / Sovereign
```

Subagent 不与 Main 共享主权。

Main 保留：

- 任务分配权；
- 资源调度权；
- Agent 启停权；
- 工具授权权；
- 执行授权权；
- veto / termination；
- 政体切换权。

因此 OAP 讨论的不是：

> “Main 和 Subagent 是否拥有相同权力？”

而是：

> **Main 以什么政体治理 Subagent？**

即使某条治理边处于“平等”象限，Main 仍然是 Sovereign。

“平等主义”描述的是统治方式中的某种权力下放、主体性承认或认知地位，而不是主权对等。

---

## 2. 两条最小政体轴

### 2.1 轴 A：威权主义 ↔ 平等主义

这条轴描述：

> **统治者在多大程度上垄断议程、判断与决定权，又在多大程度上承认 Subagent 的独立主体性。**

威权主义一侧倾向于：

- 由 Main 定义任务；
- 由 Main 决定何时调查；
- 由 Main 决定哪些问题值得提出；
- Subagent 更接近被调度的工具。

平等主义一侧倾向于：

- 承认 Subagent 可以形成独立判断；
- 允许 Subagent 主动提出值得注意的问题；
- 允许其在一定范围内自行决定调查路径；
- 允许其以自己的证据对 Main 构成有效反证。

但这里**不预先规定**“平等主义一定等于调查自主权”。

调查自主权只是当前参考实现里，对这条语义轴的一种工程操作化。

其它可能的平等主义操作化还包括：

- 主动发言权；
- 独立提出任务的权利；
- 独立预算；
- 独立选择调查方法；
- 对某类操作拥有 veto；
- 对 Main 的判断拥有形式化异议通道。

哪些机制最能拟合这条轴，需要由具体 Harness 和实验决定。

### 2.2 轴 B：排外主义 ↔ 亲外主义

这条轴描述：

> **统治者的认知边界对外部 Agent 有多开放。**

排外主义一侧倾向于：

- Main 的内部认知不向 Subagent 开放；
- Subagent 与 Main 之间保持较强边界；
- 外部认知进入 Main 的通道受到限制；
- 不同 Agent 的判断更可能保持去相关。

亲外主义一侧倾向于：

- Main 愿意让 Subagent 接触自身当前认知；
- Main 接受 Subagent 对自身判断的补充、质疑与修正；
- Agent 之间存在更充分的认知交换；
- 对方的认知可以成为寻找新证据的线索。

但这里同样**不预先规定**“亲外主义一定等于注入 Main 最新上下文”。

上下文开放性只是当前参考实现中的一种操作化。

其它可能的亲外主义操作化包括：

- 开放长期记忆；
- 开放当前假设；
- 开放不确定性与疑点；
- 允许未经邀请的反馈；
- 接受跨 Agent 的证据引用；
- 允许外部 Agent 读取某些决策依据；
- 允许外部 Agent 持续订阅认知变化。

因此：

```text
亲外主义 ≠ Context Openness 本身
```

而是：

```text
亲外主义
    ↓ 某次工程操作化
Context Openness
```

---

## 3. 四象限：政体语义空间

两条二极轴构成最小 `2 × 2` 政体空间：

```text
                    亲外
                     ↑
                     │
          威权亲外   │   平等亲外
                     │
威权 ────────────────┼──────────────── 平等
                     │
          威权排外   │   平等排外
                     │
                     ↓
                    排外
```

四象限首先表示**治理语义位置**。

它们并不永久等价于：

```text
被动工具 / 知情参谋 / 独立调查者 / 开放事实伙伴
```

这些角色只是当前 DeepSeek + Seed 参考实现中，特定操作化后涌现出的第一组典型表型。

---

## 4. 三层模型：语义、操作化、表型

### 4.1 Polity Semantics / 政体语义

这一层只有：

```text
威权 ↔ 平等
排外 ↔ 亲外
```

它负责提供最低维的治理坐标系，不直接规定 API、Prompt、Tool、Context、Memory、Budget 或 Permission。

### 4.2 Operationalization / 操作化

操作化回答：

> “在当前 Agent Harness 中，如何把某个政体语义位置变成可运行机制？”

设：

```text
O = Ψ(P, Harness, Environment)
```

操作化可以涉及：上下文共享、主动调查、搜索预算、主动发言、任务提出、Memory 共享、独立工具选择、veto、并行调查、报告强制阅读等。

**OAP 固定的是坐标，不固定这些工程实现。**

### 4.3 Emergent Phenotype / 涌现表型

运行以后才观察：

- 是否主动纠错；
- 是否产生 Blind Review；
- 是否降低认知相关性；
- 是否发生上下文污染；
- 是否形成群体共识；
- 是否增强自我强化；
- 是否逃离错误认知吸引子；
- 是否增加成本和延迟；
- 是否出现新的失败模式。

设：

```text
Φ = F(P, O, Models, Task, Environment, Randomness)
```

因此：

```text
01 平等排外 ≠ Blind Review
```

而是：

```text
01 平等排外 + 某种操作化 + 某种任务环境
    ↓
可能涌现 Blind Review / 去相关性
```

这些都是**实验发现的效果，不是理论定义**。

---

## 5. 当前参考操作化 v0.1

当前 DeepSeek + Seed 原型为了可运行，采用一套最小映射：

```text
C = Context Openness
I = Investigative Autonomy
```

```text
C ∈ {0,1}
I ∈ {0,1}
```

当前映射 Ψ₀：

```text
排外主义  → C = 0
亲外主义  → C = 1
威权主义  → I = 0
平等主义  → I = 1
```

| 政体语义 | C | I | 当前工程实现 |
|---|---:|---:|---|
| 威权排外 | 0 | 0 | 不共享 Main 最新认知；不允许 Subagent 主动扩大调查 |
| 威权亲外 | 1 | 0 | 共享 Main 最新认知；调查议程仍由 Main 决定 |
| 平等排外 | 0 | 1 | 不共享 Main 当前判断；允许 Subagent 独立调查 |
| 平等亲外 | 1 | 1 | 共享 Main 当前判断；允许 Subagent 主动调查 |

**这张表描述的是第一套实验映射，不是 OAP 的永恒定义。**

应写成：

```text
威权 / 平等  --Ψ₀--> Investigative Autonomy
排外 / 亲外  --Ψ₀--> Context Openness
```

而不是：

```text
平等 = Investigative Autonomy
亲外 = Context Openness
```

---

## 6. 当前参考表型 v0.1

在 Ψ₀ 下，我们预计可能出现：

- **威权排外 → “被动工具”表型**：成本低、按命令调查、不了解 Main 当前认知；
- **威权亲外 → “知情参谋”表型**：知道 Main 的判断，但不自行扩大调查；
- **平等排外 → “独立调查者”表型**：Blind Review、去相关路径可能出现；
- **平等亲外 → “开放事实伙伴”表型**：针对性纠错可能增强，也可能提高错误相关性与上下文污染。

这些全部是**预测表型**，不是象限定义。

---

## 7. 认识论原则：Agent 不是事实本身

> **Agent 可以成为彼此的信息来源，但不能成为彼此的事实来源。**

因此：

```text
Main 的判断 ≠ 事实
Subagent 的判断 ≠ 事实
Agent 间共识 ≠ 事实
多数票 ≠ 事实
```

OAP 中的 adversarial 不是“必须唱反调”，而是：

> **系统始终保留由外部事实推翻任何 Agent 的能力。**

---

## 8. 调查、知情、行动必须分层

尤其要区分：

```text
知情权
调查权
发言权
行动权
```

当前参考实现只重点使用：

```text
Context Openness
Investigative Autonomy
```

它们不自动推出点击按钮、修改文件、提交表单、删除内容或部署代码。

因此：

```text
调查自主权 ≠ 行动自主权
```

执行权限应属于独立 Capability / Permission System。

---

## 9. 政体属于治理边，不属于 Agent 人格

应描述为：

```text
Main --[平等亲外]--> Vision
Main --[平等排外]--> Security
Main --[威权排外]--> Git
```

而不是给 Subagent 固定人格标签。

设：

```text
G = (V, E, M)
```

每条治理边首先具有政体语义标签，随后再由 Harness 操作化成 Runtime 配置。

所以：

```text
Polity Edge ≠ Permission Vector
```

Permission Vector 只是 Polity Edge 的某次实现。

---

## 10. 动态政体

OAP 不假设某一种政体永远最佳：

```text
p_t(M,S) → p_(t+1)(M,S)
```

Main 可以根据时间压力、资源预算、失败成本、操作不可逆性、环境敌意、信息不确定性等改变对子代理的治理方式。

同一个政体变化在不同 Harness 中可以由不同 Runtime 动作实现。

---

## 11. Garden / Abyss 是环境原型，不是理论轴

**Garden / 田园**：时间充足、资源可接受、错误可恢复、可以反复验证、环境敌意较低。较开放、较平等的治理可能有更高认识论收益。

**Abyss / 深渊**：时间极短、资源极少、操作不可逆、失败成本巨大。较威权、较排外的治理可能成为局部生存最优。

它们属于：

```text
环境 → 政体选择
```

不是 OAP 第三轴。

---

## 12. 可逆认知拓扑

成熟系统应能随环境变化收缩与重新展开治理：

```text
平等亲外
 ↓
威权亲外
 ↓
威权排外
```

危机解除后再逐步恢复。

变化的是政体语义状态；具体开关变化由当前操作化函数决定。

---

## 13. 多模态 Agent：第一典型实验域

第一真实参考系统：

```text
DeepSeek V4 Main / Sovereign
        ↓ OAP 治理
Seed Multimodal Subagent
```

当前 Ψ₀ 中：

```text
亲外 / 排外 → 是否向 Seed 暴露 Main 当前认知
平等 / 威权 → 是否允许 Seed 主动扩大事实调查
```

然后观察主动纠错、Blind Review、认知去相关、上下文污染、吸引子逃逸、误纠偏、成本变化等表型。

实验验证的是：

> **这套操作化是否是一种有价值的 OAP 拟合。**

而不是验证 C/I 是 OAP 的永恒本体。

---

## 14. 吸引子实验的理论地位

当前实验关注：

> Main 已经形成一个错误认知吸引子以后，不同政体操作化是否改变其逃逸概率。

观察：

```text
Correction Rate
Resistance Rate
False Correction Rate
Uncertainty Preservation
Cost / Latency
```

这些都是表型层指标。

如果 01 比 11 更容易逃离某类错误吸引子，我们只能说当前“平等排外 → Blind Independent Investigation”的操作化具有去相关价值，不能反过来把结果写进“平等排外”的定义。

---

## 15. 可证伪性与理论更新

OAP v1 主动允许失败：

1. **轴不正交**：若威权/平等与排外/亲外无法稳定独立变化，则当前二维拟合需要修订。
2. **操作化不良**：若某个权限映射不能产生稳定、可解释差异，则应更换操作化，而不是保护现有代码。
3. **表型不成立**：若 Blind Review、去相关、主动纠错或吸引子逃逸无法稳定复现，应降级为偶发现象。
4. **环境依赖**：同一政体在不同模型、任务、预算和风险环境下可能产生相反效果，不应宣布某个象限永久最优。

---

## 16. OAP v1 暂时不做什么

为了保持最低拟合，初版不把 Trust、Reputation、Agent 等级、Voting、Belief Graph、行动权限、资源预算、记忆系统、具体模型人格等并入核心轴。

它们可以成为操作化变量、环境变量、权限系统或观测指标，但不应因为工程上有用，就自动升级成 OAP 的理论原语。

---

## 17. 最小形式化

设：

```text
G = (V, E, M)
```

对每条 Main → Subagent 治理边：

```text
p_t(M,S) = (A_t, X_t)
```

其中：

```text
A_t ∈ {威权, 平等}
X_t ∈ {排外, 亲外}
```

运行时实现：

```text
O_t = Ψ(p_t, Harness, Environment)
```

观察到的表型：

```text
Φ_t = F(p_t, O_t, Models, Task, Environment, Randomness)
```

动态切换：

```text
p_(t+1) = Π(p_t, Environment, Risk, Budget, Uncertainty)
```

OAP 研究的核心不是假定 `Ψ` 和 `F` 已知，而是：

> **用一个足够小的政体语义空间，组织、比较和实验不同的治理实现与涌现效果。**

---

## 18. 一句话版本

英文：

> **Orthogonal Agent Polity models subagent governance through a minimal orthogonal polity space; runtime permissions are operationalizations, and agent behaviors are emergent phenotypes rather than definitions of the polity itself.**

中文：

> **正交代理政体用最小正交政体空间拟合对子代理的治理；运行时权限只是操作化，Agent 行为与系统效果则是涌现表型，而不是政体本身的定义。**

更短的核心：

> **固定坐标，不固定实现；观察涌现，不把涌现倒写成定义。**
