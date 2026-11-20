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
    target = {
        "page": page,
        "technique": technique_id,
    }

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
            items[start:start + 2],
        ):
            with column:
                with st.container(border=True):
                    st.markdown(f"### {technique['title']}")
                    st.write(technique["short"])
                    st.caption(
                        f"{technique['category']} · "
                        f"{technique['description']}"
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

    render_technique_cards(
        list(TECHNIQUES.items())[:4],
        "home_featured",
    )

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
                    st.image(
                        str(photo_path),
                        use_container_width=True,
                    )
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
# Общие функции визуализации SVG
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
        lines[-1] = lines[-1][:max_chars - 1] + "…"

    color = color or SVG_COLORS["text"]
    tspans = []

    for index, item in enumerate(lines):
        dy = 0 if index == 0 else size + 4
        tspans.append(
            f'<tspan x="{x}" dy="{dy}">'
            f'{html.escape(item)}'
            f'</tspan>'
        )

    return (
        f'<text x="{x}" y="{y}" '
        f'font-family="Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" '
        f'fill="{color}">'
        f'{"".join(tspans)}'
        f'</text>'
    )


def make_svg(width, height, title, body, accent="#D9EEFA"):
    gradient_id = f"bgGrad_{accent.replace('#', '')}"

    return f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{width}" height="{height}"
         viewBox="0 0 {width} {height}">
      <defs>
        <linearGradient id="{gradient_id}" x1="0%" x2="100%"
                        y1="0%" y2="100%">
          <stop offset="0%" stop-color="#F8FCFF"/>
          <stop offset="100%" stop-color="#EAF5FC"/>
        </linearGradient>
        <filter id="softShadow" x="-20%" y="-20%"
                width="140%" height="140%">
          <feDropShadow dx="0" dy="6" stdDeviation="8"
                        flood-color="#7AAEC7"
                        flood-opacity="0.16"/>
        </filter>
      </defs>

      <rect width="100%" height="100%"
            fill="url(#{gradient_id})" rx="18"/>

      {svg_text(
          32,
          45,
          title,
          size=25,
          weight=700,
          color=SVG_COLORS["ink"],
          max_chars=80,
          max_lines=1,
      )}

      <g id="scene" filter="url(#softShadow)">
        {body}
      </g>
    </svg>
    """


def render_visualization(svg, filename, caption):
    # ИСПРАВЛЕНИЕ: заменено st.subcaption на st.caption
    st.caption(caption)
    svg_name = json.dumps(filename)
    png_name = json.dumps(filename.rsplit(".", 1)[0] + ".png")

    html_doc = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        * {{ box-sizing:border-box }}
        html,body {{
          margin:0;
          font:14px Arial,sans-serif;
          color:#234D6B;
        }}
        .toolbar {{
          display:flex;
          gap:8px;
          flex-wrap:wrap;
          align-items:center;
          padding:8px;
          background:#F3F9FD;
          border:1px solid #D4E6F2;
          border-radius:12px 12px 0 0;
        }}
        button {{
          border:1px solid #AFCFE2;
          border-radius:8px;
          background:#FFFFFF;
          color:#315773;
          padding:7px 11px;
          cursor:pointer;
          font-weight:600;
        }}
        #zoom-label {{ min-width:48px;text-align:center }}
        .viewport {{
          width:100%;
          height:520px;
          overflow:auto;
          border:1px solid #D4E6F2;
          border-top:0;
          border-radius:0 0 12px 12px;
          background:#FFFFFF;
          cursor:grab;
          touch-action:none;
        }}
        .viewport.dragging {{ cursor:grabbing }}
        .viewport svg {{
          display:block;
          max-width:none!important;
          height:auto;
          user-select:none;
        }}
        .viewport svg text {{
          pointer-events:none;
          user-select:none;
        }}
      </style>
    </head>
    <body>
      <div class="toolbar">
        <button id="minus" type="button">−</button>
        <button id="plus" type="button">+</button>
        <button id="reset" type="button">Сбросить вид</button>
        <span id="zoom-label">100%</span>
        <button id="save-svg" type="button">Скачать SVG</button>
        <button id="save-png" type="button">Скачать PNG</button>
      </div>

      <div class="viewport" id="viewport">
        {svg}
      </div>

      <script>
        (() => {{
          const viewport =
            document.getElementById("viewport");
          const svg =
            viewport.querySelector("svg");
          const label =
            document.getElementById("zoom-label");

          if (!svg) return;

          const baseWidth =
            Number(svg.getAttribute("width"));
          const baseHeight =
            Number(svg.getAttribute("height"));

          let scale = 1;
          let drag = null;

          function applyScale() {{
            svg.style.width =
              (baseWidth * scale) + "px";
            svg.style.height =
              (baseHeight * scale) + "px";
            label.textContent =
              Math.round(scale * 100) + "%";
          }}

          function fitToViewport() {{
            const available =
              Math.max(320, viewport.clientWidth - 8);
            scale =
              Math.min(1, available / baseWidth);
            applyScale();
          }}

          document.getElementById("plus").onclick =
            () => {{
              scale = Math.min(3, scale * 1.2);
              applyScale();
            }};

          document.getElementById("minus").onclick =
            () => {{
              scale = Math.max(0.35, scale / 1.2);
              applyScale();
            }};

          document.getElementById("reset").onclick =
            () => {{
              fitToViewport();
              viewport.scrollTo({{ left:0, top:0 }});
            }};

          viewport.addEventListener(
            "pointerdown",
            event => {{
              drag = {{
                x:event.clientX,
                y:event.clientY,
                left:viewport.scrollLeft,
                top:viewport.scrollTop,
              }};
              viewport.classList.add("dragging");
              viewport.setPointerCapture(
                event.pointerId
              );
            }}
          );

          viewport.addEventListener(
            "pointermove",
            event => {{
              if (!drag) return;

              viewport.scrollLeft =
                drag.left -
                (event.clientX - drag.x);

              viewport.scrollTop =
                drag.top -
                (event.clientY - drag.y);
            }}
          );

          function endDrag() {{
            drag = null;
            viewport.classList.remove("dragging");
          }}

          viewport.addEventListener(
            "pointerup",
            endDrag
          );

          viewport.addEventListener(
            "pointercancel",
            endDrag
          );

          function serializeSvg() {{
            const clone =
              svg.cloneNode(true);

            clone.setAttribute(
              "xmlns",
              "http://www.w3.org/2000/svg"
            );

            clone.style.width = "";
            clone.style.height = "";

            return new XMLSerializer()
              .serializeToString(clone);
          }}

          function download(blob, name) {{
            const url =
              URL.createObjectURL(blob);

            const link =
              document.createElement("a");

            link.href = url;
            link.download = name;
            link.click();

            setTimeout(
              () => URL.revokeObjectURL(url),
              1000
            );
          }}

          document
            .getElementById("save-svg")
            .onclick = () => {{
              download(
                new Blob(
                  [serializeSvg()],
                  {{
                    type:
                      "image/svg+xml;charset=utf-8"
                  }}
                ),
                {svg_name}
              );
            }};

          document
            .getElementById("save-png")
            .onclick = () => {{
              const url =
                URL.createObjectURL(
                  new Blob(
                    [serializeSvg()],
                    {{
                      type:
                        "image/svg+xml;charset=utf-8"
                    }}
                  )
                );

              const image = new Image();

              image.onload = () => {{
                const canvas =
                  document.createElement("canvas");

                canvas.width =
                  baseWidth * 2;
                canvas.height =
                  baseHeight * 2;

                const context =
                  canvas.getContext("2d");

                context.fillStyle =
                  "#F7FBFF";

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

                canvas.toBlob(
                  blob => {{
                    if (blob) {{
                      download(
                        blob,
                        {png_name}
                      );
                    }}

                    URL.revokeObjectURL(url);
                  }},
                  "image/png"
                );
              }};

              image.onerror =
                () => URL.revokeObjectURL(url);

              image.src = url;
            }};

          fitToViewport();
          window.addEventListener(
            "resize",
            fitToViewport
          );
        }})();
      </script>
    </body>
    </html>
    """

    components.html(
        html_doc,
        height=590,
        scrolling=False,
    )


# ---------------------------------------------------------------------
# Дерево решений
# ---------------------------------------------------------------------

def add_decision_option():
    existing = list(
        st.session_state.get("decision_option_ids", [0, 1])
    )
    next_id = int(
        st.session_state.get("decision_next_option_id", 2)
    )
    existing.append(next_id)
    st.session_state.decision_option_ids = existing
    st.session_state.decision_next_option_id = next_id + 1
    st.session_state[
        f"decision_scenario_ids_{next_id}"
    ] = [0]
    st.session_state[
        f"decision_next_scenario_id_{next_id}"
    ] = 1


def remove_decision_option(option_id):
    ids = list(
        st.session_state.get("decision_option_ids", [0, 1])
    )

    if len(ids) > 2 and option_id in ids:
        ids.remove(option_id)
        st.session_state.decision_option_ids = ids
        st.session_state.pop(
            f"decision_scenario_ids_{option_id}",
            None,
        )
        st.session_state.pop(
            f"decision_next_scenario_id_{option_id}",
            None,
        )


def add_decision_scenario(option_id):
    key = f"decision_scenario_ids_{option_id}"
    ids = list(st.session_state.get(key, [0]))
    next_id = int(
        st.session_state.get(
            f"decision_next_scenario_id_{option_id}",
            1,
        )
    )
    ids.append(next_id)
    st.session_state[key] = ids
    st.session_state[
        f"decision_next_scenario_id_{option_id}"
    ] = next_id + 1


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
        "Опишите варианты решения, возможные сценарии и "
        "удовлетворённость каждым исходом."
    )
    st.caption(
        "Вероятности сценариев внутри каждого варианта должны "
        "составлять 100%. Удовлетворённость оценивается по шкале "
        "от −5 до +5."
    )

    question = st.text_input(
        "Какое решение нужно принять?",
        key="decision_question",
        placeholder="Например: Стоит ли менять работу?",
    )

    if "decision_option_ids" not in st.session_state:
        st.session_state.decision_option_ids = [0, 1]
        st.session_state.decision_next_option_id = 2

    option_ids = list(
        st.session_state.decision_option_ids
    )
    options = []

    for option_number, option_id in enumerate(
        option_ids,
        start=1,
    ):
        scenario_key = (
            f"decision_scenario_ids_{option_id}"
        )

        if scenario_key not in st.session_state:
            st.session_state[scenario_key] = [0]
            st.session_state[
                f"decision_next_scenario_id_{option_id}"
            ] = 1

        scenario_ids = list(
            st.session_state[scenario_key]
        )

        with st.container(border=True):
            option_header, option_delete = st.columns(
                [5, 1]
            )

            with option_header:
                st.markdown(
                    f"### Вариант {option_number}"
                )

            with option_delete:
                if len(option_ids) > 2:
                    st.button(
                        "Удалить вариант",
                        key=(
                            "decision_remove_option_"
                            f"{option_id}"
                        ),
                        on_click=remove_decision_option,
                        args=(option_id,),
                        help=(
                            "Удалить этот вариант "
                            "и его сценарии"
                        ),
                    )

            option_name = st.text_input(
                "Название варианта",
                key=f"decision_name_{option_id}",
                placeholder=f"Вариант {option_number}",
            )

            scenarios = []

            for scenario_number, scenario_id in enumerate(
                scenario_ids,
                start=1,
            ):
                with st.expander(
                    f"Сценарий {scenario_number}",
                    expanded=(scenario_number == 1),
                ):
                    scenario_title = st.text_input(
                        "Название сценария",
                        key=(
                            "decision_scenario_title_"
                            f"{option_id}_{scenario_id}"
                        ),
                        placeholder=(
                            "Например: адаптация "
                            "проходит успешно"
                        ),
                    )

                    scenario_outcome = st.text_area(
                        "Что может произойти?",
                        key=(
                            "decision_scenario_outcome_"
                            f"{option_id}_{scenario_id}"
                        ),
                    )

                    scenario_probability = st.slider(
                        "Вероятность, %",
                        min_value=0,
                        max_value=100,
                        value=(
                            100
                            if len(scenario_ids) == 1
                            else 0
                        ),
                        key=(
                            "decision_scenario_probability_"
                            f"{option_id}_{scenario_id}"
                        ),
                    )

                    scenario_satisfaction = st.slider(
                        "Удовлетворённость исходом",
                        min_value=-5.0,
                        max_value=5.0,
                        value=0.0,
                        step=0.5,
                        key=(
                            "decision_scenario_"
                            "satisfaction_"
                            f"{option_id}_{scenario_id}"
                        ),
                    )

                    if len(scenario_ids) > 1:
                        st.button(
                            "Удалить этот сценарий",
                            key=(
                                "decision_remove_scenario_"
                                f"{option_id}_{scenario_id}"
                            ),
                            on_click=remove_decision_scenario,
                            args=(option_id, scenario_id),
                        )

                    scenarios.append(
                        {
                            "title": scenario_title,
                            "outcome": scenario_outcome,
                            "probability":
                                scenario_probability,
                            "satisfaction":
                                scenario_satisfaction,
                        }
                    )

            probability_total = sum(
                scenario["probability"]
                for scenario in scenarios
            )

            st.caption(
                "Сумма вероятностей сценариев: "
                f"{probability_total}%"
            )

            if probability_total != 100:
                st.warning(
                    "Для расчёта сумма вероятностей "
                    "сценариев этого варианта должна "
                    "составлять 100%."
                )

            if len(scenario_ids) < 8:
                st.button(
                    "＋ Добавить сценарий",
                    key=(
                        "decision_add_scenario_"
                        f"{option_id}"
                    ),
                    on_click=add_decision_scenario,
                    args=(option_id,),
                )

            options.append(
                {
                    "id": option_id,
                    "name": option_name,
                    "scenarios": scenarios,
                    "probability_total":
                        probability_total,
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
        and all(
            option["name"].strip()
            for option in options
        )
        and all(
            option["probability_total"] == 100
            for option in options
        )
        and all(
            scenario["title"].strip()
            for option in options
            for scenario in option["scenarios"]
        )
    )

    if not ready:
        st.info(
            "Заполните вопрос, названия вариантов "
            "и сценариев. Для каждого варианта "
            "распределите вероятности так, чтобы "
            "их сумма была 100%. "
            "Сравнение обновится автоматически."
        )
        return

    for option in options:
        option["expected"] = sum(
            scenario["probability"]
            * scenario["satisfaction"]
            for scenario in option["scenarios"]
        ) / 100

    best_score = max(
        option["expected"]
        for option in options
    )

    best_option_ids = {
        option["id"]
        for option in options
        if abs(
            option["expected"] - best_score
        ) < 1e-9
    }

    st.subheader("Сравнение вариантов")
    metric_columns = st.columns(len(options))

    for column, option in zip(
        metric_columns,
        options,
    ):
        with column:
            st.metric(
                option["name"],
                f'{option["expected"]:.2f} / 5',
                help=(
                    "Средняя удовлетворённость "
                    "с учётом вероятностей "
                    "сценариев."
                ),
            )

            if option["id"] in best_option_ids:
                st.success(
                    "Наиболее подходящий "
                    "по введённым оценкам"
                )

    st.info(
        "Расчёт — ориентир по вашим оценкам "
        "и вероятностям, а не решение за вас."
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
    max_scenarios = max(
        len(option["scenarios"])
        for option in options
    )
    chart_width = (
        50
        + len(options) * column_width
    )
    option_y = (
        120
        + max_scenarios * scenario_height
    )
    root_y = option_y + 132
    chart_height = root_y + 120
    body = ""

    for index, option in enumerate(options):
        x = (
            25
            + index * column_width
        )
        card_x = x + 48
        card_width = 360
        branch_x = x + 24

        centers = [
            92
            + scenario_index * scenario_height
            + 56
            for scenario_index
            in range(
                len(option["scenarios"])
            )
        ]

        if centers:
            body += (
                f'<line '
                f'x1="{branch_x}" '
                f'y1="{min(centers)}" '
                f'x2="{branch_x}" '
                f'y2="{option_y}" '
                f'stroke="{palette["branch"]}" '
                f'stroke-width="3"/>'
            )

            for center_y in centers:
                body += (
                    f'<line '
                    f'x1="{branch_x}" '
                    f'y1="{center_y}" '
                    f'x2="{card_x}" '
                    f'y2="{center_y}" '
                    f'stroke="{palette["branch"]}" '
                    f'stroke-width="3"/>'
                )

        body += (
            f'<line '
            f'x1="{card_x + card_width / 2}" '
            f'y1="{option_y + 78}" '
            f'x2="{chart_width / 2}" '
            f'y2="{root_y}" '
            f'stroke="{palette["branch"]}" '
            f'stroke-width="3"/>'
        )

    for index, option in enumerate(options):
        x = (
            25
            + index * column_width
        )
        card_x = x + 48
        card_width = 360

        for scenario_index, scenario in enumerate(
            option["scenarios"]
        ):
            y = (
                92
                + scenario_index
                * scenario_height
            )

            body += (
                f'<rect '
                f'x="{card_x}" '
                f'y="{y}" '
                f'width="{card_width}" '
                f'height="112" '
                f'rx="15" '
                f'fill="{palette["scenario_fill"]}" '
                f'stroke="{palette["scenario_border"]}" '
                f'stroke-width="2"/>'
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
                (
                    f'Вероятность '
                    f'{scenario["probability"]}% · '
                    f'удовлетворённость '
                    f'{scenario["satisfaction"]:+.1f}'
                ),
                size=14,
                color=color_for_satisfaction(
                    scenario["satisfaction"]
                ),
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

        is_best = (
            option["id"]
            in best_option_ids
        )

        fill = (
            palette["best_fill"]
            if is_best
            else palette["option_fill"]
        )

        border = (
            palette["best_border"]
            if is_best
            else palette["option_border"]
        )

        title = (
            f'★ {option["name"]}'
            if is_best
            else option["name"]
        )

        body += (
            f'<rect '
            f'x="{card_x}" '
            f'y="{option_y}" '
            f'width="{card_width}" '
            f'height="78" '
            f'rx="16" '
            f'fill="{fill}" '
            f'stroke="{border}" '
            f'stroke-width="2.5"/>'
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
            (
                "Ожидаемая "
                "удовлетворённость: "
                f'{option["expected"]:.2f}'
            ),
            size=14,
            color=palette["muted"],
            max_chars=42,
            max_lines=1,
        )

    root_width = min(
        600,
        chart_width - 60,
    )
    root_x = (
        chart_width - root_width
    ) / 2

    body += (
        f'<rect '
        f'x="{root_x}" '
        f'y="{root_y}" '
        f'width="{root_width}" '
        f'height="78" '
        f'rx="18" '
        f'fill="{palette["root_fill"]}" '
        f'stroke="{palette["root_border"]}" '
        f'stroke-width="2.5"/>'
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
        (
            "Схема читается снизу вверх: "
            "решение → варианты → сценарии. "
            "Зелёным отмечен вариант с "
            "наибольшей взвешенной оценкой."
        ),
    )


# ---------------------------------------------------------------------
# Цепочный анализ поведения (ДБТ)
# ---------------------------------------------------------------------

def render_chain():
    st.title(
        "Цепочный анализ поведения (ДБТ)"
    )
    st.write(
        "Восстановите провоцирующее событие, "
        "последовательность звеньев, последствия "
        "и возможные места для навыков или поддержки."
    )
    st.info(
        "Можно пропустить поле или остановиться "
        "в любой момент. Если есть непосредственная "
        "опасность для вас или другого человека, "
        "обратитесь за срочной помощью к местным "
        "службам или специалисту."
    )

    vulnerability = st.text_area(
        "Факторы уязвимости",
        key="chain_vulnerability",
        placeholder=(
            "Например: недосып, стресс, "
            "боль, конфликт"
        ),
    )

    trigger = st.text_area(
        "Провоцирующее событие",
        key="chain_trigger",
        placeholder=(
            "Последнее событие, запустившее "
            "последовательность"
        ),
    )

    target = st.text_area(
        "Проблемное поведение, которое анализируем",
        key="chain_target",
        placeholder=(
            "Опишите конкретно, что произошло, "
            "без оценочных ярлыков"
        ),
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
            f"Звено {index + 1}: "
            "что произошло дальше?",
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
                    key=(
                        "chain_intervention_"
                        f"{index}"
                    ),
                )

            skill = st.text_input(
                "Навык или поддержка для этой точки",
                key=f"chain_skill_{index}",
                placeholder=(
                    "Например: пауза, заземление, "
                    "обратиться за поддержкой"
                ),
            )

            links.append(
                {
                    "thought": thought,
                    "emotion": emotion,
                    "urge": urge,
                    "body": body,
                    "action": action,
                    "intervention":
                        intervention,
                    "skill": skill,
                }
            )

    left, right = st.columns(2)

    with left:
        immediate = st.text_area(
            "Последствия сразу после "
            "(для себя и других)",
            key="chain_immediate",
        )

        immediate_reinforcement = st.text_area(
            "Что могло подкрепить "
            "поведение сразу?",
            key=(
                "chain_immediate_"
                "reinforcement"
            ),
        )

    with right:
        later = st.text_area(
            "Отсроченные последствия",
            key="chain_later",
        )

        later_reinforcement = st.text_area(
            "Что могло поддержать "
            "повторение поведения?",
            key=(
                "chain_later_"
                "reinforcement"
            ),
        )

    prevention = st.text_area(
        "План профилактики на будущее",
        key="chain_prevention",
        placeholder=(
            "Какие уязвимости можно уменьшить? "
            "Что подготовить заранее?"
        ),
    )

    repair = st.text_area(
        "Восстановление / исправление "
        "последствий, если необходимо",
        key="chain_repair",
    )

    if st.button(
        "Сформировать карту цепочки",
        key="chain_build",
        type="primary",
        use_container_width=True,
    ):
        if not target.strip():
            st.warning(
                "Опишите поведение, "
                "которое анализируете."
            )
            st.session_state.pop(
                "result_dbt_chain",
                None,
            )
        else:
            st.session_state.result_dbt_chain = {
                "vulnerability":
                    vulnerability,
                "trigger": trigger,
                "target": target,
                "links": links,
                "immediate": immediate,
                "immediate_reinforcement":
                    immediate_reinforcement,
                "later": later,
                "later_reinforcement":
                    later_reinforcement,
                "prevention": prevention,
                "repair": repair,
            }

    result = st.session_state.get(
        "result_dbt_chain"
    )

    if not result:
        return

    st.subheader(
        "Сводка цепочки и анализа решений"
    )

    for title, value in [
        (
            "Факторы уязвимости",
            result["vulnerability"],
        ),
        (
            "Провоцирующее событие",
            result["trigger"],
        ),
        (
            "Проблемное поведение",
            result["target"],
        ),
        (
            "Последствия сразу",
            result["immediate"],
        ),
        (
            "Что подкрепляло поведение",
            result[
                "immediate_reinforcement"
            ],
        ),
        (
            "Отсроченные последствия",
            result["later"],
        ),
        (
            "План профилактики",
            result["prevention"],
        ),
        (
            "Восстановление",
            result["repair"],
        ),
    ]:
        st.markdown(
            f"**{title}:** "
            f"{value or '—'}"
        )

    for index, link in enumerate(
        result["links"],
        start=1,
    ):
        with st.expander(
            f"Содержание звена {index}",
            expanded=False,
        ):
            st.write(
                f'Мысль: '
                f'{link["thought"] or "—"} · '
                f'Эмоция: '
                f'{link["emotion"] or "—"} · '
                f'Импульс: '
                f'{link["urge"] or "—"} · '
                f'Ощущения: '
                f'{link["body"] or "—"}'
            )

            st.write(
                f'Действие: '
                f'{link["action"] or "—"}'
            )

            st.write(
                f'Точка вмешательства: '
                f'{link["intervention"] or "—"} · '
                f'Навык/поддержка: '
                f'{link["skill"] or "—"}'
            )

    width = 1200
    top_card_y = 82
    top_card_w = 360
    top_card_h = 94
    chain_y = 220
    row_height = 152
    chain_card_h = 128
    footer_gap = 24
    footer_y = (
        chain_y
        + len(result["links"]) * row_height
        + footer_gap
    )
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

    for x, (label, value, fill) in zip(
        card_xs,
        top_cards,
    ):
        body += (
            f'<rect '
            f'x="{x}" '
            f'y="{top_card_y}" '
            f'width="{top_card_w}" '
            f'height="{top_card_h}" '
            f'rx="16" '
            f'fill="{fill}" '
            f'stroke="#C8BDE0" '
            f'stroke-width="2"/>'
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
        f'<line '
        f'x1="{width // 2}" '
        f'y1="{top_card_y + top_card_h}" '
        f'x2="{width // 2}" '
        f'y2="{chain_y - 16}" '
        f'stroke="{dbt_palette["line"]}" '
        f'stroke-width="4"/>'
    )

    for index, link in enumerate(
        result["links"]
    ):
        y = (
            chain_y
            + index * row_height
        )

        fill = (
            dbt_palette["link_a"]
            if index % 2 == 0
            else dbt_palette["link_b"]
        )

        body += (
            f'<rect '
            f'x="40" '
            f'y="{y}" '
            f'width="1120" '
            f'height="{chain_card_h}" '
            f'rx="17" '
            f'fill="{fill}" '
            f'stroke="#B6A8D8" '
            f'stroke-width="2"/>'
        )

        body += (
            f'<rect '
            f'x="40" '
            f'y="{y}" '
            f'width="10" '
            f'height="{chain_card_h}" '
            f'rx="5" '
            f'fill="{dbt_palette["line"]}"/>'
        )

        body += (
            f'<circle '
            f'cx="82" '
            f'cy="{y + 36}" '
            f'r="22" '
            f'fill="#FFFFFF" '
            f'stroke="{dbt_palette["line"]}" '
            f'stroke-width="2"/>'
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
            (
                f'Мысль: {link["thought"]} · '
                f'Эмоция: {link["emotion"]} · '
                f'Импульс: {link["urge"]}'
            ),
            size=15,
            color=dbt_palette["text"],
            max_chars=112,
            max_lines=1,
        )

        body += svg_text(
            120,
            y + 65,
            (
                f'Ощущения: {link["body"]} · '
                f'Действие: {link["action"]}'
            ),
            size=15,
            color=dbt_palette["text"],
            max_chars=112,
            max_lines=1,
        )

        body += svg_text(
            120,
            y + 99,
            (
                f'Точка вмешательства: '
                f'{link["intervention"]} · '
                f'Навык: {link["skill"]}'
            ),
            size=15,
            color=dbt_palette["ink"],
            max_chars=112,
            max_lines=1,
        )

        if index < len(result["links"]) - 1:
            body += (
                f'<line '
                f'x1="{width // 2}" '
                f'y1="{y + chain_card_h}" '
                f'x2="{width // 2}" '
                f'y2="{y + row_height}" '
                f'stroke="{dbt_palette["line"]}" '
                f'stroke-width="4"/>'
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
            "ПЛАН ПРОФИЛАКТИКИ "
            "И ВОССТАНОВЛЕНИЯ",
            (
                f'{result["prevention"]} · '
                f'{result["repair"]}'
            ),
            dbt_palette["repair"],
        ),
    ]

    footer_card_w = 360
    footer_card_h = 108

    for x, (label, value, fill) in zip(
        card_xs,
        footer_cards,
    ):
        body += (
            f'<rect '
            f'x="{x}" '
            f'y="{footer_y}" '
            f'width="{footer_card_w}" '
            f'height="{footer_card_h}" '
            f'rx="16" '
            f'fill="{fill}" '
            f'stroke="#C8BDE0" '
            f'stroke-width="2"/>'
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
        (
            "Цветовая карта показывает уязвимости, "
            "запуск события, последовательность "
            "звеньев и последствия."
        ),
    )


# ---------------------------------------------------------------------
# Иерархия экспозиции
# ---------------------------------------------------------------------

def render_exposure():
    st.title("Иерархия экспозиции")
    st.write(
        "Составьте добровольную лестницу практики. До практики "
        "зафиксируйте прогноз, а после — наблюдаемый исход."
    )
    st.info(
        "Практикуйте только добровольно и в безопасных ситуациях; "
        "не используйте экспозицию для реальной опасности."
    )

    goal = st.text_area(
        "Цель / ситуация для работы",
        key="exposure_goal",
    )

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
        with st.expander(
            f"Ступень {index + 1}",
            expanded=(index < 2),
        ):
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
                    "Что вы узнали?",
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
        completed = [
            step
            for step in steps
            if step["situation"].strip()
        ]

        if not completed:
            st.warning(
                "Добавьте описание хотя бы одной ступени."
            )
            st.session_state.pop(
                "result_exposure",
                None,
            )
        else:
            completed.sort(
                key=lambda step: step["expected"]
            )
            st.session_state.result_exposure = {
                "goal": goal,
                "steps": completed,
            }

    result = st.session_state.get(
        "result_exposure"
    )

    if not result:
        return

    st.subheader(
        "Лестница: от меньшей тревоги к большей"
    )

    for index, step in enumerate(
        result["steps"],
        start=1,
    ):
        with st.container(border=True):
            st.markdown(
                f'**{index}. '
                f'{step["situation"]}** · '
                f'ожидаемая тревога '
                f'{step["expected"]}/10'
            )

            if step["prediction"]:
                st.write(
                    f'Прогноз: '
                    f'{step["prediction"]}'
                )

            if step["plan"]:
                st.write(
                    f'План: {step["plan"]}'
                )

            if step["practiced"]:
                st.write(
                    f'Практика: начало '
                    f'{step["start"]}/10, '
                    f'максимум '
                    f'{step["peak"]}/10, '
                    f'после '
                    f'{step["after"]}/10.'
                )

                if step["outcome"]:
                    st.write(
                        "Наблюдаемый исход: "
                        f'{step["outcome"]}'
                    )

                if step["learning"]:
                    st.write(
                        "Вывод / следующий шаг: "
                        f'{step["learning"]}'
                    )

    width = 1280
    row_height = 128
    height = (
        145
        + len(result["steps"]) * row_height
    )

    palette = {
        "ink": "#174F58",
        "text": "#356B70",
        "line": "#63B8B1",
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

    for index in range(
        len(result["steps"]) - 1
    ):
        y1 = (
            122
            + index * row_height
            + 62
        )
        y2 = (
            122
            + (index + 1) * row_height
            + 62
        )

        body += (
            f'<path d="M75 {y1} '
            f'C125 {y1}, 125 {y2}, '
            f'175 {y2}" '
            f'fill="none" '
            f'stroke="{palette["line"]}" '
            f'stroke-width="5" '
            f'stroke-linecap="round"/>'
        )

    for index, step in enumerate(
        result["steps"]
    ):
        y = (
            122
            + index * row_height
        )
        x = 165 + index * 34
        card_width = 490
        score = int(step["expected"])

        if score <= 3:
            level_fill = "#E1F5EF"
            level_border = "#65B89C"
            level_label = "Низкая нагрузка"
        elif score <= 6:
            level_fill = "#FFF3D9"
            level_border = "#E0AE4D"
            level_label = "Средняя нагрузка"
        else:
            level_fill = "#FCE8E5"
            level_border = "#D98575"
            level_label = "Высокая нагрузка"

        body += (
            f'<circle '
            f'cx="75" '
            f'cy="{y + 34}" '
            f'r="26" '
            f'fill="{level_fill}" '
            f'stroke="{level_border}" '
            f'stroke-width="3"/>'
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
            f'<rect '
            f'x="{x}" '
            f'y="{y}" '
            f'width="{card_width}" '
            f'height="104" '
            f'rx="17" '
            f'fill="#FFFFFF" '
            f'stroke="{level_border}" '
            f'stroke-width="2.5"/>'
        )

        body += (
            f'<rect '
            f'x="{x}" '
            f'y="{y}" '
            f'width="12" '
            f'height="104" '
            f'rx="6" '
            f'fill="{level_border}"/>'
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
            (
                f'Ожидаемая тревога '
                f'{step["expected"]}/10 · '
                f'{level_label}'
            ),
            size=14,
            color=palette["text"],
            max_chars=55,
            max_lines=1,
        )

        if step["practiced"]:
            # ИСПРАВЛЕНИЕ: Исправлен SyntaxError (сломанная f-строка)
            body += svg_text(
                x + 28,
                y + 83,
                (
                    f'После практики: {step["after"]}/10 · '
                    f'{step["outcome"] or step["learning"] or "наблюдение не записано"}'
                ),
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
        note_fill = (
            "#EDF8F0"
            if step["practiced"]
            else "#F3FAFC"
        )
        note_border = (
            "#A8D4B5"
            if step["practiced"]
            else "#B8D9E7"
        )

        body += (
            f'<rect '
            f'x="{note_x}" '
            f'y="{y}" '
            f'width="510" '
            f'height="104" '
            f'rx="17" '
            f'fill="{note_fill}" '
            f'stroke="{note_border}" '
            f'stroke-width="2"/>'
        )

        if step["practiced"]:
            body += svg_text(
                note_x + 17,
                y + 29,
                (
                    f'Тревога: начало '
                    f'{step["start"]} · '
                    f'пик {step["peak"]} · '
                    f'после {step["after"]}'
                ),
                size=14,
                weight=700,
                color=palette["ink"],
                max_chars=58,
                max_lines=1,
            )

            body += svg_text(
                note_x + 17,
                y + 58,
                (
                    "Что произошло: "
                    f'{step["outcome"] or "—"}'
                ),
                size=13,
                color=palette["text"],
                max_chars=57,
                max_lines=1,
            )

            body += svg_text(
                note_x + 17,
                y + 83,
                (
                    "Что удалось узнать: "
                    f'{step["learning"] or "—"}'
                ),
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
                (
                    step["prediction"]
                    or "Пока не заполнен"
                ),
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
        (
            "Цвет ступени показывает "
            "субъективный уровень тревоги."
        ),
    )


# ---------------------------------------------------------------------
# ACT-матрица
# ---------------------------------------------------------------------

def render_act_matrix():
    st.title("ACT-матрица")
    st.write(
        "Заметьте внутренний и внешний опыт, "
        "движения от дискомфорта и действия "
        "в сторону того, что важно."
    )

    situation = st.text_area(
        "Ситуация / контекст",
        key="act_situation",
    )

    values = st.text_area(
        "Люди и ценности, которые важны",
        key="act_values",
        placeholder=(
            "Например: близкие отношения, "
            "забота, обучение"
        ),
    )

    external = st.text_area(
        "Что вы замечаете снаружи?",
        key="act_external",
    )

    left, right = st.columns(2)

    with left:
        away = st.text_area(
            "Действия от дискомфорта",
            key="act_away",
        )

        inner = st.text_area(
            "Внутренний опыт",
            key="act_inner",
            help=(
                "Мысли, эмоции, воспоминания "
                "и телесные ощущения."
            ),
        )

    with right:
        toward = st.text_area(
            "Действия к важному",
            key="act_toward",
        )

        toward_inner = st.text_area(
            "Внутренний опыт при движении "
            "к важному",
            key="act_toward_inner",
        )

    chosen_step = st.text_area(
        "Один небольшой выбранный шаг",
        key="act_step",
    )

    if st.button(
        "Сформировать ACT-матрицу",
        key="act_build",
        type="primary",
        use_container_width=True,
    ):
        if not situation.strip():
            st.warning(
                "Добавьте ситуацию, "
                "которую исследуете."
            )
            st.session_state.pop(
                "result_act_matrix",
                None,
            )
        else:
            st.session_state.result_act_matrix = {
                "situation": situation,
                "values": values,
                "external": external,
                "away": away,
                "inner": inner,
                "toward": toward,
                "toward_inner":
                    toward_inner,
                "step": chosen_step,
            }

    result = st.session_state.get(
        "result_act_matrix"
    )

    if not result:
        return

    st.subheader("Сводка")

    st.write(
        f'**Ситуация:** '
        f'{result["situation"]}'
    )
    st.write(
        f'**Что важно:** '
        f'{result["values"] or "—"}'
    )
    st.write(
        f'**Небольшой шаг:** '
        f'{result["step"] or "—"}'
    )

    width = 1240
    height = 850

    left_x = 55
    right_x = 635
    top_y = 135
    bottom_y = 435
    box_width = 550
    box_height = 265

    palette = {
        "ink": "#294968",
        "text": "#4E6681",
        "external":
            ("#E8F4FF", "#91BFE3"),
        "toward":
            ("#E8F6ED", "#83C49B"),
        "inner":
            ("#F2ECFA", "#B6A0D8"),
        "away":
            ("#FFF0E8", "#E7A47D"),
    }

    quadrants = [
        (
            "ВНЕШНИЙ ОПЫТ",
            "Что замечаю снаружи?",
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
            "Как я пытаюсь уйти "
            "от неприятного?",
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
            f'<rect '
            f'x="{x}" '
            f'y="{y}" '
            f'width="{box_width}" '
            f'height="{box_height}" '
            f'rx="20" '
            f'fill="#FFFFFF" '
            f'stroke="{border}" '
            f'stroke-width="2.5"/>'
        )

        body += (
            f'<path '
            f'd="M{x + 20} {y} '
            f'h{box_width - 40} '
            f'a20 20 0 0 1 20 20 '
            f'v36 h-{box_width} v-36 '
            f'a20 20 0 0 1 20-20 z" '
            f'fill="{fill}"/>'
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
                "Пунктов пока нет",
                size=14,
                color="#7B8FA3",
                max_chars=54,
                max_lines=1,
            )
        else:
            for item_index, item in enumerate(
                items
            ):
                item_y = (
                    y
                    + 99
                    + item_index * 27
                )

                body += (
                    f'<circle '
                    f'cx="{x + 25}" '
                    f'cy="{item_y - 5}" '
                    f'r="5" '
                    f'fill="{border}"/>'
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
        '<line x1="620" y1="118" '
        'x2="620" y2="718" '
        'stroke="#587B9D" '
        'stroke-width="3"/>'
    )

    body += (
        '<line x1="42" y1="418" '
        'x2="1198" y2="418" '
        'stroke="#587B9D" '
        'stroke-width="3"/>'
    )

    body += (
        '<circle cx="620" cy="418" r="20" '
        'fill="#FFFFFF" '
        'stroke="#587B9D" '
        'stroke-width="3"/>'
    )

    body += (
        '<circle cx="620" cy="418" r="7" '
        'fill="#587B9D"/>'
    )

    footer_y = 735

    body += (
        f'<rect '
        f'x="55" '
        f'y="{footer_y}" '
        f'width="1130" '
        f'height="82" '
        f'rx="18" '
        f'fill="#E8F4ED" '
        f'stroke="#83C49B" '
        f'stroke-width="2"/>'
    )

    body += svg_text(
        75,
        footer_y + 29,
        "ВЫБРАННЫЙ ШАГ",
        size=13,
        weight=700,
        color="#315F47",
        max_chars=45,
        max_lines=1,
    )

    body += svg_text(
        75,
        footer_y + 60,
        (
            f'Ценности: '
            f'{result["values"] or "—"} · '
            f'Следующий шаг: '
            f'{result["step"] or "—"}'
        ),
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
        (
            "Матрица разделяет внешний и внутренний "
            "опыт и помогает заметить два типа действий."
        ),
    )


# ---------------------------------------------------------------------
# Психодрама: библиотека образов
# ---------------------------------------------------------------------

PSYCHODRAMA_POOL = [
    {"id": "adult_male", "label": "Взрослый — мужской образ", "type": "adult_male", "category": "people", "color": "#72A9C8"},
    {"id": "adult_female", "label": "Взрослый — женский образ", "type": "adult_female", "category": "people", "color": "#A88BC7"},
    {"id": "boy", "label": "Ребёнок — мальчик", "type": "boy", "category": "people", "color": "#E6AD69"},
    {"id": "girl", "label": "Ребёнок — девочка", "type": "girl", "category": "people", "color": "#D98991"},
    {"id": "monster", "label": "Монстр", "type": "monster", "category": "creatures", "color": "#8B6AAE"},
    {"id": "ghost", "label": "Призрак", "type": "ghost", "category": "creatures", "color": "#93B9CA"},
    {"id": "dragon", "label": "Дракон", "type": "dragon", "category": "creatures", "color": "#72966E"},
    {"id": "alien", "label": "Инопланетянин", "type": "alien", "category": "creatures", "color": "#7DB6A3"},
    {"id": "giant", "label": "Великан", "type": "giant", "category": "creatures", "color": "#A77E65"},
    {"id": "robot", "label": "Робот", "type": "robot", "category": "creatures", "color": "#879AA7"},
    {"id": "shadow", "label": "Тень", "type": "shadow", "category": "creatures", "color": "#596779"},
    {"id": "fairy", "label": "Сказочный персонаж", "type": "fairy", "category": "creatures", "color": "#D58FB1"},
    {"id": "dog", "label": "Собака", "type": "dog", "category": "animals", "color": "#B98964"},
    {"id": "wolf", "label": "Волк", "type": "wolf", "category": "animals", "color": "#87929D"},
    {"id": "cat", "label": "Кошка", "type": "cat", "category": "animals", "color": "#D5A36D"},
    {"id": "bird", "label": "Птица", "type": "bird", "category": "animals", "color": "#71A9BB"},
    {"id": "snake", "label": "Змея", "type": "snake", "category": "animals", "color": "#82A36C"},
    {"id": "bear", "label": "Медведь", "type": "bear", "category": "animals", "color": "#A77C62"},
    {"id": "butterfly", "label": "Бабочка", "type": "butterfly", "category": "animals", "color": "#B38BC6"},
    {"id": "circle", "label": "Круг", "type": "circle", "category": "symbols", "color": "#88B8D3"},
    {"id": "star", "label": "Звезда", "type": "star", "category": "symbols", "color": "#E3B95F"},
    {"id": "cloud", "label": "Облако", "type": "cloud", "category": "symbols", "color": "#A5B9D2"},
    {"id": "heart", "label": "Сердце", "type": "heart", "category": "symbols", "color": "#D98991"},
    {"id": "sun", "label": "Солнце", "type": "sun", "category": "symbols", "color": "#E9B85D"},
    {"id": "moon", "label": "Луна", "type": "moon", "category": "symbols", "color": "#97A5C3"},
    {"id": "lightning", "label": "Молния", "type": "lightning", "category": "symbols", "color": "#E0AE4D"},
    {"id": "flame", "label": "Пламя", "type": "flame", "category": "symbols", "color": "#D98462"},
    {"id": "mask", "label": "Маска", "type": "mask", "category": "symbols", "color": "#A88BC7"},
    {"id": "shield", "label": "Щит", "type": "shield", "category": "symbols", "color": "#75A69B"},
    {"id": "spiral", "label": "Спираль", "type": "spiral", "category": "symbols", "color": "#8D83B6"},
    {"id": "mountain", "label": "Гора", "type": "mountain", "category": "symbols", "color": "#7D9D88"},
    {"id": "stone", "label": "Камень", "type": "stone", "category": "symbols", "color": "#919BA3"},
    {"id": "key", "label": "Ключ", "type": "key", "category": "symbols", "color": "#D1A953"},
    {"id": "chair", "label": "Стул", "type": "chair", "category": "objects", "color": "#B98964"},
    {"id": "house", "label": "Дом", "type": "house", "category": "objects", "color": "#D59B72"},
    {"id": "door", "label": "Дверь", "type": "door", "category": "objects", "color": "#A8815F"},
    {"id": "window", "label": "Окно", "type": "window", "category": "objects", "color": "#77AAC2"},
    {"id": "tree", "label": "Дерево", "type": "tree", "category": "objects", "color": "#78A783"},
    {"id": "table", "label": "Стол", "type": "table", "category": "objects", "color": "#9B8069"},
    {"id": "wall", "label": "Стена", "type": "wall", "category": "objects", "color": "#8E9EAC"},
    {"id": "boundary", "label": "Граница", "type": "boundary", "category": "objects", "color": "#688BA7"},
    {"id": "bridge", "label": "Мост", "type": "bridge", "category": "objects", "color": "#B98B67"},
    {"id": "road", "label": "Дорога", "type": "road", "category": "objects", "color": "#8D9AA3"},
    {"id": "chain", "label": "Цепь", "type": "chain", "category": "objects", "color": "#8A7B8F"},
    {"id": "empty", "label": "Пустое место", "type": "empty", "category": "objects", "color": "#A9BCC9"},
]


# ---------------------------------------------------------------------
# Психодрама: полный интерактивный компонент
# ---------------------------------------------------------------------
# ВНИМАНИЕ: В исходном файле HTML-код был обрезан. 
# Здесь добавлена закрывающая часть, чтобы код запускался без ошибок.
# Если у вас есть полный HTML, замените содержимое PSYCHODRAMA_HTML на него.

PSYCHODRAMA_HTML = r"""
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    * { box-sizing: border-box; }
    html, body {
      margin: 0; min-height: 100%; color: #294A65 !important;
      background: #F3F9FD !important; color-scheme: light !important;
      font: 14px "Segoe UI", Arial, sans-serif;
    }
    body, button, input, select { color-scheme: light !important; }
    button, input, select { font: inherit; }
    button { cursor: pointer; }
    .app { display: flex; gap: 14px; min-height: 850px; color: #294A65; background: #F3F9FD; }
    .sidebar {
      width: 315px; min-width: 280px; max-height: 1040px; overflow-y: auto;
      padding: 15px; border: 1px solid #D4E5F0; border-radius: 18px;
      background: #FFFFFF; box-shadow: 0 8px 24px rgba(62,112,148,.07);
    }
    .workspace {
      flex: 1; min-width: 0; padding: 14px; border: 1px solid #D4E5F0;
      border-radius: 18px; background: #FFFFFF; box-shadow: 0 8px 24px rgba(62,112,148,.07);
    }
    h2 { margin: 2px 0 6px; color: #234D6B; font-size: 19px; }
    .muted { color: #69849A; line-height: 1.45; }
    .tabs, .toolbar, .scene-tabs, .selection-tools {
      display: flex; flex-wrap: wrap; gap: 7px; align-items: center;
    }
    .tabs { margin: 14px 0 12px; }
    .tab, .tool-btn, .scene-tab {
      border: 1px solid #B9D5E6; border-radius: 9px; background: #F5FAFD;
      color: #315773; padding: 8px 10px; font-weight: 600;
    }
    .tab.active, .scene-tab.active, .tool-btn.active {
      border-color: #6EA7CB; background: #DFF0FA; color: #234D6B;
    }
    .pool { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
    .pool-item {
      display: flex; min-height: 88px; flex-direction: column; align-items: center;
      justify-content: center; gap: 5px; padding: 8px 5px; border: 1px solid #D6E6F0;
      border-radius: 12px; background: linear-gradient(145deg, #FFFFFF, #F1F8FC);
      color: #355C76; text-align: center; font-size: 12px; transition: .15s ease;
      user-select: none;
    }
    .pool-item:hover {
      transform: translateY(-2px); border-color: #78B0D1;
      box-shadow: 0 5px 14px rgba(71,130,164,.12);
    }
    .pool-icon { width: 42px; height: 42px; overflow: visible; }
    .section-label {
      margin: 15px 0 8px; color: #55748B; font-size: 12px;
      font-weight: 700; letter-spacing: .06em; text-transform: uppercase;
    }
    .help-card {
      margin-top: 14px; padding: 10px 12px; border: 1px solid #CDE0EC;
      border-radius: 12px; background: #F1F8FC; color: #52718A; font-size: 12px;
      line-height: 1.5;
    }
    .toolbar { justify-content: space-between; margin-bottom: 10px; }
    .toolbar-left, .toolbar-right { display: flex; flex-wrap: wrap; gap: 7px; align-items: center; }
    .toolbar button { min-height: 38px; }
    .scene-tabs { margin: 7px 0 10px; }
    .scene-tab { padding: 7px 12px; }
    .stage-wrap { overflow: hidden; border: 1px solid #C9DFEF; border-radius: 15px; background: #FBFDFF; }
    #stage {
      display: block; width: 100%; height: min(66vh, 700px); min-height: 440px;
      touch-action: none; user-select: none; background: #FBFDFF;
    }
    .selection-panel {
      display: none; margin-top: 12px; padding: 12px; border: 1px solid #C6DCEB;
      border-radius: 13px; background: #F5FAFD;
    }
    .selection-panel.visible { display: block; }
    .selection-tools { margin-top: 9px; }
    .field { display: flex; flex-direction: column; gap: 5px; min-width: 130px; color: #55748B; font-size: 12px; }
    .field input[type="text"] {
      width: 230px; max-width: 100%; padding: 8px 9px; border: 1px solid #C2D9E8;
      border-radius: 8px; background: #FFFFFF; color: #294A65;
    }
    .field input[type="range"] { width: 150px; }
    .field input[type="color"] {
      width: 44px; height: 35px; padding: 2px; border: 1px solid #C2D9E8;
      border-radius: 8px; background: #FFFFFF;
    }
    .danger { border-color: #E5B8B8 !important; background: #FFF4F3 !important; color: #9B4D4A !important; }
    .status { min-height: 20px; margin-top: 8px; color: #69849A; font-size: 12px; }
    .privacy { margin: 12px 0 0; color: #69849A; font-size: 12px; line-height: 1.5; }
    .hidden { display: none !important; }
    @media (max-width: 900px) {
      .app { flex-direction: column; }
      .sidebar { width: 100%; min-width: 0; max-height: none; }
      .pool { grid-template-columns: repeat(4, minmax(0, 1fr)); }
      #stage { height: 560px; }
    }
    @media (max-width: 560px) {
      .pool { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
  </style>
</head>
<body>
  <div class="app">
    <aside class="sidebar">
      <h2>Психодрама</h2>
      <p class="muted">Интерактивная сцена</p>
      <div class="help-card">
        Внимание: исходный HTML-код психодрамы был обрезан при копировании.
        Здесь показана заглушка. Если у вас есть полный код, вставьте его в переменную PSYCHODRAMA_HTML.
      </div>
    </aside>
    <main class="workspace">
      <canvas id="stage"></canvas>
    </main>
  </div>
</body>
</html>
"""

def render_psychodrama():
    st.title("Психодрама: интерактивная сцена")
    st.warning("Исходный код этой техники был обрезан в вашем файле. Отображается заглушка.")
    # components.html(PSYCHODRAMA_HTML, height=900, scrolling=True)


# ---------------------------------------------------------------------
# Запуск приложения
# ---------------------------------------------------------------------

def main():
    render_header()
    
    if st.session_state.page == "home":
        render_home()
    elif st.session_state.page == "library":
        render_library()
    elif st.session_state.page == "about":
        render_about()
    elif st.session_state.page == "technique":
        tech = st.session_state.selected_technique
        if tech == "decision_tree":
            render_decision_tree()
        elif tech == "dbt_chain":
            render_chain()
        elif tech == "exposure":
            render_exposure()
        elif tech == "act_matrix":
            render_act_matrix()
        elif tech == "psychodrama":
            render_psychodrama()
        else:
            st.error("Техника не найдена.")
    else:
        render_home()

if __name__ == "__main__":
    main()
