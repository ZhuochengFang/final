# 相关电平移位（CLS）技术综述

## 1. 背景与概念

在低电压、低功耗模拟/混合信号电路（尤其是动态放大器、离散时间积分器与数据转换器）中，传统增益与线性提升方法常受头间距（headroom）限制。**电平移位（Level Shifting）**通过改变关键信号节点的直流电平或共模，提升有效摆幅利用率。  

**Correlated Level Shifting, CLS（相关电平移位）**进一步强调“相关性”：在时钟相关相位（如采样相/放大相）内执行受控电平平移，使平移带来的误差项在后续处理链中被相关抑制，从而在低压下改善线性、噪声与功耗效率。

---

## 2. references/CLS 目录内文献解读

### 2.1 A 1.2-V 2.87-μW 94.0-dB SNDR Discrete-Time 2–0 MASH Delta-Sigma ADC

- **来源**：IEEE JSSC, 2023（对应 ISSCC 2022 前序工作）
- **核心问题**：在 1.2V 供电与微瓦级功耗下，如何保持高 SNDR。
- **CLS作用（论文主线）**：将 CLS 与离散时间前端放大/积分路径结合，用相关相位电平平移减轻低压下的动态放大非线性与增益不足影响。
- **代表指标**（文献标题可确认）：
  - 供电：1.2 V
  - 功耗：2.87 μW
  - SNDR：94.0 dB
- **技术意义**：证明 CLS 可在超低功耗高精度 ΔΣ ADC 中成为“低压性能恢复器件级手段”。

### 2.2 Ping-Pong Operated Inverter-based OTA using Correlated Level Shifting Technique

- **来源**：IEEE ICSICT, 2020
- **核心问题**：inverter-based OTA 在低压条件下的增益、线性与效率折中。
- **CLS作用（论文主线）**：在 ping-pong（交替工作）结构中引入 CLS，使不同相位的放大路径共享更有利的工作点，提升有效驱动与摆幅利用。
- **技术意义**：说明 CLS 不只服务于 ADC 系统级，也可作为 OTA 级别的方法论，与交替放大结构协同。

> 注：以上两篇中，个别细节参数（如某些二级指标）建议在你后续精读原文时再逐项补齐到图表中。

---

## 3. CLS 技术路径与分类

### 3.1 按时间域分类

1. **DT-CLS（离散时间 CLS）**  
   依赖开关电容与多相时钟，在采样/放大相完成电平重定位；常见于 ΔΣ、SC 积分器前端。

2. **CT-CLS（连续时间 CLS）**  
   将相关电平控制嵌入连续时间链路，适配更高速或更宽摆幅前端。

### 3.2 按协同机制分类

1. **CLS + 动态放大器/FIA**：提升低压下有效增益与线性。  
2. **CLS + Ping-Pong 交替结构**：用相位复用降低瞬态压力、提升效率。  
3. **CLS + 体偏置/噪声整形**：把器件级与系统级优化同时纳入设计。

---

## 4. 设计收益与代价

### 4.1 主要收益

- 更高摆幅利用率（低压下尤为关键）
- 在相近功耗下改善线性/SNDR
- 为 inverter-based、dynamic 等低功耗拓扑提供额外设计自由度

### 4.2 主要代价

- 对时钟相位关系更敏感（非重叠、抖动、相位偏差）
- 开关注入、寄生耦合与电容失配更容易转化为误差
- 电路时序与版图约束更复杂

---

## 5. 工程实践建议

1. 先做行为级模型，量化“CLS收益对相位误差/失配”的敏感性。  
2. 在晶体管级重点验证：PVT、Monte Carlo、开关注入与寄生耦合。  
3. 版图上保证 CLS 关键节点短互连与对称性，降低系统性失配。  
4. 系统级上将 CLS 与噪声整形、数字校正协同设计，而非孤立优化单个模块。

---

## 6. 可补充的外部相关文献（在线）

1. **Hu et al., ISSCC 2022**  
   *A 2.87μW 1kHz-BW 94.0dB-SNDR 2-0 MASH ADC Using FIA with Dynamic-Body-Biasing Assisted CLS Technique*  
   DOI: https://doi.org/10.1109/ISSCC42614.2022.9731544

2. **Meng et al., JSSC 2023**  
   *A 1.2-V 2.87-μW 94.0-dB SNDR Discrete-Time 2–0 MASH Delta-Sigma ADC*  
   DOI: https://doi.org/10.1109/JSSC.2022.3208144

3. **Ye et al., ISSCC 2025**  
   *A Rail-to-Rail 3rd-Order Noise-Shaping SAR ADC Using Continuous-Time Correlated Level Shifting*  
   DOI: https://doi.org/10.1109/ISSCC49661.2025.10904773

4. **ICSICT 2020（本地已有）**  
   *Ping-Pong Operated Inverter-based OTA using Correlated Level Shifting Technique*  
   DOI: https://doi.org/10.1109/ICSICT49897.2020.9278332

---

## 7. 小结

CLS 的本质是在“相关相位”内重新分配电平与误差，使低压模拟电路在不显著增加静态功耗的前提下获得更好的线性与动态性能。现有代表工作显示，CLS 已从 OTA 局部技巧扩展到 ADC 系统级关键技术。对工程实现而言，成败通常不在概念本身，而在时序、寄生与失配控制是否闭环到位。
