import html
import json
from pathlib import Path
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="ПСИ-БЛОК",
    page_icon="favicon.jpg",
    layout="wide",
)

# Положи свой логотип рядом с app.py как logo.png
LOGO_PATH = Path(__file__).resolve().parent / "logo.png"


# ---------------------------------------------------------------------
# Декоративный фон с нейронными связями
# ---------------------------------------------------------------------

NEURON_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="800" viewBox="0 0 1000 800">
  <g fill="none" stroke="#4389B5" stroke-opacity="0.13" stroke-width="2">
    <path d="M25 92 L130 145 L225 80 L340 150 L455 70 L565 145 L690 86 L815 155 L955 82"/>
    <path d="M130 145 L175 290 L300 340 L420 250 L565 145"/>
    <path d="M225 80 L245 20"/>
    <path d="M340 150 L325 235 L420 250 L500 360 L635 325 L760 390"/>
    <path d="M455 70 L485 20"/>
    <path d="M565 145 L635 210 L760 170 L815 155"/>
    <path d="M690 86 L710 25"/>
    <path d="M815 155 L860 275 L955 310"/>
    <path d="M175 290 L100 430 L215 510 L300 430 L300 340"/>
    <path d="M420 250 L380 430 L500 520 L635 450 L635 325"/>
    <path d="M760 390 L840 500 L950 455"/>
    <path d="M100 430 L55 600 L180 700 L310 635 L300 520 L215 510"/>
    <path d="M500 520 L455 660 L570 760 L710 675 L635 560 L635 450"/>
    <path d="M840 500 L815 650 L930 735"/>
    <path d="M310 635 L390 760"/>
  </g>
  <g fill="#4389B5" fill-opacity="0.17" stroke="#FFFFFF" stroke-opacity="0.8" stroke-width="3">
    <circle cx="25" cy="92" r="8"/><circle cx="130" cy="145" r="12"/>
    <circle cx="225" cy="80" r="9"/><circle cx="340" cy="150" r="12"/>
    <circle cx="455" cy="70" r="8"/><circle cx="565" cy="145" r="11"/>
    <circle cx="690" cy="86" r="9"/><circle cx="815" cy="155" r="12"/>
    <circle cx="955" cy="82" r="8"/><circle cx="175" cy="290" r="10"/>
    <circle cx="300" cy="340" r="8"/><circle cx="420" cy="250" r="12"/>
    <circle cx="500" cy="360" r="9"/><circle cx="635" cy="325" r="12"/>
    <circle cx="760" cy="390" r="10"/><circle cx="100" cy="430" r="8"/>
    <circle cx="215" cy="510" r="12"/><circle cx="380" cy="430" r="9"/>
    <circle cx="500" cy="520" r="12"/><circle cx="635" cy="450" r="9"/>
    <circle cx="840" cy="500" r="11"/><circle cx="180" cy="700" r="9"/>
    <circle cx="310" cy="635" r="11"/><circle cx="570" cy="760" r="8"/>
    <circle cx="710" cy="675" r="12"/><circle cx="930" cy="735" r="9"/>
  </g>
</svg>
"""

neuron_background = quote(NEURON_SVG, safe="")


# ---------------------------------------------------------------------
# Каталог техник
# ---------------------------------------------------------------------

TECHNIQUES = {
    "decision_tree": {
        "title": "Дерево решений",
        "short": "Разложить сложный выбор на варианты и возможные последствия.",
        "description": "Сценарии, вероятности и оценки удовлетворённости исходом.",
        "keywords": "выбор решение последствия вероятность варианты",
        "category": "Мышление",
    },
    "dbt_chain": {
        "title": "Цепочный анализ поведения (ДБТ)",
        "short": "Исследовать последовательность событий, реакций и последствий.",
        "description": "Уязвимости, звенья цепочки, последствия и точки вмешательства.",
        "keywords": "эмоции поведение дбт реакция событие цепочка",
        "category": "Эмоции",
    },
    "exposure": {
        "title": "Иерархия экспозиции",
        "short": "Составить лестницу ситуаций для постепенной практики.",
        "description": "Прогнозы, уровни тревоги, наблюдения и обучение на опыте.",
        "keywords": "тревога тревожность страх экспозиция ситуации практика",
        "category": "Тревожность",
    },
    "act_matrix": {
        "title": "ACT-матрица",
        "short": "Исследовать действия от дискомфорта и шаги к ценностям.",
        "description": "Карта внутреннего опыта, поведения и выбранных действий.",
        "keywords": "ценности дискомфорт действия мысли осознанность act",
        "category": "Самоосознание",
    },
    "psychodrama": {
        "title": "Психодрама: интерактивная сцена",
        "short": "Разместить образы на сцене, соединить их и дорисовать детали.",
        "description": "Своя библиотека фигур, несколько сцен, связи, рисунки и сохранение проекта.",
        "keywords": "психодрама сцена образы фигуры рисунок связи ассоциации",
        "category": "Самоосознание",
    },
}


# ---------------------------------------------------------------------
# Состояние приложения и навигация
# ---------------------------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_technique" not in st.session_state:
    st.session_state.selected_technique = None

if "page_history" not in st.session_state:
    st.session_state.page_history = []

if "home_search" not in st.session_state:
    st.session_state.home_search = ""

if "library_search" not in st.session_state:
    st.session_state.library_search = ""


def clear_searches():
    st.session_state.home_search = ""
    st.session_state.library_search = ""


def navigate(page, technique_id=None):
    current = {
        "page": st.session_state.page,
        "technique": st.session_state.selected_technique,
    }
    target = {"page": page, "technique": technique_id}

    if current != target:
        st.session_state.page_history.append(current)
        st.session_state.page_history = st.session_state.page_history[-30:]

    st.session_state.page = page
    st.session_state.selected_technique = technique_id


def go_home():
    clear_searches()
    navigate("home")


def go_library():
    clear_searches()
    navigate("library")


def go_about():
    clear_searches()
    navigate("about")


def go_back():
    clear_searches()
    if st.session_state.page_history:
        previous = st.session_state.page_history.pop()
        st.session_state.page = previous["page"]
        st.session_state.selected_technique = previous["technique"]
    else:
        st.session_state.page = "home"
        st.session_state.selected_technique = None


def open_technique(technique_id):
    navigate("technique", technique_id)


def search_techniques(query):
    query = " ".join((query or "").casefold().split())
    if not query:
        return list(TECHNIQUES.items())

    words = query.split()
    results = []

    for technique_id, technique in TECHNIQUES.items():
        searchable = " ".join(
            [
                technique["title"],
                technique["short"],
                technique["description"],
                technique["keywords"],
                technique["category"],
            ]
        ).casefold()

        if all(word in searchable for word in words):
            results.append((technique_id, technique))

    return results


# ---------------------------------------------------------------------
# Стили сайта
# ---------------------------------------------------------------------

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&display=swap');

    :root {{
        color-scheme: light !important;
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        color-scheme: light !important;
        background-color: #F3F9FD !important;
        color: #294A65 !important;
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background-image:
            radial-gradient(ellipse at 10% 5%, rgba(196,228,248,.58), transparent 34%),
            radial-gradient(ellipse at 92% 18%, rgba(219,239,251,.68), transparent 36%);
    }}

    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        opacity: .56;
        background-image: url("data:image/svg+xml,{neuron_background}");
        background-repeat: repeat;
        background-size: 1000px 800px;
        background-position: left top;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        position: relative;
        z-index: 1;
    }}

    [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    .block-container {{
        max-width: 1160px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }}

    h1, h2, h3, h4, p, label, button, input, textarea, select {{
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    h1, h2, h3, h4 {{
        color: #294A65 !important;
        letter-spacing: -0.025em;
    }}

    h1 {{ font-size: 2.5rem !important; font-weight: 800 !important; }}
    h2 {{ font-size: 1.8rem !important; font-weight: 800 !important; }}
    h3 {{ font-size: 1.25rem !important; font-weight: 800 !important; }}

    p, label, [data-testid="stCaptionContainer"], [data-testid="stMarkdownContainer"] {{
        color: #476B85 !important;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        border: 1px solid #C9DFEF !important;
        border-radius: 18px !important;
        background: rgba(248,252,255,.94) !important;
        box-shadow: 0 8px 22px rgba(62,112,148,.06);
    }}

    [data-testid="stTextInput"] [data-baseweb="input"],
    [data-testid="stTextArea"] [data-baseweb="textarea"],
    [data-testid="stNumberInput"] [data-baseweb="input"],
    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-baseweb="input"],
    [data-baseweb="textarea"] {{
        color-scheme: light !important;
        background: #FFFFFF !important;
        border: 1px solid #C9DDEB !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }}

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] input,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {{
        color: #294A65 !important;
        background: #FFFFFF !important;
        -webkit-text-fill-color: #294A65 !important;
        border: 0 !important;
        box-shadow: none !important;
        outline: none !important;
        caret-color: #315773 !important;
    }}

    input::placeholder,
    textarea::placeholder {{
        color: #7893A8 !important;
        -webkit-text-fill-color: #7893A8 !important;
        opacity: 1 !important;
    }}

    .stButton > button {{
        min-height: 44px;
        border: 1px solid #AFCFE2 !important;
        border-radius: 13px !important;
        background: #F1F8FD !important;
        color: #315773 !important;
        font-size: .98rem;
        font-weight: 700;
        transition: .18s ease;
    }}

    .stButton > button:hover:not(:disabled) {{
        border-color: #6EA7CB !important;
        background: #E0F0FA !important;
        color: #234D6B !important;
        transform: translateY(-1px);
    }}

    .stButton > button:disabled {{
        opacity: .45;
    }}

    .stButton > button[kind="primary"] {{
        min-height: 50px;
        border: 1px solid #6EA7CB !important;
        border-radius: 14px !important;
        background: linear-gradient(135deg, #D9EEFA, #E5F3FC) !important;
        color: #234D6B !important;
        font-weight: 800;
    }}

    [data-testid="stAlert"] {{
        border: 1px solid #BCD9EB !important;
        border-radius: 14px !important;
        background: #EAF5FC !important;
    }}

    [data-testid="stMetric"] {{
        border: 1px solid #C9DFEF;
        border-radius: 16px;
        background: rgba(248,252,255,.96);
        padding: 14px;
    }}

    hr {{
        border-color: #D7E6F0 !important;
    }}

    .brand-name {{
        color: #234D6B;
        font-size: clamp(1.7rem, 3vw, 2.25rem);
        font-weight: 800;
        line-height: 1.05;
        letter-spacing: -.045em;
        white-space: nowrap;
    }}

    .brand-fallback {{
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #BBD9EB;
        border-radius: 12px;
        background: rgba(255,255,255,.65);
    }}

    .hero {{
        position: relative;
        display: flex;
        align-items: center;
        min-height: 340px;
        overflow: hidden;
        padding: 38px 44px;
        margin: 20px 0 22px;
        border: 1px solid #D3E5F2;
        border-radius: 28px;
        background:
            radial-gradient(circle at 79% 42%, rgba(174,222,241,.66) 0 18%, transparent 18.5%),
            linear-gradient(110deg, #F8FCFF 0%, #EAF5FC 100%);
    }}

    .hero-copy {{
        position: relative;
        z-index: 1;
        max-width: 530px;
    }}

    .hero-title {{
        margin: 0;
        color: #214D6C;
        font-size: clamp(2.8rem, 6vw, 4.3rem);
        font-weight: 800;
        line-height: 1.04;
        letter-spacing: -.05em;
    }}

    .hero-subtitle {{
        max-width: 490px;
        margin: 12px 0 18px;
        color: #294A65;
        font-size: clamp(1.25rem, 2.5vw, 1.85rem);
        font-weight: 700;
        line-height: 1.3;
    }}

    .hero-description {{
        max-width: 460px;
        color: #476B85;
        font-size: 1.05rem;
        line-height: 1.6;
    }}

    .hero-art {{
        position: absolute;
        top: 50%;
        right: 3%;
        width: min(42%, 430px);
        transform: translateY(-50%);
        opacity: .78;
    }}

    .section-title {{
        margin: 28px 0 12px;
        color: #294A65;
        font-size: 1.7rem;
        font-weight: 800;
    }}

    .category-card {{
        min-height: 125px;
        padding: 17px;
        border: 1px solid #D3E3EF;
        border-radius: 18px;
        background: rgba(248,252,255,.94);
    }}

    .category-title {{
        color: #294A65;
        font-size: 1.04rem;
        font-weight: 800;
    }}

    .category-description {{
        margin-top: 7px;
        color: #648198;
        font-size: .9rem;
        line-height: 1.45;
    }}

    @media (max-width: 700px) {{
        .hero {{ min-height: 290px; padding: 25px 22px; }}
        .hero-art {{ right: -10%; width: 58%; opacity: .2; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Шапка и карточки техник
# ---------------------------------------------------------------------

def render_header():
    brand_col, home_col, library_col, about_col, back_col = st.columns(
        [2.3, 1, 1.25, 1.1, 1]
    )

    with brand_col:
        logo_col, name_col = st.columns([0.6, 3.4])

        with logo_col:
            if LOGO_PATH.is_file():
                st.image(str(LOGO_PATH), width=42)
            else:
                st.markdown(
                    """
                    <div class="brand-fallback">
                      <svg width="30" height="30" viewBox="0 0 30 30"
                           xmlns="http://www.w3.org/2000/svg">
                        <g fill="none" stroke="#315773" stroke-width="1.5"
                           stroke-linecap="round">
                          <path d="M14.8 5.2c-4-3-8 0-7.5 4-3.8 1.3-3.4 6.1-.3 7.4-2.2 3.2.3 6.5 3.7 5.1 1.3 3 4.5 2.6 5.3.2"/>
                          <path d="M15.2 5.2c4-3 8 0 7.5 4 3.8 1.3 3.4 6.1.3 7.4 2.2 3.2-.3 6.5-3.7 5.1-1.3 3-4.5 2.6-5.3.2"/>
                          <path d="M15 5v17M9 10c2 0 3 1 3 3m-5 3c2-.5 4 .5 4 2m10-8c-2 0-3 1-3 3m5 3c-2-.5-4 .5-4 2"/>
                        </g>
                      </svg>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with name_col:
            st.markdown(
                '<div class="brand-name">ПСИ-БЛОК</div>',
                unsafe_allow_html=True,
            )

    with home_col:
        st.button(
            "Главная",
            key="header_home",
            on_click=go_home,
            use_container_width=True,
        )

    with library_col:
        st.button(
            "Библиотека",
            key="header_library",
            on_click=go_library,
            use_container_width=True,
        )

    with about_col:
        st.button(
            "О проекте",
            key="header_about",
            on_click=go_about,
            use_container_width=True,
        )

    with back_col:
        st.button(
            "Назад",
            key="header_back",
            on_click=go_back,
            disabled=not st.session_state.page_history,
            use_container_width=True,
        )


def render_technique_cards(items, key_prefix):
    if not items:
        st.info("Ничего не найдено. Попробуйте изменить поисковый запрос.")
        return

    for start in range(0, len(items), 2):
        columns = st.columns(2)

        for column, (technique_id, technique) in zip(
            columns,
            items[start : start + 2],
        ):
            with column:
                with st.container(border=True):
                    st.markdown(f"### {technique['title']}")
                    st.write(technique["short"])
                    st.caption(
                        f"{technique['category']} · {technique['description']}"
                    )
                    st.button(
                        "Открыть",
                        key=f"{key_prefix}_{technique_id}",
                        on_click=open_technique,
                        args=(technique_id,),
                        use_container_width=True,
                    )


# ---------------------------------------------------------------------
# Главная страница
# ---------------------------------------------------------------------

def render_home():
    st.markdown(
        """
        <section class="hero">
          <div class="hero-copy">
            <h1 class="hero-title">ПСИ-БЛОК</h1>
            <div class="hero-subtitle">
              Инструменты для глубокой психологической работы
            </div>
            <div class="hero-description">
              Библиотека психологических техник для специалистов и клиентов.
              Выбирайте инструмент и исследуйте важные вопросы в удобном темпе.
            </div>
          </div>

          <div class="hero-art" aria-hidden="true">
            <svg viewBox="0 0 440 300" xmlns="http://www.w3.org/2000/svg">
              <path d="M225 18 C155 8 100 48 89 108 C81 151 99 180 72 204
                       C61 214 48 225 51 234 C55 244 73 246 82 250
                       C89 254 85 265 94 269 C105 275 119 269 126 282
                       C132 294 154 296 176 289 L225 278"
                    fill="none" stroke="#5B87A2" stroke-width="3"
                    stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M222 22 C292 17 347 55 356 113 C362 154 343 185 373 212
                       C390 228 412 233 411 244 C410 254 390 260 382 270
                       C374 280 362 291 341 289 L226 278"
                    fill="none" stroke="#5B87A2" stroke-width="3"
                    stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M223 54 C194 33 163 47 162 72 C133 75 132 108 154 119
                       C139 141 159 162 181 156 C188 179 215 178 226 160
                       C240 180 267 173 271 151 C297 151 305 124 287 108
                       C300 84 281 60 258 64 C251 47 236 46 223 54Z"
                    fill="none" stroke="#5B87A2" stroke-width="2.5"
                    stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M222 55 L222 159
                       M162 73 C183 83 187 101 181 117
                       M258 64 C242 79 242 96 254 109
                       M154 119 C174 117 187 127 181 156
                       M287 108 C264 111 253 127 271 151
                       M188 78 C204 88 206 105 196 119
                       M239 78 C222 90 223 108 239 118
                       M201 140 C212 130 225 131 234 143"
                    fill="none" stroke="#5B87A2" stroke-width="2"
                    stroke-linecap="round"/>
              <ellipse cx="224" cy="150" rx="190" ry="76"
                       transform="rotate(-12 224 150)"
                       fill="none" stroke="#76A6C0" stroke-width="2"/>
            </svg>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    action_col, about_col, _ = st.columns([1.7, 1.2, 3.5])

    with action_col:
        st.button(
            "Перейти в библиотеку",
            key="home_library_button",
            type="primary",
            on_click=go_library,
            use_container_width=True,
        )

    with about_col:
        st.button(
            "Узнать больше",
            key="home_about_button",
            on_click=go_about,
            use_container_width=True,
        )

    st.markdown(
        '<div class="section-title">Найти технику</div>',
        unsafe_allow_html=True,
    )

    query = st.text_input(
        "Поиск по техникам",
        key="home_search",
        placeholder="Например: тревожность, самооценка, выбор...",
        label_visibility="collapsed",
    )

    if query.strip():
        st.markdown("#### Результаты поиска")
        render_technique_cards(
            search_techniques(query),
            "home_search_result",
        )
        return

    st.markdown(
        '<div class="section-title">Исследуйте библиотеку</div>',
        unsafe_allow_html=True,
    )

    categories = [
        ("Эмоции", "Работа с эмоциональными состояниями"),
        ("Коммуникация", "Взаимодействие и отношения"),
        ("Самооценка", "Образ себя и личные границы"),
        ("Мышление", "Убеждения и автоматические мысли"),
    ]

    category_columns = st.columns(4)
    for column, (title, description) in zip(category_columns, categories):
        with column:
            st.markdown(
                f"""
                <div class="category-card">
                    <div class="category-title">{title}</div>
                    <div class="category-description">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">Популярные инструменты</div>',
        unsafe_allow_html=True,
    )
    render_technique_cards(list(TECHNIQUES.items())[:2], "home_featured")

    st.markdown(
        '<div class="section-title">ПСИ-БЛОК — ваш помощник</div>',
        unsafe_allow_html=True,
    )
    st.info(
        "Инструменты помогают структурировать совместную работу и обсуждение. "
        "Они не заменяют профессиональную психологическую помощь."
    )


# ---------------------------------------------------------------------
# Библиотека и раздел «О проекте»
# ---------------------------------------------------------------------

def render_library():
    st.title("Библиотека техник")
    st.write("Ищите по названию, теме или описанию техники.")

    query = st.text_input(
        "Поиск по библиотеке",
        key="library_search",
        placeholder="Например: тревожность, поведение, выбор...",
        label_visibility="collapsed",
    )

    render_technique_cards(
        search_techniques(query),
        "library_result",
    )


def render_about():
    st.title("О проекте")
    st.markdown(
        """
        **ПСИ-БЛОК** — библиотека интерактивных инструментов
        для психологических консультаций. Она помогает специалисту
        и клиенту совместно структурировать обсуждение и фиксировать идеи.
        """
    )

    st.divider()
    st.subheader("Команда разработчиков")

    developers = [
        {
            "name": "Артём Черемкин",
            "role": "Разработчик сайта, практикующий психолог",
            "photo": "developer1.jpg",
        },
        {
            "name": "Анна Пыжьянова",
            "role": "Практикующий психолог",
            "photo": "developer2.jpg",
        },
        {
            "name": "Ферузахон Сайдазимова",
            "role": "Практикующий психолог",
            "photo": "developer3.jpg",
        },
    ]

    columns = st.columns(3)
    app_dir = Path(__file__).resolve().parent

    for column, person in zip(columns, developers):
        with column:
            with st.container(border=True):
                photo_path = app_dir / person["photo"]
                if photo_path.is_file():
                    st.image(str(photo_path), use_container_width=True)
                else:
                    st.markdown(
                        """
                        <div style="
                            height:220px;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            border-radius:14px;
                            background:linear-gradient(135deg,#DDEFFA,#F2F8FC);
                            color:#5F86A0;">
                            Фото разработчика
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(f"**{html.escape(person['name'])}**")
                st.caption(person["role"])

# ---------------------------------------------------------------------
# Общие функции визуализации
# ---------------------------------------------------------------------

SVG_COLORS = {
    "ink": "#234D6B",
    "text": "#476B85",
    "line": "#80AFCB",
    "border": "#B9D9EB",
    "panel": "#F7FBFF",
    "pale": "#E7F3FB",
    "white": "#FFFFFF",
    "accent": "#D9EEFA",
}


def svg_text(
    x,
    y,
    value,
    size=15,
    weight=400,
    color=None,
    max_chars=48,
    max_lines=3,
):
    text = " ".join(str(value or "—").split())
    words = text.split()
    lines = []
    line = ""

    for word in words:
        candidate = f"{line} {word}".strip()
        if len(candidate) > max_chars and line:
            lines.append(line)
            line = word
        else:
            line = candidate

    if line:
        lines.append(line)

    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: max_chars - 1] + "…"

    color = color or SVG_COLORS["text"]
    tspans = []

    for index, item in enumerate(lines):
        dy = 0 if index == 0 else size + 4
        tspans.append(
            f'<tspan x="{x}" dy="{dy}">{html.escape(item)}</tspan>'
        )

    return (
        f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}">'
        f'{"".join(tspans)}</text>'
    )


def make_svg(width, height, title, body, accent="#D9EEFA"):
    gradient_id = f"bgGrad_{accent.replace('#', '')}"
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{width}" height="{height}"
         viewBox="0 0 {width} {height}">
      <defs>
        <linearGradient id="{gradient_id}" x1="0%" x2="100%" y1="0%" y2="100%">
          <stop offset="0%" stop-color="#F8FCFF"/>
          <stop offset="100%" stop-color="#EAF5FC"/>
        </linearGradient>
        <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#7AAEC7" flood-opacity="0.16"/>
        </filter>
      </defs>
      <rect width="100%" height="100%" fill="url(#{gradient_id})" rx="18"/>
      <g opacity="0.18">
        <path d="M0 200 L120 150 L200 220 L320 180 L520 250" stroke="#8BBDDB" fill="none" stroke-width="1.5"/>
        <path d="M140 540 L310 450 L470 520 L700 430 L860 520" stroke="#8BBDDB" fill="none" stroke-width="1.5"/>
      </g>
      {svg_text(
          32, 45, title, size=25, weight=700,
          color=SVG_COLORS["ink"], max_chars=80, max_lines=1
      )}
      <g id="scene" filter="url(#softShadow)">{body}</g>
    </svg>
    """


def render_visualization(svg, filename, caption):
    st.subheader("Визуализация")
    st.caption(caption)

    svg_name = json.dumps(filename)
    png_name = json.dumps(filename.rsplit(".", 1)[0] + ".png")

    html_doc = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        * {{ box-sizing: border-box; }}
        html, body {{
          margin: 0;
          padding: 0;
          font: 14px Arial, sans-serif;
          color: #234D6B;
        }}
        body {{
          user-select: none;
          -webkit-user-select: none;
        }}
        .toolbar {{
          display: flex;
          gap: 8px;
          align-items: center;
          flex-wrap: wrap;
          padding: 8px;
          background: #F3F9FD;
          border: 1px solid #D4E6F2;
          border-radius: 12px 12px 0 0;
        }}
        button {{
          border: 1px solid #AFCFE2;
          border-radius: 8px;
          background: #FFFFFF;
          color: #315773;
          padding: 7px 11px;
          cursor: pointer;
          font-weight: 600;
        }}
        #zoom-label {{
          min-width: 48px;
          text-align: center;
        }}
        .viewport {{
          width: 100%;
          height: 520px;
          overflow: auto;
          border: 1px solid #D4E6F2;
          border-top: 0;
          border-radius: 0 0 12px 12px;
          background: #FFFFFF;
          cursor: grab;
          touch-action: none;
        }}
        .viewport.dragging {{ cursor: grabbing; }}
        .viewport svg {{
          display: block;
          max-width: none !important;
          height: auto;
          flex: none;
          user-select: none;
          -webkit-user-select: none;
        }}
        .viewport svg text {{
          user-select: none;
          -webkit-user-select: none;
          pointer-events: none;
        }}
        @media (max-width: 700px) {{
          .viewport {{ height: 430px; }}
        }}
      </style>
    </head>
    <body>
      <div class="toolbar">
        <button id="minus" type="button" aria-label="Уменьшить">−</button>
        <button id="plus" type="button" aria-label="Увеличить">+</button>
        <button id="reset" type="button">Сбросить вид</button>
        <span id="zoom-label">100%</span>
        <button id="save-svg" type="button">Скачать SVG</button>
        <button id="save-png" type="button">Скачать PNG</button>
      </div>
      <div class="viewport" id="viewport">{svg}</div>

      <script>
        (() => {{
          const viewport = document.getElementById("viewport");
          const svg = viewport.querySelector("svg");
          const label = document.getElementById("zoom-label");
          if (!svg) return;

          const baseWidth = Number(svg.getAttribute("width"));
          const baseHeight = Number(svg.getAttribute("height"));
          let scale = 1;
          let drag = null;

          function applyScale() {{
            svg.style.width = (baseWidth * scale) + "px";
            svg.style.height = (baseHeight * scale) + "px";
            label.textContent = Math.round(scale * 100) + "%";
          }}

          function fitToViewport() {{
            const availableWidth = Math.max(320, viewport.clientWidth - 8);
            scale = Math.min(1, availableWidth / baseWidth);
            applyScale();
          }}

          document.getElementById("plus").onclick = () => {{
            scale = Math.min(3, scale * 1.2);
            applyScale();
          }};

          document.getElementById("minus").onclick = () => {{
            scale = Math.max(0.35, scale / 1.2);
            applyScale();
          }};

          document.getElementById("reset").onclick = () => {{
            fitToViewport();
            viewport.scrollTo({{left: 0, top: 0}});
          }};

          viewport.addEventListener("pointerdown", (event) => {{
            if (event.target.closest("button")) return;
            drag = {{
              x: event.clientX,
              y: event.clientY,
              left: viewport.scrollLeft,
              top: viewport.scrollTop
            }};
            viewport.classList.add("dragging");
            viewport.setPointerCapture(event.pointerId);
          }});

          viewport.addEventListener("pointermove", (event) => {{
            if (!drag) return;
            viewport.scrollLeft = drag.left - (event.clientX - drag.x);
            viewport.scrollTop = drag.top - (event.clientY - drag.y);
          }});

          function endDrag() {{
            drag = null;
            viewport.classList.remove("dragging");
          }}

          viewport.addEventListener("pointerup", endDrag);
          viewport.addEventListener("pointercancel", endDrag);

          viewport.addEventListener("wheel", (event) => {{
            if (!event.ctrlKey && !event.metaKey) return;
            event.preventDefault();
            scale = Math.max(
              0.35,
              Math.min(3, scale * (event.deltaY < 0 ? 1.1 : 0.9))
            );
            applyScale();
          }}, {{passive: false}});

          function serializeSvg() {{
            const clone = svg.cloneNode(true);
            clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
            clone.style.width = "";
            clone.style.height = "";
            return new XMLSerializer().serializeToString(clone);
          }}

          function download(blob, name) {{
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = name;
            link.click();
            setTimeout(() => URL.revokeObjectURL(url), 1000);
          }}

          document.getElementById("save-svg").onclick = () => {{
            download(
              new Blob([serializeSvg()], {{
                type: "image/svg+xml;charset=utf-8"
              }}),
              {svg_name}
            );
          }};

          document.getElementById("save-png").onclick = () => {{
            const url = URL.createObjectURL(
              new Blob([serializeSvg()], {{
                type: "image/svg+xml;charset=utf-8"
              }})
            );
            const image = new Image();

            image.onload = () => {{
              const canvas = document.createElement("canvas");
              canvas.width = baseWidth * 2;
              canvas.height = baseHeight * 2;
              const context = canvas.getContext("2d");
              context.fillStyle = "#F7FBFF";
              context.fillRect(0, 0, canvas.width, canvas.height);
              context.drawImage(image, 0, 0, canvas.width, canvas.height);
              canvas.toBlob((blob) => {{
                if (blob) download(blob, {png_name});
                URL.revokeObjectURL(url);
              }}, "image/png");
            }};

            image.onerror = () => URL.revokeObjectURL(url);
            image.src = url;
          }};

          fitToViewport();
          window.addEventListener("resize", fitToViewport);
        }})();
      </script>
    </body>
    </html>
    """

    components.html(html_doc, height=590, scrolling=False)


# ---------------------------------------------------------------------
# Дерево решений
# ---------------------------------------------------------------------

def add_decision_option():
    existing = list(st.session_state.get("decision_option_ids", [0, 1]))
    next_id = int(st.session_state.get("decision_next_option_id", 2))
    existing.append(next_id)
    st.session_state.decision_option_ids = existing
    st.session_state.decision_next_option_id = next_id + 1
    st.session_state[f"decision_scenario_ids_{next_id}"] = [0]
    st.session_state[f"decision_next_scenario_id_{next_id}"] = 1


def remove_decision_option(option_id):
    ids = list(st.session_state.get("decision_option_ids", [0, 1]))
    if len(ids) > 2 and option_id in ids:
        ids.remove(option_id)
        st.session_state.decision_option_ids = ids
        st.session_state.pop(f"decision_scenario_ids_{option_id}", None)
        st.session_state.pop(f"decision_next_scenario_id_{option_id}", None)


def add_decision_scenario(option_id):
    key = f"decision_scenario_ids_{option_id}"
    ids = list(st.session_state.get(key, [0]))
    next_id = int(st.session_state.get(f"decision_next_scenario_id_{option_id}", 1))
    ids.append(next_id)
    st.session_state[key] = ids
    st.session_state[f"decision_next_scenario_id_{option_id}"] = next_id + 1


def remove_decision_scenario(option_id, scenario_id):
    key = f"decision_scenario_ids_{option_id}"
    ids = list(st.session_state.get(key, [0]))
    if len(ids) > 1 and scenario_id in ids:
        ids.remove(scenario_id)
        st.session_state[key] = ids


def color_for_satisfaction(value):
    if value > 0:
        return "#237A5B"
    if value < 0:
        return "#B94E49"
    return "#496C86"


def render_decision_tree():
    st.title("Дерево решений")
    st.write(
        "Опишите варианты решения, возможные сценарии и удовлетворённость "
        "каждым исходом."
    )
    st.caption(
        "Вероятности сценариев внутри каждого варианта должны составлять "
        "100%. Удовлетворённость оценивается по шкале от −5 до +5."
    )

    question = st.text_input(
        "Какое решение нужно принять?",
        key="decision_question",
        placeholder="Например: Стоит ли менять работу?",
    )

    if "decision_option_ids" not in st.session_state:
        st.session_state.decision_option_ids = [0, 1]
        st.session_state.decision_next_option_id = 2

    option_ids = list(st.session_state.decision_option_ids)
    options = []

    for option_number, option_id in enumerate(option_ids, start=1):
        scenario_key = f"decision_scenario_ids_{option_id}"
        if scenario_key not in st.session_state:
            st.session_state[scenario_key] = [0]
            st.session_state[f"decision_next_scenario_id_{option_id}"] = 1

        scenario_ids = list(st.session_state[scenario_key])

        with st.container(border=True):
            option_header, option_delete = st.columns([5, 1])
            with option_header:
                st.markdown(f"### Вариант {option_number}")

            with option_delete:
                if len(option_ids) > 2:
                    st.button(
                        "Удалить вариант",
                        key=f"decision_remove_option_{option_id}",
                        on_click=remove_decision_option,
                        args=(option_id,),
                        help="Удалить этот вариант и его сценарии",
                    )

            option_name = st.text_input(
                "Название варианта",
                key=f"decision_name_{option_id}",
                placeholder=f"Вариант {option_number}",
            )

            scenarios = []
            for scenario_number, scenario_id in enumerate(
                scenario_ids, start=1
            ):
                with st.expander(
                    f"Сценарий {scenario_number}",
                    expanded=(scenario_number == 1),
                ):
                    scenario_title = st.text_input(
                        "Название сценария",
                        key=f"decision_scenario_title_{option_id}_{scenario_id}",
                        placeholder="Например: адаптация проходит успешно",
                    )
                    scenario_outcome = st.text_area(
                        "Что может произойти?",
                        key=f"decision_scenario_outcome_{option_id}_{scenario_id}",
                    )
                    scenario_probability = st.slider(
                        "Вероятность, %",
                        min_value=0,
                        max_value=100,
                        value=100 if len(scenario_ids) == 1 else 0,
                        key=f"decision_scenario_probability_{option_id}_{scenario_id}",
                    )
                    scenario_satisfaction = st.slider(
                        "Удовлетворённость исходом",
                        min_value=-5.0,
                        max_value=5.0,
                        value=0.0,
                        step=0.5,
                        key=f"decision_scenario_satisfaction_{option_id}_{scenario_id}",
                    )

                    if len(scenario_ids) > 1:
                        st.button(
                            "Удалить этот сценарий",
                            key=f"decision_remove_scenario_{option_id}_{scenario_id}",
                            on_click=remove_decision_scenario,
                            args=(option_id, scenario_id),
                        )

                    scenarios.append(
                        {
                            "title": scenario_title,
                            "outcome": scenario_outcome,
                            "probability": scenario_probability,
                            "satisfaction": scenario_satisfaction,
                        }
                    )

            probability_total = sum(
                scenario["probability"] for scenario in scenarios
            )

            st.caption(f"Сумма вероятностей сценариев: {probability_total}%")

            if probability_total != 100:
                st.warning(
                    "Для расчёта сумма вероятностей сценариев этого варианта "
                    "должна составлять 100%."
                )

            if len(scenario_ids) < 8:
                st.button(
                    "＋ Добавить сценарий",
                    key=f"decision_add_scenario_{option_id}",
                    on_click=add_decision_scenario,
                    args=(option_id,),
                )

            options.append(
                {
                    "id": option_id,
                    "name": option_name,
                    "scenarios": scenarios,
                    "probability_total": probability_total,
                }
            )

    if len(option_ids) < 5:
        st.button(
            "＋ Добавить вариант",
            key="decision_add_option",
            on_click=add_decision_option,
        )

    ready = (
        bool(question.strip())
        and all(option["name"].strip() for option in options)
        and all(option["probability_total"] == 100 for option in options)
        and all(
            scenario["title"].strip()
            for option in options
            for scenario in option["scenarios"]
        )
    )

    if not ready:
        st.info(
            "Заполните вопрос, названия вариантов и сценариев. "
            "Для каждого варианта распределите вероятности так, чтобы "
            "их сумма была 100%. Сравнение обновится автоматически."
        )
        return

    for option in options:
        option["expected"] = sum(
            scenario["probability"] * scenario["satisfaction"]
            for scenario in option["scenarios"]
        ) / 100

    best_score = max(option["expected"] for option in options)
    best_option_ids = {
        option["id"]
        for option in options
        if abs(option["expected"] - best_score) < 1e-9
    }

    st.subheader("Сравнение вариантов")
    metric_columns = st.columns(len(options))

    for column, option in zip(metric_columns, options):
        with column:
            st.metric(
                option["name"],
                f'{option["expected"]:.2f} / 5',
                help="Средняя удовлетворённость с учётом вероятностей сценариев.",
            )
            if option["id"] in best_option_ids:
                st.success("Наиболее подходящий по введённым оценкам")

    st.info(
        "Расчёт — ориентир по вашим оценкам и вероятностям, "
        "а не решение за вас."
    )

    palette = {
        "root_fill": "#D8ECFA",
        "root_border": "#397EA5",
        "branch": "#86B5CE",
        "option_fill": "#E8F6FF",
        "option_border": "#75B4D5",
        "best_fill": "#DDF3E7",
        "best_border": "#45A779",
        "scenario_fill": "#FFFFFF",
        "scenario_border": "#BBD9E9",
        "text": "#244E69",
        "muted": "#496F87",
    }

    column_width = 440
    scenario_height = 142
    max_scenarios = max(len(option["scenarios"]) for option in options)
    chart_width = 50 + len(options) * column_width
    option_y = 120 + max_scenarios * scenario_height
    root_y = option_y + 132
    chart_height = root_y + 120
    body = ""

    for index, option in enumerate(options):
        x = 25 + index * column_width
        card_x = x + 48
        card_width = 360
        branch_x = x + 24
        centers = [
            92 + scenario_index * scenario_height + 56
            for scenario_index in range(len(option["scenarios"]))
        ]

        if centers:
            body += (
                f'<line x1="{branch_x}" y1="{min(centers)}" '
                f'x2="{branch_x}" y2="{option_y}" '
                f'stroke="{palette["branch"]}" stroke-width="3"/>'
            )
            for center_y in centers:
                body += (
                    f'<line x1="{branch_x}" y1="{center_y}" '
                    f'x2="{card_x}" y2="{center_y}" '
                    f'stroke="{palette["branch"]}" stroke-width="3"/>'
                )

        body += (
            f'<line x1="{card_x + card_width / 2}" y1="{option_y + 78}" '
            f'x2="{chart_width / 2}" y2="{root_y}" '
            f'stroke="{palette["branch"]}" stroke-width="3"/>'
        )

    for index, option in enumerate(options):
        x = 25 + index * column_width
        card_x = x + 48
        card_width = 360

        for scenario_index, scenario in enumerate(option["scenarios"]):
            y = 92 + scenario_index * scenario_height
            body += (
                f'<rect x="{card_x}" y="{y}" width="{card_width}" '
                f'height="112" rx="15" fill="{palette["scenario_fill"]}" '
                f'stroke="{palette["scenario_border"]}" stroke-width="2"/>'
            )
            body += svg_text(
                card_x + 16,
                y + 29,
                scenario["title"],
                size=17,
                weight=700,
                color=palette["text"],
                max_chars=38,
                max_lines=1,
            )
            body += svg_text(
                card_x + 16,
                y + 57,
                f'Вероятность {scenario["probability"]}% · '
                f'удовлетворённость {scenario["satisfaction"]:+.1f}',
                size=14,
                color=color_for_satisfaction(scenario["satisfaction"]),
                max_chars=42,
                max_lines=1,
            )
            body += svg_text(
                card_x + 16,
                y + 85,
                scenario["outcome"],
                size=14,
                color=palette["muted"],
                max_chars=40,
                max_lines=2,
            )

        is_best = option["id"] in best_option_ids
        fill = palette["best_fill"] if is_best else palette["option_fill"]
        border = palette["best_border"] if is_best else palette["option_border"]
        title = f'★ {option["name"]}' if is_best else option["name"]

        body += (
            f'<rect x="{card_x}" y="{option_y}" width="{card_width}" '
            f'height="78" rx="16" fill="{fill}" '
            f'stroke="{border}" stroke-width="2.5"/>'
        )
        body += svg_text(
            card_x + 16,
            option_y + 30,
            title,
            size=18,
            weight=700,
            color=palette["text"],
            max_chars=38,
            max_lines=1,
        )
        body += svg_text(
            card_x + 16,
            option_y + 59,
            f'Ожидаемая удовлетворённость: {option["expected"]:.2f}',
            size=14,
            color=palette["muted"],
            max_chars=42,
            max_lines=1,
        )

    root_width = min(600, chart_width - 60)
    root_x = (chart_width - root_width) / 2

    body += (
        f'<rect x="{root_x}" y="{root_y}" width="{root_width}" '
        f'height="78" rx="18" fill="{palette["root_fill"]}" '
        f'stroke="{palette["root_border"]}" stroke-width="2.5"/>'
    )
    body += svg_text(
        root_x + 20,
        root_y + 31,
        "Решение",
        size=19,
        weight=700,
        color=palette["text"],
        max_chars=60,
        max_lines=1,
    )
    body += svg_text(
        root_x + 20,
        root_y + 60,
        question,
        size=16,
        color=palette["muted"],
        max_chars=66,
        max_lines=1,
    )

    svg = make_svg(
        chart_width,
        chart_height,
        "Дерево решений",
        body,
        accent="#CFE9F6",
    )
    render_visualization(
        svg,
        "decision_tree.svg",
        "Схема читается снизу вверх: решение → варианты → сценарии. "
        "Зелёным отмечен вариант с наибольшей взвешенной оценкой.",
    )


# ---------------------------------------------------------------------
# Цепочный анализ поведения (ДБТ)
# ---------------------------------------------------------------------

def render_chain():
    st.title("Цепочный анализ поведения (ДБТ)")
    st.write(
        "Восстановите провоцирующее событие, последовательность звеньев, "
        "последствия и возможные места для навыков или поддержки."
    )
    st.info(
        "Можно пропустить поле или остановиться в любой момент. "
        "Если есть непосредственная опасность для вас или другого человека, "
        "обратитесь за срочной помощью к местным службам или специалисту."
    )

    vulnerability = st.text_area(
        "Факторы уязвимости",
        key="chain_vulnerability",
        placeholder="Например: недосып, стресс, боль, конфликт",
    )
    trigger = st.text_area(
        "Провоцирующее событие",
        key="chain_trigger",
        placeholder="Последнее событие, запустившее последовательность",
    )
    target = st.text_area(
        "Проблемное поведение, которое анализируем",
        key="chain_target",
        placeholder="Опишите конкретно, что произошло, без оценочных ярлыков",
    )

    link_count = int(
        st.number_input(
            "Количество звеньев цепочки",
            min_value=1,
            max_value=8,
            value=4,
            step=1,
            key="chain_link_count",
        )
    )

    links = []
    for index in range(link_count):
        with st.expander(
            f"Звено {index + 1}: что произошло дальше?",
            expanded=(index < 2),
        ):
            left, right = st.columns(2)

            with left:
                thought = st.text_area(
                    "Мысль / интерпретация",
                    key=f"chain_thought_{index}",
                )
                emotion = st.text_input(
                    "Эмоция",
                    key=f"chain_emotion_{index}",
                )
                urge = st.text_input(
                    "Побуждение / импульс",
                    key=f"chain_urge_{index}",
                )

            with right:
                body = st.text_input(
                    "Телесные ощущения",
                    key=f"chain_body_{index}",
                )
                action = st.text_area(
                    "Действие / следующий шаг",
                    key=f"chain_action_{index}",
                )
                intervention = st.text_area(
                    "Возможная точка вмешательства",
                    key=f"chain_intervention_{index}",
                )

            skill = st.text_input(
                "Навык или поддержка для этой точки",
                key=f"chain_skill_{index}",
                placeholder="Например: пауза, заземление, обратиться за поддержкой",
            )

            links.append(
                {
                    "thought": thought,
                    "emotion": emotion,
                    "urge": urge,
                    "body": body,
                    "action": action,
                    "intervention": intervention,
                    "skill": skill,
                }
            )

    left, right = st.columns(2)

    with left:
        immediate = st.text_area(
            "Последствия сразу после (для себя и других)",
            key="chain_immediate",
        )
        immediate_reinforcement = st.text_area(
            "Что могло подкрепить поведение сразу?",
            key="chain_immediate_reinforcement",
        )

    with right:
        later = st.text_area(
            "Отсроченные последствия",
            key="chain_later",
        )
        later_reinforcement = st.text_area(
            "Что могло поддержать повторение поведения?",
            key="chain_later_reinforcement",
        )

    prevention = st.text_area(
        "План профилактики на будущее",
        key="chain_prevention",
        placeholder="Какие уязвимости можно уменьшить? Что подготовить заранее?",
    )
    repair = st.text_area(
        "Восстановление / исправление последствий, если необходимо",
        key="chain_repair",
    )

    if st.button(
        "Сформировать карту цепочки",
        key="chain_build",
        type="primary",
        use_container_width=True,
    ):
        if not target.strip():
            st.warning("Опишите поведение, которое анализируете.")
            st.session_state.pop("result_dbt_chain", None)
        else:
            st.session_state.result_dbt_chain = {
                "vulnerability": vulnerability,
                "trigger": trigger,
                "target": target,
                "links": links,
                "immediate": immediate,
                "immediate_reinforcement": immediate_reinforcement,
                "later": later,
                "later_reinforcement": later_reinforcement,
                "prevention": prevention,
                "repair": repair,
            }

    result = st.session_state.get("result_dbt_chain")
    if not result:
        return

    st.subheader("Сводка цепочки и анализа решений")
    for title, value in [
        ("Факторы уязвимости", result["vulnerability"]),
        ("Провоцирующее событие", result["trigger"]),
        ("Проблемное поведение", result["target"]),
        ("Последствия сразу", result["immediate"]),
        ("Что подкрепляло поведение", result["immediate_reinforcement"]),
        ("Отсроченные последствия", result["later"]),
        ("План профилактики", result["prevention"]),
        ("Восстановление", result["repair"]),
    ]:
        st.markdown(f"**{title}:** {value or '—'}")

    for index, link in enumerate(result["links"], start=1):
        with st.expander(f"Содержание звена {index}", expanded=False):
            st.write(
                f'Мысль: {link["thought"] or "—"} · '
                f'Эмоция: {link["emotion"] or "—"} · '
                f'Импульс: {link["urge"] or "—"} · '
                f'Ощущения: {link["body"] or "—"}'
            )
            st.write(f'Действие: {link["action"] or "—"}')
            st.write(
                f'Точка вмешательства: {link["intervention"] or "—"} · '
                f'Навык/поддержка: {link["skill"] or "—"}'
            )

    width = 1200
    top_card_y = 82
    top_card_w = 360
    top_card_h = 94
    chain_y = 220
    row_height = 152
    chain_card_h = 128
    footer_gap = 24
    footer_y = chain_y + len(result["links"]) * row_height + footer_gap
    height = footer_y + 180

    dbt_palette = {
        "ink": "#493B72",
        "text": "#554E70",
        "line": "#A18ACB",
        "vulnerability": "#EEE8FA",
        "trigger": "#FFF0D8",
        "behavior": "#FCE4E4",
        "link_a": "#E7F5F2",
        "link_b": "#EAF1FC",
        "consequence": "#FFF3E7",
        "repair": "#E8F4E8",
        "white": "#FFFFFF",
    }

    body = ""

    top_cards = [
        (
            "ФАКТОРЫ УЯЗВИМОСТИ",
            result["vulnerability"],
            dbt_palette["vulnerability"],
        ),
        (
            "ПРОВОЦИРУЮЩЕЕ СОБЫТИЕ",
            result["trigger"],
            dbt_palette["trigger"],
        ),
        (
            "ПРОБЛЕМНОЕ ПОВЕДЕНИЕ",
            result["target"],
            dbt_palette["behavior"],
        ),
    ]

    card_xs = [40, 420, 800]

    for x, (label, value, fill) in zip(card_xs, top_cards):
        body += (
            f'<rect x="{x}" y="{top_card_y}" width="{top_card_w}" '
            f'height="{top_card_h}" rx="16" fill="{fill}" '
            f'stroke="#C8BDE0" stroke-width="2"/>'
        )
        body += svg_text(
            x + 17,
            top_card_y + 29,
            label,
            size=14,
            weight=700,
            color=dbt_palette["ink"],
            max_chars=38,
            max_lines=1,
        )
        body += svg_text(
            x + 17,
            top_card_y + 58,
            value,
            size=15,
            color=dbt_palette["text"],
            max_chars=42,
            max_lines=2,
        )

    body += (
        f'<line x1="{width // 2}" y1="{top_card_y + top_card_h}" '
        f'x2="{width // 2}" y2="{chain_y - 16}" '
        f'stroke="{dbt_palette["line"]}" stroke-width="4"/>'
    )

    for index, link in enumerate(result["links"]):
        y = chain_y + index * row_height
        fill = dbt_palette["link_a"] if index % 2 == 0 else dbt_palette["link_b"]

        body += (
            f'<rect x="40" y="{y}" width="1120" height="{chain_card_h}" '
            f'rx="17" fill="{fill}" stroke="#B6A8D8" stroke-width="2"/>'
        )
        body += (
            f'<rect x="40" y="{y}" width="10" height="{chain_card_h}" '
            f'rx="5" fill="{dbt_palette["line"]}"/>'
        )
        body += (
            f'<circle cx="82" cy="{y + 36}" r="22" '
            f'fill="#FFFFFF" stroke="{dbt_palette["line"]}" stroke-width="2"/>'
        )
        body += svg_text(
            74,
            y + 42,
            str(index + 1),
            size=17,
            weight=700,
            color=dbt_palette["ink"],
            max_chars=3,
            max_lines=1,
        )

        body += svg_text(
            120,
            y + 31,
            f'Мысль: {link["thought"]} · Эмоция: {link["emotion"]} · '
            f'Импульс: {link["urge"]}',
            size=15,
            color=dbt_palette["text"],
            max_chars=112,
            max_lines=1,
        )
        body += svg_text(
            120,
            y + 65,
            f'Ощущения: {link["body"]} · Действие: {link["action"]}',
            size=15,
            color=dbt_palette["text"],
            max_chars=112,
            max_lines=1,
        )
        body += svg_text(
            120,
            y + 99,
            f'Точка вмешательства: {link["intervention"]} · '
            f'Навык: {link["skill"]}',
            size=15,
            color=dbt_palette["ink"],
            max_chars=112,
            max_lines=1,
        )

        if index < len(result["links"]) - 1:
            body += (
                f'<line x1="{width // 2}" y1="{y + chain_card_h}" '
                f'x2="{width // 2}" y2="{y + row_height}" '
                f'stroke="{dbt_palette["line"]}" stroke-width="4"/>'
            )

    footer_cards = [
        (
            "ПОСЛЕДСТВИЯ СРАЗУ",
            result["immediate"],
            dbt_palette["consequence"],
        ),
        (
            "ОТСРОЧЕННЫЕ ПОСЛЕДСТВИЯ",
            result["later"],
            dbt_palette["consequence"],
        ),
        (
            "ПЛАН ПРОФИЛАКТИКИ И ВОССТАНОВЛЕНИЯ",
            f'{result["prevention"]} · {result["repair"]}',
            dbt_palette["repair"],
        ),
    ]

    footer_card_w = 360
    footer_card_h = 108

    for x, (label, value, fill) in zip(card_xs, footer_cards):
        body += (
            f'<rect x="{x}" y="{footer_y}" width="{footer_card_w}" '
            f'height="{footer_card_h}" rx="16" fill="{fill}" '
            f'stroke="#C8BDE0" stroke-width="2"/>'
        )
        body += svg_text(
            x + 17,
            footer_y + 31,
            label,
            size=14,
            weight=700,
            color=dbt_palette["ink"],
            max_chars=38,
            max_lines=1,
        )
        body += svg_text(
            x + 17,
            footer_y + 63,
            value,
            size=15,
            color=dbt_palette["text"],
            max_chars=42,
            max_lines=2,
        )

    svg = make_svg(
        width,
        height,
        "ДБТ · анализ цепочки и решений",
        body,
        accent="#E8DFF7",
    )
    render_visualization(
        svg,
        "dbt_chain.svg",
        "Цветовая карта показывает уязвимости, запуск события, "
        "последовательность звеньев и последствия. Схему можно масштабировать, "
        "перемещать и скачать.",
    )

# ---------------------------------------------------------------------
# Иерархия экспозиции
# ---------------------------------------------------------------------

def render_exposure():
    st.title("Иерархия экспозиции")
    st.write(
        "Составьте добровольную лестницу практики. До практики зафиксируйте "
        "прогноз, а после — наблюдаемый исход и то, что удалось узнать."
    )
    st.info(
        "Практикуйте только добровольно и в безопасных ситуациях; "
        "не используйте экспозицию для реальной опасности. "
        "План можно обсудить со специалистом."
    )

    goal = st.text_area("Цель / ситуация для работы", key="exposure_goal")

    step_count = int(
        st.number_input(
            "Количество ступеней",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            key="exposure_count",
        )
    )

    steps = []

    for index in range(step_count):
        with st.expander(f"Ступень {index + 1}", expanded=(index < 2)):
            situation = st.text_input(
                "Ситуация / упражнение",
                key=f"exposure_situation_{index}",
            )

            left, right = st.columns(2)

            with left:
                expected = st.slider(
                    "Ожидаемая тревога (0–10)",
                    min_value=0,
                    max_value=10,
                    value=3,
                    key=f"exposure_distress_{index}",
                )
                prediction = st.text_area(
                    "Прогноз или опасение",
                    key=f"exposure_prediction_{index}",
                )
                plan = st.text_area(
                    "Посильный план практики",
                    key=f"exposure_plan_{index}",
                )

            with right:
                practiced = st.checkbox(
                    "Практика выполнена",
                    key=f"exposure_practiced_{index}",
                )
                start = st.slider(
                    "Тревога в начале (0–10)",
                    min_value=0,
                    max_value=10,
                    value=0,
                    key=f"exposure_start_{index}",
                )
                peak = st.slider(
                    "Максимальная тревога (0–10)",
                    min_value=0,
                    max_value=10,
                    value=0,
                    key=f"exposure_peak_{index}",
                )
                after = st.slider(
                    "Тревога после практики (0–10)",
                    min_value=0,
                    max_value=10,
                    value=0,
                    key=f"exposure_after_{index}",
                )
                outcome = st.text_area(
                    "Что произошло на самом деле?",
                    key=f"exposure_outcome_{index}",
                )
                learning = st.text_area(
                    "Что вы узнали / что попробовать дальше?",
                    key=f"exposure_learning_{index}",
                )

            steps.append(
                {
                    "situation": situation,
                    "expected": expected,
                    "prediction": prediction,
                    "plan": plan,
                    "practiced": practiced,
                    "start": start,
                    "peak": peak,
                    "after": after,
                    "outcome": outcome,
                    "learning": learning,
                }
            )

    if st.button(
        "Сформировать лестницу",
        key="exposure_build",
        type="primary",
        use_container_width=True,
    ):
        completed = [step for step in steps if step["situation"].strip()]
        if not completed:
            st.warning("Добавьте описание хотя бы одной ступени.")
            st.session_state.pop("result_exposure", None)
        else:
            completed.sort(key=lambda step: step["expected"])
            st.session_state.result_exposure = {
                "goal": goal,
                "steps": completed,
            }

    result = st.session_state.get("result_exposure")
    if not result:
        return

    st.subheader("Лестница: от меньшей ожидаемой тревоги к большей")
    for index, step in enumerate(result["steps"], start=1):
        with st.container(border=True):
            st.markdown(
                f'**{index}. {step["situation"]}** · '
                f'ожидаемая тревога {step["expected"]}/10'
            )
            if step["prediction"]:
                st.write(f'Прогноз: {step["prediction"]}')
            if step["plan"]:
                st.write(f'План: {step["plan"]}')
            if step["practiced"]:
                st.write(
                    f'Практика: начало {step["start"]}/10, '
                    f'максимум {step["peak"]}/10, '
                    f'после {step["after"]}/10.'
                )
                if step["outcome"]:
                    st.write(f'Наблюдаемый исход: {step["outcome"]}')
                if step["learning"]:
                    st.write(f'Вывод / следующий шаг: {step["learning"]}')

    width = 1280
    row_height = 128
    height = 145 + len(result["steps"]) * row_height

    palette = {
        "ink": "#174F58",
        "text": "#356B70",
        "line": "#63B8B1",
        "track": "#D8EFED",
        "card": "#FFFFFF",
        "border": "#A7DCD7",
        "badge": "#DDF4F0",
    }

    body = svg_text(
        38,
        82,
        f'Цель: {result["goal"]}',
        size=16,
        color=palette["ink"],
        max_chars=110,
        max_lines=1,
    )

    for index in range(len(result["steps"]) - 1):
        y1 = 122 + index * row_height + 62
        y2 = 122 + (index + 1) * row_height + 62
        body += (
            f'<path d="M75 {y1} C125 {y1}, 125 {y2}, 175 {y2}" '
            f'fill="none" stroke="{palette["line"]}" '
            f'stroke-width="5" stroke-linecap="round"/>'
        )

    for index, step in enumerate(result["steps"]):
        y = 122 + index * row_height
        x = 165 + index * 34
        card_width = 490
        score = int(step["expected"])

        if score <= 3:
            level_fill, level_border = "#E1F5EF", "#65B89C"
            level_label = "Низкая нагрузка"
        elif score <= 6:
            level_fill, level_border = "#FFF3D9", "#E0AE4D"
            level_label = "Средняя нагрузка"
        else:
            level_fill, level_border = "#FCE8E5", "#D98575"
            level_label = "Высокая нагрузка"

        body += (
            f'<circle cx="75" cy="{y + 34}" r="26" '
            f'fill="{level_fill}" stroke="{level_border}" stroke-width="3"/>'
        )
        body += svg_text(
            63,
            y + 41,
            str(index + 1),
            size=19,
            weight=700,
            color=palette["ink"],
            max_chars=3,
            max_lines=1,
        )

        body += (
            f'<rect x="{x}" y="{y}" width="{card_width}" height="104" '
            f'rx="17" fill="{palette["card"]}" '
            f'stroke="{level_border}" stroke-width="2.5"/>'
        )
        body += (
            f'<rect x="{x}" y="{y}" width="12" height="104" '
            f'rx="6" fill="{level_border}"/>'
        )

        body += svg_text(
            x + 28,
            y + 30,
            step["situation"],
            size=17,
            weight=700,
            color=palette["ink"],
            max_chars=48,
            max_lines=1,
        )
        body += svg_text(
            x + 28,
            y + 57,
            f'Ожидаемая тревога {step["expected"]}/10 · {level_label}',
            size=14,
            color=palette["text"],
            max_chars=55,
            max_lines=1,
        )

        if step["practiced"]:
            body += svg_text(
                x + 28,
                y + 83,
                f'После практики: {step["after"]}/10 · '
                f'{step["outcome"] or step["learning"] or "наблюдение не записано"}',
                size=13,
                color=palette["text"],
                max_chars=58,
                max_lines=1,
            )
        elif step["plan"]:
            body += svg_text(
                x + 28,
                y + 83,
                f'План: {step["plan"]}',
                size=13,
                color=palette["text"],
                max_chars=58,
                max_lines=1,
            )

        note_x = 710
        note_fill = "#F3FAFC" if not step["practiced"] else "#EDF8F0"
        note_border = "#B8D9E7" if not step["practiced"] else "#A8D4B5"
        body += (
            f'<rect x="{note_x}" y="{y}" width="510" height="104" '
            f'rx="17" fill="{note_fill}" stroke="{note_border}" '
            f'stroke-width="2"/>'
        )

        if step["practiced"]:
            body += svg_text(
                note_x + 17,
                y + 29,
                f'Тревога: начало {step["start"]} · '
                f'пик {step["peak"]} · после {step["after"]}',
                size=14,
                weight=700,
                color=palette["ink"],
                max_chars=58,
                max_lines=1,
            )
            body += svg_text(
                note_x + 17,
                y + 58,
                f'Что произошло: {step["outcome"] or "—"}',
                size=13,
                color=palette["text"],
                max_chars=57,
                max_lines=1,
            )
            body += svg_text(
                note_x + 17,
                y + 83,
                f'Что удалось узнать: {step["learning"] or "—"}',
                size=13,
                color=palette["text"],
                max_chars=57,
                max_lines=1,
            )
        else:
            body += svg_text(
                note_x + 17,
                y + 29,
                "ПРОГНОЗ",
                size=12,
                weight=700,
                color=palette["ink"],
                max_chars=20,
                max_lines=1,
            )
            body += svg_text(
                note_x + 17,
                y + 57,
                step["prediction"] or "Пока не заполнен",
                size=14,
                color=palette["text"],
                max_chars=58,
                max_lines=1,
            )
            body += svg_text(
                note_x + 17,
                y + 83,
                "Практика ещё не отмечена",
                size=13,
                color=palette["text"],
                max_chars=52,
                max_lines=1,
            )

    svg = make_svg(
        width,
        height,
        "Иерархия экспозиции",
        body,
        accent="#D7F1EB",
    )
    render_visualization(
        svg,
        "exposure_hierarchy.svg",
        "Цвет ступени показывает субъективный уровень ожидаемой тревоги. "
        "Отдельные карточки отражают план, прогноз и результат практики.",
    )


# ---------------------------------------------------------------------
# ACT-матрица
# ---------------------------------------------------------------------

def render_act_matrix():
    st.title("ACT-матрица")
    st.write(
        "Заметьте внутренний и внешний опыт, движения от дискомфорта "
        "и действия в сторону того, что важно."
    )
    st.info(
        "Матрица — способ исследовать выбор, а не оценка поведения. "
        "В поля можно записывать несколько пунктов через новую строку."
    )

    situation = st.text_area(
        "Ситуация / контекст",
        key="act_situation",
    )
    values = st.text_area(
        "Люди и ценности, которые важны",
        key="act_values",
        placeholder="Например: близкие отношения, забота, обучение",
    )
    external = st.text_area(
        "Что вы замечаете снаружи пятью чувствами?",
        key="act_external",
        placeholder="Что можно увидеть, услышать или заметить в ситуации?",
    )

    left, right = st.columns(2)

    with left:
        away = st.text_area(
            "Действия от дискомфорта",
            key="act_away",
            help="Что вы делаете, чтобы уйти от неприятного опыта?",
        )
        inner = st.text_area(
            "Внутренний опыт",
            key="act_inner",
            help="Мысли, эмоции, воспоминания, импульсы и ощущения.",
        )

    with right:
        toward = st.text_area(
            "Действия к важному",
            key="act_toward",
            help="Что приближает к людям и ценностям, которые важны?",
        )
        toward_inner = st.text_area(
            "Внутренний опыт при движении к важному",
            key="act_toward_inner",
        )

    chosen_step = st.text_area(
        "Один небольшой выбранный шаг к важному",
        key="act_step",
    )

    if st.button(
        "Сформировать ACT-матрицу",
        key="act_build",
        type="primary",
        use_container_width=True,
    ):
        if not situation.strip():
            st.warning("Добавьте ситуацию, которую исследуете.")
            st.session_state.pop("result_act_matrix", None)
        else:
            st.session_state.result_act_matrix = {
                "situation": situation,
                "values": values,
                "external": external,
                "away": away,
                "inner": inner,
                "toward": toward,
                "toward_inner": toward_inner,
                "step": chosen_step,
            }

    result = st.session_state.get("result_act_matrix")
    if not result:
        return

    st.subheader("Сводка")
    st.write(f'**Ситуация:** {result["situation"]}')
    st.write(f'**Что важно:** {result["values"] or "—"}')
    st.write(f'**Небольшой шаг:** {result["step"] or "—"}')

    width, height = 1240, 850

    left_x, right_x = 55, 635
    top_y, bottom_y = 135, 435
    box_width, box_height = 550, 265

    palette = {
        "ink": "#294968",
        "text": "#4E6681",
        "axis": "#587B9D",
        "external": ("#E8F4FF", "#91BFE3"),
        "toward": ("#E8F6ED", "#83C49B"),
        "inner": ("#F2ECFA", "#B6A0D8"),
        "away": ("#FFF0E8", "#E7A47D"),
    }

    quadrants = [
        (
            "ВНЕШНИЙ ОПЫТ",
            "Что замечаю пятью чувствами?",
            left_x,
            top_y,
            result["external"],
            palette["external"],
        ),
        (
            "ДЕЙСТВИЯ К ВАЖНОМУ",
            "Что приближает к ценностям?",
            right_x,
            top_y,
            result["toward"],
            palette["toward"],
        ),
        (
            "ВНУТРЕННИЙ ОПЫТ",
            "Что происходит внутри?",
            left_x,
            bottom_y,
            result["inner"],
            palette["inner"],
        ),
        (
            "ДЕЙСТВИЯ ОТ ДИСКОМФОРТА",
            "Как я пытаюсь уйти от неприятного?",
            right_x,
            bottom_y,
            result["away"],
            palette["away"],
        ),
    ]

    body = svg_text(
        55,
        82,
        f'Контекст: {result["situation"]}',
        size=16,
        color=palette["ink"],
        max_chars=110,
        max_lines=1,
    )

    for title, subtitle, x, y, value, colors in quadrants:
        fill, border = colors

        body += (
            f'<rect x="{x}" y="{y}" width="{box_width}" '
            f'height="{box_height}" rx="20" fill="#FFFFFF" '
            f'stroke="{border}" stroke-width="2.5"/>'
        )
        body += (
            f'<path d="M{x + 20} {y} h{box_width - 40} '
            f'a20 20 0 0 1 20 20 v36 h-{box_width} v-36 '
            f'a20 20 0 0 1 20-20 z" fill="{fill}"/>'
        )
        body += svg_text(
            x + 20,
            y + 29,
            title,
            size=16,
            weight=700,
            color=palette["ink"],
            max_chars=56,
            max_lines=1,
        )
        body += svg_text(
            x + 20,
            y + 57,
            subtitle,
            size=13,
            color=palette["text"],
            max_chars=58,
            max_lines=1,
        )

        items = [
            item.strip()
            for item in (value or "").splitlines()
            if item.strip()
        ][:6]

        if not items:
            body += svg_text(
                x + 22,
                y + 105,
                "Добавленные пункты появятся здесь",
                size=14,
                color="#7B8FA3",
                max_chars=54,
                max_lines=1,
            )
        else:
            for index, item in enumerate(items):
                item_y = y + 99 + index * 27
                body += (
                    f'<circle cx="{x + 25}" cy="{item_y - 5}" '
                    f'r="5" fill="{border}"/>'
                )
                body += svg_text(
                    x + 43,
                    item_y,
                    item,
                    size=15,
                    color=palette["text"],
                    max_chars=58,
                    max_lines=1,
                )

    body += (
        '<line x1="620" y1="118" x2="620" y2="718" '
        'stroke="#587B9D" stroke-width="3"/>'
    )
    body += (
        '<line x1="42" y1="418" x2="1198" y2="418" '
        'stroke="#587B9D" stroke-width="3"/>'
    )

    body += (
        '<circle cx="620" cy="418" r="20" fill="#FFFFFF" '
        'stroke="#587B9D" stroke-width="3"/>'
    )
    body += (
        '<circle cx="620" cy="418" r="7" fill="#587B9D"/>'
    )

    footer_y = 735
    body += (
        f'<rect x="55" y="{footer_y}" width="1130" height="82" '
        'rx="18" fill="#E8F4ED" stroke="#83C49B" stroke-width="2"/>'
    )
    body += svg_text(
        75,
        footer_y + 29,
        "ВЫБРАННЫЙ ШАГ К ВАЖНОМУ",
        size=13,
        weight=700,
        color="#315F47",
        max_chars=45,
        max_lines=1,
    )
    body += svg_text(
        75,
        footer_y + 60,
        f'Ценности: {result["values"] or "—"} · '
        f'Следующий шаг: {result["step"] or "—"}',
        size=15,
        color="#315F47",
        max_chars=120,
        max_lines=1,
    )

    svg = make_svg(
        width,
        height,
        "ACT-матрица · замечать и выбирать",
        body,
        accent="#DFECFA",
    )
    render_visualization(
        svg,
        "act_matrix.svg",
        "У квадрантов разные цветовые акценты: внешний опыт, внутренний опыт, "
        "действия к важному и действия от дискомфорта. Выбранный шаг выделен "
        "отдельной зелёной плашкой.",
    )


# ---------------------------------------------------------------------
# Психодрама: библиотека образов
# ---------------------------------------------------------------------

POOL = [
    {
        "id": "adult_male",
        "label": "Мужской образ",
        "type": "adult_male",
        "category": "people",
        "color": "#72A9C8",
    },
    {
        "id": "adult_female",
        "label": "Женский образ",
        "type": "adult_female",
        "category": "people",
        "color": "#A88BC7",
    },
    {
        "id": "boy",
        "label": "Ребёнок — мальчик",
        "type": "boy",
        "category": "people",
        "color": "#E6AD69",
    },
    {
        "id": "girl",
        "label": "Ребёнок — девочка",
        "type": "girl",
        "category": "people",
        "color": "#D98991",
    },
    {
        "id": "monster",
        "label": "Монстр",
        "type": "monster",
        "category": "creatures",
        "color": "#8B6AAE",
    },
    {
        "id": "ghost",
        "label": "Призрак",
        "type": "ghost",
        "category": "creatures",
        "color": "#93B9CA",
    },
    {
        "id": "dragon",
        "label": "Дракон",
        "type": "dragon",
        "category": "creatures",
        "color": "#72966E",
    },
    {
        "id": "alien",
        "label": "Инопланетянин",
        "type": "alien",
        "category": "creatures",
        "color": "#7DB6A3",
    },
    {
        "id": "giant",
        "label": "Великан",
        "type": "giant",
        "category": "creatures",
        "color": "#A77E65",
    },
    {
        "id": "robot",
        "label": "Робот",
        "type": "robot",
        "category": "creatures",
        "color": "#879AA7",
    },
    {
        "id": "shadow",
        "label": "Тень",
        "type": "shadow",
        "category": "creatures",
        "color": "#596779",
    },
    {
        "id": "fairy",
        "label": "Сказочный персонаж",
        "type": "fairy",
        "category": "creatures",
        "color": "#D58FB1",
    },
    {
        "id": "dog",
        "label": "Собака",
        "type": "dog",
        "category": "animals",
        "color": "#B98964",
    },
    {
        "id": "wolf",
        "label": "Волк",
        "type": "wolf",
        "category": "animals",
        "color": "#87929D",
    },
    {
        "id": "cat",
        "label": "Кошка",
        "type": "cat",
        "category": "animals",
        "color": "#D5A36D",
    },
    {
        "id": "bird",
        "label": "Птица",
        "type": "bird",
        "category": "animals",
        "color": "#71A9BB",
    },
    {
        "id": "snake",
        "label": "Змея",
        "type": "snake",
        "category": "animals",
        "color": "#82A36C",
    },
    {
        "id": "bear",
        "label": "Медведь",
        "type": "bear",
        "category": "animals",
        "color": "#A77C62",
    },
    {
        "id": "butterfly",
        "label": "Бабочка",
        "type": "butterfly",
        "category": "animals",
        "color": "#B38BC6",
    },
    {
        "id": "circle",
        "label": "Круг",
        "type": "circle",
        "category": "symbols",
        "color": "#88B8D3",
    },
    {
        "id": "star",
        "label": "Звезда",
        "type": "star",
        "category": "symbols",
        "color": "#E3B95F",
    },
    {
        "id": "cloud",
        "label": "Облако",
        "type": "cloud",
        "category": "symbols",
        "color": "#A5B9D2",
    },
    {
        "id": "heart",
        "label": "Сердце",
        "type": "heart",
        "category": "symbols",
        "color": "#D98991",
    },
    {
        "id": "sun",
        "label": "Солнце",
        "type": "sun",
        "category": "symbols",
        "color": "#E9B85D",
    },
    {
        "id": "moon",
        "label": "Луна",
        "type": "moon",
        "category": "symbols",
        "color": "#97A5C3",
    },
    {
        "id": "lightning",
        "label": "Молния",
        "type": "lightning",
        "category": "symbols",
        "color": "#E0AE4D",
    },
    {
        "id": "flame",
        "label": "Пламя",
        "type": "flame",
        "category": "symbols",
        "color": "#D98462",
    },
    {
        "id": "mask",
        "label": "Маска",
        "type": "mask",
        "category": "symbols",
        "color": "#A88BC7",
    },
    {
        "id": "shield",
        "label": "Щит",
        "type": "shield",
        "category": "symbols",
        "color": "#75A69B",
    },
    {
        "id": "spiral",
        "label": "Спираль",
        "type": "spiral",
        "category": "symbols",
        "color": "#8D83B6",
    },
    {
        "id": "mountain",
        "label": "Гора",
        "type": "mountain",
        "category": "symbols",
        "color": "#7D9D88",
    },
    {
        "id": "stone",
        "label": "Камень",
        "type": "stone",
        "category": "symbols",
        "color": "#919BA3",
    },
    {
        "id": "key",
        "label": "Ключ",
        "type": "key",
        "category": "symbols",
        "color": "#D1A953",
    },
    {
        "id": "chair",
        "label": "Стул",
        "type": "chair",
        "category": "objects",
        "color": "#B98964",
    },
    {
        "id": "house",
        "label": "Дом",
        "type": "house",
        "category": "objects",
        "color": "#D59B72",
    },
    {
        "id": "door",
        "label": "Дверь",
        "type": "door",
        "category": "objects",
        "color": "#A8815F",
    },
    {
        "id": "window",
        "label": "Окно",
        "type": "window",
        "category": "objects",
        "color": "#77AAC2",
    },
    {
        "id": "tree",
        "label": "Дерево",
        "type": "tree",
        "category": "objects",
        "color": "#78A783",
    },
    {
        "id": "table",
        "label": "Стол",
        "type": "table",
        "category": "objects",
        "color": "#9B8069",
    },
    {
        "id": "wall",
        "label": "Стена",
        "type": "wall",
        "category": "objects",
        "color": "#8E9EAC",
    },
    {
        "id": "boundary",
        "label": "Граница",
        "type": "boundary",
        "category": "objects",
        "color": "#688BA7",
    },
    {
        "id": "bridge",
        "label": "Мост",
        "type": "bridge",
        "category": "objects",
        "color": "#B98B67",
    },
    {
        "id": "road",
        "label": "Дорога",
        "type": "road",
        "category": "objects",
        "color": "#8D9AA3",
    },
    {
        "id": "chain",
        "label": "Цепь",
        "type": "chain",
        "category": "objects",
        "color": "#8A7B8F",
    },
    {
        "id": "empty",
        "label": "Пустое место",
        "type": "empty",
        "category": "objects",
        "color": "#A9BCC9",
    },
]


APP_HTML = r"""
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <style>
    * {
      box-sizing: border-box;
    }

    html,
    body {
      margin: 0;
      min-height: 100%;
      color: #294A65 !important;
      background: #F3F9FD !important;
      color-scheme: light !important;
      font: 14px "Segoe UI", Arial, sans-serif;
    }

    body,
    button,
    input,
    select {
      color-scheme: light !important;
    }

    button,
    input,
    select {
      font: inherit;
    }

    button {
      cursor: pointer;
    }

    .app {
      display: flex;
      gap: 14px;
      min-height: 850px;
      color: #294A65;
      background: #F3F9FD;
    }

    .sidebar {
      width: 315px;
      min-width: 280px;
      max-height: 1040px;
      overflow-y: auto;
      padding: 15px;
      border: 1px solid #D4E5F0;
      border-radius: 18px;
      background: #FFFFFF;
      box-shadow: 0 8px 24px rgba(62,112,148,.07);
    }

    .workspace {
      flex: 1;
      min-width: 0;
      padding: 14px;
      border: 1px solid #D4E5F0;
      border-radius: 18px;
      background: #FFFFFF;
      box-shadow: 0 8px 24px rgba(62,112,148,.07);
    }

    h2 {
      margin: 2px 0 6px;
      color: #234D6B;
      font-size: 19px;
    }

    .muted {
      color: #69849A;
      line-height: 1.45;
    }

    .tabs,
    .toolbar,
    .scene-tabs,
    .selection-tools {
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
      align-items: center;
    }

    .tabs {
      margin: 14px 0 12px;
    }

    .tab,
    .tool-btn,
    .scene-tab {
      border: 1px solid #B9D5E6;
      border-radius: 9px;
      background: #F5FAFD;
      color: #315773;
      padding: 8px 10px;
      font-weight: 600;
    }

    .tab.active,
    .scene-tab.active,
    .tool-btn.active {
      border-color: #6EA7CB;
      background: #DFF0FA;
      color: #234D6B;
    }

    .pool {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
    }

    .pool-item {
      display: flex;
      min-height: 88px;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 5px;
      padding: 8px 5px;
      border: 1px solid #D6E6F0;
      border-radius: 12px;
      background: linear-gradient(145deg, #FFFFFF, #F1F8FC);
      color: #355C76;
      text-align: center;
      font-size: 12px;
      transition: .15s ease;
      user-select: none;
    }

    .pool-item:hover {
      transform: translateY(-2px);
      border-color: #78B0D1;
      box-shadow: 0 5px 14px rgba(71,130,164,.12);
    }

    .pool-icon {
      width: 42px;
      height: 42px;
      overflow: visible;
    }

    .section-label {
      margin: 15px 0 8px;
      color: #55748B;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .06em;
      text-transform: uppercase;
    }

    .help-card {
      margin-top: 14px;
      padding: 10px 12px;
      border: 1px solid #CDE0EC;
      border-radius: 12px;
      background: #F1F8FC;
      color: #52718A;
      font-size: 12px;
      line-height: 1.5;
    }

    .toolbar {
      justify-content: space-between;
      margin-bottom: 10px;
    }

    .toolbar-left,
    .toolbar-right {
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
      align-items: center;
    }

    .toolbar button {
      min-height: 38px;
    }

    .scene-tabs {
      margin: 7px 0 10px;
    }

    .scene-tab {
      padding: 7px 12px;
    }

    .stage-wrap {
      overflow: hidden;
      border: 1px solid #C9DFEF;
      border-radius: 15px;
      background: #FBFDFF;
    }

    #stage {
      display: block;
      width: 100%;
      height: min(66vh, 700px);
      min-height: 440px;
      touch-action: none;
      user-select: none;
      background: #FBFDFF;
    }

    .selection-panel {
      display: none;
      margin-top: 12px;
      padding: 12px;
      border: 1px solid #C6DCEB;
      border-radius: 13px;
      background: #F5FAFD;
    }

    .selection-panel.visible {
      display: block;
    }

    .selection-tools {
      margin-top: 9px;
    }

    .field {
      display: flex;
      flex-direction: column;
      gap: 5px;
      min-width: 130px;
      color: #55748B;
      font-size: 12px;
    }

    .field input[type="text"] {
      width: 230px;
      max-width: 100%;
      padding: 8px 9px;
      border: 1px solid #C2D9E8;
      border-radius: 8px;
      background: #FFFFFF;
      color: #294A65;
    }

    .field input[type="range"] {
      width: 150px;
    }

    .field input[type="color"] {
      width: 44px;
      height: 35px;
      padding: 2px;
      border: 1px solid #C2D9E8;
      border-radius: 8px;
      background: #FFFFFF;
    }

    .danger {
      border-color: #E5B8B8 !important;
      background: #FFF4F3 !important;
      color: #9B4D4A !important;
    }

    .status {
      min-height: 20px;
      margin-top: 8px;
      color: #69849A;
      font-size: 12px;
    }

    .privacy {
      margin: 12px 0 0;
      color: #69849A;
      font-size: 12px;
      line-height: 1.5;
    }

    .hidden {
      display: none !important;
    }

    @media (max-width: 900px) {
      .app {
        flex-direction: column;
      }

      .sidebar {
        width: 100%;
        min-width: 0;
        max-height: none;
      }

      .pool {
        grid-template-columns: repeat(4, minmax(0, 1fr));
      }

      #stage {
        height: 560px;
      }
    }

    @media (max-width: 560px) {
      .pool {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      #stage {
        min-height: 390px;
        height: 440px;
      }

      .toolbar {
        align-items: flex-start;
      }
    }
  </style>
</head>

<body>
  <div class="app">
    <aside class="sidebar">
      <h2>Библиотека образов</h2>

      <div class="muted">
        Выбирайте человечков, фантастические образы, животных, символы и предметы.
        Цвет фигуры и подпись можно изменить на свой вкус.
      </div>

      <div class="tabs" id="category-tabs"></div>
      <div class="pool" id="pool"></div>

      <div class="help-card">
        Пол, цвет и форма фигуры — только визуальные варианты, а не указание на
        личность или значение. Смысл образу и подписи придаёте вы.
      </div>

      <div class="section-label">Свои ассоциации</div>
      <div class="muted">
        Создайте свою фигуру или символ: выберите форму, задайте подпись и цвет.
      </div>

      <div class="selection-tools" style="margin-top:8px">
        <select id="custom-type" aria-label="Форма новой фигуры">
          <option value="adult_male">Взрослый — мужской образ</option>
          <option value="adult_female">Взрослый — женский образ</option>
          <option value="boy">Ребёнок — мальчик</option>
          <option value="girl">Ребёнок — девочка</option>
          <option value="monster">Существо</option>
          <option value="circle">Круг</option>
          <option value="star">Звезда</option>
          <option value="cloud">Облако</option>
          <option value="shadow">Тень</option>
          <option value="heart">Сердце</option>
        </select>

        <input
          id="custom-label"
          type="text"
          maxlength="60"
          placeholder="Название образа"
        >

        <input
          id="custom-color"
          type="color"
          value="#A88BC7"
          aria-label="Цвет своей фигуры"
        >

        <button class="tool-btn" id="add-custom" type="button">
          Добавить свою фигуру
        </button>
      </div>
    </aside>

    <main class="workspace">
      <div class="toolbar">
        <div class="toolbar-left">
          <button class="tool-btn" id="grid-toggle" type="button">
            Сетка: выкл.
          </button>

          <button class="tool-btn" id="connect-toggle" type="button">
            Создать связь
          </button>

          <button class="tool-btn" id="draw-toggle" type="button">
            Рисовать
          </button>

          <button class="tool-btn" id="undo-drawing" type="button">
            Отменить штрих
          </button>

          <button class="tool-btn" id="redo-drawing" type="button">
            Повторить штрих
          </button>

          <label class="field" style="min-width:auto">
            Цвет рисунка
            <input id="draw-color" type="color" value="#587E9A">
          </label>

          <label class="field" style="min-width:100px">
            Толщина
            <input id="draw-width" type="range" min="2" max="18" value="5">
          </label>

          <button class="tool-btn" id="clear-drawings" type="button">
            Удалить рисунки
          </button>

          <button class="tool-btn" id="clear-scene" type="button">
            Очистить сцену
          </button>
        </div>

        <div class="toolbar-right">
          <button class="tool-btn" id="export-svg" type="button">
            Скачать SVG
          </button>

          <button class="tool-btn" id="export-png" type="button">
            Скачать PNG
          </button>

          <button class="tool-btn" id="export-json" type="button">
            Скачать проект
          </button>

          <button class="tool-btn" id="import-json-btn" type="button">
            Открыть проект
          </button>

          <input
            id="import-json"
            class="hidden"
            type="file"
            accept=".json,application/json"
          >
        </div>
      </div>

      <div class="muted" id="interaction-instructions">
        Перетаскивайте образы мышью. Для рисования нажмите «Рисовать».
      </div>

      <div class="scene-tabs" id="scene-tabs"></div>

      <div class="stage-wrap" id="stage-wrap">
        <svg
          id="stage"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 1200 760"
          aria-label="Доска-сцена"
        >
          <defs>
            <pattern
              id="grid-pattern"
              width="32"
              height="32"
              patternUnits="userSpaceOnUse"
            >
              <circle cx="2" cy="2" r="1.2" fill="#D9E7F0"/>
            </pattern>

            <linearGradient
              id="stage-gradient"
              x1="0"
              x2="1"
              y1="0"
              y2="1"
            >
              <stop offset="0%" stop-color="#FCFEFF"/>
              <stop offset="100%" stop-color="#F3F9FD"/>
            </linearGradient>

            <marker
              id="arrowhead"
              markerWidth="10"
              markerHeight="8"
              refX="8"
              refY="4"
              orient="auto"
              markerUnits="strokeWidth"
            >
              <path d="M0,0 L10,4 L0,8 Z" fill="#688BA7"/>
            </marker>
          </defs>

          <rect
            id="stage-background"
            x="0"
            y="0"
            width="1200"
            height="760"
            fill="url(#stage-gradient)"
          />

          <rect
            id="stage-grid"
            x="0"
            y="0"
            width="1200"
            height="760"
            fill="url(#grid-pattern)"
            opacity="0"
          />

          <g id="scene-drawings"></g>
          <g id="scene-connections"></g>
          <g id="scene-items"></g>

          <g id="drop-hint" pointer-events="none">
            <text
              x="600"
              y="365"
              text-anchor="middle"
              fill="#8BA5B8"
              font-size="24"
              font-family="Segoe UI, Arial"
            >
              Добавьте образы из библиотеки
            </text>

            <text
              x="600"
              y="399"
              text-anchor="middle"
              fill="#A0B4C3"
              font-size="16"
              font-family="Segoe UI, Arial"
            >
              Расставьте их, соедините или дорисуйте собственные детали
            </text>
          </g>
        </svg>
      </div>

      <div class="selection-panel" id="node-panel">
        <strong id="node-selection-title">Выбранный образ</strong>

        <div class="selection-tools">
          <label class="field">
            Подпись
            <input
              id="node-label"
              type="text"
              maxlength="60"
              placeholder="Например: Я"
            >
          </label>

          <label class="field">
            Цвет
            <input
              id="node-color"
              type="color"
              value="#72A9C8"
            >
          </label>

          <label class="field">
            Размер
            <input
              id="node-size"
              type="range"
              min="0.65"
              max="1.6"
              step="0.05"
              value="1"
            >
          </label>

          <label class="field">
            Поворот
            <input
              id="node-rotation"
              type="range"
              min="-180"
              max="180"
              step="5"
              value="0"
            >
          </label>

          <button class="tool-btn danger" id="delete-node" type="button">
            Удалить образ
          </button>
        </div>
      </div>

      <div class="selection-panel" id="connection-panel">
        <strong id="connection-selection-title">Выбранная связь</strong>

        <div class="selection-tools">
          <label class="field">
            Подпись связи
            <input
              id="connection-label"
              type="text"
              maxlength="80"
              placeholder="Например: поддержка, дистанция"
            >
          </label>

          <label class="field">
            Цвет линии
            <input
              id="connection-color"
              type="color"
              value="#688BA7"
            >
          </label>

          <label class="field">
            Стиль
            <select id="connection-style">
              <option value="solid">Сплошная</option>
              <option value="dashed">Пунктирная</option>
              <option value="dotted">Точечная</option>
            </select>
          </label>

          <label class="field">
            <span>Стрелка</span>
            <input id="connection-arrow" type="checkbox">
          </label>

          <button
            class="tool-btn danger"
            id="delete-connection"
            type="button"
          >
            Удалить связь
          </button>
        </div>
      </div>

      <div class="status" id="status"></div>

      <div class="privacy">
        Это визуальный инструмент для исследования ситуации, а не диагностика.
        Образы, рисунки, линии, цвет и положение не интерпретируются автоматически.
        Упражнение добровольное: можно сделать паузу или завершить его в любой момент.
        Для продолжения позже скачайте файл проекта JSON.
      </div>
    </main>
  </div>

  <script>
    (() => {
      const POOL = __POOL_JSON__;
      const svgNS = "http://www.w3.org/2000/svg";

      const categories = [
        {
          id: "people",
          label: "Люди",
          types: ["adult_male", "adult_female", "boy", "girl"]
        },
        {
          id: "creatures",
          label: "Существа",
          types: [
            "monster",
            "ghost",
            "dragon",
            "alien",
            "giant",
            "robot",
            "shadow",
            "fairy"
          ]
        },
        {
          id: "animals",
          label: "Животные",
          types: [
            "dog",
            "wolf",
            "cat",
            "bird",
            "snake",
            "bear",
            "butterfly"
          ]
        },
        {
          id: "symbols",
          label: "Символы",
          types: [
            "circle",
            "star",
            "cloud",
            "heart",
            "sun",
            "moon",
            "lightning",
            "flame",
            "mask",
            "shield",
            "spiral",
            "mountain",
            "stone",
            "key"
          ]
        },
        {
          id: "objects",
          label: "Предметы и пространство",
          types: [
            "chair",
            "house",
            "door",
            "window",
            "tree",
            "table",
            "wall",
            "boundary",
            "bridge",
            "road",
            "chain",
            "empty"
          ]
        }
      ];

      const stage = document.getElementById("stage");
      const layer = document.getElementById("scene-items");
      const connectionLayer = document.getElementById("scene-connections");
      const drawingLayer = document.getElementById("scene-drawings");
      const hint = document.getElementById("drop-hint");
      const pool = document.getElementById("pool");
      const tabsRoot = document.getElementById("category-tabs");
      const sceneTabs = document.getElementById("scene-tabs");
      const nodePanel = document.getElementById("node-panel");
      const connectionPanel = document.getElementById("connection-panel");
      const status = document.getElementById("status");
      const grid = document.getElementById("stage-grid");
      const instructions = document.getElementById("interaction-instructions");

      let scenes = [
        {
          name: "Сцена 1",
          nodes: [],
          connections: [],
          drawings: []
        }
      ];

      let activeScene = 0;
      let activeCategory = "people";
      let selectedId = null;
      let selectedConnectionId = null;
      let nextId = 1;
      let nextConnectionId = 1;
      let nextDrawingId = 1;
      let gridOn = false;
      let dragState = null;
      let connectMode = false;
      let pendingConnectionFrom = null;
      let drawMode = false;
      let drawingState = null;

      let drawingUndoStack = [];
      let drawingRedoStack = [];

      const currentScene = () => scenes[activeScene];

      function setStatus(message) {
        status.textContent = message || "";
      }

      function svgEl(tag, attrs = {}) {
        const element = document.createElementNS(svgNS, tag);

        for (const [key, value] of Object.entries(attrs)) {
          element.setAttribute(key, value);
        }

        return element;
      }

      function addShape(type, color, parent) {
        const add = (tag, attrs) =>
          parent.appendChild(svgEl(tag, attrs));

        const stroke = "#506F84";

        function personShape(scale, style) {
          const group = svgEl("g", {
            transform: `scale(${scale})`
          });

          parent.appendChild(group);

          const isFemaleStyle =
            style === "female" || style === "girl";

          if (isFemaleStyle) {
            group.appendChild(svgEl("path", {
              d:
                "M-13 -25 Q-18 -43 0 -43 Q18 -43 13 -25 " +
                "L15 4 Q14 12 10 14 L9 -12 Q0 -21 -9 -12 " +
                "L-10 14 Q-15 10 -15 2 Z",
              fill: "#70574D",
              stroke: "#59463F",
              "stroke-width": 1.5,
              "stroke-linejoin": "round"
            }));
          } else {
            group.appendChild(svgEl("path", {
              d:
                "M-11 -28 Q-10 -40 0 -40 Q11 -40 12 -27 " +
                "Q5 -31 0 -29 Q-6 -30 -11 -27 Z",
              fill: "#70574D",
              stroke: "#59463F",
              "stroke-width": 1.5,
              "stroke-linejoin": "round"
            }));
          }

          group.appendChild(svgEl("path", {
            d: "M-7 24 L-11 45 M7 24 L11 45",
            fill: "none",
            stroke: "#506F84",
            "stroke-width": 4.5,
            "stroke-linecap": "round"
          }));

          group.appendChild(svgEl("path", {
            d: "M-12 -2 L-24 13 M12 -2 L24 13",
            fill: "none",
            stroke: "#506F84",
            "stroke-width": 4.5,
            "stroke-linecap": "round"
          }));

          if (isFemaleStyle) {
            group.appendChild(svgEl("path", {
              d:
                "M-11 -8 Q0 -14 11 -8 L15 5 " +
                "L23 25 Q0 32 -23 25 L-15 5 Z",
              fill: color,
              stroke: "#506F84",
              "stroke-width": 2,
              "stroke-linejoin": "round"
            }));
          } else {
            group.appendChild(svgEl("path", {
              d:
                "M-12 -8 Q0 -14 12 -8 L17 22 " +
                "L12 27 L0 23 L-12 27 L-17 22 Z",
              fill: color,
              stroke: "#506F84",
              "stroke-width": 2,
              "stroke-linejoin": "round"
            }));
          }

          group.appendChild(svgEl("circle", {
            cx: 0,
            cy: -24,
            r: 12,
            fill: "#F1C9A8",
            stroke: "#506F84",
            "stroke-width": 2
          }));

          group.appendChild(svgEl("circle", {
            cx: -4,
            cy: -24,
            r: 1.3,
            fill: "#344955"
          }));

          group.appendChild(svgEl("circle", {
            cx: 4,
            cy: -24,
            r: 1.3,
            fill: "#344955"
          }));

          group.appendChild(svgEl("path", {
            d: "M-3 -18 Q0 -16 3 -18",
            fill: "none",
            stroke: "#8B6258",
            "stroke-width": 1.4,
            "stroke-linecap": "round"
          }));
        }

        if (type === "adult_male") {
          personShape(1, "male");
        } else if (type === "adult_female") {
          personShape(1, "female");
        } else if (type === "boy") {
          personShape(.78, "boy");
        } else if (type === "girl") {
          personShape(.78, "girl");
        } else if (type === "giant") {
          personShape(1.35, "male");
        } else if (type === "monster") {
          add("path", {
            d:
              "M-34 25 Q-40 0 -29 -16 L-39 -37 L-18 -29 " +
              "Q-8 -39 2 -29 L20 -41 L19 -20 Q39 -7 33 19 " +
              "L25 33 L13 29 L8 43 L-5 32 L-20 41 L-23 27 Z",
            fill: color,
            stroke: "#49385D",
            "stroke-width": 3,
            "stroke-linejoin": "round"
          });

          add("path", {
            d: "M-24 -13 L-6 -7 M24 -13 L6 -7",
            fill: "none",
            stroke: "#342B3E",
            "stroke-width": 5,
            "stroke-linecap": "round"
          });

          add("ellipse", {
            cx: -14,
            cy: -2,
            rx: 5,
            ry: 7,
            fill: "#FFF4D8"
          });

          add("ellipse", {
            cx: 14,
            cy: -2,
            rx: 5,
            ry: 7,
            fill: "#FFF4D8"
          });

          add("circle", {
            cx: -14,
            cy: -1,
            r: 2.5,
            fill: "#A93838"
          });

          add("circle", {
            cx: 14,
            cy: -1,
            r: 2.5,
            fill: "#A93838"
          });

          add("path", {
            d: "M-19 10 Q0 4 19 10 L16 27 Q0 36 -16 27 Z",
            fill: "#3A2932",
            stroke: "#49385D",
            "stroke-width": 2
          });

          add("path", {
            d: "M-15 11 L-10 21 L-5 12 L0 22 L5 11 L10 21 L15 10",
            fill: "#FFFFFF",
            stroke: "#FFFFFF",
            "stroke-width": 2,
            "stroke-linejoin": "round"
          });
        } else if (type === "ghost") {
          add("path", {
            d:
              "M-30 30 L-27 -12 Q-23 -37 0 -38 " +
              "Q23 -37 27 -12 L30 30 L16 22 L5 32 " +
              "L-5 22 L-17 32 Z",
            fill: color,
            "fill-opacity": .82,
            stroke: "#637F92",
            "stroke-width": 2.5,
            "stroke-linejoin": "round"
          });

          add("ellipse", {
            cx: -10,
            cy: -8,
            rx: 4,
            ry: 6,
            fill: "#3D5362"
          });

          add("ellipse", {
            cx: 10,
            cy: -8,
            rx: 4,
            ry: 6,
            fill: "#3D5362"
          });

          add("ellipse", {
            cx: 0,
            cy: 8,
            rx: 5,
            ry: 7,
            fill: "#3D5362"
          });
        } else if (type === "dragon") {
          add("path", {
            d:
              "M-34 17 Q-39 -3 -20 -10 L-9 -28 L0 -12 " +
              "Q16 -20 27 -5 L41 -12 L35 3 L43 13 L25 18 " +
              "Q12 34 -8 26 L-20 39 L-22 22 Z",
            fill: color,
            stroke: "#486848",
            "stroke-width": 2.5,
            "stroke-linejoin": "round"
          });

          add("path", {
            d: "M-10 -7 L-39 -31 L-12 -21 Z M12 -7 L29 -34 L28 -11 Z",
            fill: color,
            stroke: "#486848",
            "stroke-width": 2.5,
            "stroke-linejoin": "round"
          });

          add("circle", {
            cx: 23,
            cy: -3,
            r: 3,
            fill: "#283A2C"
          });

          add("path", {
            d:
              "M35 2 Q47 -8 55 -20 Q53 -4 66 -4 " +
              "Q59 5 69 11 Q54 13 49 25 Q47 12 35 13 Z",
            fill: "#F28B45",
            stroke: "#C85C38",
            "stroke-width": 2,
            "stroke-linejoin": "round"
          });

          add("path", {
            d:
              "M37 5 Q49 0 56 -10 Q53 0 62 4 " +
              "Q53 6 48 15 Q46 8 37 10 Z",
            fill: "#FFD36A",
            stroke: "#F0A544",
            "stroke-width": 1.5,
            "stroke-linejoin": "round"
          });
        } else if (type === "alien") {
          add("ellipse", {
            cx: 0,
            cy: -12,
            rx: 26,
            ry: 35,
            fill: color,
            stroke: "#4D786D",
            "stroke-width": 2.5
          });

          add("ellipse", {
            cx: -10,
            cy: -14,
            rx: 6,
            ry: 10,
            fill: "#293E43"
          });

          add("ellipse", {
            cx: 10,
            cy: -14,
            rx: 6,
            ry: 10,
            fill: "#293E43"
          });

          add("path", {
            d: "M-12 21 L-24 39 M12 21 L24 39 M-22 1 L-38 12 M22 1 L38 12",
            fill: "none",
            stroke: "#4D786D",
            "stroke-width": 4,
            "stroke-linecap": "round"
          });
        } else if (type === "robot") {
          add("rect", {
            x: -27,
            y: -37,
            width: 54,
            height: 46,
            rx: 8,
            fill: color,
            stroke: "#536D7E",
            "stroke-width": 3
          });

          add("path", {
            d: "M0 -37 V-49 M-8 -49 H8",
            fill: "none",
            stroke: "#536D7E",
            "stroke-width": 3,
            "stroke-linecap": "round"
          });

          add("circle", {
            cx: -12,
            cy: -17,
            r: 5,
            fill: "#FFFFFF",
            stroke: "#536D7E",
            "stroke-width": 2
          });

          add("circle", {
            cx: 12,
            cy: -17,
            r: 5,
            fill: "#FFFFFF",
            stroke: "#536D7E",
            "stroke-width": 2
          });

          add("path", {
            d: "M-12 -1 H12 M-20 11 L-32 26 M20 11 L32 26 M-13 9 L-18 37 M13 9 L18 37",
            fill: "none",
            stroke: "#536D7E",
            "stroke-width": 5,
            "stroke-linecap": "round"
          });
        } else if (type === "shadow") {
          add("path", {
            d:
              "M0 -39 C-19 -34 -32 -12 -27 8 C-24 24 " +
              "-34 33 -28 40 Q-12 47 -5 34 Q3 45 12 36 " +
              "Q30 43 26 24 C40 4 25 -31 0 -39 Z",
            fill: color,
            "fill-opacity": .8,
            stroke: "#465568",
            "stroke-width": 2.5
          });
        } else if (type === "fairy") {
          add("path", {
            d:
              "M0 -20 Q-40 -47 -38 -10 Q-34 10 -8 7 " +
              "M0 -20 Q40 -47 38 -10 Q34 10 8 7",
            fill: color,
            "fill-opacity": .45,
            stroke: "#A65F8C",
            "stroke-width": 2
          });

          personShape(.82, "female");
        } else if (type === "dog") {
          add("path", {
            d:
              "M-24 -13 Q-31 -31 -43 -25 Q-47 -5 -34 5 " +
              "L-31 18 Q-28 35 0 35 Q28 35 31 18 " +
              "L34 5 Q47 -5 43 -25 Q31 -31 24 -13 " +
              "Q12 -23 0 -23 Q-12 -23 -24 -13 Z",
            fill: color,
            stroke: "#6E5948",
            "stroke-width": 2.5,
            "stroke-linejoin": "round"
          });

          add("ellipse", {
            cx: -11,
            cy: -2,
            rx: 3,
            ry: 4,
            fill: "#2F3D43"
          });

          add("ellipse", {
            cx: 11,
            cy: -2,
            rx: 3,
            ry: 4,
            fill: "#2F3D43"
          });

          add("ellipse", {
            cx: 0,
            cy: 12,
            rx: 12,
            ry: 9,
            fill: "#F2E2D2",
            stroke: "#6E5948",
            "stroke-width": 1.5
          });

          add("ellipse", {
            cx: 0,
            cy: 8,
            rx: 4,
            ry: 3,
            fill: "#39484F"
          });

          add("path", {
            d: "M0 11 Q-2 19 -8 17 M0 11 Q2 19 8 17 M29 10 Q44 8 42 -5",
            fill: "none",
            stroke: "#6E5948",
            "stroke-width": 2.5,
            "stroke-linecap": "round"
          });
        } else if (
          type === "wolf" ||
          type === "cat" ||
          type === "bear"
        ) {
          const ears =
            type === "cat"
              ? "M-25 -10 L-30 -38 L-7 -26 M25 -10 L30 -38 L7 -26"
              : type === "wolf"
                ? "M-26 -8 L-33 -42 L-7 -27 M26 -8 L33 -42 L7 -27"
                : "M-25 -17 Q-28 -34 -12 -34 Q-4 -34 -4 -24 M25 -17 Q28 -34 12 -34 Q4 -34 4 -24";

          add("path", {
            d:
              ears +
              " M-30 2 Q-29 -27 0 -29 Q29 -27 30 2 " +
              "Q30 30 0 32 Q-30 30 -30 2 Z",
            fill: color,
            stroke: "#526878",
            "stroke-width": 2.5,
            "stroke-linejoin": "round"
          });

          add("ellipse", {
            cx: -11,
            cy: -4,
            rx: 3.2,
            ry: 4,
            fill: "#263A46"
          });

          add("ellipse", {
            cx: 11,
            cy: -4,
            rx: 3.2,
            ry: 4,
            fill: "#263A46"
          });

          if (type === "wolf") {
            add("path", {
              d: "M-14 8 Q0 17 14 8 L10 27 Q0 34 -10 27 Z",
              fill: "#49363A",
              stroke: "#526878",
              "stroke-width": 1.5
            });

            add("path", {
              d: "M-11 9 L-7 24 L-3 13 L1 26 L6 12 L11 9",
              fill: "#FFFFFF",
              stroke: "#FFFFFF",
              "stroke-width": 2,
              "stroke-linejoin": "round"
            });
          } else {
            add("path", {
              d: "M-6 10 Q0 15 6 10 L0 16 Z",
              fill: "#4E5960"
            });
          }
        } else if (type === "bird") {
          add("path", {
            d: "M-9 -1 Q-29 -27 -47 -13 Q-43 8 -16 17 Z",
            fill: color,
            stroke: "#496E7F",
            "stroke-width": 2.5,
            "stroke-linejoin": "round"
          });

          add("path", {
            d: "M9 -1 Q29 -27 47 -13 Q43 8 16 17 Z",
            fill: color,
            stroke: "#496E7F",
            "stroke-width": 2.5,
            "stroke-linejoin": "round"
          });

          add("path", {
            d: "M-15 1 L-37 -11 M-14 8 L-34 2 M15 1 L37 -11 M14 8 L34 2",
            fill: "none",
            stroke: "#FFFFFF",
            "stroke-width": 2,
            "stroke-linecap": "round"
          });

          add("ellipse", {
            cx: 0,
            cy: 5,
            rx: 17,
            ry: 25,
            fill: color,
            stroke: "#496E7F",
            "stroke-width": 2.5
          });

          add("circle", {
            cx: 0,
            cy: -20,
            r: 13,
            fill: color,
            stroke: "#496E7F",
            "stroke-width": 2
          });

          add("circle", {
            cx: 5,
            cy: -22,
            r: 2.5,
            fill: "#263A46"
          });

          add("path", {
            d: "M12 -19 L31 -12 L12 -8 Z",
            fill: "#E0AE4D",
            stroke: "#927333",
            "stroke-width": 1.5,
            "stroke-linejoin": "round"
          });
        } else if (type === "snake") {
          add("path", {
            d:
              "M-32 25 C-42 2 -12 -14 7 0 C25 14 2 31 -11 16 " +
              "C-22 3 -6 -11 10 -21 Q24 -30 33 -17",
            fill: "none",
            stroke: color,
            "stroke-width": 13,
            "stroke-linecap": "round"
          });

          add("circle", {
            cx: 32,
            cy: -17,
            r: 9,
            fill: color,
            stroke: "#526B4B",
            "stroke-width": 2
          });

          add("circle", {
            cx: 35,
            cy: -20,
            r: 1.8,
            fill: "#263A46"
          });
        } else if (type === "butterfly") {
          add("ellipse", {
            cx: -18,
            cy: -14,
            rx: 18,
            ry: 23,
            fill: color,
            stroke: "#66577B",
            "stroke-width": 2
          });

          add("ellipse", {
            cx: 18,
            cy: -14,
            rx: 18,
            ry: 23,
            fill: color,
            stroke: "#66577B",
            "stroke-width": 2
          });

          add("ellipse", {
            cx: -16,
            cy: 17,
            rx: 14,
            ry: 18,
            fill: color,
            stroke: "#66577B",
            "stroke-width": 2
          });

          add("ellipse", {
            cx: 16,
            cy: 17,
            rx: 14,
            ry: 18,
            fill: color,
            stroke: "#66577B",
            "stroke-width": 2
          });

          add("path", {
            d: "M0 -20 V27 M0 -18 Q-7 -34 -13 -35 M0 -18 Q7 -34 13 -35",
            fill: "none",
            stroke: "#66577B",
            "stroke-width": 3,
            "stroke-linecap": "round"
          });
        } else if (type === "circle") {
          add("circle", {
            cx: 0,
            cy: 0,
            r: 30,
            fill: color,
            "fill-opacity": .82,
            stroke,
            "stroke-width": 2.5
          });
        } else if (type === "star") {
          add("path", {
            d: "M0-36 L9-12 L35-11 L15 5 L22 31 L0 16 L-22 31 L-15 5 L-35-11 L-9-12 Z",
            fill: color,
            stroke: "#927333",
            "stroke-width": 2
          });
        } else if (type === "cloud") {
          add("path", {
            d:
              "M-31 13 Q-39 -2 -23 -9 Q-20 -29 0 -21 " +
              "Q15 -35 25 -17 Q42 -14 36 2 Q40 17 23 19 " +
              "L-22 19 Q-36 19 -31 13 Z",
            fill: color,
            stroke: "#647D96",
            "stroke-width": 2.5
          });
        } else if (type === "heart") {
          add("path", {
            d:
              "M0 29 C-8 19 -34 2 -31 -15 C-29 -32 " +
              "-8 -34 0 -19 C9 -34 30 -32 32 -15 " +
              "C34 2 9 20 0 29 Z",
            fill: color,
            stroke: "#925D66",
            "stroke-width": 2
          });
        } else if (type === "sun") {
          for (let i = 0; i < 8; i++) {
            const angle = i * Math.PI / 4;

            add("line", {
              x1: Math.cos(angle) * 25,
              y1: Math.sin(angle) * 25,
              x2: Math.cos(angle) * 39,
              y2: Math.sin(angle) * 39,
              stroke: color,
              "stroke-width": 5,
              "stroke-linecap": "round"
            });
          }

          add("circle", {
            cx: 0,
            cy: 0,
            r: 21,
            fill: color,
            stroke: "#A4772A",
            "stroke-width": 2
          });
        } else if (type === "moon") {
          add("path", {
            d: "M18 -33 Q-20 -24 -20 9 Q-17 37 13 34 Q-7 19 -1 0 Q4 -21 18 -33 Z",
            fill: color,
            stroke: "#64718B",
            "stroke-width": 2.5
          });
        } else if (type === "lightning") {
          add("path", {
            d: "M5 -40 L-25 5 L-4 5 L-12 39 L28 -10 L7 -10 Z",
            fill: color,
            stroke: "#A07828",
            "stroke-width": 2.5,
            "stroke-linejoin": "round"
          });
        } else if (type === "flame") {
          add("path", {
            d:
              "M0 40 Q-35 22 -24 -4 Q-20 -20 -7 -28 " +
              "Q-8 -6 4 -1 Q10 -22 18 -34 Q41 1 27 24 " +
              "Q18 40 0 40 Z",
            fill: color,
            stroke: "#A85C43",
            "stroke-width": 2.5
          });
        } else if (type === "mask") {
          add("path", {
            d: "M-34 -21 Q0 -37 34 -21 L29 17 Q0 42 -29 17 Z",
            fill: color,
            stroke: "#66577B",
            "stroke-width": 2.5
          });

          add("path", {
            d: "M-23 -4 Q-12 -13 -2 -4 M2 -4 Q13 -13 23 -4",
            fill: "none",
            stroke: "#FFFFFF",
            "stroke-width": 3
          });
        } else if (type === "shield") {
          add("path", {
            d: "M0 -39 L31 -27 L27 10 Q19 31 0 41 Q-19 31 -27 10 L-31 -27 Z",
            fill: color,
            stroke: "#4E776E",
            "stroke-width": 3
          });

          add("path", {
            d: "M0 -25 V27 M-18 0 H18",
            fill: "none",
            stroke: "#FFFFFF",
            "stroke-width": 3
          });
        } else if (type === "spiral") {
          add("path", {
            d:
              "M0 0 C4 -2 7 3 4 7 C-2 14 -14 7 -12 -3 " +
              "C-10 -19 14 -23 24 -10 C38 9 22 34 1 35 " +
              "C-27 36 -43 7 -31 -19",
            fill: "none",
            stroke: color,
            "stroke-width": 5,
            "stroke-linecap": "round"
          });
        } else if (type === "mountain") {
          add("path", {
            d: "M-42 30 L-10 -24 L3 -3 L18 -37 L45 30 Z",
            fill: color,
            stroke: "#5E7E72",
            "stroke-width": 2.5
          });
        } else if (type === "stone") {
          add("path", {
            d: "M-36 20 L-28 -12 L-5 -31 L23 -25 L38 3 L27 27 L-17 32 Z",
            fill: color,
            stroke: "#677681",
            "stroke-width": 2.5
          });
        } else if (type === "key") {
          add("circle", {
            cx: -18,
            cy: 0,
            r: 17,
            fill: "none",
            stroke: color,
            "stroke-width": 7
          });

          add("path", {
            d: "M-2 0 H36 M22 0 V12 M32 0 V9",
            fill: "none",
            stroke: color,
            "stroke-width": 7,
            "stroke-linecap": "round"
          });
        } else if (type === "chair") {
          add("path", {
            d: "M-20 -25 L18 -25 L18 3 L-20 3 Z M-20 3 L-20 31 M18 3 L18 31",
            fill: "none",
            stroke: color,
            "stroke-width": 7,
            "stroke-linecap": "round"
          });
        } else if (type === "house") {
          add("path", {
            d: "M-36 -3 L0 -33 L36 -3 L29 0 L29 32 L-29 32 L-29 0 Z",
            fill: color,
            stroke: "#765744",
            "stroke-width": 2.5
          });

          add("rect", {
            x: -7,
            y: 9,
            width: 14,
            height: 23,
            rx: 2,
            fill: "#FFF9F1",
            stroke: "#765744",
            "stroke-width": 2
          });
        } else if (type === "door") {
          add("rect", {
            x: -25,
            y: -38,
            width: 50,
            height: 76,
            rx: 3,
            fill: color,
            stroke: "#765744",
            "stroke-width": 3
          });

          add("circle", {
            cx: 14,
            cy: 3,
            r: 3,
            fill: "#765744"
          });
        } else if (type === "window") {
          add("rect", {
            x: -34,
            y: -31,
            width: 68,
            height: 62,
            rx: 4,
            fill: color,
            "fill-opacity": .35,
            stroke: "#557E93",
            "stroke-width": 4
          });

          add("path", {
            d: "M0 -29 V29 M-32 0 H32",
            fill: "none",
            stroke: "#557E93",
            "stroke-width": 3
          });
        } else if (type === "tree") {
          add("path", {
            d: "M-7 8 L-12 42 L12 42 L7 8 Z",
            fill: "#A77B55",
            stroke: "#795A42",
            "stroke-width": 2
          });

          add("circle", {
            cx: 0,
            cy: -10,
            r: 27,
            fill: color,
            stroke: "#547B5A",
            "stroke-width": 2
          });

          add("circle", {
            cx: -18,
            cy: 1,
            r: 17,
            fill: color,
            stroke: "#547B5A",
            "stroke-width": 2
          });

          add("circle", {
            cx: 18,
            cy: 1,
            r: 17,
            fill: color,
            stroke: "#547B5A",
            "stroke-width": 2
          });
        } else if (type === "table") {
          add("path", {
            d: "M-34 -12 L34 -12 L30 1 L-30 1 Z M-24 1 L-28 33 M24 1 L28 33",
            fill: color,
            stroke: "#765D4A",
            "stroke-width": 4
          });
        } else if (type === "wall") {
          add("rect", {
            x: -34,
            y: -39,
            width: 68,
            height: 78,
            rx: 5,
            fill: color,
            "fill-opacity": .66,
            stroke: "#677B8A",
            "stroke-width": 2.5
          });

          add("path", {
            d: "M-34 -10 H34 M-34 16 H34 M0 -39 V-10 M-16 -10 V16 M12 -10 V16 M-2 16 V39",
            fill: "none",
            stroke: "#FFFFFF",
            "stroke-width": 2
          });
        } else if (type === "boundary") {
          add("ellipse", {
            cx: 0,
            cy: 0,
            rx: 42,
            ry: 28,
            fill: "none",
            stroke: color,
            "stroke-width": 4,
            "stroke-dasharray": "9 7"
          });
        } else if (type === "bridge") {
          add("path", {
            d: "M-40 25 Q0 -30 40 25 M-40 25 H40 M-30 17 V30 M-15 4 V30 M0 -2 V30 M15 4 V30 M30 17 V30",
            fill: "none",
            stroke: color,
            "stroke-width": 5,
            "stroke-linecap": "round"
          });
        } else if (type === "road") {
          add("path", {
            d: "M-25 40 L-12 -40 H12 L25 40 Z",
            fill: color,
            "fill-opacity": .55,
            stroke: "#667887",
            "stroke-width": 2
          });

          add("path", {
            d: "M0 -30 V-12 M0 0 V14 M0 27 V36",
            fill: "none",
            stroke: "#FFFFFF",
            "stroke-width": 3,
            "stroke-dasharray": "6 5"
          });
        } else if (type === "chain") {
          add("ellipse", {
            cx: -15,
            cy: 0,
            rx: 20,
            ry: 12,
            fill: "none",
            stroke: color,
            "stroke-width": 7,
            transform: "rotate(-35 -15 0)"
          });

          add("ellipse", {
            cx: 15,
            cy: 0,
            rx: 20,
            ry: 12,
            fill: "none",
            stroke: color,
            "stroke-width": 7,
            transform: "rotate(-35 15 0)"
          });
        } else if (type === "empty") {
          add("circle", {
            cx: 0,
            cy: 0,
            r: 30,
            fill: "#FFFFFF",
            stroke: color,
            "stroke-width": 3,
            "stroke-dasharray": "6 5"
          });

          add("path", {
            d: "M-10 0 H10 M0 -10 V10",
            fill: "none",
            stroke: color,
            "stroke-width": 3,
            "stroke-linecap": "round"
          });
        }
      }

      function renderPoolIcon(parent, item) {
        const icon = svgEl("svg", {
          viewBox: "-65 -62 145 125",
          class: "pool-icon",
          "aria-hidden": "true"
        });

        addShape(item.type, item.color, icon);
        parent.appendChild(icon);
      }

      function renderTabs() {
        tabsRoot.innerHTML = "";

        categories.forEach(category => {
          const button = document.createElement("button");
          button.type = "button";
          button.className =
            "tab" + (activeCategory === category.id ? " active" : "");
          button.textContent = category.label;

          button.onclick = () => {
            activeCategory = category.id;
            renderTabs();
            renderPool();
          };

          tabsRoot.appendChild(button);
        });
      }

      function renderPool() {
        pool.innerHTML = "";

        const category = categories.find(
          item => item.id === activeCategory
        );

        const items = POOL.filter(
          item => category.types.includes(item.type)
        );

        items.forEach(item => {
          const button = document.createElement("button");
          button.type = "button";
          button.className = "pool-item";
          button.draggable = true;
          button.title =
            "Нажмите, чтобы добавить, или перетащите на сцену";

          renderPoolIcon(button, item);

          const label = document.createElement("span");
          label.textContent = item.label;
          button.appendChild(label);

          button.onclick = () => addNode(item);

          button.ondragstart = event => {
            event.dataTransfer.setData("text/plain", item.id);
            event.dataTransfer.effectAllowed = "copy";
          };

          pool.appendChild(button);
        });
      }

      function renderSceneTabs() {
        sceneTabs.innerHTML = "";

        scenes.forEach((scene, index) => {
          const button = document.createElement("button");
          button.type = "button";
          button.className =
            "scene-tab" + (index === activeScene ? " active" : "");
          button.textContent = scene.name;
          button.title =
            "Дважды нажмите, чтобы переименовать сцену";

          button.onclick = () => switchScene(index);

          button.ondblclick = event => {
            event.preventDefault();

            const newName = prompt(
              "Название сцены:",
              scene.name
            );

            if (newName && newName.trim()) {
              scene.name = newName.trim().slice(0, 40);
              renderSceneTabs();
            }
          };

          sceneTabs.appendChild(button);
        });

        if (scenes.length < 6) {
          const addButton = document.createElement("button");
          addButton.type = "button";
          addButton.className = "scene-tab";
          addButton.textContent = "＋ Новая сцена";
          addButton.onclick = addScene;
          sceneTabs.appendChild(addButton);
        }

        const hintText = document.createElement("span");
        hintText.className = "muted";
        hintText.textContent =
          "Двойной клик по вкладке — переименовать";
        sceneTabs.appendChild(hintText);
      }

      function switchScene(index) {
        activeScene = index;
        selectedId = null;
        selectedConnectionId = null;
        pendingConnectionFrom = null;
        drawingState = null;

        renderSceneTabs();
        renderStage();
        updateSelectionPanels();
      }

      function addScene() {
        if (scenes.length >= 6) return;

        scenes.push({
          name: `Сцена ${scenes.length + 1}`,
          nodes: [],
          connections: [],
          drawings: []
        });

        activeScene = scenes.length - 1;
        selectedId = null;
        selectedConnectionId = null;

        renderSceneTabs();
        renderStage();
        updateSelectionPanels();
        setStatus("Создана новая пустая сцена.");
      }

      function addNode(item, position = null) {
        const offset =
          (currentScene().nodes.length % 8) * 20;

        const node = {
          id: `figure_${nextId++}`,
          type: item.type,
          label: item.label,
          color: item.color,
          size: 1,
          rotation: 0,
          x: position ? position.x : 430 + offset,
          y: position ? position.y : 300 + offset
        };

        currentScene().nodes.push(node);
        selectedId = node.id;
        selectedConnectionId = null;

        renderStage();
        updateSelectionPanels();

        setStatus(
          `Добавлен образ «${item.label}». Цвет и подпись можно изменить.`
        );
      }

      function findSelectedNode() {
        return currentScene().nodes.find(
          node => node.id === selectedId
        ) || null;
      }

      function findSelectedConnection() {
        return currentScene().connections.find(
          connection => connection.id === selectedConnectionId
        ) || null;
      }

      function renderDrawing(drawing) {
        if (
          !Array.isArray(drawing.points) ||
          drawing.points.length < 2
        ) {
          return null;
        }

        const d = drawing.points
          .map((point, index) =>
            `${index === 0 ? "M" : "L"} ${point.x} ${point.y}`
          )
          .join(" ");

        return svgEl("path", {
          d,
          fill: "none",
          stroke: drawing.color || "#587E9A",
          "stroke-width": drawing.width || 5,
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          "pointer-events": "none"
        });
      }

      function renderNode(node) {
        const group = svgEl("g", {
          "data-node-id": node.id,
          transform:
            `translate(${node.x} ${node.y}) ` +
            `rotate(${node.rotation}) ` +
            `scale(${node.size})`,
          tabindex: "0",
          role: "button",
          "aria-label": node.label || "Образ"
        });

        if (node.id === selectedId) {
          group.appendChild(svgEl("circle", {
            class: "selection-ring",
            cx: 0,
            cy: 2,
            r: 57,
            fill: "#DFF1FA",
            "fill-opacity": .5,
            stroke: "#347FA7",
            "stroke-width": 2.5,
            "stroke-dasharray": "6 5"
          }));
        }

        addShape(node.type, node.color, group);

        const caption = svgEl("text", {
          x: 0,
          y: 70,
          "text-anchor": "middle",
          "font-family": "Segoe UI, Arial, sans-serif",
          "font-size": 15,
          "font-weight": 600,
          fill: "#294A65",
          stroke: "#FFFFFF",
          "stroke-width": 4,
          "paint-order": "stroke",
          "stroke-linejoin": "round",
          "pointer-events": "none"
        });

        caption.textContent = node.label || "Без подписи";
        group.appendChild(caption);

        return group;
      }

      function renderConnection(connection) {
        const from = currentScene().nodes.find(
          node => node.id === connection.from
        );

        const to = currentScene().nodes.find(
          node => node.id === connection.to
        );

        if (!from || !to) return null;

        const group = svgEl("g", {
          "data-connection-id": connection.id,
          tabindex: "0",
          role: "button",
          "aria-label": connection.label || "Связь"
        });

        const dx = to.x - from.x;
        const dy = to.y - from.y;
        const length = Math.max(1, Math.sqrt(dx * dx + dy * dy));
        const ux = dx / length;
        const uy = dy / length;

        const startX = from.x + ux * 40;
        const startY = from.y + uy * 40;
        const endX = to.x - ux * 45;
        const endY = to.y - uy * 45;

        const dash =
          connection.style === "dashed"
            ? "10 8"
            : connection.style === "dotted"
              ? "2 8"
              : "";

        if (connection.id === selectedConnectionId) {
          group.appendChild(svgEl("line", {
            x1: startX,
            y1: startY,
            x2: endX,
            y2: endY,
            stroke: "#B8DDF1",
            "stroke-width": 13,
            "stroke-linecap": "round"
          }));
        }

        const visibleLine = svgEl("line", {
          x1: startX,
          y1: startY,
          x2: endX,
          y2: endY,
          stroke: connection.color || "#688BA7",
          "stroke-width":
            connection.id === selectedConnectionId ? 4 : 3,
          "stroke-linecap": "round"
        });

        if (dash) {
          visibleLine.setAttribute("stroke-dasharray", dash);
        }

        if (connection.arrow) {
          visibleLine.setAttribute(
            "marker-end",
            "url(#arrowhead)"
          );
        }

        group.appendChild(visibleLine);

        group.appendChild(svgEl("line", {
          x1: startX,
          y1: startY,
          x2: endX,
          y2: endY,
          stroke: "transparent",
          "stroke-width": 18,
          "pointer-events": "stroke"
        }));

        if (connection.label) {
          const label = svgEl("text", {
            x: (startX + endX) / 2,
            y: (startY + endY) / 2 - 9,
            "text-anchor": "middle",
            "font-family": "Segoe UI, Arial, sans-serif",
            "font-size": 14,
            "font-weight": 600,
            fill: "#294A65",
            stroke: "#FFFFFF",
            "stroke-width": 5,
            "paint-order": "stroke",
            "pointer-events": "none"
          });

          label.textContent = connection.label;
          group.appendChild(label);
        }

        return group;
      }

      function renderStage() {
        drawingLayer.innerHTML = "";
        connectionLayer.innerHTML = "";
        layer.innerHTML = "";

        currentScene().drawings.forEach(drawing => {
          const path = renderDrawing(drawing);
          if (path) drawingLayer.appendChild(path);
        });

        currentScene().connections.forEach(connection => {
          const rendered = renderConnection(connection);
          if (rendered) connectionLayer.appendChild(rendered);
        });

        currentScene().nodes.forEach(node => {
          layer.appendChild(renderNode(node));
        });

        hint.style.display =
          currentScene().nodes.length ||
          currentScene().connections.length ||
          currentScene().drawings.length
            ? "none"
            : "block";

        grid.setAttribute("opacity", gridOn ? "1" : "0");
      }

      function updateSelectionPanels() {
        const node = findSelectedNode();
        const connection = findSelectedConnection();

        nodePanel.classList.toggle("visible", Boolean(node));
        connectionPanel.classList.toggle(
          "visible",
          Boolean(connection)
        );

        if (node) {
          document.getElementById("node-selection-title").textContent =
            `Выбран образ: ${node.label || "Без подписи"}`;

          document.getElementById("node-label").value =
            node.label || "";

          document.getElementById("node-color").value =
            node.color || "#72A9C8";

          document.getElementById("node-size").value =
            node.size || 1;

          document.getElementById("node-rotation").value =
            node.rotation || 0;
        }

        if (connection) {
          document.getElementById("connection-selection-title").textContent =
            `Связь: ${connection.label || "без подписи"}`;

          document.getElementById("connection-label").value =
            connection.label || "";

          document.getElementById("connection-color").value =
            connection.color || "#688BA7";

          document.getElementById("connection-style").value =
            connection.style || "solid";

          document.getElementById("connection-arrow").checked =
            Boolean(connection.arrow);
        }
      }

      function pointerToSvg(event) {
        const point = stage.createSVGPoint();
        point.x = event.clientX;
        point.y = event.clientY;

        const matrix = stage.getScreenCTM();
        if (!matrix) return {x: 600, y: 380};

        const local = point.matrixTransform(matrix.inverse());

        return {
          x: local.x,
          y: local.y
        };
      }

      function createConnection(fromId, toId) {
        if (fromId === toId) {
          pendingConnectionFrom = null;
          setStatus("Выберите две разные фигуры.");
          renderStage();
          return;
        }

        const duplicate = currentScene().connections.some(
          connection =>
            (
              connection.from === fromId &&
              connection.to === toId
            ) ||
            (
              connection.from === toId &&
              connection.to === fromId
            )
        );

        if (duplicate) {
          pendingConnectionFrom = null;
          connectMode = false;

          document
            .getElementById("connect-toggle")
            .classList.remove("active");

          document.getElementById("connect-toggle").textContent =
            "Создать связь";

          setStatus("Эти фигуры уже соединены.");
          renderStage();
          return;
        }

        const connection = {
          id: `connection_${nextConnectionId++}`,
          from: fromId,
          to: toId,
          label: "",
          color: "#688BA7",
          style: "solid",
          arrow: false
        };

        currentScene().connections.push(connection);
        selectedConnectionId = connection.id;
        selectedId = null;
        pendingConnectionFrom = null;
        connectMode = false;

        document
          .getElementById("connect-toggle")
          .classList.remove("active");

        document.getElementById("connect-toggle").textContent =
          "Создать связь";

        setStatus(
          "Связь создана. Можно добавить подпись и настроить линию."
        );

        renderStage();
        updateSelectionPanels();
      }

      stage.addEventListener("pointerdown", event => {
        if (drawMode) {
          const point = pointerToSvg(event);

          drawingState = {
            id: `drawing_${nextDrawingId++}`,
            points: [point],
            color: document.getElementById("draw-color").value,
            width: Number(
              document.getElementById("draw-width").value
            )
          };

          currentScene().drawings.push(drawingState);
          stage.setPointerCapture(event.pointerId);

          selectedId = null;
          selectedConnectionId = null;
          updateSelectionPanels();

          event.preventDefault();
          return;
        }

        const connectionGroup =
          event.target.closest("[data-connection-id]");

        if (connectionGroup) {
          if (connectMode) return;

          selectedConnectionId =
            connectionGroup.getAttribute("data-connection-id");

          selectedId = null;
          renderStage();
          updateSelectionPanels();
          event.preventDefault();
          return;
        }

        const nodeGroup =
          event.target.closest("[data-node-id]");

        if (connectMode) {
          if (!nodeGroup) {
            pendingConnectionFrom = null;
            setStatus(
              "Связь отменена. Выберите первую фигуру или выключите режим связи."
            );
            renderStage();
            return;
          }

          const nodeId =
            nodeGroup.getAttribute("data-node-id");

          if (!pendingConnectionFrom) {
            pendingConnectionFrom = nodeId;
            selectedId = nodeId;
            selectedConnectionId = null;

            setStatus("Теперь выберите вторую фигуру.");
            renderStage();
            updateSelectionPanels();
          } else {
            createConnection(pendingConnectionFrom, nodeId);
          }

          event.preventDefault();
          return;
        }

        if (!nodeGroup) {
          selectedId = null;
          selectedConnectionId = null;
          renderStage();
          updateSelectionPanels();
          return;
        }

        const nodeId =
          nodeGroup.getAttribute("data-node-id");

        const node = currentScene().nodes.find(
          item => item.id === nodeId
        );

        if (!node) return;

        selectedId = nodeId;
        selectedConnectionId = null;

        const point = pointerToSvg(event);

        dragState = {
          id: nodeId,
          offsetX: point.x - node.x,
          offsetY: point.y - node.y
        };

        stage.setPointerCapture(event.pointerId);
        renderStage();
        updateSelectionPanels();
        event.preventDefault();
      });

      stage.addEventListener("pointermove", event => {
        if (drawMode && drawingState) {
          const point = pointerToSvg(event);
          const points = drawingState.points;
          const previous = points[points.length - 1];

          const distance = Math.hypot(
            point.x - previous.x,
            point.y - previous.y
          );

          if (distance > 2) {
            points.push(point);
            renderStage();
          }

          event.preventDefault();
          return;
        }

        if (!dragState) return;

        const node = currentScene().nodes.find(
          item => item.id === dragState.id
        );

        if (!node) return;

        const point = pointerToSvg(event);

        node.x = Math.max(
          50,
          Math.min(1150, point.x - dragState.offsetX)
        );

        node.y = Math.max(
          55,
          Math.min(705, point.y - dragState.offsetY)
        );

        renderStage();
      });

      function stopPointerAction() {
        if (drawingState) {
          if (drawingState.points.length > 1) {
            drawingUndoStack.push({
              sceneIndex: activeScene,
              drawing: JSON.parse(
                JSON.stringify(drawingState)
              )
            });

            drawingRedoStack = [];
            setStatus("Штрих добавлен. Его можно отменить.");
          } else {
            currentScene().drawings =
              currentScene().drawings.filter(
                item => item.id !== drawingState.id
              );
          }

          drawingState = null;
          renderStage();
        }

        dragState = null;
      }

      stage.addEventListener("pointerup", stopPointerAction);
      stage.addEventListener("pointercancel", stopPointerAction);

      stage.addEventListener("keydown", event => {
        const nodeGroup =
          event.target.closest("[data-node-id]");

        if (
          nodeGroup &&
          ["Enter", " "].includes(event.key)
        ) {
          event.preventDefault();

          selectedId =
            nodeGroup.getAttribute("data-node-id");
          selectedConnectionId = null;

          renderStage();
          updateSelectionPanels();
          return;
        }

        const connectionGroup =
          event.target.closest("[data-connection-id]");

        if (
          connectionGroup &&
          ["Enter", " "].includes(event.key)
        ) {
          event.preventDefault();

          selectedConnectionId =
            connectionGroup.getAttribute("data-connection-id");
          selectedId = null;

          renderStage();
          updateSelectionPanels();
        }
      });

      function undoLastDrawing() {
        if (drawingState) {
          currentScene().drawings =
            currentScene().drawings.filter(
              item => item.id !== drawingState.id
            );

          drawingState = null;
          renderStage();
          setStatus("Текущий штрих отменён.");
          return;
        }

        if (!drawingUndoStack.length) {
          setStatus("Нет штриха для отмены.");
          return;
        }

        const action = drawingUndoStack.pop();
        const scene = scenes[action.sceneIndex];

        if (scene) {
          scene.drawings = scene.drawings.filter(
            drawing => drawing.id !== action.drawing.id
          );

          drawingRedoStack.push(action);
          renderStage();
          setStatus("Последний штрих отменён.");
        }
      }

      function redoLastDrawing() {
        if (!drawingRedoStack.length) {
          setStatus("Нет штриха для повторения.");
          return;
        }

        const action = drawingRedoStack.pop();
        const scene = scenes[action.sceneIndex];

        if (scene) {
          scene.drawings.push(
            JSON.parse(JSON.stringify(action.drawing))
          );

          drawingUndoStack.push(action);
          renderStage();
          setStatus("Штрих восстановлен.");
        }
      }

      document.getElementById("undo-drawing").onclick =
        undoLastDrawing;

      document.getElementById("redo-drawing").onclick =
        redoLastDrawing;

      window.addEventListener("keydown", event => {
        const target = event.target;
        const isTextField =
          target &&
          (
            target.tagName === "INPUT" ||
            target.tagName === "TEXTAREA" ||
            target.tagName === "SELECT" ||
            target.isContentEditable
          );

        if (isTextField) return;

        if (
          (event.ctrlKey || event.metaKey) &&
          event.key.toLowerCase() === "z"
        ) {
          event.preventDefault();
          undoLastDrawing();
        } else if (
          (event.ctrlKey || event.metaKey) &&
          event.key.toLowerCase() === "y"
        ) {
          event.preventDefault();
          redoLastDrawing();
        }
      });

      document.getElementById("draw-toggle").onclick = event => {
        drawMode = !drawMode;

        if (drawMode) {
          connectMode = false;
          pendingConnectionFrom = null;

          document
            .getElementById("connect-toggle")
            .classList.remove("active");

          document.getElementById("connect-toggle").textContent =
            "Создать связь";
        }

        event.target.classList.toggle("active", drawMode);
        event.target.textContent =
          drawMode
            ? "Режим рисования: вкл."
            : "Рисовать";

        instructions.textContent = drawMode
          ? "Режим рисования включён: рисуйте мышью или пальцем прямо на сцене."
          : "Перетаскивайте образы мышью. Для рисования нажмите «Рисовать».";

        setStatus(
          drawMode
            ? "Можно рисовать на доске."
            : "Режим рисования выключен."
        );
      };

      document.getElementById("connect-toggle").onclick = event => {
        connectMode = !connectMode;
        pendingConnectionFrom = null;

        if (connectMode) {
          drawMode = false;

          document
            .getElementById("draw-toggle")
            .classList.remove("active");

          document.getElementById("draw-toggle").textContent =
            "Рисовать";
        }

        event.target.classList.toggle("active", connectMode);
        event.target.textContent =
          connectMode
            ? "Выберите 2 фигуры…"
            : "Создать связь";

        instructions.textContent = connectMode
          ? "Нажмите на первую фигуру, затем на вторую, чтобы соединить их."
          : "Перетаскивайте образы мышью. Для рисования нажмите «Рисовать».";

        setStatus(
          connectMode
            ? "Выберите первую фигуру для связи."
            : "Режим связи выключен."
        );

        renderStage();
      };

      document.getElementById("node-label").addEventListener(
        "input",
        event => {
          const node = findSelectedNode();
          if (!node) return;

          node.label = event.target.value;
          renderStage();

          document.getElementById(
            "node-selection-title"
          ).textContent =
            `Выбран образ: ${node.label || "Без подписи"}`;
        }
      );

      document.getElementById("node-color").addEventListener(
        "input",
        event => {
          const node = findSelectedNode();
          if (!node) return;

          node.color = event.target.value;
          renderStage();
        }
      );

      document.getElementById("node-size").addEventListener(
        "input",
        event => {
          const node = findSelectedNode();
          if (!node) return;

          node.size = Number(event.target.value);
          renderStage();
        }
      );

      document.getElementById("node-rotation").addEventListener(
        "input",
        event => {
          const node = findSelectedNode();
          if (!node) return;

          node.rotation = Number(event.target.value);
          renderStage();
        }
      );

      document.getElementById("delete-node").onclick = () => {
        if (!selectedId) return;

        currentScene().nodes =
          currentScene().nodes.filter(
            node => node.id !== selectedId
          );

        currentScene().connections =
          currentScene().connections.filter(
            connection =>
              connection.from !== selectedId &&
              connection.to !== selectedId
          );

        selectedId = null;
        renderStage();
        updateSelectionPanels();
        setStatus("Образ и связанные с ним линии удалены.");
      };

      document.getElementById("connection-label").addEventListener(
        "input",
        event => {
          const connection = findSelectedConnection();
          if (!connection) return;

          connection.label = event.target.value;
          renderStage();

          document.getElementById(
            "connection-selection-title"
          ).textContent =
            `Связь: ${connection.label || "без подписи"}`;
        }
      );

      document.getElementById("connection-color").addEventListener(
        "input",
        event => {
          const connection = findSelectedConnection();
          if (!connection) return;

          connection.color = event.target.value;
          renderStage();
        }
      );

      document.getElementById("connection-style").addEventListener(
        "change",
        event => {
          const connection = findSelectedConnection();
          if (!connection) return;

          connection.style = event.target.value;
          renderStage();
        }
      );

      document.getElementById("connection-arrow").addEventListener(
        "change",
        event => {
          const connection = findSelectedConnection();
          if (!connection) return;

          connection.arrow = event.target.checked;
          renderStage();
        }
      );

      document.getElementById("delete-connection").onclick = () => {
        if (!selectedConnectionId) return;

        currentScene().connections =
          currentScene().connections.filter(
            connection =>
              connection.id !== selectedConnectionId
          );

        selectedConnectionId = null;
        renderStage();
        updateSelectionPanels();
        setStatus("Связь удалена.");
      };

      document.getElementById("grid-toggle").onclick = event => {
        gridOn = !gridOn;
        event.target.textContent =
          `Сетка: ${gridOn ? "вкл." : "выкл."}`;
        renderStage();
      };

      document.getElementById("clear-drawings").onclick = () => {
        if (!currentScene().drawings.length) return;

        if (!confirm(
          "Удалить все свободные рисунки с текущей сцены?"
        )) return;

        currentScene().drawings = [];
        drawingUndoStack = [];
        drawingRedoStack = [];
        renderStage();
        setStatus("Свободные рисунки удалены.");
      };

      document.getElementById("clear-scene").onclick = () => {
        const scene = currentScene();

        if (
          !scene.nodes.length &&
          !scene.connections.length &&
          !scene.drawings.length
        ) return;

        if (!confirm(
          "Очистить текущую сцену? Это действие нельзя отменить."
        )) return;

        scene.nodes = [];
        scene.connections = [];
        scene.drawings = [];

        drawingUndoStack = [];
        drawingRedoStack = [];
        selectedId = null;
        selectedConnectionId = null;

        renderStage();
        updateSelectionPanels();
        setStatus("Текущая сцена очищена.");
      };

      document.getElementById("add-custom").onclick = () => {
        const type =
          document.getElementById("custom-type").value;

        const label =
          document.getElementById("custom-label").value.trim() ||
          "Мой образ";

        const color =
          document.getElementById("custom-color").value;

        addNode({type, label, color});
        document.getElementById("custom-label").value = "";
      };

      stage.addEventListener("dragover", event => {
        event.preventDefault();
        event.dataTransfer.dropEffect = "copy";
      });

      stage.addEventListener("drop", event => {
        event.preventDefault();

        const poolId =
          event.dataTransfer.getData("text/plain");

        const item = POOL.find(
          entry => entry.id === poolId
        );

        if (!item) return;

        addNode(item, pointerToSvg(event));
      });

      function makeExportSvg() {
        const clone = stage.cloneNode(true);

        clone.setAttribute(
          "xmlns",
          "http://www.w3.org/2000/svg"
        );
        clone.setAttribute("width", "1600");
        clone.setAttribute("height", "1013");

        clone.querySelectorAll(".selection-ring").forEach(
          element => element.remove()
        );

        const dropHint = clone.querySelector("#drop-hint");
        const scene = currentScene();

        if (
          dropHint &&
          (
            scene.nodes.length ||
            scene.connections.length ||
            scene.drawings.length
          )
        ) {
          dropHint.remove();
        }

        return new XMLSerializer().serializeToString(clone);
      }

      function downloadBlob(blob, filename) {
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");

        link.href = url;
        link.download = filename;

        document.body.appendChild(link);
        link.click();
        link.remove();

        setTimeout(() => URL.revokeObjectURL(url), 1200);
      }

      document.getElementById("export-svg").onclick = () => {
        downloadBlob(
          new Blob(
            [makeExportSvg()],
            {type: "image/svg+xml;charset=utf-8"}
          ),
          "psychodrama_scene.svg"
        );

        setStatus("SVG-файл подготовлен для скачивания.");
      };

      document.getElementById("export-png").onclick = () => {
        const url = URL.createObjectURL(
          new Blob(
            [makeExportSvg()],
            {type: "image/svg+xml;charset=utf-8"}
          )
        );

        const image = new Image();

        image.onload = () => {
          const canvas = document.createElement("canvas");
          canvas.width = 1600;
          canvas.height = 1013;

          const context = canvas.getContext("2d");
          context.fillStyle = "#F8FCFF";
          context.fillRect(
            0,
            0,
            canvas.width,
            canvas.height
          );
          context.drawImage(
            image,
            0,
            0,
            canvas.width,
            canvas.height
          );

          canvas.toBlob(blob => {
            if (blob) {
              downloadBlob(blob, "psychodrama_scene.png");
              setStatus("PNG-файл подготовлен для скачивания.");
            }

            URL.revokeObjectURL(url);
          }, "image/png");
        };

        image.onerror = () => {
          URL.revokeObjectURL(url);
          setStatus(
            "Не удалось создать PNG. Попробуйте скачать SVG."
          );
        };

        image.src = url;
      };

      document.getElementById("export-json").onclick = () => {
        const project = {
          version: 4,
          scenes,
          activeScene
        };

        downloadBlob(
          new Blob(
            [JSON.stringify(project, null, 2)],
            {type: "application/json;charset=utf-8"}
          ),
          "psychodrama_project.json"
        );

        setStatus(
          "Файл проекта JSON подготовлен для скачивания."
        );
      };

      const importInput =
        document.getElementById("import-json");

      document.getElementById("import-json-btn").onclick =
        () => importInput.click();

      importInput.addEventListener("change", async event => {
        const file =
          event.target.files && event.target.files[0];

        if (!file) return;

        try {
          const data = JSON.parse(await file.text());

          if (
            !Array.isArray(data.scenes) ||
            !data.scenes.length
          ) {
            throw new Error("В файле нет списка сцен.");
          }

          const allowedTypes =
            new Set(POOL.map(item => item.type));

          scenes = data.scenes.slice(0, 6).map(
            (scene, index) => {
              const nodes = Array.isArray(scene.nodes)
                ? scene.nodes
                    .filter(
                      node =>
                        node &&
                        allowedTypes.has(node.type)
                    )
                    .map(node => ({
                      id: String(
                        node.id || `figure_${nextId++}`
                      ),
                      type: node.type,
                      label: String(node.label || "").slice(0, 60),
                      color:
                        /^#[0-9A-Fa-f]{6}$/.test(node.color)
                          ? node.color
                          : "#72A9C8",
                      size: Math.max(
                        0.65,
                        Math.min(1.6, Number(node.size) || 1)
                      ),
                      rotation: Number(node.rotation) || 0,
                      x: Math.max(
                        50,
                        Math.min(1150, Number(node.x) || 600)
                      ),
                      y: Math.max(
                        55,
                        Math.min(705, Number(node.y) || 380)
                      )
                    }))
                : [];

              const nodeIds =
                new Set(nodes.map(node => node.id));

              const connections =
                Array.isArray(scene.connections)
                  ? scene.connections
                      .filter(
                        connection =>
                          connection &&
                          nodeIds.has(connection.from) &&
                          nodeIds.has(connection.to) &&
                          connection.from !== connection.to
                      )
                      .map(connection => ({
                        id: String(
                          connection.id ||
                          `connection_${nextConnectionId++}`
                        ),
                        from: connection.from,
                        to: connection.to,
                        label: String(
                          connection.label || ""
                        ).slice(0, 80),
                        color:
                          /^#[0-9A-Fa-f]{6}$/.test(connection.color)
                            ? connection.color
                            : "#688BA7",
                        style:
                          ["solid", "dashed", "dotted"].includes(
                            connection.style
                          )
                            ? connection.style
                            : "solid",
                        arrow: Boolean(connection.arrow)
                      }))
                  : [];

              const drawings =
                Array.isArray(scene.drawings)
                  ? scene.drawings
                      .filter(
                        drawing =>
                          drawing &&
                          Array.isArray(drawing.points)
                      )
                      .map(drawing => ({
                        id: String(
                          drawing.id ||
                          `drawing_${nextDrawingId++}`
                        ),
                        color:
                          /^#[0-9A-Fa-f]{6}$/.test(drawing.color)
                            ? drawing.color
                            : "#587E9A",
                        width: Math.max(
                          2,
                          Math.min(18, Number(drawing.width) || 5)
                        ),
                        points: drawing.points
                          .filter(
                            point =>
                              point &&
                              Number.isFinite(Number(point.x)) &&
                              Number.isFinite(Number(point.y))
                          )
                          .map(point => ({
                            x: Math.max(
                              0,
                              Math.min(1200, Number(point.x))
                            ),
                            y: Math.max(
                              0,
                              Math.min(760, Number(point.y))
                            )
                          }))
                      }))
                  : [];

              return {
                name: String(
                  scene.name || `Сцена ${index + 1}`
                ).slice(0, 40),
                nodes,
                connections,
                drawings
              };
            }
          );

          if (!scenes.length) {
            scenes = [{
              name: "Сцена 1",
              nodes: [],
              connections: [],
              drawings: []
            }];
          }

          activeScene = Math.max(
            0,
            Math.min(
              scenes.length - 1,
              Number(data.activeScene) || 0
            )
          );

          selectedId = null;
          selectedConnectionId = null;
          pendingConnectionFrom = null;
          drawingState = null;
          drawingUndoStack = [];
          drawingRedoStack = [];

          nextId += 1;
          nextConnectionId += 1;
          nextDrawingId += 1;

          renderSceneTabs();
          renderStage();
          updateSelectionPanels();
          setStatus("Проект загружен.");
        } catch (error) {
          setStatus(
            `Не удалось открыть проект: ${error.message}`
          );
        } finally {
          importInput.value = "";
        }
      });

      renderTabs();
      renderPool();
      renderSceneTabs();
      renderStage();
    })();
  </script>
</body>
</html>
"""


def render_psychodrama():
    st.title("Психодрама: интерактивная сцена")
    st.write(
        "Выбирайте образы, размещайте их на сцене, соединяйте линиями "
        "и дорисовывайте детали от руки."
    )

    st.info(
        "Это визуальный инструмент для исследования ситуации, а не диагностика. "
        "Образы, рисунки, линии, цвет и положение не интерпретируются автоматически. "
        "Вы сами выбираете значение образов и подписей; упражнение можно остановить "
        "в любой момент."
    )

    components.html(
        APP_HTML.replace(
            "__POOL_JSON__",
            json.dumps(POOL, ensure_ascii=False),
        ),
        height=1120,
        scrolling=False,
    )


# ---------------------------------------------------------------------
# Запуск приложения и роутинг
# ---------------------------------------------------------------------

def render_selected_technique():
    technique_id = st.session_state.selected_technique

    renderers = {
        "decision_tree": render_decision_tree,
        "dbt_chain": render_chain,
        "exposure": render_exposure,
        "act_matrix": render_act_matrix,
        "psychodrama": render_psychodrama,
    }

    renderer = renderers.get(technique_id)
    if renderer:
        renderer()
    else:
        st.warning("Техника не найдена.")


# Сама точка входа в приложение
render_header()

if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "library":
    render_library()
elif st.session_state.page == "about":
    render_about()
elif st.session_state.page == "technique":
    render_selected_technique()
else:
    st.session_state.page = "home"
    render_home()
