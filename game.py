import streamlit as st
import random

# إعدادات الصفحة
st.set_page_config(page_title="لعبة السالفة الاحترافية", layout="centered")

# --- قاعدة البيانات ---
DATA = {
    "أنمي 🐉": ["ون بيس", "ناروتو", "هجوم العمالقة", "دراجون بول", "قاتل الشياطين", "هنتر x هنتر", "كونان", "مذكرة الموت", "بليتش", "جوجوتسو كايسن", "طوكيو غول", "ماجيك كايتو", "فول ميتال ألكيميست", "بوكيمون", "كابتن ماجد", "هايكيو", "بلاك كلوفر", "ون بنش مان", "سول ليفيلينج", "أكاديمية بطلي"],
    "مهن 🕵️‍♂️": ["نصاب", "حرامي", "مهرب", "جاسوس", "قاتل مأجور", "طيار", "طبيب جراح", "مبرمج", "حلاق", "رائد فضاء", "نجار", "محامي", "طباخ", "شرطي", "مزارع", "رسام", "ميكانيكي", "مدير بنك", "عامل نظافة", "وزير"],
    "حيوانات 🦁": ["أسد", "زرافة", "بطريق", "تمساح", "نمر", "فيل", "قرد", "دلفين", "ثعبان", "خفاش", "كنغر", "سنجاب", "أرنب", "حصان", "جمل", "ذئب", "ثعلب", "حوت", "قرش", "نسر", "صقر", "بومة", "فهد", "غزال", "حمار وحشي", "دب قطبي", "فرس النهر", "وحيد القرن", "نملة", "نحلة", "عنكبوت", "عقرب", "طاووس", "نعامة", "قنفذ", "سلحفاة", "كوالا"],
    "أماكن 🗺️": ["المستشفى", "المطار", "المدرسة", "الغابة", "السينما", "المطعم", "المتحف", "القمر", "الشاطئ", "ملعب كرة قدم", "سجن", "قصر المهجور", "محطة فضاء", "منجم ذهب", "مكتبة قديمة"],
    "أشياء عشوائية 📦": ["كأس", "فوطة", "وسادة", "تيشيرت", "صندل", "ساعة يد", "نظارة", "مظلة", "حقيبة", "سجادة", "مفتاح", "قلم", "جوال", "شاحن", "ملعقة", "سكين", "مروحة", "كنبة", "لوحة فنية", "مزهرية", "مشط", "مقص", "خريطة", "بوصلة", "كمامة", "عطر", "ولاعة", "طفاية حريق", "مطرقة", "مسمار"]
}

# خيار عشوائي كلي
all_items = []
for items in DATA.values(): all_items.extend(items)
DATA["🎲 عشوائي (كل شيء)"] = all_items

# --- إدارة الذاكرة (النقاط والمراحل) ---
if 'scores' not in st.session_state: st.session_state.scores = {}
if 'stage' not in st.session_state: st.session_state.stage = 'setup'

# --- الواجهة ---
st.markdown("<h1 style='text-align: center; color: #E74C3C;'>🕵️ لـعـبـة السـالـفـة</h1>", unsafe_allow_html=True)

# عرض جدول النقاط في الجانب
with st.sidebar:
    st.header("🏆 جدول النقاط")
    if st.session_state.scores:
        for player, score in st.session_state.scores.items():
            st.write(f"**{player}**: {score} نقطة")
    else:
        st.write("ابدأ اللعب لتجميع النقاط!")

# --- مرحلة الإعداد ---
if st.session_state.stage == 'setup':
    st.subheader("🛠️ إعدادات الجولة الجديدة")
    category = st.selectbox("اختر نوع السالفة:", list(DATA.keys()))
    names_input = st.text_area("أدخل أسماء اللاعبين (اسم في كل سطر):", "لاعب 1\nلاعب 2\nلاعب 3")
    players = [n.strip() for n in names_input.split('\n') if n.strip()]
    
    col1, col2 = st.columns(2)
    with col1: out_count = st.number_input("العدد اللي برا:", 1, max(1, len(players)-1), 1)
    with col2: know_others = st.checkbox("اللي برا يعرفون بعض؟")

    if st.button("ابدأ اللعبة 🔥", use_container_width=True):
        if len(players) < 3: st.error("أدخل 3 لاعبين على الأقل!")
        else:
            for p in players:
                if p not in st.session_state.scores: st.session_state.scores[p] = 0
            
            out_players = random.sample(players, out_count)
            st.session_state.game_data = {
                "players": players, "out_players": out_players,
                "word": random.choice(DATA[category]), "know_others": know_others,
                "revealed": [], "votes": {}
            }
            st.session_state.stage = 'distribute'
            st.rerun()

# --- مرحلة توزيع الكلمات ---
elif st.session_state.stage == 'distribute':
    data = st.session_state.game_data
    st.info(f"مرر الجوال بين اللاعبين لرؤية الأدوار..")
    
    for player in data['players']:
        if player not in data['revealed']:
            if st.button(f"أنا {player} (اضغط للعرض)", key=player, use_container_width=True):
                if player in data['out_players']:
                    st.error("🤫 أنت برا السالفة!")
                    if data['know_others'] and len(data['out_players']) > 1:
                        others = [p for p in data['out_players'] if p != player]
                        st.info(f"شركاؤك هم: {', '.join(others)}")
                else:
                    st.success(f"✅ أنت داخل السالفة! الكلمة هي: **{data['word']}**")
                
                if st.button("تم (أخفِ المعلومة)", key=f"h_{player}"):
                    data['revealed'].append(player)
                    st.rerun()
                st.stop()
        else: st.write(f"✅ {player} رأى الكلمة")

    if len(data['revealed']) == len(data['players']):
        if st.button("انتقل للتصويت بعد النقاش 🗳️", use_container_width=True):
            st.session_state.stage = 'voting'
            st.rerun()

# --- مرحلة التصويت ---
elif st.session_state.stage == 'voting':
    data = st.session_state.game_data
    st.subheader("🗳️ من تشكون أنه برا السالفة؟")
    
    current_voter_idx = len(data['votes'])
    if current_voter_idx < len(data['players']):
        voter = data['players'][current_voter_idx]
        st.write(f"دور اللاعب: **{voter}** ليصوت")
        target = st.selectbox(f"يا {voter}، من برا السالفة؟", [p for p in data['players'] if p != voter])
        if st.button(f"تأكيد تصويت {voter}"):
            data['votes'][voter] = target
            st.rerun()
    else:
        st.subheader("📊 نتائج التصويت")
        vote_counts = {p: list(data['votes'].values()).count(p) for p in data['players']}
        suspect = max(vote_counts, key=vote_counts.get)
        
        st.write(f"أكثر لاعب حصل على أصوات هو: **{suspect}** ({vote_counts[suspect]} صوت)")
        
        if suspect in data['out_players']:
            st.success(f"صح! **{suspect}** كان برا السالفة فعلاً. (الكلمة كانت: {data['word']})")
            # توزيع نقاط
            for p in data['players']:
                if p not in data['out_players']: st.session_state.scores[p] += 1
        else:
            st.error(f"خطأ! **{suspect}** كان داخل السالفة. اللي برا السالفة هم: {', '.join(data['out_players'])}")
            for p in data['out_players']: st.session_state.scores[p] += 2

        if st.button("جولة جديدة 🔄", use_container_width=True):
            st.session_state.stage = 'setup'
            st.rerun()

# تصميم CSS
st.markdown("""
<style>
    .stButton>button { border-radius: 15px; background-color: #f8f9fa; border: 2px solid #E74C3C; color: #333; }
    .stButton>button:hover { background-color: #E74C3C; color: white; }
    .sidebar .sidebar-content { background-color: #f1f3f6; }
</style>
""", unsafe_allow_html=True)
