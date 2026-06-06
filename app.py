from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

tournament = {
    "groups": [],
    "matches": []
}

# ================= HOME =================
HOME_HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>مسابقات پینگ پنگ</title>

<style>

*{
box-sizing:border-box;
font-family:tahoma;
}

body{
margin:0;
padding:20px;
background:linear-gradient(135deg,#0f172a,#1e293b);
color:white;
}

.container{
max-width:900px;
margin:auto;
}

.card{
background:rgba(255,255,255,.08);
backdrop-filter:blur(12px);
border:1px solid rgba(255,255,255,.1);
border-radius:30px;
padding:25px;
box-shadow:0 10px 30px rgba(0,0,0,.35);
}

h1{
text-align:center;
font-size:34px;
}

.sub{
text-align:center;
opacity:.8;
margin-bottom:20px;
}

textarea{
width:100%;
height:320px;
border:none;
outline:none;
resize:none;
border-radius:25px;
padding:20px;
font-size:18px;
background:rgba(255,255,255,.08);
color:white;
}

textarea::placeholder{
color:#cbd5e1;
}

.btn{
width:100%;
padding:18px;
font-size:20px;
border:none;
border-radius:20px;
cursor:pointer;
margin-top:20px;
background:linear-gradient(90deg,#2563eb,#06b6d4);
color:white;
font-weight:bold;
}

.error{
margin-top:20px;
background:rgba(239,68,68,.15);
border:1px solid rgba(239,68,68,.5);
padding:18px;
border-radius:20px;
text-align:center;
}
</style>

</head>

<body>

<div class="container">
<div class="card">

<h1>🏓 مسابقات پینگ پنگ</h1>
<div class="sub">هر خط یک بازیکن</div>

<form method="POST" action="/create">

<textarea name="players" placeholder="علی
رضا
مهدی
سورنا"></textarea>

<button class="btn">ساخت گروه‌ها</button>

</form>

{% if error %}
<div class="error">{{ error }}</div>
{% endif %}

</div>
</div>

</body>
</html>
"""

# ================= GROUP =================
GROUP_HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>گروه‌ها</title>

<style>

*{
box-sizing:border-box;
font-family:tahoma;
}

body{
margin:0;
padding:20px;
background:linear-gradient(135deg,#020617,#0f172a);
color:white;
}

.title{
text-align:center;
font-size:34px;
margin-bottom:30px;
}

.grid{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(320px,1fr));
gap:20px;
}

.group-card{
background:rgba(255,255,255,.08);
backdrop-filter:blur(12px);
border:1px solid rgba(255,255,255,.08);
border-radius:28px;
padding:20px;
box-shadow:0 8px 30px rgba(0,0,0,.35);
}

.group-title{
font-size:26px;
text-align:center;
margin-bottom:15px;
}

.player{
background:rgba(255,255,255,.08);
padding:14px;
border-radius:16px;
margin-bottom:10px;
font-size:18px;
}

.match{
margin-top:12px;
padding:12px;
background:rgba(0,0,0,.25);
border-radius:15px;
}

input{
width:45%;
padding:8px;
border:none;
border-radius:10px;
text-align:center;
margin-top:6px;
}

button{
margin-top:8px;
padding:8px;
border:none;
border-radius:10px;
cursor:pointer;
background:#22c55e;
color:white;
}

.done{
margin-top:8px;
color:#22c55e;
font-weight:bold;
}

.final{
width:100%;
margin-top:20px;
padding:15px;
border:none;
border-radius:15px;
background:#f59e0b;
color:white;
font-size:18px;
cursor:pointer;
}
</style>

</head>

<body>

<h1 class="title">🏓 گروه‌بندی مسابقات</h1>

<div class="grid">

{% for g in groups %}
{% set gid = loop.index0 %}

<div class="group-card">

<div class="group-title">گروه {{ loop.index }}</div>

{% for p in g %}
<div class="player">👤 {{ p["name"] }}</div>
{% endfor %}

{% for m in matches[gid] %}

<div class="match">

<b>{{ m["p1"]["name"] }} vs {{ m["p2"]["name"] }}</b>

<form method="POST" action="/save">

<input name="s1" placeholder="امتیاز 1">
<input name="s2" placeholder="امتیاز 2">

<input type="hidden" name="g" value="{{ gid }}">
<input type="hidden" name="m" value="{{ loop.index0 }}">

<button name="w" value="0">{{ m["p1"]["name"] }} برد</button>
<button name="w" value="1">{{ m["p2"]["name"] }} برد</button>

</form>

{% if m.get("done") %}
<div class="done">
✔ انجام شد | برنده: {{ m["winner"]["name"] }}
</div>
{% endif %}

</div>

{% endfor %}

</div>

{% endfor %}

</div>

<form method="POST" action="/final">
<button class="final">🏆 نمایش رتبه نهایی و صعودکنندگان</button>
</form>

</body>
</html>
"""

# ================= FINAL =================
FINAL_HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>نتایج نهایی</title>

<style>
body{
margin:0;
padding:20px;
font-family:tahoma;
background:linear-gradient(135deg,#0f172a,#1e293b);
color:white;
}

.card{
max-width:800px;
margin:auto;
background:rgba(255,255,255,.08);
padding:20px;
border-radius:20px;
}

.rank{
padding:15px;
margin:10px 0;
background:rgba(255,255,255,.08);
border-radius:15px;
}
</style>

</head>

<body>

<div class="card">

<h1 style="text-align:center;">🏆 نتایج نهایی</h1>

{% for g in results %}

<div class="rank">

<b>گروه {{ loop.index }}</b><br><br>

🥇 اول: {{ g[0]["name"] }}<br>
🥈 دوم: {{ g[1]["name"] }}<br>
🥉 سوم: {{ g[2]["name"] }}<br><br>

🚀 صعودکنندگان: {{ g[0]["name"] }} ، {{ g[1]["name"] }}

</div>

{% endfor %}

</div>

</body>
</html>
"""

# ================= LOGIC =================

def make(name):
    return {
        "name": name,
        "win": 0,
        "sf": 0,
        "sa": 0
    }


def rank(group):
    return sorted(group, key=lambda x:(x["win"], x["sf"]-x["sa"]), reverse=True)


@app.route("/")
def home():
    return render_template_string(HOME_HTML)


@app.route("/create", methods=["POST"])
def create():

    raw = request.form.get("players","")
    players = [p.strip() for p in raw.split("\n") if p.strip()]

    if len(players) == 0:
        return render_template_string(HOME_HTML, error="حداقل یک اسم وارد کن")

    if len(players) % 3 != 0:
        need = 3 - (len(players) % 3)
        return render_template_string(HOME_HTML, error=f"{need} نفر دیگر لازم است")

    random.shuffle(players)

    groups = []
    matches = []

    for i in range(0, len(players), 3):

        chunk = players[i:i+3]

        group = [
            make(chunk[0]),
            make(chunk[1]),
            make(chunk[2])
        ]

        groups.append(group)

        matches.append([
            {"p1":group[0],"p2":group[1]},
            {"p1":group[0],"p2":group[2]},
            {"p1":group[1],"p2":group[2]},
        ])

    tournament["groups"] = groups
    tournament["matches"] = matches

    return render_template_string(GROUP_HTML, groups=groups, matches=matches)


@app.route("/save", methods=["POST"])
def save():

    g = int(request.form["g"])
    m = int(request.form["m"])
    w = int(request.form["w"])

    try:
        s1 = int(request.form.get("s1","0"))
        s2 = int(request.form.get("s2","0"))
    except:
        return "عدد اشتباه"

    match = tournament["matches"][g][m]

    if w == 0:
        winner = match["p1"]
        loser = match["p2"]
    else:
        winner = match["p2"]
        loser = match["p1"]

    match["winner"] = winner
    match["done"] = True

    winner["win"] += 1
    winner["sf"] += max(s1,s2)
    winner["sa"] += min(s1,s2)

    loser["sf"] += min(s1,s2)
    loser["sa"] += max(s1,s2)

    return render_template_string(GROUP_HTML, groups=tournament["groups"], matches=tournament["matches"])


@app.route("/final", methods=["POST"])
def final():

    results = []

    for g in tournament["groups"]:
        results.append(rank(g))

    return render_template_string(FINAL_HTML, results=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)