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

### 2.3 A 0.39-mm² Stacked Standard-CMOS Humidity Sensor Using a Charge-Redistribution Correlated Level Shifting FIA and a VCO-Based Zoom CDC

- **来源**：IEEE JSSC, 2024, 59(2):435-448，DOI: https://doi.org/10.1109/JSSC.2023.3307427  
- **应用场景**：标准 CMOS 湿度传感器读出链路中的 Zoom CDC（电容-数字转换）。
- **文中 CLS 形式**：提出 **CR-CLS（Charge-Redistribution Correlated Level Shifting）FIA**。其核心不是“固定偏置电平平移”，而是把电平移位动作嵌入开关电容电荷重分配过程，使电平平移与采样/放大相位相关联。

#### 该 CR-CLS 的独特性

1. **由电荷重分配实现电平移位**：不依赖额外静态偏置链路，减少纯模拟偏置依赖。  
2. **“相关”而非“独立”的电平平移**：移位量与离散时间相位及采样电荷关联，能在系统链路中抑制部分增益误差映射。  
3. **与 FIA 深耦合**：CLS 不是外围补偿模块，而是直接作用于 FIA 开环增益与闭环误差。  
4. **与 VCO-based Zoom CDC 协同优化**：属于“前端放大器 + 后端量化”联合设计，不是单模块孤立优化。  
5. **传感器-电路一体化导向**：结合 stacked 标准 CMOS 湿度传感结构，目标是系统面积/成本与精度同时优化。

#### 该 CR-CLS 带来的优势（文中给出的代表结果）

- 相比常规 CLS-FIA，**开环增益至少提升 13.5 dB**（覆盖 -40°C 到 85°C 及极端工艺角）。  
- 由此减小闭环 FIA 增益误差，降低 CDC 非线性与湿度误差。  
- 传感器实现了 **±0.8%RH 峰峰值精度**（40 颗芯片，20%RH–85%RH，文中并给出 3σ 误差 2.5%RH）。  
- **FoMw = 87 fJ/conversion-step**，能效指标优于文中对比的已有工作。  
- 在总输入电容 3 pF 条件下，电容分辨率 **197 aF**、湿度分辨率 **0.094%RH**。  
- 在 2.5 MHz、每次转换周期数 N=16 下，ENOB 为 **12.1 bit**；转换时间 0.04 ms 时功耗约 **9.57 μW**。  
- 芯片面积 **0.39 mm²**，并通过 stacked 传感器方案实现面积/成本优势。

> 小结：这篇工作中的 CLS 独特之处在于“**电荷重分配驱动 + 相位相关**”的实现路径。它把低压动态放大器中常见的增益与线性瓶颈，转化为可在系统级（Zoom CDC）中协同优化的问题，因此在能效、精度和面积三者之间取得了更好的综合平衡。

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
