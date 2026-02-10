import streamlit as st
import random

# إعدادات الصفحة
st.set_page_config(page_title="لعبة السالفة الاحترافية", layout="centered")

# --- قاعدة البيانات ---
DATA = {
    "أنمي 🐉": ["ون بيس", "ناروتو", "هجوم العمالقة", "دراجون بول", "قاتل الشياطين", "هنتر x هنتر", "كونان", "مذكرة الموت", "بليتش", "جوجوتسو كايسن", "طوكيو غول", "ماجيك كايتو", "فول ميتال ألكيميست", "بوكيمون", "كابتن ماجد", "هايكيو", "بلاك كلوفر", "ون بنش مان", "سول ليفيلينج", "أكاديمية بطلي"],
    "مهنة 🕵️‍♂️": ["نصاب", "حرامي", "مهرب", "جاسوس", "قاتل مأجور", "طيار", "طبيب جراح", "مبرمج", "حلاق", "رائد فضاء", "نجار", "محامي", "طباخ", "شرطي", "مزارع", "رسام", "ميكانيكي", "مدير بنك", "عامل نظافة", "وزير"],
    "حيوانات 🦁": ["أسد", "زرافة", "بطريق", "تمساح", "نمر", "فيل", "قرد", "دلفين", "ثعبان", "خفاش", "كنغر", "سنجاب", "أرنب", "حصان", "جمل", "ذئب", "ثعلب", "حوت", "قرش", "نسر", "صقر", "بومة", "فهد", "غزال", "حمار وحشي", "دب قطبي", "فرس النهر", "وحيد القرن", "نملة", "نحلة", "عنكبوت", "عقرب", "طاووس", "نعامة", "قنفذ", "سلحفاة", "كوالا"],
    "أماكن 🗺️": ["المستشفى", "المطار", "المدرسة", "الغابة", "السينما", "المطعم", "المتحف", "القمر", "الشاطئ", "ملعب كرة قدم", "سجن", "قصر المهجور", "محطة فضاء", "منجم ذهب", "مكتبة قديمة"],
    "أشياء عشوائية 📦": ["كأس", "فوطة", "وسادة", "تيشيرت", "صندل", "ساعة يد", "نظارة", "مظلة", "حقيبة", "سجادة", "مفتاح", "قلم", "جوال", "شاحن", "ملعقة", "سكين", "مروحة", "كنبة", "لوحة فنية", "مزهرية", "مشط", "مقص", "خريطة", "بوصلة", "كمامة", "عطر", "ولاعة", "طفاية حريق", "مطرقة", "مسمار"]
}

all_items = []
for items in DATA.values(): all_items.extend(items)
DATA["🎲 عشوائي (كل شيء)"] = all_items

# إدارة الحالة (Session State)
if 'scores' not in st.session_state: st.session_state.scores = {}
if 'stage' not in st.session_state: st.session_state.stage = 'setup'
if 'current_player_idx' not in st.session_state: st.session_state.current_player_idx = 0

st.markdown("<h1 style='text-align: center; color: #E74C3C;'>🕵️ لـعـبـة السـالـفـة</h1>", unsafe_allow_html=True)

# عرض النقاط في الجانب
with st.sidebar:
    st.header("🏆 جدول النقاط")
    if st.session_state.scores:
        for player, score in st.session_state.scores.items():
            st.write(f"**{player}**: {score} نقطة")
    else:
        st.write("ابدأ اللعب لتجميع النقاط!")

# --- 1. مرحلة الإعداد ---
if st.session_state.stage == 'setup':
    st.session_state.current_player_idx = 0
    st.subheader("🛠️ إعدادات الجولة")
    category = st.selectbox("اختر نوع السالفة:", list(DATA.keys()))
    names_input = st.text_area("أسماء اللاعبين (اسم في كل سطر):", "أحمد\nأيوب\nسارة")
    players = [n.strip() for n in names_input.split('\n') if n.strip()]
    
    col1, col2 = st.columns(2)
    with col1: out_count = st.number_input("العدد اللي برا:", 1, max(1, len(players)-1), 1)
    with col2: know_others = st.checkbox("اللي برا يعرفون بعض؟")

    if st.button("ابدأ اللعبة 🔥", use_container_width=True):
        if len(players) < 3: st.error("أدخل 3 لاعبين على الأقل!")
        else:
            for p in players:
                if p not in st.session_state.scores: st.session_state.scores[p] = 0
            
            st.session_state.game_data = {
                "players": players,
                "out_players": random.sample(players, int(out_count)),
                "word": random.choice(DATA[category]),
                "know_others": know_others,
                "votes": {}
            }
            st.session_state.stage = 'distribute'
            st.rerun()

# --- 2. مرحلة توزيع الهاتف (أعطِ الهاتف لـ...) ---
elif st.session_state.stage == 'distribute':
    data = st.session_state.game_data
    idx = st.session_state.current_player_idx
    
    if idx < len(data['players']):
        current_player = data['players'][idx]
        st.markdown(f"""
            <div style='text-align:center; padding:30px; border:3px solid #E74C3C; border-radius:20px; background-color:#f9f9f9;'>
                <h2 style='color:#333;'>📱 أعطِ الهاتف لـ:</h2>
                <h1 style='color:#E74C3C; font-size: 50px;'>{current_player}</h1>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("") # مساحة
        
        if st.button(f"أنا {current_player} (أظهر دوري سرياً)", use_container_width=True):
            if current_player in data['out_players']:
                st.error("🤫 أنت برا السالفة!")
                if data['know_others'] and len(data['out_players']) > 1:
                    others = [p for p in data['out_players'] if p != current_player]
                    st.info(f"شركاؤك اللي برا السالفة هم: {', '.join(others)}")
            else:
                st.success(f"✅ أنت داخل السالفة! الكلمة هي: **{data['word']}**")
            
            if st.button("فهمت، اخفاء المعلومة ➡️"):
                st.session_state.current_player_idx += 1
                st.rerun()
    else:
        # انتهى توزيع الهاتف، ننتقل للنقاش ثم التصويت
        st.session_state.stage = 'voting'
        st.rerun()

# --- 3. مرحلة التصويت ---
elif st.session_state.stage == 'voting':
    data = st.session_state.game_data
    st.subheader("🗳️ مرحلة التصويت (بعد النقاش)")
    
    voters = data['players']
    current_voter_idx = len(data['votes'])
    
    if current_voter_idx < len(voters):
        voter = voters[current_voter_idx]
        st.markdown(f"### دور اللاعب: <span style='color:#E74C3C;'>{voter}</span> ليصوت سرياً", unsafe_allow_html=True)
        target = st.selectbox(f"يا {voter}، من تشك أنه برا السالفة؟", [p for p in voters if p != voter], key=f"v_{voter}")
        
        if st.button(f"تأكيد تصويت {voter}"):
            data['votes'][voter] = target
            st.rerun()
    else:
        # عرض النتائج
        st.header("📊 النتائج النهائية")
        vote_counts = {p: list(data['votes'].values()).count(p) for p in data['players']}
        suspect = max(vote_counts, key=vote_counts.get)
        
        st.write(f"أكثر شخص تم التصويت عليه هو: **{suspect}** بمجموع {vote_counts[suspect]} أصوات.")
        
        if suspect in data['out_players']:
            st.success(f"اجابة صحيحة! **{suspect}** كان فعلاً برا السالفة.")
            st.info(f"الكلمة كانت: **{data['word']}**")
            # توزيع النقاط للداخلين
            for p in data['players']:
                if p not in data['out_players']: st.session_state.scores[p] += 1
        else:
            st.error(f"للأسف! **{suspect}** كان داخل السالفة.")
            st.warning(f"اللي كانوا برا السالفة هم: {', '.join(data['out_players'])}")
            # توزيع النقاط للي برا
            for p in data['out_players']: st.session_state.scores[p] += 2

        if st.button("بدء جولة جديدة 🔄", use_container_width=True):
            st.session_state.stage = 'setup'
            st.rerun()

# تحسين مظهر الأزرار بـ CSS
st.markdown("""
<style>
    .stButton>button { border-radius: 15px; height: 3.5em; font-weight: bold; border: 2px solid #E74C3C; }
    .stButton>button:hover { background-color: #E74C3C; color: white; }
</style>
""", unsafe_allow_html=True)

