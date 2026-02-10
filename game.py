import streamlit as st
import random

# 1. قاعدة البيانات: القوالب، الكلمات، وصورها
categories = {
    "أنمي": {
        "ناروتو": "https://img.viva.ro/wp-content/uploads/2023/10/naruto.jpg",
        "ون بيس": "https://wallpapercave.com/wp/wp1810629.jpg",
        "هجوم العمالقة": "https://wallpapercave.com/wp/wp1916328.jpg"
    },
    "مهن": {
        "طبيب": "https://cdn-icons-png.flaticon.com/512/3774/3774299.png",
        "مهندس": "https://cdn-icons-png.flaticon.com/512/943/943579.png",
        "رائد فضاء": "https://cdn-icons-png.flaticon.com/512/2026/2026521.png"
    },
    "أماكن": {
        "مستشفى": "https://cdn-icons-png.flaticon.com/512/2966/2966327.png",
        "مطار": "https://cdn-icons-png.flaticon.com/512/723/723985.png",
        "مدرسة": "https://cdn-icons-png.flaticon.com/512/167/167707.png"
    },
    "حيوانات": {
        "أسد": "https://cdn-icons-png.flaticon.com/512/616/616412.png",
        "فيل": "https://cdn-icons-png.flaticon.com/512/616/616430.png",
        "زرافة": "https://cdn-icons-png.flaticon.com/512/616/616438.png"
    }
}

# صور ثابتة للحالات الخاصة
IMG_IMPOSTOR = "https://cdn-icons-png.flaticon.com/512/1022/1022334.png" # صورة الجاسوس
IMG_MYSTERY = "https://cdn-icons-png.flaticon.com/512/1022/1022319.png"  # صورة الغموض

st.set_page_config(page_title="برا السالفة برو", layout="centered")
st.title("🕵️ لعبة برا السالفة - النسخة الاحترافية")

# 2. إعدادات اللعبة في الجانب
with st.sidebar:
    st.header("⚙️ الإعدادات")
    category_choice = st.selectbox("اختر القالب:", list(categories.keys()))
    
    player_names_input = st.text_area("أدخل أسماء اللاعبين (اسم في كل سطر):", "أحمد\nسارة\nمحمد")
    player_names = [n.strip() for n in player_names_input.split("\n") if n.strip()]

# 3. منطق اللعبة
if "game_started" not in st.session_state:
    st.session_state.game_started = False

if st.button("🚀 ابدأ اللعبة"):
    if len(player_names) < 3:
        st.error("أدخل 3 أسماء على الأقل!")
    else:
        # اختيار الكلمة والصورة عشوائياً من القالب المختار
        word_list = list(categories[category_choice].keys())
        secret_word = random.choice(word_list)
        secret_image = categories[category_choice][secret_word]
        
        impostor_name = random.choice(player_names)
        
        # تخزين البيانات
        st.session_state.roles = {}
        for name in player_names:
            if name == impostor_name:
                st.session_state.roles[name] = {"word": "أنت برا السالفة!", "img": IMG_IMPOSTOR, "is_impostor": True}
            else:
                st.session_state.roles[name] = {"word": secret_word, "img": secret_image, "is_impostor": False}
        
        st.session_state.player_list = player_names
        st.session_state.current_idx = 0
        st.session_state.game_started = True
        st.session_state.show_card = False

# 4. واجهة عرض الأدوار
if st.session_state.game_started:
    idx = st.session_state.current_idx
    if idx < len(st.session_state.player_list):
        player_name = st.session_state.player_list[idx]
        
        st.divider()
        st.subheader(f"الدور الآن على: {player_name}")
        st.image(IMG_MYSTERY, width=150)
        
        if st.button(f"اكشف البطاقة لـ {player_name}", key=f"btn_{idx}"):
            st.session_state.show_card = True
            
        if st.session_state.show_card:
            role_data = st.session_state.roles[player_name]
            st.image(role_data["img"], width=250)
            
            if role_data["is_impostor"]:
                st.error(role_data["word"])
            else:
                st.success(f"الكلمة هي: {role_data['word']}")
                
            if st.button("فهمت، انتقل للاعب التالي"):
                st.session_state.current_idx += 1
                st.session_state.show_card = False
                st.rerun()
    else:
        st.balloons()
        st.success("✅ الجميع عرف دوره! ابدأوا النقاش الآن.")
        if st.button("لعبة جديدة"):
            st.session_state.game_started = False
            st.rerun()