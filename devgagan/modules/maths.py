import asyncio
from devgagan import sex
from telethon import events, functions
from telethon.tl.types import InputRichMessageMarkdown

SIGNATURE = "\n\n---\n🛡️ **Owner:** [𝗖𝗛𝗢𝗦𝗘𝗡 𝗢𝗡𝗘 ⚝](https://t.me/CHOSEN_ONEx_bot)"

START_TEXT = r"""
# 🎓 Ultimate Study & Math Reference Bot

Welcome! I'm formatted using **Telegram's Rich Markdown** (tables, LaTeX math, checklists, quotes, code).

Here is the directory of available reference commands:

- `/math` - Higher Mathematics (Algebra, Calculus, Statistics)
- `/arithmetic` - Percentage, Ratio, Interest & Proportion formulas
- `/geometry` - Area, Perimeter, and Volume of 2D/3D shapes
- `/cheatsheet` - Formula quick reference table (Physics, Chemistry & Math)
- `/reasoning` - Direction & Distance Reasoning Tricks & Formulas
- `/coding` - Coding-Decoding Reasoning logic & Shift Diagram
- `/chart` - Alphabet A-Z Position Reference Grid Chart

*Use these commands to quickly pull up study materials anytime!*""" + SIGNATURE

MATH_TEXT = r"""
# 📐 Higher Mathematics Formulas

## 1. Algebra & Series

* **Quadratic Formula:**
  If $ax^2 + bx + c = 0$, then:
  
  $$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$
  
* **Binomial Theorem:**
  $$(a+b)^n = \sum_{k=0}^{n} \binom{n}{k} a^{n-k} b^k$$

## 2. Calculus

* **Derivative Definition:**
  $$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$
  
* **Integration by Parts:**
  $$\int u\,dv = uv - \int v\,du$$

## 3. Probability & Statistics

* **Bayes' Theorem:**
  $$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$
  
* **Standard Deviation (Sample):**
  $$s = \sqrt{\frac{\sum_{i=1}^{n} (x_i - \bar{x})^2}{n-1}}$$""" + SIGNATURE

ARITHMETIC_TEXT = r"""
# 🧮 Arithmetic: Percentages & Ratios

## 1. Percentages

* **Percentage Change:**
  $$\text{Percentage Change} = \frac{\text{New Value} - \text{Old Value}}{\text{Old Value}} \times 100\%$$
  
* **Profit & Loss Percentage:**
  $$\text{Profit \%} = \frac{\text{Selling Price} - \text{Cost Price}}{\text{Cost Price}} \times 100\%$$
  
  $$\text{Loss \%} = \frac{\text{Cost Price} - \text{Selling Price}}{\text{Cost Price}} \times 100\%$$
  
* **Simple Interest:**
  $$I = \frac{P \cdot r \cdot t}{100}$$
  
* **Compound Interest:**
  $$A = P \left(1 + \frac{r}{n}\right)^{nt}$$
  
  _Where $A$ is the total amount, $P$ is principal, $r$ is interest rate, $n$ is compounding frequency, and $t$ is time._

## 2. Ratio & Proportion

* **Ratio Equality (Proportion):**
  $$\frac{a}{b} = \frac{c}{d} \implies a \cdot d = b \cdot c$$
  
* **Compound Ratio:**
  $$\text{Compound of } a:b \text{ and } c:d \text{ is } (a \cdot c) : (b \cdot d)$$
  
* **Direct Variation:** $y = k \cdot x$ (where $k$ is constant)

* **Inverse Variation:** $y = \frac{k}{x} \implies x \cdot y = k$""" + SIGNATURE

GEOMETRY_TEXT = r"""
# 📏 Geometry: Area & Volume Formulas

## 1. 2D Shapes (Area & Perimeter)

* **Circle:**
  * $\text{Area} = \pi r^2$
  * $\text{Circumference} = 2\pi r$
  
* **Triangle:**
  * $\text{Area} = \frac{1}{2} \cdot b \cdot h$
  * $\text{Heron's Formula:} \sqrt{s(s-a)(s-b)(s-c)} \quad \text{where } s = \frac{a+b+c}{2}$

## 2. 3D Solids (Volume & Surface Area)

| Solid Shape | Volume Formula | Total Surface Area (TSA) |
|:---|:---:|:---|
| **Sphere** | $V = \frac{4}{3}\pi r^3$ | $A = 4\pi r^2$ |
| **Cylinder** | $V = \pi r^2 h$ | $A = 2\pi r(r + h)$ |
| **Cone** | $V = \frac{1}{3}\pi r^2 h$ | $A = \pi r(r + \sqrt{r^2 + h^2})$ |
| **Cube** | $V = a^3$ | $A = 6a^2$ |
| **Rect. Prism** | $V = l \cdot w \cdot h$ | $A = 2(lw + lh + wh)$ |""" + SIGNATURE

CHEATSHEET_TEXT = r"""
# 📊 Subject Cheat Sheet

| Subject | Topic | Key Formula | Explanation |
|:---|:---|:---:|:---|
| **Physics** | Gravity | $F = G \frac{m_1 m_2}{r^2}$ | Universal Gravitational Force |
| **Physics** | Einstein | $E = mc^2$ | Mass-energy Equivalence |
| **Chemistry**| Ideal Gas | $PV = nRT$ | Pressure, Vol, Temp relation |
| **Chemistry**| pH Value | $\text{pH} = -\log_{10}[\text{H}^+]$ | Acidity/Alkalinity measure |
| **Math** | Euler Poly | $V - E + F = 2$ | Vertices, Edges, Faces |
| **Math** | Euler Identity| $e^{i\pi} + 1 = 0$ | Linking 5 major constants |""" + SIGNATURE

REASONING_TEXT = r"""
# 🧭 Direction & Distance Tricks & Formulas

## 1. The 8 Main Directions

```
       N (North)
    NW  │  NE
      \ │ /
W ──────┼────── E (East)
(West) /│\
      / │ \
    SW  │  SE
       S (South)
```

## 2. Key Rules & Tricks

* **Pythagoras Theorem:** For finding the shortest distance:
  $$H^2 = B^2 + P^2 \implies H = \sqrt{B^2 + P^2}$$
  
  _Where $H$ is the hypotenuse (shortest distance), $B$ is the base, and $P$ is the perpendicular._
  
* **Turn Angles:**
  * Left turn = $90^\circ$ Counter-Clockwise (CCW)
  * Right turn = $90^\circ$ Clockwise (CW)
  
* **Shadow Cases:**
  * **Sunrise (East):** Shadow is always in the **West**.
  * **Sunset (West):** Shadow is always in the **East**.
  * **Noon (12 PM):** No shadow is formed.""" + SIGNATURE

CODING_TEXT = r"""
# 🔐 Coding-Decoding Reasoning Guide

## ❓ Problem Example

In a certain secret code language:
> **"STUDY"** is coded as **"VwxgB"**

**How will the word "SMART" be coded in that same language?**

---

## 🗺️ Logic Shift Diagram

Here is how each letter shifts forward by **+3 positions** in the alphabet:

```
Input Word:  S   T   U   D   Y
             │   │   │   │   │
Shift Value: +3  +3  +3  +3  +3
             ▼   ▼   ▼   ▼   ▼
Coded Word:  V   W   X   G   B
```

*(Note: For Y + 3, we wrap around: Y ➔ Z ➔ A ➔ B)*

---

## 💡 Step-by-Step Decoding for "SMART"

Applying the exact same **+3 shift** logic to each letter of **"SMART"**:

| Letter | Shift Logic | Resulting Letter |
|:---:|:---:|:---:|
| **S** | $S \xrightarrow{+3} (T, U, V)$ | **V** |
| **M** | $M \xrightarrow{+3} (N, O, P)$ | **P** |
| **A** | $A \xrightarrow{+3} (B, C, D)$ | **D** |
| **R** | $R \xrightarrow{+3} (S, T, W)$ | **U** |
| **T** | $T \xrightarrow{+3} (U, V, W)$ | **W** |

### 📐 Final Coded Answer:

> **"SMART"** ➔ **"VpdUW"**""" + SIGNATURE

CHART_TEXT = r"""
# 🔠 Alphabet Position Reference Chart

Use this grid reference chart for solving **Coding-Decoding** problems:

| Letter | Position | Letter | Position |
|:---:|:---:|:---:|:---:|
| **A** | `1` | **N** | `14` |
| **B** | `2` | **O** | `15` |
| **C** | `3` | **P** | `16` |
| **D** | `4` | **Q** | `17` |
| **E** | `5` | **R** | `18` |
| **F** | `6` | **S** | `19` |
| **G** | `7` | **T** | `20` |
| **H** | `8` | **U** | `21` |
| **I** | `9` | **V** | `22` |
| **J** | `10` | **W** | `23` |
| **K** | `11` | **X** | `24` |
| **L** | `12` | **Y** | `25` |
| **M** | `13` | **Z** | `26` |

> **Tip:** Memorizing this chart or writing it down quickly in exams will save you valuable time!""" + SIGNATURE

@sex.on(events.NewMessage(pattern=r"^/(math|maths)$"))
async def maths_menu_handler(e):
    chat = await e.get_input_chat()
    await sex(functions.messages.SendMessageRequest(
        peer=chat,
        message="Study Reference Menu",
        rich_message=InputRichMessageMarkdown(markdown=START_TEXT),
    ))

@sex.on(events.NewMessage(pattern=r"^/algebra$"))
async def algebra_handler(e):
    chat = await e.get_input_chat()
    await sex(functions.messages.SendMessageRequest(
        peer=chat,
        message="Mathematics Formulas",
        rich_message=InputRichMessageMarkdown(markdown=MATH_TEXT),
    ))

@sex.on(events.NewMessage(pattern=r"^/arithmetic$"))
async def arithmetic_handler(e):
    chat = await e.get_input_chat()
    await sex(functions.messages.SendMessageRequest(
        peer=chat,
        message="Arithmetic Formulas",
        rich_message=InputRichMessageMarkdown(markdown=ARITHMETIC_TEXT),
    ))

@sex.on(events.NewMessage(pattern=r"^/geometry$"))
async def geometry_handler(e):
    chat = await e.get_input_chat()
    await sex(functions.messages.SendMessageRequest(
        peer=chat,
        message="Geometry Formulas",
        rich_message=InputRichMessageMarkdown(markdown=GEOMETRY_TEXT),
    ))

@sex.on(events.NewMessage(pattern=r"^/cheatsheet$"))
async def cheatsheet_handler(e):
    chat = await e.get_input_chat()
    await sex(functions.messages.SendMessageRequest(
        peer=chat,
        message="Cheat Sheet",
        rich_message=InputRichMessageMarkdown(markdown=CHEATSHEET_TEXT),
    ))

@sex.on(events.NewMessage(pattern=r"^/reasoning$"))
async def reasoning_handler(e):
    chat = await e.get_input_chat()
    await sex(functions.messages.SendMessageRequest(
        peer=chat,
        message="Direction & Distance Reasoning",
        rich_message=InputRichMessageMarkdown(markdown=REASONING_TEXT),
    ))

@sex.on(events.NewMessage(pattern=r"^/coding$"))
async def coding_handler(e):
    chat = await e.get_input_chat()
    await sex(functions.messages.SendMessageRequest(
        peer=chat,
        message="Coding-Decoding Guide",
        rich_message=InputRichMessageMarkdown(markdown=CODING_TEXT),
    ))

@sex.on(events.NewMessage(pattern=r"^/chart$"))
async def chart_handler(e):
    chat = await e.get_input_chat()
    await sex(functions.messages.SendMessageRequest(
        peer=chat,
        message="Alphabet Position Reference Chart",
        rich_message=InputRichMessageMarkdown(markdown=CHART_TEXT),
    ))
