from devgagan import sex
from telethon import events, functions
from telethon.tl.types import InputRichMessageMarkdown

MATHS_TEXT = """
# 📐 મુખ્ય સંદર્ભ મેનૂ (Master Reference)

ફોર્મ્યુલા ડેટાબેઝમાં આપનું સ્વાગત છે. તમને જોઈતો વિભાગ પસંદ કરો:
- `/algebra` — ઉચ્ચ ગણિત (બીજગણિત, કલનશાસ્ત્ર અને સંભાવના)
- `/arithmetic` — અંકગણિત (ટકાવારી, ગુણોત્તર અને ચક્રવૃદ્ધિ વ્યાજ)
- `/geometry` — ભૂમિતિ (દ્વિ-પરિમાણીય અને ત્રિ-પરિમાણીય આકારોના કોષ્ટકો)
- `/cheatsheet` — વિજ્ઞાન ચીટ શીટ (ભૌતિકશાસ્ત્ર અને રસાયણશાસ્ત્ર)
- `/timetable` — સાપ્તાહિક અભ્યાસ પત્રક (ટાઇમટેબલ)
- `/checklist` — સિલેબસ પ્રગતિ ચેકલિસ્ટ

---
સંકલનકર્તા: **𝗖𝗛𝗢𝗦𝗘𝗡 𝗢𝗡𝗘 ⚝**
"""

ALGEBRA_TEXT = """
# 📐 ઉચ્ચ ગણિતના સૂત્રો (Higher Maths)

## ૧. બીજગણિત અને શ્રેણી (Algebra & Series)
* **દ્વિઘાત સમીકરણનું સૂત્ર (Quadratic Formula):**
  જો $ax^2 + bx + c = 0$ હોય, તો તેના ઉકેલ:
  $$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$
* **દ્વિપદી પ્રમેય (Binomial Theorem):**
  $$(a+b)^n = \\sum_{k=0}^{n} \\binom{n}{k} a^{n-k} b^k$$

## ૨. કલનશાસ્ત્ર (Calculus)
* **વિકલનની વ્યાખ્યા (Derivative):**
  $$f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$$
* **ખંડશઃ સંકલન (Integration by Parts):**
  $$\\int u\\,dv = uv - \\int v\\,du$$

## ૩. સંભાવના અને આંકડાશાસ્ત્ર (Probability & Stats)
* **બેઝનું પ્રમેય (Bayes' Theorem):**
  $$P(A|B) = \\frac{P(B|A) \\cdot P(A)}{P(B)}$$
* **પ્રમાણિત વિચલન (Standard Deviation - Sample):**
  $$s = \\sqrt{\\frac{\\sum_{i=1}^{n} (x_i - \\bar{x})^2}{n-1}}$$

---
🛡️ માલિક: **𝗖𝗛𝗢𝗦𝗘𝗡 𝗢𝗡𝗘 ⚝**
"""

ARITHMETIC_TEXT = """
# 🧮 અંકગણિત: ટકાવારી અને ગુણોત્તર

## ૧. ટકાવારી (Percentages)
* **ટકાવારીમાં ફેરફાર (Percentage Change):**
  $$\\text{ટકાવારી ફેરફાર} = \\frac{\\text{નવી કિંમત} - \\text{જૂની કિંમત}}{\\text{જૂની કિંમત}} \\times 100\\%$$
* **નફો અને નુકસાન ટકાવારી (Profit & Loss %):**
  $$\\text{નફો \\%} = \\frac{\\text{વેચાણ કિંમત} - \\text{ખરીદ કિંમત}}{\\text{ખરીદ કિંમત}} \\times 100\\%$$
  $$\\text{નુકસાન \\%} = \\frac{\\text{ખરીદ કિંમત} - \\text{વેચાણ કિંમત}}{\\text{ખરીદ કિંમત}} \\times 100\\%$$
* **સાદું વ્યાજ (Simple Interest):**
  $$I = \\frac{P \\cdot r \\cdot t}{100}$$
* **ચક્રવૃદ્ધિ વ્યાજ (Compound Interest):**
  $$A = P \\left(1 + \\frac{r}{n}\\right)^{nt}$$
  _જ્યાં $A$ કુલ વ્યાજમુદ્દલ છે, $P$ મુદ્દલ છે, $r$ વ્યાજનો દર છે, $n$ વ્યાજ ગણતરીની ચક્રવૃદ્ધિ આવૃત્તિ છે, અને $t$ સમય છે._

## ૨. ગુણોત્તર અને પ્રમાણ (Ratio & Proportion)
* **ગુણોત્તર સમાનતા (Proportion):**
  $$\\frac{a}{b} = \\frac{c}{d} \\implies a \\cdot d = b \\cdot c$$
* **મિશ્ર ગુણોત્તર (Compound Ratio):**
  $$a:b \\text{ અને } c:d \\text{ નો મિશ્ર ગુણોત્તર } (a \\cdot c) : (b \\cdot d) \\text{ થાય.}$$
* **સમપ્રમાણ (Direct Variation):** $y = k \\cdot x$ (જ્યાં $k$ અચળાંક છે)
* **વ્યસ્તપ્રમાણ (Inverse Variation):** $y = \\frac{k}{x} \\implies x \\cdot y = k$

---
🛡️ માલિક: **𝗖𝗛𝗢𝗦𝗘𝗡 𝗢𝗡𝗘 ⚝**
"""

GEOMETRY_TEXT = """
# 📏 ભૂમિતિ: ક્ષેત્રફળ અને ઘનફળ

## ૧. દ્વિ-પરિમાણીય આકારો (2D Shapes)
* **વર્તુળ (Circle):**
  * $\\text{ક્ષેત્રફળ} = \\pi r^2$
  * $\\text{પરિધ} = 2\\pi r$
* **ત્રિકોણ (Triangle):**
  * $\\text{ક્ષેત્રફળ} = \\frac{1}{2} \\cdot \\text{પાયો} \\cdot \\text{વેધ}$
  * $\\text{હેરોનનું સૂત્ર:} \\sqrt{s(s-a)(s-b)(s-c)} \\quad \\text{જ્યાં } s = \\frac{a+b+c}{2}$

## ૨. ત્રિ-પરિમાણીય આકારો (3D Solids)
| આકાર | ઘનફળનું સૂત્ર (Volume) | કુલ પૃષ્ઠફળ (Surface Area) |
|:---|:---:|:---|
| **ગોળો (Sphere)** | $V = \\frac{4}{3}\\pi r^3$ | $A = 4\\pi r^2$ |
| **નળાકાર (Cylinder)** | $V = \\pi r^2 h$ | $A = 2\\pi r(r + h)$ |
| **શંકુ (Cone)** | $V = \\frac{1}{3}\\pi r^2 h$ | $A = \\pi r(r + \\sqrt{r^2 + h^2})$ |
| **સમઘન (Cube)** | $V = a^3$ | $A = 6a^2$ |
| **લંબઘન (Prism)** | $V = l \\cdot w \\cdot h$ | $A = 2(lw + lh + wh)$ |

---
🛡️ માલિક: **𝗖𝗛𝗢𝗦𝗘𝗡 𝗢𝗡𝗘 ⚝**
"""

CHEATSHEET_TEXT = """
# 📊 વિજ્ઞાન ચીટ શીટ (Science Cheat Sheet)

| વિષય | પ્રકરણ / ટોપિક | મુખ્ય સૂત્ર | ટૂંકી સમજૂતી |
|:---|:---|:---:|:---|
| **ભૌતિકશાસ્ત્ર** | ગુરુત્વાકર્ષણ | $F = G \\frac{m_1 m_2}{r^2}$ | સાર્વત્રિક ગુરુત્વાકર્ષણ બળ |
| **ભૌતિકશાસ્ત્ર** | સાપેક્ષતા | $E = mc^2$ | દળ-ઊર્જા સમતુલ્યતા સૂત્ર |
| **રસાયણશાસ્ત્ર**| આદર્શ વાયુ | $PV = nRT$ | દબાણ, કદ અને તાપમાન સંબંધ |
| **રસાયણશાસ્ત્ર**| pH માપક્રમ | $\\text{pH} = -\\log_{10}[\\text{H}^+]$ | એસિડ અને બેઇઝનું માપ |
| **ગણિત** | યુલર બહુકોણ | $V - E + F = 2$ | શિરોબિંદુ, ધાર અને ફલક સંબંધ |
| **ગણિત** | યુલર આઇડેન્ટિટી| $e^{i\\pi} + 1 = 0$ | ૫ મુખ્ય ગાણિતિક અચળાંકો |

---
🛡️ માલિક: **𝗖𝗛𝗢𝗦𝗘𝗡 𝗢𝗡𝗘 ⚝**
"""

TIMETABLE_TEXT = """
# 📅 સાપ્તાહિક અભ્યાસ પત્રક (Study Timetable)

| દિવસ | સવારે ૦૯:૦૦ - ૧૨:૦૦ | બપોરે ૧૪:૦૦ - ૧૭:૦૦ | સાંજે ૧૯:૦૦ - ૨૨:૦૦ |
|:---|:---:|:---:|:---:|
| **સોમવાર** | ગણિત (બીજગણિત) 📐 | ભૌતિકશાસ્ત્ર (મિકેનિક્સ) ⚛️ | પુનરાવર્તન અને હોમવર્ક 📝 |
| **મંગળવાર** | રસાયણશાસ્ત્ર (ઓર્ગેનિક) 🧪| અંગ્રેજી સાહિત્ય 📖 | કોડિંગ પ્રેક્ટિસ 💻 |
| **બુધવાર** | જીવવિજ્ઞાન (જીનેટિક્સ) 🌿 | ઇતિહાસ 🏛️ | મોક ટેસ્ટ પ્રેક્ટિસ ⏱️ |
| **ગુરુવાર** | ગણિત (કલનશાસ્ત્ર) 📐 | ભૌતિકશાસ્ત્ર (ઓપ્ટિક્સ) ⚛️ | કોડિંગ પ્રેક્ટિસ 💻 |
| **શુક્રવાર** | રસાયણશાસ્ત્ર (ઇનઓર્ગેનિક) 🧪| પુનરાવર્તન 📝 | પ્રોજેક્ટ વર્ક 🚀 |
| **શનિવાર** | ફુલ મોક ટેસ્ટ 🏆 | પરિણામ વિશ્લેષણ 📊 | સામાન્ય જ્ઞાન (GK) 🌍 |
| **રવિવાર** | રજા / આરામ 🏖️ | આવતા અઠવાડિયાનું આયોજન 📅 | પુસ્તક વાંચન 📚 |

---
🛡️ માલિક: **𝗖𝗛𝗢𝗦𝗘𝗡 𝗢𝗡𝗘 ⚝**
"""

CHECKLIST_TEXT = """
# 📋 સિલેબસ પ્રગતિ ચેકલિસ્ટ

## ૧. ગણિત (Mathematics)
- [x] બીજગણિત: દ્વિઘાત સમીકરણો અને દ્વિપદી પ્રમેય
- [x] કલનશાસ્ત્ર: વિકલનની વ્યાખ્યા અને મૂળભૂત નિયમો
- [ ] સંકલન: નિયત અને અનિયત સંકલન
- [ ] આંકડાશાસ્ત્ર: પ્રમાણિત વિચલન અને વિચરણ

## ૨. અંકગણિત (Arithmetic)
- [x] ગુણોત્તર અને પ્રમાણના નિયમો
- [x] સાદું અને ચક્રવૃદ્ધિ વ્યાજ
- [ ] ટકાવારી: નફો, નુકસાન અને વળતર

## ૩. ભૌતિકશાસ્ત્ર (Physics)
- [x] મિકેનિક્સ: ન્યૂટનના નિયમો અને ઘર્ષણ
- [ ] ગુરુત્વાકર્ષણ અને ભ્રમણકક્ષા
- [ ] થર્મોડાયનેમિક્સ અને હીટ ટ્રાન્સફર

---
🛡️ માલિક: **𝗖𝗛𝗢𝗦𝗘𝗡 𝗢𝗡𝗘 ⚝**
"""

@sex.on(events.NewMessage(pattern="/maths"))
async def maths_handler(e):
    await sex(functions.messages.SendMessageRequest(
        peer=await e.get_input_chat(),
        message="મુખ્ય સંદર્ભ મેનૂ",
        rich_message=InputRichMessageMarkdown(markdown=MATHS_TEXT),
    ))

@sex.on(events.NewMessage(pattern="/algebra"))
async def algebra_handler(e):
    await sex(functions.messages.SendMessageRequest(
        peer=await e.get_input_chat(),
        message="બીજગણિતના સૂત્રો",
        rich_message=InputRichMessageMarkdown(markdown=ALGEBRA_TEXT),
    ))

@sex.on(events.NewMessage(pattern="/arithmetic"))
async def arithmetic_handler(e):
    await sex(functions.messages.SendMessageRequest(
        peer=await e.get_input_chat(),
        message="અંકગણિતના સૂત્રો",
        rich_message=InputRichMessageMarkdown(markdown=ARITHMETIC_TEXT),
    ))

@sex.on(events.NewMessage(pattern="/geometry"))
async def geometry_handler(e):
    await sex(functions.messages.SendMessageRequest(
        peer=await e.get_input_chat(),
        message="ભૂમિતિના સૂત્રો",
        rich_message=InputRichMessageMarkdown(markdown=GEOMETRY_TEXT),
    ))

@sex.on(events.NewMessage(pattern="/cheatsheet"))
async def cheatsheet_handler(e):
    await sex(functions.messages.SendMessageRequest(
        peer=await e.get_input_chat(),
        message="વિજ્ઞાન ચીટ શીટ",
        rich_message=InputRichMessageMarkdown(markdown=CHEATSHEET_TEXT),
    ))

@sex.on(events.NewMessage(pattern="/timetable"))
async def timetable_handler(e):
    await sex(functions.messages.SendMessageRequest(
        peer=await e.get_input_chat(),
        message="અભ્યાસ ટાઇમટેબલ",
        rich_message=InputRichMessageMarkdown(markdown=TIMETABLE_TEXT),
    ))

@sex.on(events.NewMessage(pattern="/checklist"))
async def checklist_handler(e):
    await sex(functions.messages.SendMessageRequest(
        peer=await e.get_input_chat(),
        message="સિલેબસ ચેકલિસ્ટ",
        rich_message=InputRichMessageMarkdown(markdown=CHECKLIST_TEXT),
    ))
