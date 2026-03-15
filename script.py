import sys
import re

file_path = r"d:\Documents\TitanDex\src\pages\index.astro"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Frontmatter
content = content.replace("---\n---", "---\nimport titansData from '../data/titans.json';\nconst titansJSON = JSON.stringify(titansData);\n---")

# 2. Before <script is:inline>
content = content.replace("<script is:inline>", '<script id="titans-data" type="application/json" set:html={titansJSON}></script>\n<script is:inline>')

# 3. TITANS array
# Match const TITANS = [ ... ]; exactly, taking everything until the FIRST ];
titans_pattern = re.compile(r'const TITANS = \[.*?\];', re.DOTALL)
content = titans_pattern.sub("const TITANS = JSON.parse(document.getElementById('titans-data').textContent);", content, count=1)

# 4. Field names
replacements = {
    "t.alignment": "t.align",
    'data-a="${t.alignment}"': 'data-a="${t.align}"',
    "t.id_code": "t.id",
    "t.bio": "t.origin",
    "t.weaknesses.map(": "[t.weakness].map(",
    "t.appearances.map(": "[t.first].map(",
    "t.power": "50",
    "`tl-${t.threat.toLowerCase()}`": "`tl-${t.threat}`"
}
for k, v in replacements.items():
    content = content.replace(k, v)

# 5. Mini strip HTML
strip_pattern = re.compile(r'<div class="tmini-grid">.*?VIEW ALL 48 →</div></div>\s*</div>', re.DOTALL)
content = strip_pattern.sub('<div class="tmini-grid" id="home-titan-strip"></div>', content, count=1)

# 6. Add JS block
js_block = """const TITANS = JSON.parse(document.getElementById('titans-data').textContent);
const strip = document.getElementById('home-titan-strip');
if(strip) {
  strip.innerHTML = TITANS.slice(0,7).map(t=>`
    <div class="tmini" onclick="openTitan('${t.id}')">
      <div class="tmini-e">${t.emoji}</div>
      <div class="tmini-n">${t.name}</div>
      <div class="tmini-s">${t.status.toUpperCase()} · ${t.threat.toUpperCase()}</div>
    </div>
  `).join('') + `<div class="tmini tmini-more" onclick="showPage('titandex')">
    <div style="font-family:var(--font-mono);font-size:0.6rem;color:var(--nuclear);letter-spacing:3px">VIEW ALL ${TITANS.length} →</div>
  </div>`;
}"""
content = content.replace("const TITANS = JSON.parse(document.getElementById('titans-data').textContent);", js_block)

# 7. openTitan lookup
content = content.replace("const t=TITANS.find(x=>x.id===id);", "const t = TITANS.find(x => x.id === id);")
content = content.replace("const t = TITANS.find(x=>x.id===id);", "const t = TITANS.find(x => x.id === id);")

# 8. Score calculation
score_pattern = re.compile(r'const scoreA=.*?\n\s*const scoreB=.*?;')
new_score = """const threatScore = {omega:4, high:3, medium:2, low:1};
  const scoreA = (threatScore[a.threat]||1)*25 + (parseFloat(a.height)*0.1);
  const scoreB = (threatScore[b.threat]||1)*25 + (parseFloat(b.height)*0.1);"""
content = score_pattern.sub(new_score, content, count=1)

content = content.replace("{label:'POWER INDEX',va:a.power,vb:b.power},", "{label:'THREAT TIER', va:threatScore[a.threat]||1, vb:threatScore[b.threat]||1, labels:['Low','Medium','High','Omega']},")


with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Modifications complete.")
