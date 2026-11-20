import json

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Психодрама — сцена",
    page_icon="🎭",
    layout="wide",
)

# Принудительно используем светлую тему Streamlit.
st.markdown(
    """
    <style>
    :root,
    html,
    body,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"] {
        color-scheme: light !important;
        background-color: #F3F9FD !important;
        color: #294A65 !important;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 10% 5%, rgba(196,228,248,.42), transparent 34%),
            radial-gradient(ellipse at 92% 18%, rgba(219,239,251,.55), transparent 36%),
            #F3F9FD !important;
    }

    [data-testid="stHeader"],
    [data-testid="stToolbar"] {
        background: #F3F9FD !important;
        color: #294A65 !important;
    }

    [data-testid="stDecoration"] {
        background-image: linear-gradient(90deg, #6EA7CB, #9AC7DF) !important;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, p, label {
        color: #294A65 !important;
    }

    [data-testid="stAlert"] {
        background: #EAF5FC !important;
        border: 1px solid #BCD9EB !important;
        color: #294A65 !important;
    }

    [data-testid="stAlert"] * {
        color: #294A65 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Библиотека образов
# ---------------------------------------------------------------------

POOL = [
    # Люди
    {
        "id": "adult_male",
        "label": "Взрослый — мужской образ",
        "type": "adult_male",
        "category": "people",
        "color": "#72A9C8",
    },
    {
        "id": "adult_female",
        "label": "Взрослый — женский образ",
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

    # Существа
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

    # Животные
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

    # Символы
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

    # Предметы и пространство
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

      // История отмены/повтора хранит только отдельные штрихи.
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

          // Волосы размещаются позади головы: лицо остаётся открытым.
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

          // Руки и ноги.
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

          // Одежда слегка отличается силуэтом.
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

          // Голова поверх причёски.
          group.appendChild(svgEl("circle", {
            cx: 0,
            cy: -24,
            r: 12,
            fill: "#F1C9A8",
            stroke: "#506F84",
            "stroke-width": 2
          }));

          // Нейтральные черты лица.
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
          // Голова с рожками и выступами.
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

          // Нахмуренные брови и заметные глаза.
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

          // Открытая пасть и острые зубы.
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
          // Тело и голова дракона.
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

          // Крылья.
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

          // Два слоя пламени направлены от морды вправо.
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
            // Пасть и заметные клыки волка.
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
          // Крылья отрисовываются за телом.
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

          // Линии перьев.
          add("path", {
            d: "M-15 1 L-37 -11 M-14 8 L-34 2 M15 1 L37 -11 M14 8 L34 2",
            fill: "none",
            stroke: "#FFFFFF",
            "stroke-width": 2,
            "stroke-linecap": "round"
          });

          // Тело, голова, глаз и клюв.
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
