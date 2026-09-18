# -*- coding: utf-8 -*-
"""Generate Wah Fung Engineering static pages."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SITES = [
    {
        "slug": "engineering",
        "en": "Wah Fung Engineering Company Limited",
        "tc": "華丰工程有限公司",
        "sc": "华丰工程有限公司",
        "desc": {
            "en": "Wah Fung Engineering Company Limited — civil and building engineering in Hong Kong.",
            "tc": "華丰工程有限公司 — 香港土木及建築工程承建商。",
            "sc": "华丰工程有限公司 — 香港土木及建筑工程承建商。",
        },
    },
    {
        "slug": "building",
        "en": "Wah Fung Building & Engineering Limited",
        "tc": "華丰建設工程有限公司",
        "sc": "华丰建设工程有限公司",
        "desc": {
            "en": "Wah Fung Building & Engineering Limited — civil and building engineering in Hong Kong.",
            "tc": "華丰建設工程有限公司 — 香港土木及建築工程承建商。",
            "sc": "华丰建设工程有限公司 — 香港土木及建筑工程承建商。",
        },
    },
    {
        "slug": "dixie",
        "en": "Dixie Engineering Company Limited",
        "tc": "仁利工程有限公司",
        "sc": "仁利工程有限公司",
        "desc": {
            "en": "Dixie Engineering Company Limited — civil and building engineering in Hong Kong.",
            "tc": "仁利工程有限公司 — 香港土木及建築工程承建商。",
            "sc": "仁利工程有限公司 — 香港土木及建筑工程承建商。",
        },
    },
]
CURRENT_SITE = SITES[0]
COMPANY = {lang: CURRENT_SITE[lang] for lang in ("en", "tc", "sc")}
COPYRIGHT = {
    "en": f"© 2026 {CURRENT_SITE['en']}. All Rights Reserved.",
    "tc": f"© 2026 {CURRENT_SITE['tc']}。版權所有。",
    "sc": f"© 2026 {CURRENT_SITE['sc']}。版权所有。",
}
CONTACT_LABEL = {"en": "Contact us", "tc": "聯繫我們", "sc": "联系我们"}
NAV = {
    "en": [
        ("index.php", "home"),
        ("aboutus.php", "about us"),
        ("expertise.php", "our expertise"),
        ("projects.php", "projects"),
        ("sustainability.php", "safety, quality & environment"),
        ("talent.php", "talent<br>development"),
        ("news.php", "news"),
    ],
    "tc": [
        ("index.php", "首頁"),
        ("aboutus.php", "關於我們"),
        ("expertise.php", "專業資格"),
        ("projects.php", "項目"),
        ("sustainability.php", "安全、品質及環境"),
        ("talent.php", "人才發展"),
        ("news.php", "新聞"),
    ],
    "sc": [
        ("index.php", "首页"),
        ("aboutus.php", "关于我们"),
        ("expertise.php", "专业资格"),
        ("projects.php", "项目"),
        ("sustainability.php", "安全、品质及环境"),
        ("talent.php", "人才发展"),
        ("news.php", "新闻"),
    ],
}

SLIDES = [
    {
        "img": "../images/background/1.jpg",
        "en": ("Drainage Maintenance", "Drainage maintenance and construction works on Hong Kong channels."),
        "tc": ("渠務保養", "香港渠務設施保養及建造工程。"),
        "sc": ("渠务保养", "香港渠务设施保养及建造工程。"),
    },
    {
        "img": "../images/background/2.jpg",
        "en": ("Urban Traffic Management", "Night-time barriers, cones and plant on live urban roads."),
        "tc": ("市區交通管理", "在用市區道路的夜間圍欄、雪糕筒及機械。"),
        "sc": ("市区交通管理", "在用市区道路的夜间围栏、雪糕筒及机械。"),
    },
    {
        "img": "../images/background/3.jpg",
        "en": ("Road Maintenance", "Lane control and works vehicles on high speed roads."),
        "tc": ("道路維修", "高速路行車線管制及工程車輛。"),
        "sc": ("道路维修", "高速路行车线管制及工程车辆。"),
    },
    {
        "img": "../images/background/4.jpg",
        "en": ("Plant and Equipment", "Wah Fung plant and vehicles ready for term-contract operations."),
        "tc": ("機械及車輛", "華丰工程車輛，支援定期合約作業。"),
        "sc": ("机械及车辆", "华丰工程车辆，支援定期合约作业。"),
    },
]

HOME_TILES = [
    ("aboutus.php", "../images/tile/1.jpg", {"en": "About us", "tc": "關於我們", "sc": "关于我们"}),
    ("expertise.php", "../images/tile/2.jpg", {"en": "Expertise", "tc": "專業資格", "sc": "专业资格"}),
    ("sustainability.php", "../images/tile/4.jpg", {"en": "Safety, Quality & Environment", "tc": "安全、品質及環境", "sc": "安全、品质及环境"}),
    ("projects.php", "../images/tile/3.jpg", {"en": "Projects", "tc": "項目", "sc": "项目"}),
    ("news.php", "../images/tile/5.jpg", {"en": "News", "tc": "新聞", "sc": "新闻"}),
    ("aboutus.php", "../images/tile/6.jpg", {"en": "Contact us", "tc": "聯繫我們", "sc": "联系我们"}),
]
HOME_TAGLINE = {
    "en": "Civil and building engineering for Hong Kong — planned, built and maintained with care.",
    "tc": "華丰於香港承辦土木及建築工程，從策劃、建造到保養，務求做好。",
    "sc": "华丰于香港承办土木及建筑工程，从策划、建造到保养，务求做好。",
}

PROJECTS = [
    {
        "id": 10,
        "cover": "../images/project/1/cover.jpg",
        "gallery": ["../images/project/1/1.jpg", "../images/project/1/2.jpg", "../images/project/1/3.jpg"],
        "en": {
            "title": "Highways Department Term Contract (Maintenance of High Speed Roads in New Territories West and Kowloon 1998 – 2001)",
            "no": "10/HY/1997",
            "value": "Highways Department",
            "period": "1998 – 2001",
            "role": "Participated in the maintenance of high speed roads in New Territories West and Kowloon, including lane control, night works and emergency attendance.",
        },
        "tc": {
            "title": "路政署定期合約（新界西及九龍快速公路之維修，1998 – 2001）",
            "no": "10/HY/1997",
            "value": "路政署",
            "period": "1998 – 2001",
            "role": "參與新界西及九龍快速公路維修，包括行車線管制、夜間工程及緊急出勤。",
        },
        "sc": {
            "title": "路政署定期合约（新界西及九龙快速公路之维修，1998 – 2001）",
            "no": "10/HY/1997",
            "value": "路政署",
            "period": "1998 – 2001",
            "role": "参与新界西及九龙快速公路维修，包括行车线管制、夜间工程及紧急出勤。",
        },
    },
    {
        "id": 9,
        "cover": "../images/project/2/cover.jpg",
        "gallery": ["../images/project/2/1.jpg", "../images/project/2/2.jpg", "../images/project/2/3.jpg"],
        "en": {
            "title": "Highways Department Term Contract (Maintenance of High Speed Roads in New Territories West and Kowloon 2001 – 2004)",
            "no": "11/HY/2000",
            "value": "Highways Department",
            "period": "2001 – 2004",
            "role": "Participated in the maintenance of high speed roads in New Territories West and Kowloon, including lane control, night works and emergency attendance.",
        },
        "tc": {
            "title": "路政署定期合約（新界西及九龍快速公路之維修，2001 – 2004）",
            "no": "11/HY/2000",
            "value": "路政署",
            "period": "2001 – 2004",
            "role": "參與新界西及九龍快速公路維修，包括行車線管制、夜間工程及緊急出勤。",
        },
        "sc": {
            "title": "路政署定期合约（新界西及九龙快速公路之维修，2001 – 2004）",
            "no": "11/HY/2000",
            "value": "路政署",
            "period": "2001 – 2004",
            "role": "参与新界西及九龙快速公路维修，包括行车线管制、夜间工程及紧急出勤。",
        },
    },
    {
        "id": 12,
        "cover": "../images/project/3/cover.jpg",
        "gallery": ["../images/project/3/1.jpg", "../images/project/3/2.jpg", "../images/project/3/3.jpg"],
        "en": {
            "title": "Highways Department Term Contract (Management and Maintenance of Roads in Tuen Mun and Yuen Long Districts 2002 – 2005)",
            "no": "08/HY/2001",
            "value": "Highways Department",
            "period": "2002 – 2005",
            "role": "Participated in the management and maintenance of roads in Tuen Mun and Yuen Long Districts, including routine repairs, lane closures and emergency attendance.",
        },
        "tc": {
            "title": "路政署定期合約（屯門及元朗區道路之管理及維修，2002 – 2005）",
            "no": "08/HY/2001",
            "value": "路政署",
            "period": "2002 – 2005",
            "role": "參與屯門及元朗區道路管理及維修，包括日常修補、封路及緊急出勤。",
        },
        "sc": {
            "title": "路政署定期合约（屯门及元朗区道路之管理及维修，2002 – 2005）",
            "no": "08/HY/2001",
            "value": "路政署",
            "period": "2002 – 2005",
            "role": "参与屯门及元朗区道路管理及维修，包括日常修补、封路及紧急出勤。",
        },
    },
    {
        "id": 8,
        "cover": "../images/project/4/cover.jpg",
        "gallery": ["../images/project/4/1.jpg", "../images/project/4/2.jpg", "../images/project/4/3.jpg"],
        "en": {
            "title": "Highways Department Term Contract (Maintenance of High Speed Roads in New Territories West and Kowloon 2004 – 2008)",
            "no": "16/HY/2003",
            "value": "Highways Department",
            "period": "2004 – 2008",
            "role": "Participated in the maintenance of high speed roads in New Territories West and Kowloon, including lane control, night works and emergency attendance.",
        },
        "tc": {
            "title": "路政署定期合約（新界西及九龍快速公路之維修，2004 – 2008）",
            "no": "16/HY/2003",
            "value": "路政署",
            "period": "2004 – 2008",
            "role": "參與新界西及九龍快速公路維修，包括行車線管制、夜間工程及緊急出勤。",
        },
        "sc": {
            "title": "路政署定期合约（新界西及九龙快速公路之维修，2004 – 2008）",
            "no": "16/HY/2003",
            "value": "路政署",
            "period": "2004 – 2008",
            "role": "参与新界西及九龙快速公路维修，包括行车线管制、夜间工程及紧急出勤。",
        },
    },
    {
        "id": 13,
        "cover": "../images/project/5/cover.jpg",
        "gallery": ["../images/project/5/1.jpg", "../images/project/5/2.jpg", "../images/project/5/3.jpg"],
        "en": {
            "title": "Highways Department Term Contract (Management and Maintenance of Roads in Tai Po and North Districts excluding High Speed Roads 2007 – 2012)",
            "no": "05/HY/2006",
            "value": "Highways Department",
            "period": "2007 – 2012",
            "role": "Participated in the management and maintenance of roads in Tai Po and North Districts (excluding high speed roads), including routine repairs, lane closures and emergency attendance.",
        },
        "tc": {
            "title": "路政署定期合約（大埔及北區道路（快速公路除外）之管理及維修，2007 – 2012）",
            "no": "05/HY/2006",
            "value": "路政署",
            "period": "2007 – 2012",
            "role": "參與大埔及北區道路（快速公路除外）管理及維修，包括日常修補、封路及緊急出勤。",
        },
        "sc": {
            "title": "路政署定期合约（大埔及北区道路（快速公路除外）之管理及维修，2007 – 2012）",
            "no": "05/HY/2006",
            "value": "路政署",
            "period": "2007 – 2012",
            "role": "参与大埔及北区道路（快速公路除外）管理及维修，包括日常修补、封路及紧急出勤。",
        },
    },
    {
        "id": 7,
        "cover": "../images/project/6/cover.jpg",
        "gallery": ["../images/project/6/1.jpg", "../images/project/6/2.jpg", "../images/project/6/3.jpg"],
        "en": {
            "title": "Highways Department Term Contract (Management and Maintenance of High Speed Roads in New Territories West and Kowloon, and Roads in the Hong Kong Port Area 2008 – 2016)",
            "no": "11/HY/2007",
            "value": "Highways Department",
            "period": "2008 – 2016",
            "role": "Participated in the management and maintenance of high speed roads in New Territories West and Kowloon, and roads in the Hong Kong Port Area, including lane control and night works.",
        },
        "tc": {
            "title": "路政署定期合約（新界西及九龍快速公路及香港口岸區道路之管理及維修，2008 – 2016）",
            "no": "11/HY/2007",
            "value": "路政署",
            "period": "2008 – 2016",
            "role": "參與新界西及九龍快速公路及香港口岸區道路管理及維修，包括行車線管制及夜間工程。",
        },
        "sc": {
            "title": "路政署定期合约（新界西及九龙快速公路及香港口岸区道路之管理及维修，2008 – 2016）",
            "no": "11/HY/2007",
            "value": "路政署",
            "period": "2008 – 2016",
            "role": "参与新界西及九龙快速公路及香港口岸区道路管理及维修，包括行车线管制及夜间工程。",
        },
    },
    {
        "id": 6,
        "cover": "../images/project/7/cover.jpg",
        "gallery": ["../images/project/7/1.jpg", "../images/project/7/2.jpg", "../images/project/7/3.jpg"],
        "en": {
            "title": "Highways Department Term Contract (Management and Maintenance of Roads in Tai Po and North Districts excluding High Speed Roads 2012 – 2016)",
            "no": "06/HY/2011",
            "value": "Highways Department",
            "period": "2012 – 2016",
            "role": "Participated in the management and maintenance of roads in Tai Po and North Districts (excluding high speed roads), including routine repairs, lane closures and emergency attendance.",
        },
        "tc": {
            "title": "路政署定期合約（大埔及北區道路（快速公路除外）之管理及維修，2012 – 2016）",
            "no": "06/HY/2011",
            "value": "路政署",
            "period": "2012 – 2016",
            "role": "參與大埔及北區道路（快速公路除外）管理及維修，包括日常修補、封路及緊急出勤。",
        },
        "sc": {
            "title": "路政署定期合约（大埔及北区道路（快速公路除外）之管理及维修，2012 – 2016）",
            "no": "06/HY/2011",
            "value": "路政署",
            "period": "2012 – 2016",
            "role": "参与大埔及北区道路（快速公路除外）管理及维修，包括日常修补、封路及紧急出勤。",
        },
    },
    {
        "id": 1,
        "cover": "../images/project/8/cover.jpg",
        "gallery": ["../images/project/8/1.jpg", "../images/project/8/2.jpg", "../images/project/8/3.jpg"],
        "en": {
            "title": "Highways Department Term Contract (Management and Maintenance of Roads in Tai Po and North Districts excluding High Speed Roads 2016 – 2022)",
            "no": "02/HY/2015",
            "value": "Highways Department",
            "period": "2016 – 2022",
            "role": "Participated in the management and maintenance of roads in Tai Po and North Districts (excluding high speed roads), including routine repairs, lane closures and emergency attendance.",
        },
        "tc": {
            "title": "路政署定期合約（大埔及北區道路（快速公路除外）之管理及維修，2016 – 2022）",
            "no": "02/HY/2015",
            "value": "路政署",
            "period": "2016 – 2022",
            "role": "參與大埔及北區道路（快速公路除外）管理及維修，包括日常修補、封路及緊急出勤。",
        },
        "sc": {
            "title": "路政署定期合约（大埔及北区道路（快速公路除外）之管理及维修，2016 – 2022）",
            "no": "02/HY/2015",
            "value": "路政署",
            "period": "2016 – 2022",
            "role": "参与大埔及北区道路（快速公路除外）管理及维修，包括日常修补、封路及紧急出勤。",
        },
    },
    {
        "id": 2,
        "cover": "../images/project/9/cover.jpg",
        "gallery": ["../images/project/9/1.jpg", "../images/project/9/2.jpg", "../images/project/9/3.jpg"],
        "en": {
            "title": "Highways Department Term Contract (Management and Maintenance of Roads on Hong Kong Island excluding High Speed Roads 2017 – 2023)",
            "no": "01/HY/2016",
            "value": "Highways Department",
            "period": "2017 – 2023",
            "role": "Participated in the management and maintenance of roads on Hong Kong Island (excluding high speed roads), including routine repairs, lane closures and night works.",
        },
        "tc": {
            "title": "路政署定期合約（香港島道路（快速公路除外）之管理及維修，2017 – 2023）",
            "no": "01/HY/2016",
            "value": "路政署",
            "period": "2017 – 2023",
            "role": "參與香港島道路（快速公路除外）管理及維修，包括日常修補、封路及夜間工程。",
        },
        "sc": {
            "title": "路政署定期合约（香港岛道路（快速公路除外）之管理及维修，2017 – 2023）",
            "no": "01/HY/2016",
            "value": "路政署",
            "period": "2017 – 2023",
            "role": "参与香港岛道路（快速公路除外）管理及维修，包括日常修补、封路及夜间工程。",
        },
    },
    {
        "id": 3,
        "cover": "../images/project/10/cover.jpg",
        "gallery": ["../images/project/10/1.jpg", "../images/project/10/2.jpg", "../images/project/10/3.jpg"],
        "en": {
            "title": "Highways Department Term Contract (Management and Maintenance of Roads on Hong Kong Island excluding Expressways and High Speed Roads 2021 – 2025)",
            "no": "18/HY/2020",
            "value": "Highways Department",
            "period": "2021 – 2025",
            "role": "Participated in the management and maintenance of roads on Hong Kong Island (excluding expressways and high speed roads), including routine repairs, lane closures and night works.",
        },
        "tc": {
            "title": "路政署定期合約（香港島道路（快速公路及高速道路除外）之管理及維修，2021 – 2025）",
            "no": "18/HY/2020",
            "value": "路政署",
            "period": "2021 – 2025",
            "role": "參與香港島道路（快速公路及高速道路除外）管理及維修，包括日常修補、封路及夜間工程。",
        },
        "sc": {
            "title": "路政署定期合约（香港岛道路（快速公路及高速道路除外）之管理及维修，2021 – 2025）",
            "no": "18/HY/2020",
            "value": "路政署",
            "period": "2021 – 2025",
            "role": "参与香港岛道路（快速公路及高速道路除外）管理及维修，包括日常修补、封路及夜间工程。",
        },
    },
    {
        "id": 5,
        "cover": "../images/project/11/cover.jpg",
        "gallery": ["../images/project/11/1.jpg", "../images/project/11/2.jpg", "../images/project/11/3.jpg"],
        "en": {
            "title": "Drainage Services Department Term Contract (Drainage Maintenance and Construction in Kowloon and New Territories South 2023 – 2027)",
            "no": "DC/2023/04",
            "value": "Drainage Services Department",
            "period": "2023 – 2027",
            "role": "Participated in drainage maintenance and construction in Kowloon and New Territories South (Chiu Hing – Dixie Joint Venture), including channel works, manholes and emergency attendance.",
        },
        "tc": {
            "title": "渠務署定期合約（九龍及新界南區的渠務維修及建造工程，2023 – 2027）",
            "no": "DC/2023/04",
            "value": "渠務署",
            "period": "2023 – 2027",
            "role": "參與九龍及新界南區渠務維修及建造工程（昭興–仁利聯營），包括渠道、沙井及緊急出勤。",
        },
        "sc": {
            "title": "渠务署定期合约（九龙及新界南区的渠务维修及建造工程，2023 – 2027）",
            "no": "DC/2023/04",
            "value": "渠务署",
            "period": "2023 – 2027",
            "role": "参与九龙及新界南区渠务维修及建造工程（昭兴–仁利联营），包括渠道、沙井及紧急出勤。",
        },
    },
    {
        "id": 4,
        "cover": "../images/project/12/cover.jpg",
        "gallery": ["../images/project/12/1.jpg", "../images/project/12/2.jpg", "../images/project/12/3.jpg"],
        "en": {
            "title": "Highways Department Term Contract (Management and Maintenance of Roads in Sha Tin, Sai Kung and Islands Districts excluding Expressways and High Speed Roads 2024 – 2029)",
            "no": "03/HY/2023",
            "value": "Highways Department",
            "period": "2024 – 2029",
            "role": "Participated in the management and maintenance of roads in Sha Tin, Sai Kung and Islands Districts (excluding expressways and high speed roads), including routine repairs, lane closures and night works.",
        },
        "tc": {
            "title": "路政署定期合約（沙田、西貢及離島區道路（快速公路及高速道路除外）之管理及維修，2024 – 2029）",
            "no": "03/HY/2023",
            "value": "路政署",
            "period": "2024 – 2029",
            "role": "參與沙田、西貢及離島區道路（快速公路及高速道路除外）管理及維修，包括日常修補、封路及夜間工程。",
        },
        "sc": {
            "title": "路政署定期合约（沙田、西贡及离岛区道路（快速公路及高速道路除外）之管理及维修，2024 – 2029）",
            "no": "03/HY/2023",
            "value": "路政署",
            "period": "2024 – 2029",
            "role": "参与沙田、西贡及离岛区道路（快速公路及高速道路除外）管理及维修，包括日常修补、封路及夜间工程。",
        },
    },
    {
        "id": 11,
        "cover": "../images/project/13/cover.jpg",
        "gallery": [
            "../images/project/13/1.jpg",
            "../images/project/13/2.jpg",
            "../images/project/13/3.jpg",
            "../images/project/13/4.jpg",
            "../images/project/13/5.jpg",
            "../images/project/13/6.jpg",
            "../images/project/13/7.jpg",
            "../images/project/13/8.jpg",
        ],
        "en": {
            "title": "Major Events: Standard Chartered Hong Kong Marathon and Cycling Festival — Road Closures",
            "no": "Major Events",
            "value": "Standard Chartered Hong Kong Marathon / Cycling Festival",
            "period": "Event days",
            "role": "Wah Fung provided temporary traffic arrangements and road-closure support for the Standard Chartered Hong Kong Marathon and the Cycling Festival, including barriers, cones, lighting and night works on live urban roads.",
        },
        "tc": {
            "title": "大型盛事：渣打香港馬拉松及單車節封路",
            "no": "大型盛事",
            "value": "渣打香港馬拉松／單車節",
            "period": "盛事期間",
            "role": "華丰為渣打香港馬拉松及單車節提供臨時交通安排及封路支援，包括圍欄、雪糕筒、照明，以及在用市區道路的夜間工程。",
        },
        "sc": {
            "title": "大型盛事：渣打香港马拉松及单车节封路",
            "no": "大型盛事",
            "value": "渣打香港马拉松／单车节",
            "period": "盛事期间",
            "role": "华丰为渣打香港马拉松及单车节提供临时交通安排及封路支援，包括围栏、雪糕筒、照明，以及在用市区道路的夜间工程。",
        },
    },
]


def contract_slug(no: str) -> str:
    return "-".join(no.replace("/", "-").split())


def bind_project_photos(projects: list) -> list:
    for p in projects:
        slug = contract_slug(p["en"]["no"])
        rel = f"../images/project/{slug}"
        folder = ROOT / "images" / "project" / slug
        numbered = []
        if folder.is_dir():
            for f in folder.iterdir():
                if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"} and f.stem.isdigit():
                    numbered.append((int(f.stem), f.name))
        numbered.sort()
        photos = [f"{rel}/{name}" for _, name in numbered] or [f"{rel}/1.jpg"]
        p["cover"] = photos[0]
        p["gallery"] = photos[1:] or [p["cover"]]
    return projects


PROJECTS = bind_project_photos(PROJECTS)

NEWS = [
    {
        "id": 5,
        "date": {"en": "3 August 2026", "tc": "2026年8月3日", "sc": "2026年8月3日"},
        "en": {
            "title": "Smoking cessation talk and incentive scheme",
            "body": "<p>A smoking cessation talk was held for frontline colleagues, supported by the Tobacco and Alcohol Control Office of the Department of Health and the smoking-cessation behavioural therapy team of Eastern Hospital.</p><p>The talk covered smoking and health, and the treatment of tobacco addiction. Colleagues who join the incentive scheme complete a nicotine saliva test, attend the talk, and take a follow-up test after the observation period to confirm that they have stopped smoking.</p><p>The talk was held in a site meeting room so that frontline staff could take part during the working day.</p>",
        },
        "tc": {
            "title": "工友戒煙講座及獎勵計劃",
            "body": "<p>為前線工友舉辦戒煙講座，由衞生署控煙酒辦公室及東區醫院戒煙行為治療小組支援。</p><p>講座內容涵蓋吸煙與健康，以及煙草成癮治療。參加獎勵計劃的工友須完成尼古丁唾液測試、出席講座，並於觀察期後再測，以確認已戒煙。</p><p>講座於地盤會議室舉行，方便前線同事在工作日參與。</p>",
        },
        "sc": {
            "title": "工友戒烟讲座及奖励计划",
            "body": "<p>为前线工友举办戒烟讲座，由卫生署控烟酒办公室及东区医院戒烟行为治疗小组支援。</p><p>讲座内容涵盖吸烟与健康，以及烟草成瘾治疗。参加奖励计划的工友须完成尼古丁唾液测试、出席讲座，并于观察期后再测，以确认已戒烟。</p><p>讲座于地盘会议室举行，方便前线同事在工作日参与。</p>",
        },
    },
    {
        "id": 2,
        "date": {"en": "July 2026", "tc": "2026年7月", "sc": "2026年7月"},
        "imgs": ["../images/news/youxin.png"],
        "en": {
            "title": "Worker-Friendly Construction Site",
            "body": "<p>The Construction Industry Council has recognised the site as a Worker-Friendly Construction Site (友心工地). Certificate no. WFCS-842.</p><p>The scheme looks after workers’ welfare, rest facilities and a safer workplace — rest areas and day-to-day care of frontline colleagues.</p>",
        },
        "tc": {
            "title": "友心工地",
            "body": "<p>建造業議會嘉許地盤為「友心工地」，證書編號 WFCS-842。</p><p>計劃表揚照顧工友福利、休息設施及更安全工作環境，包括休息地方及前線工友的日常關懷。</p>",
        },
        "sc": {
            "title": "友心工地",
            "body": "<p>建造业议会嘉许地盘为「友心工地」，证书编号 WFCS-842。</p><p>计划表扬照顾工友福利、休息设施及更安全工作环境，包括休息地方及前线工友的日常关怀。</p>",
        },
    },
    {
        "id": 6,
        "date": {"en": "July 2026", "tc": "2026年7月", "sc": "2026年7月"},
        "imgs": ["../images/news/ccsas.jpg"],
        "en": {
            "title": "Considerate Contractors Site Award Scheme (CCSAS) banners",
            "body": "<p>Sites display banners for the Considerate Contractors Site Award Scheme (CCSAS), organised by the Development Bureau and the Construction Industry Council.</p><p>The scheme asks sites to put safety first, care for workers, protect the environment and be considerate to the neighbourhood. Notices remind colleagues of identity checks, safety equipment and the Smart Site Safety System (4S).</p>",
        },
        "tc": {
            "title": "公德地盤嘉許計劃（CCSAS）橫額",
            "body": "<p>地盤展示公德地盤嘉許計劃（CCSAS）橫額。計劃由發展局及建造業議會推行，鼓勵地盤以安全為先、關懷工友、保護環境及體諒鄰里。</p><p>通告提醒同事核對身份、佩戴安全裝備，以及安全智慧工地系統（4S）。</p>",
        },
        "sc": {
            "title": "公德地盘嘉许计划（CCSAS）横额",
            "body": "<p>地盘展示公德地盘嘉许计划（CCSAS）横额。计划由发展局及建造业议会推行，鼓励地盘以安全为先、关怀工友、保护环境及体谅邻里。</p><p>通告提醒同事核对身份、佩戴安全装备，以及安全智慧工地系统（4S）。</p>",
        },
    },
    {
        "id": 13,
        "date": {"en": "July 2026", "tc": "2026年7月", "sc": "2026年7月"},
        "imgs": ["../images/news/aed.jpg", "../images/news/heat.jpg"],
        "en": {
            "title": "Heatstroke prevention, depot AED and safety talks",
            "body": "<p>An automated external defibrillator (AED) is kept at the depot, with posted instructions on CPR and how to use the device.</p><p>In hot weather, heatstroke-prevention supplies and drinking water are arranged for workers. Lunchtime and evening talks cover lifting and the opening of manholes.</p><p>Frontline colleagues have water, first-aid equipment and a briefing before they start work.</p>",
        },
        "tc": {
            "title": "防中暑、車房 AED 及安全講座",
            "body": "<p>車房設有自動心臟除顫器（AED），並張貼心肺復甦及使用方法。</p><p>酷熱天氣期間，地盤安排防中暑物料及飲用水。午膳及晚間講座涵蓋吊運及沙井開啟。</p><p>前線工友開工前有食水、急救設備及交底。</p>",
        },
        "sc": {
            "title": "防中暑、车房 AED 及安全讲座",
            "body": "<p>车房设有自动心脏除颤器（AED），并张贴心肺复苏及使用方法。</p><p>酷热天气期间，地盘安排防中暑物料及饮用水。午膳及晚间讲座涵盖吊运及沙井开启。</p><p>前线工友开工前有食水、急救设备及交底。</p>",
        },
    },
    {
        "id": 7,
        "date": {"en": "July 2026", "tc": "2026年7月", "sc": "2026年7月"},
        "imgs": ["../images/news/frontline.png"],
        "en": {
            "title": "Frontline Personnel Safety Performance Recording Scheme",
            "body": "<p>The Construction Industry Council Frontline Personnel Safety Performance Recording Scheme is in use on site. It is part of Life First / Walk the Talk and records the safety performance of frontline personnel.</p><p>The scheme standardises how safety performance is recorded, promotes safe working habits, and encourages frontline staff to join safety training and work with other parties on site.</p><p>Colleagues may enter records through the CIC platform.</p>",
        },
        "tc": {
            "title": "前線人員安全表現紀錄計劃",
            "body": "<p>地盤採用建造業議會「前線人員安全表現紀錄計劃」。計劃屬「生命第一／行出安全」系列，用以紀錄前線人員的安全表現。</p><p>計劃以統一標準紀錄安全表現，促進安全施工習慣，並鼓勵前線人員參與培訓及與地盤各方合作。</p><p>同事可經議會平台登入。</p>",
        },
        "sc": {
            "title": "前线人员安全表现纪录计划",
            "body": "<p>地盘采用建造业议会「前线人员安全表现纪录计划」。计划属「生命第一／行出安全」系列，用以纪录前线人员的安全表现。</p><p>计划以统一标准纪录安全表现，促进安全施工习惯，并鼓励前线人员参与培训及与地盘各方合作。</p><p>同事可经议会平台登入。</p>",
        },
    },
    {
        "id": 8,
        "date": {"en": "July 2026", "tc": "2026年7月", "sc": "2026年7月"},
        "imgs": ["../images/news/football.jpg"],
        "en": {
            "title": "Construction Industry 5-a-side Football Competition 2026 (CISVP)",
            "body": "<p>The Construction Industry Council, through the Construction Industry Sports and Volunteering Programme (CISVP), will hold the Construction Industry 5-a-side Football Competition 2026 on 8 November 2026, from 8:00 a.m. to 6:00 p.m., at the Jockey Club HKFA Football Training Centre.</p><p>The competition encourages practitioners to take part in sport, build ties across the industry, and keep fit. Colleagues who wish to join may do so.</p>",
        },
        "tc": {
            "title": "建造業五人足球比賽 2026（CISVP）",
            "body": "<p>建造業議會透過建造業運動及義工計劃（CISVP），將於 2026 年 11 月 8 日上午 8 時至下午 6 時，在賽馬會香港足球總會足球訓練中心舉行「建造業五人足球比賽 2026」。</p><p>賽事鼓勵從業員參與運動、聯繫同業。同事可自行報名參加。</p>",
        },
        "sc": {
            "title": "建造业五人足球比赛 2026（CISVP）",
            "body": "<p>建造业议会透过建造业运动及义工计划（CISVP），将于 2026 年 11 月 8 日上午 8 时至下午 6 时，在赛马会香港足球总会足球训练中心举行「建造业五人足球比赛 2026」。</p><p>赛事鼓励从业员参与运动、联系同业。同事可自行报名参加。</p>",
        },
    },
    {
        "id": 9,
        "date": {"en": "27 April 2026", "tc": "2026年4月27日", "sc": "2026年4月27日"},
        "en": {
            "title": "DSD Safety Culture Workshop",
            "body": "<p>Colleagues took part in a Drainage Services Department Safety Culture Workshop.</p><p>Supervisors shared how briefing, supervision and care of workers are put into practice on live roads and channels.</p>",
        },
        "tc": {
            "title": "渠務署安全文化工作坊",
            "body": "<p>同事參加渠務署安全文化工作坊。</p><p>督導人員交流如何於在用道路及渠道上交底、監督及照顧工友。</p>",
        },
        "sc": {
            "title": "渠务署安全文化工作坊",
            "body": "<p>同事参加渠务署安全文化工作坊。</p><p>督导人员交流如何于在用道路及渠道上交底、监督及照顾工友。</p>",
        },
    },
    {
        "id": 10,
        "date": {"en": "27 January 2026", "tc": "2026年1月27日", "sc": "2026年1月27日"},
        "en": {
            "title": "OSHC safety training for DSD emergency works in adverse weather",
            "body": "<p>Colleagues attended the Occupational Safety and Health Council course on safety for emergency drainage works in adverse weather.</p><p>The course covers rain, storms and other bad weather, including night call-outs, so that emergency attendance is planned and supervised to the same standard as programmed works.</p>",
        },
        "tc": {
            "title": "職安局惡劣天氣應急工程安全訓練",
            "body": "<p>同事出席職業安全健康局「惡劣天氣下渠務緊急工作安全培訓」。</p><p>課程涵蓋暴雨、風暴及其他惡劣天氣，包括夜間出勤，使緊急出勤在策劃及監督上與日常工程同一標準。</p>",
        },
        "sc": {
            "title": "职安局恶劣天气应急工程安全训练",
            "body": "<p>同事出席职业安全健康局「恶劣天气下渠务紧急工作安全培训」。</p><p>课程涵盖暴雨、风暴及其他恶劣天气，包括夜间出勤，使紧急出勤在策划及监督上与日常工程同一标准。</p>",
        },
    },
    {
        "id": 3,
        "date": {"en": "December 2025", "tc": "2025年12月", "sc": "2025年12月"},
        "imgs": ["../images/news/zero-pins.jpg", "../images/news/zero-declaration.png"],
        "en": {
            "title": "Zero Accident Ambassador Award 2025",
            "body": "<p>Frontline colleagues received the Zero Accident Ambassador Award 2025 from the Development Bureau and the Construction Industry Council.</p><p>The award recognises workers and supervisors who promote a zero-accident culture. A Zero Accident joint declaration was also signed.</p>",
        },
        "tc": {
            "title": "零意外大使獎 2025",
            "body": "<p>前線工友獲發展局及建造業議會頒發「零意外大使獎 2025」。</p><p>獎項表揚在地盤推動零意外文化的工友及督導人員。亦已簽署零意外聯合宣言。</p>",
        },
        "sc": {
            "title": "零意外大使奖 2025",
            "body": "<p>前线工友获发展局及建造业议会颁发「零意外大使奖 2025」。</p><p>奖项表扬在地盘推动零意外文化的工友及督导人员。亦已签署零意外联合宣言。</p>",
        },
    },
    {
        "id": 11,
        "date": {"en": "December 2025", "tc": "2025年12月", "sc": "2025年12月"},
        "en": {
            "title": "Lifting safety supervisor training",
            "body": "<p>Colleagues completed the Hong Kong Institute of Construction 22.5-hour programme and were awarded the Certificate for Lifting Safety Supervisors. The certificates are dated 17 November 2025 and 15 December 2025.</p><p>The course covers the planning and supervision of lifting operations. Plant, loads and exclusion zones are controlled before a lift starts.</p>",
        },
        "tc": {
            "title": "香港建造學院吊運安全督導訓練",
            "body": "<p>同事完成香港建造學院 22.5 小時課程，獲頒「吊運安全督導員」證書，日期分別為 2025 年 11 月 17 日及 12 月 15 日。</p><p>課程涵蓋吊運作業的策劃及監督。機械、荷載及隔離範圍在起吊前須受控制。</p>",
        },
        "sc": {
            "title": "香港建造学院吊运安全督导训练",
            "body": "<p>同事完成香港建造学院 22.5 小时课程，获颁「吊运安全督导员」证书，日期分别为 2025 年 11 月 17 日及 12 月 15 日。</p><p>课程涵盖吊运作业的策划及监督。机械、荷载及隔离范围在起吊前须受控制。</p>",
        },
    },
    {
        "id": 12,
        "date": {"en": "June 2025", "tc": "2025年6月", "sc": "2025年6月"},
        "imgs": ["../images/news/lifefirst.png"],
        "en": {
            "title": "Life First 2025 — Walk the Talk",
            "body": "<p>The Construction Industry Council “Life First 2025” campaign has the theme “Walk the Talk – Care round-the-clock” (關愛同心 行出安全).</p><p>Sites review high-risk work — working at height, heavy lifting, heavy plant, confined space and temporary works — and practise a zero-accident culture.</p>",
        },
        "tc": {
            "title": "生命第一 2025－關愛同心 行出安全",
            "body": "<p>建造業議會「生命第一 2025」安全推廣，主題為「關愛同心 行出安全」。</p><p>工地檢視高風險工序——高空工作、大型吊運、重型機械、密閉空間及臨時工程——並實踐零意外文化。</p>",
        },
        "sc": {
            "title": "生命第一 2025－关爱同心 行出安全",
            "body": "<p>建造业议会「生命第一 2025」安全推广，主题为「关爱同心 行出安全」。</p><p>工地检视高风险工序——高空工作、大型吊运、重型机械、密闭空间及临时工程——并实践零意外文化。</p>",
        },
    },
    {
        "id": 4,
        "date": {"en": "8 January 2026", "tc": "2026年1月8日", "sc": "2026年1月8日"},
        "en": {
            "title": "Responsible construction in the community",
            "body": "<p>Much of the work takes place on live roads, channels and in built-up neighbourhoods. Construction nuisance — noise, dust, wastewater and waste — is planned and controlled so that neighbouring residents and road users are protected while the works proceed.</p><p>Typical measures include agreed working hours, watering and screening for dust, proper collection of wastewater, and the timely removal of waste. Temporary traffic arrangements, barriers and lighting are set out so that pedestrians and vehicles can pass the site in safety.</p><p>Supervisors check the site boundary and the effect on the neighbourhood as regularly as they check production.</p>",
        },
        "tc": {
            "title": "對社區負責任的施工",
            "body": "<p>不少工程位於在用道路、渠道及已建成社區。施工滋擾——噪音、塵埃、污水及廢物——須事先策劃及控制，使工程進行期間保障鄰近居民及道路使用者。</p><p>常見措施包括議定施工時間、灑水及圍擋控制揚塵、妥善收集污水，以及準時清走廢物。臨時交通措施、圍欄及照明亦須設置妥當，讓行人及車輛安全經過地盤。</p><p>督導人員須如檢查進度一樣，定期檢查圍界及對鄰里的影響。</p>",
        },
        "sc": {
            "title": "对社区负责任的施工",
            "body": "<p>不少工程位于在用道路、渠道及已建成社区。施工滋扰——噪音、尘埃、污水及废物——须事先策划及控制，使工程进行期间保障邻近居民及道路使用者。</p><p>常见措施包括议定施工时间、洒水及围挡控制扬尘、妥善收集污水，以及准时清走废物。临时交通措施、围栏及照明亦须设置妥当，让行人及车辆安全经过地盘。</p><p>督导人员须如检查进度一样，定期检查围界及对邻里的影响。</p>",
        },
    },
    {
        "id": 14,
        "date": {"en": "August 2026", "tc": "2026年8月", "sc": "2026年8月"},
        "imgs": [
            "../images/news/manhole-cam.jpg",
            "../images/news/manhole-sign.jpg",
            "../images/news/manhole-gas.jpg",
        ],
        "en": {
            "title": "Fire drill and manhole-opening drill",
            "body": "<p>Colleagues took part in a fire drill and a manhole-opening drill.</p><p>The fire drill covered evacuation and the use of extinguishers at the depot. The manhole drill practised confined-space controls: gas testing, barriers, breathing apparatus and a lifeline before anyone enters underground pipework.</p>",
        },
        "tc": {
            "title": "火警演習及沙井開啟演習",
            "body": "<p>同事進行火警演習及沙井開啟演習。</p><p>火警演習涵蓋車房疏散及滅火筒使用。沙井演習練習密閉空間管控：進入地下喉管前須檢測氣體、設置圍欄、配戴認可呼吸器具及救生繩。</p>",
        },
        "sc": {
            "title": "火警演习及沙井开启演习",
            "body": "<p>同事进行火警演习及沙井开启演习。</p><p>火警演习涵盖车房疏散及灭火筒使用。沙井演习练习密闭空间管控：进入地下喉管前须检测气体、设置围栏、配戴认可呼吸器具及救生绳。</p>",
        },
    },
    {
        "id": 15,
        "date": {"en": "August 2026", "tc": "2026年8月", "sc": "2026年8月"},
        "imgs": ["../images/news/cic-health.png"],
        "en": {
            "title": "CIC medical check-up for registered construction workers",
            "body": "<p>The Construction Industry Council is running a medical check-up scheme for registered construction workers, with outreach on site.</p><p>For a fee of HK$10, the check-up covers body-mass index, blood pressure, pulse, blood sugar, cholesterol, liver and kidney function, and uric acid. Healthcare staff come to the site. A meeting room is enough; more than 50 registered workers can be seen in half a day. Reports are issued within 14 working days.</p>",
        },
        "tc": {
            "title": "議會註冊建造業工人醫療體檢計劃",
            "body": "<p>建造業議會推出「註冊建造業工人醫療體檢計劃 — 工地外展服務」，方便工友在地盤接受體檢。</p><p>收費 10 港元，項目包括身體質量指數（BMI）、血壓、脈搏、血糖、膽固醇、肝功能、腎功能及尿酸。由醫護人員到地盤進行，一般會議室即可，半天可為超過 50 名註冊工友完成體檢。報告於 14 個工作天內發出。</p>",
        },
        "sc": {
            "title": "议会注册建造业工人医疗体检计划",
            "body": "<p>建造业议会推出「注册建造业工人医疗体检计划 — 工地外展服务」，方便工友在地盘接受体检。</p><p>收费 10 港元，项目包括身体质量指数（BMI）、血压、脉搏、血糖、胆固醇、肝功能、肾功能及尿酸。由医护人员到地盘进行，一般会议室即可，半天可为超过 50 名注册工友完成体检。报告于 14 个工作天内发出。</p>",
        },
    },
    {
        "id": 16,
        "date": {"en": "August 2026", "tc": "2026年8月", "sc": "2026年8月"},
        "imgs": ["../images/news/smoke-locker.jpg", "../images/news/smoke-box.jpg"],
        "en": {
            "title": "No-smoking lockers and tobacco boxes on site",
            "body": "<p>Lockers and sealed boxes are provided so that tobacco is not kept in vehicles or inside the site fence.</p><p>This follows the ban on smoking on construction sites. Notices remind colleagues that smoking is not allowed in the works area.</p>",
        },
        "tc": {
            "title": "地盤控煙設施",
            "body": "<p>設置煙儲存櫃及密封香煙存放盒，煙草不得放在工程車內或地盤圍欄內。</p><p>此安排配合建築地盤全面禁煙。告示提醒同事不得在工地範圍吸煙。</p>",
        },
        "sc": {
            "title": "地盘控烟设施",
            "body": "<p>设置烟储存柜及密封香烟存放盒，烟草不得放在工程车内或地盘围栏内。</p><p>此安排配合建筑地盘全面禁烟。告示提醒同事不得在工地范围吸烟。</p>",
        },
    },
    {
        "id": 18,
        "date": {"en": "August 2026", "tc": "2026年8月", "sc": "2026年8月"},
        "en": {
            "title": "Safety video, site newsletter, spot checks, breath tests and worker QR codes",
            "body": "<p>A safety video is shown on the depot television. Safety newsletters are posted at the depot and on site. Senior staff carry out spot checks on live works. Random breath tests for alcohol are made with a handheld meter. Helmets carry a QR code so that a worker’s training record can be checked.</p>",
        },
        "tc": {
            "title": "車房職安短片、地盤通訊、巡查、酒精測試及工友資料二維碼",
            "body": "<p>車房電視播放職安短片。車房及地盤張貼安全通訊。管理層到在用工程抽查。同事以手提儀器進行隨機酒精呼氣測試。安全帽貼有二維碼，方便核對工友培訓紀錄。</p>",
        },
        "sc": {
            "title": "车房职安短片、地盘通讯、巡查、酒精测试及工友资料二维码",
            "body": "<p>车房电视播放职安短片。车房及地盘张贴安全通讯。管理层到在用工程抽查。同事以手提仪器进行随机酒精呼气测试。安全帽贴有二维码，方便核对工友培训纪录。</p>",
        },
    },
    {
        "id": 19,
        "date": {"en": "August 2026", "tc": "2026年8月", "sc": "2026年8月"},
        "en": {
            "title": "Safety working team award",
            "body": "<p>Frontline teams received a safety working team award.</p><p>The scheme recognises teams that keep to site rules and look after one another.</p>",
        },
        "tc": {
            "title": "安全工作隊伍獎勵",
            "body": "<p>前線隊伍獲安全工作隊伍獎勵。</p><p>計劃表揚遵守地盤規則、互相照顧的隊伍。</p>",
        },
        "sc": {
            "title": "安全工作队伍奖励",
            "body": "<p>前线队伍获安全工作队伍奖励。</p><p>计划表扬遵守地盘规则、互相照顾的队伍。</p>",
        },
    },
    {
        "id": 20,
        "date": {"en": "August 2026", "tc": "2026年8月", "sc": "2026年8月"},
        "en": {
            "title": "Toolbox talks",
            "body": "<p>Colleagues attend toolbox talks on the hazards of the day’s work. Induction and refresher training are also held.</p><p>Talks cover lifting, manhole opening and work on live roads and channels, so that the briefing matches what colleagues will actually do that shift.</p>",
        },
        "tc": {
            "title": "工具箱講座",
            "body": "<p>同事出席工具箱講座，講解當日工序的危害。地盤亦舉辦入職及重溫訓練。</p><p>講座涵蓋吊運、沙井開啟，以及在用道路及渠道作業，使交底與當更實際工作相符。</p>",
        },
        "sc": {
            "title": "工具箱讲座",
            "body": "<p>同事出席工具箱讲座，讲解当日工序的危害。地盘亦举办入职及重温训练。</p><p>讲座涵盖吊运、沙井开启，以及在用道路及渠道作业，使交底与当更实际工作相符。</p>",
        },
    },
]

NEWS_CATES = {
    "en": [("news.php", "Latest News"), ("news_cate-10.php", "Recruitment"), ("news_cate-13.php", "Integrity Management Policy")],
    "tc": [("news.php", "最新消息"), ("news_cate-10.php", "招聘"), ("news_cate-13.php", "誠信管理政策")],
    "sc": [("news.php", "最新消息"), ("news_cate-10.php", "招聘"), ("news_cate-13.php", "诚信管理政策")],
}

LABELS = {
    "en": {
        "about": "About us",
        "expertise": "Our expertise",
        "projects": "Projects",
        "sustainability": "Safety, Quality & Environment",
        "talent": "Talent development",
        "news": "News",
        "contact": "Contact us",
        "culture": "Company Culture",
        "vision": "Our Vision",
        "contract_no": "Contract No",
        "contract_value": "Client",
        "period": "Period",
        "details": "Read more",
        "latest": "Latest News",
        "news_back": "Back to latest news",
        "office": "Main Office",
        "email": "E-mail",
        "website": "Website",
        "tel": "Tel",
        "fax": "Fax",
        "participate": "Participated in",
        "role": "Our role",
        "role_value": "Participated in the works of this term contract",
        "projects_intro": "Selected Highways Department and Drainage Services Department term contracts, and major-event road works, in which Wah Fung has taken part.",
        "address": "Rm. 310, 3/F, Fuk Shing Commercial Building, No.28, On Lok Mun Street, On Lok Tsuen, Fanling, N.T., Hong Kong",
    },
    "tc": {
        "about": "關於我們",
        "expertise": "專業資格",
        "projects": "項目",
        "sustainability": "安全、品質及環境",
        "talent": "人才發展",
        "news": "新聞",
        "contact": "聯繫我們",
        "culture": "公司文化",
        "vision": "我們的願景",
        "contract_no": "合約編號",
        "contract_value": "服務對象",
        "period": "期間",
        "details": "詳情",
        "latest": "最新消息",
        "news_back": "返回最新消息",
        "office": "總辦事處",
        "email": "電郵",
        "website": "網站",
        "tel": "電話",
        "fax": "傳真",
        "participate": "本公司有參與",
        "role": "參與角色",
        "role_value": "參與此定期合約工程",
        "projects_intro": "華丰曾參與的路政署及渠務署定期合約，以及大型盛事封路工程如下。",
        "address": "香港新界粉嶺安樂村安樂門街28號福成商業大廈3樓310室",
    },
    "sc": {
        "about": "关于我们",
        "expertise": "专业资格",
        "projects": "项目",
        "sustainability": "安全、品质及环境",
        "talent": "人才发展",
        "news": "新闻",
        "contact": "联系我们",
        "culture": "公司文化",
        "vision": "我们的愿景",
        "contract_no": "合约编号",
        "contract_value": "服务对象",
        "period": "期间",
        "details": "详情",
        "latest": "最新消息",
        "news_back": "返回最新消息",
        "office": "总办事处",
        "email": "电邮",
        "website": "网站",
        "tel": "电话",
        "fax": "传真",
        "participate": "本公司有参与",
        "role": "参与角色",
        "role_value": "参与此定期合约工程",
        "projects_intro": "华丰曾参与的路政署及渠务署定期合约，以及大型盛事封路工程如下。",
        "address": "香港新界粉岭安乐村安乐门街28号福成商业大厦3楼310室",
    },
}

EMAIL = "enquiry@chdx-jv.com"
PHONE = "(852) 2818 3428"
FAX = "(852) 2818 3511"
LINKEDIN = "https://www.linkedin.com/company/wah-fung-engineering-company-limited"
DIXIE_LABEL = {
    "en": "Dixie Engineering Office",
    "tc": "仁利工程辦事處",
    "sc": "仁利工程办事处",
}
DIXIE_ADDR = {
    "en": "Unit 21, 20/F, Block A, Wah Lok Industrial Centre, 31-41 Shan Mei Street, Fo Tan, Sha Tin, New Territories, Hong Kong",
    "tc": "香港新界沙田火炭山尾街31-41號華樂工業中心A座20樓21室",
    "sc": "香港新界沙田火炭山尾街31-41号华乐工业中心A座20楼21室",
}
MAPS_EMBED = (
    "https://www.google.com/maps?q=Fuk+Shing+Commercial+Building,"
    "+28+On+Lok+Mun+Street,+Fanling,+Hong+Kong&hl=en&z=17&output=embed"
)


HTML_LANG = {"en": "en", "tc": "zh-Hant", "sc": "zh-Hans"}


def head(title: str, lang: str = "en") -> str:
    desc = CURRENT_SITE["desc"][lang]
    return f"""<!DOCTYPE html>
<html lang="{HTML_LANG[lang]}">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="{title}">
<meta property="og:title" content="{title}">
<meta property="og:site_name" content="{title}">
<meta property="og:description" content="{desc}">
<style>
html{{font-size:16px}}
body{{margin:0;font-size:14px;line-height:1.5;color:#243044}}
.wf-page-title{{font-size:34px;font-weight:700;line-height:1.2}}
#header .main-nav > li > a{{font-size:12px;font-weight:600}}
</style>
<link href="../images/favicon.ico" type="image/x-icon" rel="icon" />
<link rel="stylesheet" href="../vendor/maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
<link href="../vendor/maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
<link href="../css/ui.css?v=n21" rel="stylesheet">
<style>
.news_list .news{{display:flex !important;align-items:center;gap:16px;padding:16px;overflow:visible !important;position:relative}}
.news_list .news_thumb{{flex:0 0 128px !important;position:static !important;left:auto !important;top:auto !important;width:128px !important;height:86px !important;overflow:hidden;margin:0}}
.news_list .news_thumb img{{width:128px !important;height:86px !important;max-width:none !important;object-fit:cover;object-position:top center;display:block}}
.news_list .news_copy{{flex:1 1 auto;min-width:0}}
.news_list .news_btn{{flex:0 0 auto;position:static !important;margin:0;top:auto !important;right:auto !important}}
@media (max-width:575px){{
.news_list .news{{flex-direction:column;align-items:stretch}}
.news_list .news_thumb,.news_list .news_thumb img{{width:100% !important;height:160px !important}}
.news_list .news_btn{{align-self:flex-start;margin-top:12px}}
}}
</style>
</head>
<body>
<div class="main-wrapper">
"""


def header(lang: str, page: str) -> str:
    fname = page
    def lang_href(target: str) -> str:
        return fname if lang == target else f"../{target}/{fname}"
    items = [
        f'<a href="{lang_href("tc")}">繁</a>',
        f'<a href="{lang_href("sc")}">簡</a>',
        f'<a href="{lang_href("en")}">Eng</a>',
    ]
    nav = []
    activated = set()
    for href, label in NAV[lang]:
        active = ""
        here = href == page
        if href == "projects.php" and page.startswith("projects-detail"):
            here = True
        elif href == "news.php" and (page.startswith("news") or page.startswith("news_")):
            here = True
        if here and href not in activated:
            active = ' class="active"'
            activated.add(href)
        nav.append(f'<li{active}><a href="{href}">{label}</a></li>')
    brands = []
    for c in GROUP_COMPANIES:
        d = c[lang]
        href = c.get("linkedin") or "aboutus.php"
        extra = ' target="_blank" rel="noopener"' if c.get("linkedin") else ""
        label = d.get("short_en") or d["short"]
        brands.append(
            f'<a class="wf-brand" href="{href}"{extra}>'
            f'<img src="{c["logo"]}" alt="{label}">'
            f"<span>{label}</span></a>"
        )
    return f"""
<nav id="header" class="navbar navbar-main">
  <div class="container">
    <div class="wf-bar">
      <div class="wf-brands" id="brand">{''.join(brands)}</div>
      <div class="wf-header-tools">
        <div class="language-link">{''.join(items)}</div>
        <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
          <span class="sr-only">Toggle navigation</span>
          <span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span>
        </button>
      </div>
    </div>
  </div>
  <div id="navigation" class="container-fluid pad-0">
    <div class="container">
      <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
        <ul class="nav navbar-nav main-nav">
          {''.join(nav)}
        </ul>
      </div>
    </div>
  </div>
</nav>
"""


def footer(lang: str) -> str:
    return f"""
</div>
<div class="clear-fix"></div>
<footer>
  <div class="wf-footer">
    <div class="container wf-foot-inner">
      <div class="wf-foot-left">
        <a class="contactus" href="aboutus.php">{CONTACT_LABEL[lang]}</a>
      </div>
      <p class="copy">{COPYRIGHT[lang]}</p>
    </div>
  </div>
</footer>
<script src="../vendor/ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="../vendor/maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" type="text/javascript"></script>
<script src="../js/custom.js"></script>
</body>
</html>
"""


def inner_page(image: str, title: str, body: str) -> str:
    return f"""
<article class="wf-page">
  <header class="wf-page-top">
    <div class="container">
      <h1 class="wf-page-title">{title}</h1>
    </div>
  </header>
  <figure class="wf-page-shot"><img src="{image}" alt=""></figure>
  <div class="wf-page-main">
    <div class="container">
      {body}
    </div>
  </div>
</article>
"""


def with_assets(html: str) -> str:
    for folder in ("images", "vendor", "css", "js"):
        html = html.replace(f"../{folder}/", f"../../{folder}/")
    return html


def write_page(lang: str, filename: str, body: str) -> None:
    html = head(CURRENT_SITE[lang], lang) + header(lang, filename) + body + footer(lang)
    html = html.replace(".php", ".html")
    html = with_assets(html)
    stem = filename[:-4] if filename.endswith(".php") else Path(filename).stem
    out = ROOT / CURRENT_SITE["slug"] / lang
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{stem}.html").write_text(html, encoding="utf-8")


def page_home(lang: str) -> str:
    slides = []
    tabs = []
    for i, s in enumerate(SLIDES):
        active = " active" if i == 0 else ""
        title, desc = s[lang]
        slides.append(f'''
        <div class="item{active}">
          <img src="{s["img"]}" alt="{title}">
          <div class="wf-hero-cap">
            <h2>{title}</h2>
            <p>{desc}</p>
          </div>
        </div>''')
        tabs.append(
            f'<li data-target="#home-hero" data-slide-to="{i}" class="{active.strip()}">{title}</li>'
        )
    tiles = []
    for i, (href, img, titles) in enumerate(HOME_TILES):
        tiles.append(f'''
        <a class="wf-bento-item wf-bento-{i}" href="{href}">
          <img src="{img}" alt="">
          <span>{titles[lang]}</span>
        </a>''')
    return f"""
<section class="wf-hero">
  <div id="home-hero" class="carousel slide carousel-fade" data-ride="carousel" data-interval="5500">
    <div class="carousel-inner" role="listbox">
      {''.join(slides)}
    </div>
    <ol class="carousel-indicators wf-hero-tabs">
      {''.join(tabs)}
    </ol>
  </div>
</section>
<section class="wf-band">
  <div class="container">
    <h2>{HOME_TAGLINE[lang]}</h2>
  </div>
</section>
<section class="wf-bento-wrap">
  <div class="container">
    <div class="wf-bento">
      {''.join(tiles)}
    </div>
  </div>
</section>
"""


ABOUT = {
    "en": """
<p>The Wah Fung group is a privately held Hong Kong civil and building engineering contractor group. Together we deliver civil engineering, building and related construction and maintenance services to public and private clients.</p>
<p>The group focuses on practical, well-managed projects — roads and drainage, site formation, slope works and general repair and maintenance works. Our teams combine site experience with careful planning, cost control and a strong sense of responsibility on safety and quality.</p>
<p>We aim to be a trusted construction partner. We work closely with clients, consultants and subcontractors, and we are committed to finishing works that stand up to inspection, operation and the expectations of the community.</p>
""",
    "tc": """
<p>華丰集團為香港私人持有的土木及建築工程承建商集團，為公營及私營客戶提供土木工程、建築及相關建造及維修服務。</p>
<p>集團專注務實而有序的工程項目，業務涵蓋道路及渠務、地盤平整、斜坡工程及一般維修保養工程。團隊結合地盤經驗與審慎策劃、成本控制，並對安全及品質抱持高度責任感。</p>
<p>我們致力成為值得信賴的建造合作夥伴，與客戶、顧問及分包商緊密合作，務求完成經得起檢查、營運及社區期望的工程。</p>
""",
    "sc": """
<p>华丰集团为香港私人持有的土木及建筑工程承建商集团，为公营及私营客户提供土木工程、建筑及相关建造及维修服务。</p>
<p>集团专注务实而有序的工程项目，业务涵盖道路及渠务、地盘平整、斜坡工程及一般维修保养工程。团队结合地盘经验与审慎策划、成本控制，并对安全及品质抱持高度责任感。</p>
<p>我们致力成为值得信赖的建造合作伙伴，与客户、顾问及分包商紧密合作，务求完成经得起检查、营运及社区期望的工程。</p>
""",
}

GROUP_TITLE = {"en": "Our Companies", "tc": "集團公司", "sc": "集团公司"}
GROUP_COMPANIES = [
    {
        "no": "1",
        "logo": "../images/company/1.png",
        "linkedin": "https://www.linkedin.com/company/wah-fung-engineering-company-limited",
        "en": {
            "zh": "華丰工程有限公司",
            "en": "WAH FUNG ENGINEERING COMPANY LIMITED",
            "short": "華丰",
            "short_en": "WAH FUNG",
            "note": "Civil engineering contractor, founded 1998",
        },
        "tc": {
            "zh": "華丰工程有限公司",
            "en": "WAH FUNG ENGINEERING COMPANY LIMITED",
            "short": "華丰",
            "note": "土木工程承建商，1998年成立",
        },
        "sc": {
            "zh": "华丰工程有限公司",
            "en": "WAH FUNG ENGINEERING COMPANY LIMITED",
            "short": "华丰",
            "note": "土木工程承建商，1998年成立",
        },
        "facts": {
            "en": [
                ("Founded", "1998"),
                ("Industry", "Civil Engineering"),
                ("Company type", "Privately held"),
                ("Company size", "201 – 500 employees"),
                ("Company no.", "0655644"),
                ("Office", "Fanling, New Territories, Hong Kong"),
            ],
            "tc": [
                ("成立年份", "1998"),
                ("行業", "土木工程"),
                ("公司類型", "私人持有"),
                ("公司規模", "201 – 500 人"),
                ("公司註冊編號", "0655644"),
                ("辦事處", "香港新界粉嶺"),
            ],
            "sc": [
                ("成立年份", "1998"),
                ("行业", "土木工程"),
                ("公司类型", "私人持有"),
                ("公司规模", "201 – 500 人"),
                ("公司注册编号", "0655644"),
                ("办事处", "香港新界粉岭"),
            ],
        },
    },
    {
        "no": "2",
        "logo": "../images/company/2.png",
        "linkedin": "https://www.linkedin.com/company/wah-fung-building-engineering-limited",
        "en": {
            "zh": "華丰建設工程有限公司",
            "en": "WAH FUNG BUILDING &amp; ENGINEERING LIMITED",
            "short": "華丰建設",
            "short_en": "WAH FUNG BUILDING",
            "note": "Building and engineering contractor, founded 2011",
        },
        "tc": {
            "zh": "華丰建設工程有限公司",
            "en": "WAH FUNG BUILDING &amp; ENGINEERING LIMITED",
            "short": "華丰建設",
            "note": "建設工程承建商，2011年成立",
        },
        "sc": {
            "zh": "华丰建设工程有限公司",
            "en": "WAH FUNG BUILDING &amp; ENGINEERING LIMITED",
            "short": "华丰建设",
            "note": "建设工程承建商，2011年成立",
        },
        "facts": {
            "en": [
                ("Founded", "2011"),
                ("Industry", "Building and Engineering"),
                ("Company type", "Privately held"),
                ("Company no.", "58340844"),
                ("Office", "Fanling, New Territories, Hong Kong"),
            ],
            "tc": [
                ("成立年份", "2011"),
                ("行業", "建設工程"),
                ("公司類型", "私人持有"),
                ("公司註冊編號", "58340844"),
                ("辦事處", "香港新界粉嶺"),
            ],
            "sc": [
                ("成立年份", "2011"),
                ("行业", "建设工程"),
                ("公司类型", "私人持有"),
                ("公司注册编号", "58340844"),
                ("办事处", "香港新界粉岭"),
            ],
        },
    },
    {
        "no": "3",
        "logo": "../images/company/3.png",
        "linkedin": "https://www.linkedin.com/company/dixie-engineering-company-limited",
        "en": {
            "zh": "仁利工程有限公司",
            "en": "DIXIE ENGINEERING COMPANY LIMITED",
            "short": "仁利",
            "short_en": "DIXIE",
            "note": "Civil engineering contractor, founded 1989",
        },
        "tc": {
            "zh": "仁利工程有限公司",
            "en": "DIXIE ENGINEERING COMPANY LIMITED",
            "short": "仁利",
            "note": "土木工程承建商，1989年成立",
        },
        "sc": {
            "zh": "仁利工程有限公司",
            "en": "DIXIE ENGINEERING COMPANY LIMITED",
            "short": "仁利",
            "note": "土木工程承建商，1989年成立",
        },
        "facts": {
            "en": [
                ("Founded", "1989"),
                ("Industry", "Civil Engineering"),
                ("Company type", "Privately held"),
                ("Company no.", "12798229"),
                ("Office", "Fo Tan, Sha Tin, New Territories, Hong Kong"),
            ],
            "tc": [
                ("成立年份", "1989"),
                ("行業", "土木工程"),
                ("公司類型", "私人持有"),
                ("公司註冊編號", "12798229"),
                ("辦事處", "香港新界沙田火炭"),
            ],
            "sc": [
                ("成立年份", "1989"),
                ("行业", "土木工程"),
                ("公司类型", "私人持有"),
                ("公司注册编号", "12798229"),
                ("办事处", "香港新界沙田火炭"),
            ],
        },
    },
]


def facts_grid_html(pairs) -> str:
    return "\n            ".join(
        f'<div class="col-xs-12 col-sm-6 col-md-4">\n'
        f'              <div class="wf-fact">\n'
        f'                <h4>{k}</h4>\n'
        f'                <p>{v}</p>\n'
        f'              </div>\n'
        f'            </div>'
        for k, v in pairs
    )


def company_list_html(lang: str, selectable: bool = False) -> str:
    li_lab = {"en": "LinkedIn", "tc": "LinkedIn", "sc": "LinkedIn"}[lang]
    items = []
    for c in GROUP_COMPANIES:
        d = c[lang]
        link = ""
        if c.get("linkedin"):
            link = (
                f'<a class="wf-co-li" href="{c["linkedin"]}" target="_blank" rel="noopener">'
                f"{li_lab}</a>"
            )
        extra = ""
        caret = ""
        profile = ""
        if selectable:
            extra = f' data-co="{c["no"]}"'
            caret = '<span class="wf-co-caret" aria-hidden="true"><i class="fa fa-angle-down"></i></span>'
            profile = f"""
            <div class="wf-co-profile" id="wf-profile-{c["no"]}">
              <div class="wf-co-profile-title">{FACTS_TITLE[lang]}</div>
              <div class="row wf-facts">
                {facts_grid_html(c["facts"][lang])}
              </div>
            </div>"""
        items.append(
            f"""<li{extra}>
            <div class="wf-co-toggle" role="button" tabindex="0" aria-expanded="false">
              <div class="wf-co-num">{c["no"]}</div>
              <div class="wf-co-logo"><img src="{c["logo"]}" alt="{d["en"]}"></div>
              <div class="wf-co-body">
                <span class="wf-co-zh">{d["zh"]}</span>
                <span class="wf-co-en">{d["en"]}</span>
                <p>{d["note"]}</p>
                {link}
              </div>
              {caret}
            </div>
            {profile}
          </li>"""
        )
    cls = "wf-company-list wf-company-select" if selectable else "wf-company-list"
    return f'<ol class="{cls}">\n          ' + "\n          ".join(items) + "\n        </ol>"
VISION = {
    "en": "We value people as highly as technical performance. Wah Fung seeks steady growth together with uncompromising standards in quality, safety and environmental protection. Clear communication, recognition of good work and a practical, people-first culture support our aim to compete and to serve with excellence.",
    "tc": "我們如同重視技術一樣重視員工。華丰在追求穩健發展的同時，堅持品質、安全及環境保護的標準。清晰溝通、肯定優秀表現，以及務實、以人為本的文化，支持我們競爭並以卓越服務客戶。",
    "sc": "我们如同重视技术一样重视员工。华丰在追求稳健发展的同时，坚持品质、安全及环境保护的标准。清晰沟通、肯定优秀表现，以及务实、以人为本的文化，支持我们竞争并以卓越服务客户。",
}


FACTS = {
    "en": [
        ("Founded", "1998"),
        ("Industry", "Civil Engineering"),
        ("Company type", "Privately held"),
        ("Company size", "201 – 500 employees"),
        ("Company no.", "0655644"),
        ("Office", "Fanling, New Territories, Hong Kong"),
    ],
    "tc": [
        ("成立年份", "1998"),
        ("行業", "土木工程"),
        ("公司類型", "私人持有"),
        ("公司規模", "201 – 500 人"),
        ("公司註冊編號", "0655644"),
        ("辦事處", "香港新界粉嶺"),
    ],
    "sc": [
        ("成立年份", "1998"),
        ("行业", "土木工程"),
        ("公司类型", "私人持有"),
        ("公司规模", "201 – 500 人"),
        ("公司注册编号", "0655644"),
        ("办事处", "香港新界粉岭"),
    ],
}
FACTS_TITLE = {"en": "Company Profile", "tc": "公司概況", "sc": "公司概况"}


def office_block_html(lang: str) -> str:
    L = LABELS[lang]
    return f"""
          <div class="row" style="margin-top:20px;">
            <div class="col-sm-7">
              <h3 class="red-txt">{L["office"]}</h3>
              <p>{L["address"]}</p>
              <p>
                  {L["tel"]}: {PHONE}<br/>
                  {L["fax"]}: {FAX}<br/>
                  {L["email"]}: <a href="mailto:{EMAIL}">{EMAIL}</a><br/>
                  LinkedIn: <a href="{LINKEDIN}" target="_blank" rel="noopener">Wah Fung Engineering Company Limited</a>
              </p>
              <h3 class="red-txt">{DIXIE_LABEL[lang]}</h3>
              <p>{DIXIE_ADDR[lang]}</p>
            </div>
            <div class="col-sm-5">
              <iframe src="{MAPS_EMBED}" width="100%" height="300" frameborder="0" style="border:0;max-width:100%;" allowfullscreen></iframe>
            </div>
          </div>
"""


def page_about(lang: str) -> str:
    L = LABELS[lang]
    return inner_page("../images/banner/1.jpg", L["about"], f"""
        <div class="about-content">
          {ABOUT[lang].strip()}
        </div>
        <div class="company-name">
          <div class="wf-block-title"><h2>{GROUP_TITLE[lang]}</h2></div>
          {company_list_html(lang, selectable=True)}
          <div class="wf-block-title"><h2>{L["culture"]}</h2></div>
          <div class="wf-culture">
            <h3 class="red-txt">{L["vision"]}</h3>
            <p>{VISION[lang]}</p>
          </div>
          {office_block_html(lang)}
        </div>
""")


EXPERTISE_INTRO = {
    "en": "Wah Fung undertakes a range of civil and building engineering works, from constrained urban operations to larger infrastructure packages. Work typically includes:",
    "tc": "華丰承接各類土木及建築工程，由受限制的市區作業以至較大型基建項目。工作範疇主要包括：",
    "sc": "华丰承接各类土木及建筑工程，由受限制的市区作业以至较大型基建项目。工作范畴主要包括：",
}
EXPERTISE_ITEMS = {
    "en": ["Roads and Drainage", "Site Formation", "Slope Works", "General Building Works", "Maintenance and Term Contracts"],
    "tc": ["道路及渠務", "地盤平整", "斜坡工程", "一般建築工程", "保養及定期合約"],
    "sc": ["道路及渠务", "地盘平整", "斜坡工程", "一般建筑工程", "保养及定期合约"],
}
EXPERTISE_MORE = {
    "en": """
<p>Wah Fung organises each project around programme, safety, quality and cost. Typical services include construction, maintenance, improvement and refurbishment of civil and building assets in Hong Kong.</p>
<p>We work with government departments, public organisations and private employers, and we tailor the site establishment, plant and labour to the constraints of each location.</p>
""",
    "tc": """
<p>華丰以進度、安全、品質及成本組織每個項目。服務包括香港土木及建築資產的建造、保養、改善及翻新。</p>
<p>我們與政府部門、公營機構及私人僱主合作，並按每個地盤的限制調配場地、機械及人手。</p>
""",
    "sc": """
<p>华丰以进度、安全、品质及成本组织每个项目。服务包括香港土木及建筑资产的建造、保养、改善及翻新。</p>
<p>我们与政府部门、公营机构及私人雇主合作，并按每个地盘的限制调配场地、机械及人手。</p>
""",
}

ISO_HEADING = {
    "en": "ISO Certifications",
    "tc": "ISO 認證",
    "sc": "ISO 认证",
}
ISO_INTRO = {
    "en": "Dixie Engineering Company Limited holds the following accredited management system certificates. They apply to construction of civil engineering works (waterworks, site formation, roads and drainage) and maintenance of civil engineering works.",
    "tc": "仁利工程有限公司持有以下經認可的管理體系證書，適用於土木工程的建造（水務工程、地盤平整、道路和渠務）及土木工程的維修保養。",
    "sc": "仁利工程有限公司持有以下经认可的管理体系证书，适用于土木工程的建造（水务工程、地盘平整、道路和渠务）及土木工程的维修保养。",
}
ISO_NO = {"en": "Certificate No.", "tc": "證書編號", "sc": "证书编号"}
ISO_CERTS = [
    {
        "file": "iso-9001-2015.pdf",
        "img": "iso-9001.png",
        "code": "ISO 9001:2015",
        "no": "Q1505",
        "en": "Quality Management System",
        "tc": "品質管理體系",
        "sc": "品质管理体系",
    },
    {
        "file": "iso-14001-2015.pdf",
        "img": "iso-14001.png",
        "code": "ISO 14001:2015",
        "no": "E855",
        "en": "Environmental Management System",
        "tc": "環境管理體系",
        "sc": "环境管理体系",
    },
    {
        "file": "iso-45001-2018.pdf",
        "img": "iso-45001.png",
        "code": "ISO 45001:2018",
        "no": "S681",
        "en": "Occupational Health and Safety",
        "tc": "職業健康及安全管理體系",
        "sc": "职业健康及安全管理体系",
    },
]


FOUR_S = {
    "en": {
        "h": "Smart Site Safety System (4S)",
        "intro": "On Drainage Services Department Term Contract DC/2023/04 (drainage maintenance and construction in Kowloon and New Territories South), Wah Fung applies the Construction Industry Council Smart Site Safety System (4S). Confined-space monitoring supports site safety.",
        "label": "Smart Site Safety System labelling",
        "label_meta": "Contract DC/2023/04",
        "conf": "Confined-space monitoring",
        "conf_meta": "Centralised Management Platform (CMP) and alert system",
    },
    "tc": {
        "h": "安全智慧工地 4S",
        "intro": "華丰於渠務署定期合約 DC/2023/04（九龍及新界南區的渠務維修及建造工程）地盤，採用建造業議會安全智慧工地系統（4S），以密閉空間監察加強職安。",
        "label": "安全智慧工地系統標籤",
        "label_meta": "合約 DC/2023/04",
        "conf": "密閉空間監察",
        "conf_meta": "中央管理平台（CMP）及警報系統",
    },
    "sc": {
        "h": "安全智慧工地 4S",
        "intro": "华丰于渠务署定期合约 DC/2023/04（九龙及新界南区的渠务维修及建造工程）地盘，采用建造业议会安全智慧工地系统（4S），以密闭空间监察加强职安。",
        "label": "安全智慧工地系统标签",
        "label_meta": "合约 DC/2023/04",
        "conf": "密闭空间监察",
        "conf_meta": "中央管理平台（CMP）及警报系统",
    },
}


def four_s_html(lang: str) -> str:
    t = FOUR_S[lang]
    return f"""
<h3 class="red-txt">{t["h"]}</h3>
<p>{t["intro"]}</p>
<div class="wf-certs wf-4s">
      <div class="wf-cert">
        <span class="wf-cert-shot"><img src="../images/certs/4s-label.jpg" alt="4S L 04218"></span>
        <span class="wf-cert-body">
          <strong>4S L 04218</strong>
          <em>{t["label"]}</em>
          <span class="wf-cert-meta">{t["label_meta"]}</span>
        </span>
      </div>
      <div class="wf-cert">
        <span class="wf-4s-icon"><i class="fa fa-eye" aria-hidden="true"></i></span>
        <span class="wf-cert-body">
          <strong>{t["conf"]}</strong>
          <em>{t["conf_meta"]}</em>
        </span>
      </div>
</div>
"""


def iso_certs_html(lang: str) -> str:
    cards = []
    for c in ISO_CERTS:
        cards.append(f'''
      <div class="wf-cert">
        <span class="wf-cert-shot"><img src="../images/certs/{c["img"]}" alt="{c["code"]}"></span>
        <span class="wf-cert-body">
          <strong>{c["code"]}</strong>
          <em>{c[lang]}</em>
          <span class="wf-cert-meta">{ISO_NO[lang]} {c["no"]}</span>
        </span>
      </div>''')
    return f"""
<h3 class="red-txt">{ISO_HEADING[lang]}</h3>
<p>{ISO_INTRO[lang]}</p>
<div class="wf-certs">{''.join(cards)}
</div>
"""


def page_expertise(lang: str) -> str:
    L = LABELS[lang]
    lis = "".join(f'<li>{x}</li>' for x in EXPERTISE_ITEMS[lang])
    return inner_page("../images/banner/2.jpg", L["expertise"], f"""
    <div class="about-content">
      <p>{EXPERTISE_INTRO[lang]}</p>
      <ul class="wf-skills">{lis}</ul>
      {EXPERTISE_MORE[lang]}
      {iso_certs_html(lang)}
    </div>
""")


def _project_start_year(p: dict) -> int:
    m = re.search(r"(\d{4})", p["en"]["period"])
    return int(m.group(1)) if m else 9999


def page_projects(lang: str) -> str:
    L = LABELS[lang]
    cards = []
    for p in sorted(PROJECTS, key=_project_start_year, reverse=True):
        t = p[lang]
        cards.append(f'''
        <div class="col-xs-12 col-sm-6 col-md-4">
          <a class="wf-job" href="projects-detail_id-{p["id"]}.php">
            <span class="wf-job-media"><img src="{p["cover"]}" alt="{t["title"]}"></span>
            <span class="wf-job-body">
              <span class="wf-contract-no">{t["no"]}</span>
              <span class="wf-job-title">{t["title"]}</span>
            </span>
          </a>
        </div>''')
    return inner_page("../images/banner/3.jpg", L["projects"], f"""
      <p class="about-content wf-lead">{L["projects_intro"]}</p>
      <div class="row product-boxes">
      {''.join(cards)}
      </div>
""")


def page_project_detail(lang: str, p: dict) -> str:
    L = LABELS[lang]
    t = p[lang]
    role_text = t.get("role", L["role_value"])
    cover = p["cover"]
    return inner_page("../images/banner/3.jpg", L["projects"], f"""
    <div class="project-details"><h2>{t["title"]}</h2></div>
    <ul class="wf-spec">
      <li><em>{L["contract_no"]}</em><span>{t["no"]}</span></li>
      <li><em>{L["contract_value"]}</em><span>{t["value"]}</span></li>
      <li><em>{L["period"]}</em><span>{t["period"]}</span></li>
      <li><em>{L["role"]}</em><span>{role_text}</span></li>
    </ul>
    <div class="wf-gallery">
      <div class="carousel slide" id="article-photo-carousel" data-ride="carousel" data-interval="false">
        <div class="carousel-inner"><div class="item active"><img alt="" src="{cover}"></div></div>
      </div>
    </div>
""")


SUST = {
    "en": """
<h3 class="red-txt">Safety, Quality and Environmental Policy</h3>
<p>Wah Fung complies with applicable ordinances and regulations. The aim of the Company is to protect the health, safety and welfare of employees, subcontractors and the public during the works, and to reduce noise, air and water pollution as well as construction waste.</p>
<p>Operations are planned to meet contractual requirements. Inspection, supervision and corrective action are part of daily site practice.</p>
<h3 class="red-txt">Social Responsibility</h3>
<p>Beyond the contract, Wah Fung acts as a responsible contractor in the neighbourhood of each site. We manage working hours, site cleanliness and public access so that construction can proceed with as little disruption as possible.</p>
<h3 class="red-txt">Community Involvement</h3>
<p>The Company supports a culture of care in the construction industry — looking after workers, neighbours and the environment in every assignment we take on.</p>
""",
    "tc": """
<h3 class="red-txt">安全、品質及環境政策</h3>
<p>華丰遵守適用法例及規例。公司宗旨是在施工期間保障僱員、分包商及公眾的健康、安全及福利，並減少噪音、空氣及水質污染以及建築廢料。</p>
<p>各項作業按合約要求策劃，檢查、監督及糾正行動屬日常地盤工作的一部分。</p>
<h3 class="red-txt">社會責任</h3>
<p>除履行合約外，華丰在每個地盤鄰近範圍以負責任承建商自居，管理工時、場地整潔及公眾通道，盡量減低施工對四周的影響。</p>
<h3 class="red-txt">社區參與</h3>
<p>本公司推動建造業關懷文化，在每項工程中照顧工人、鄰里及環境。</p>
""",
    "sc": """
<h3 class="red-txt">安全、品质及环境政策</h3>
<p>华丰遵守适用法例及规例。公司宗旨是在施工期间保障雇员、分包商及公众的健康、安全及福利，并减少噪音、空气及水质污染以及建筑废料。</p>
<p>各项作业按合约要求策划，检查、监督及纠正行动属日常地盘工作的一部分。</p>
<h3 class="red-txt">社会责任</h3>
<p>除履行合约外，华丰在每个地盘邻近范围以负责任承建商自居，管理工时、场地整洁及公众通道，尽量减低施工对四周的影响。</p>
<h3 class="red-txt">社区参与</h3>
<p>本公司推动建造业关怀文化，在每项工程中照顾工人、邻里及环境。</p>
""",
}


def page_sust(lang: str) -> str:
    L = LABELS[lang]
    return inner_page("../images/banner/4.jpg", L["sustainability"], f"""
    <div class="about-content">{SUST[lang]}
      {four_s_html(lang)}
    </div>
""")


TALENT = {
    "en": """
<h3 class="red-txt">Developing our people</h3>
<p>Wah Fung Engineering, Wah Fung Building &amp; Engineering and Dixie Engineering invest in the skills of engineers, site supervisors and frontline workers. Each person is trained for the work of their own contract, to one standard of competence and conduct across the group.</p>
<ul class="wf-skills">
  <li>Technical competence</li>
  <li>Safety and site leadership</li>
  <li>Programme and quality control</li>
  <li>Professional ethics</li>
</ul>
<p>Graduate and junior staff are guided by experienced site personnel, so that theory is put into daily construction practice.</p>
<h3 class="red-txt">Site training</h3>
<p>Wah Fung Engineering trains staff on live roads, including temporary traffic arrangements, night works, plant and emergency attendance.</p>
<p>Wah Fung Building &amp; Engineering trains staff on building sites, including trade supervision, programme control and finishing quality.</p>
<p>Dixie Engineering trains staff on drainage and civil maintenance, including channel and confined-space work, lifting, and safety workshops held by the client.</p>
<h3 class="red-txt">Courses and practice</h3>
<p>Staff attend programmes of the Construction Industry Council, the Hong Kong Institute of Construction and the Occupational Safety and Health Council, as well as workshops arranged by clients. High-risk work is assigned to trained supervisors, and what is taught is put into practice on site.</p>
""",
    "tc": """
<h3 class="red-txt">培育人才</h3>
<p>華丰工程、華丰建設工程及仁利工程投放資源，培育工程師、地盤督導及前線員工。培訓配合各人負責的合約，專業要求全集團一致。</p>
<ul class="wf-skills">
  <li>技術能力</li>
  <li>安全及地盤領導</li>
  <li>進度及品質控制</li>
  <li>專業操守</li>
</ul>
<p>畢業生及初級員工由經驗豐富的地盤人員帶領，把理論應用於日常施工。</p>
<h3 class="red-txt">在職培訓</h3>
<p>華丰工程的同事接受在用道路作業培訓，包括臨時交通安排、夜間施工、機械操作及緊急出勤。</p>
<p>華丰建設工程的同事於建築地盤受訓，包括工種督導、進度控制及完工品質。</p>
<p>仁利工程的同事於渠務及土木保養工程受訓，包括渠道及密閉空間作業、吊運，以及委託人舉辦的安全工作坊。</p>
<h3 class="red-txt">課程與實踐</h3>
<p>同事會參加建造業議會、香港建造學院及職業安全健康局的課程，以及委託人工作坊。高風險工序交由受訓督導人員負責，所學須在地盤實踐。</p>
""",
    "sc": """
<h3 class="red-txt">培育人才</h3>
<p>华丰工程、华丰建设工程及仁利工程投放资源，培育工程师、地盘督导及前线员工。培训配合各人负责的合约，专业要求全集团一致。</p>
<ul class="wf-skills">
  <li>技术能力</li>
  <li>安全及地盘领导</li>
  <li>进度及品质控制</li>
  <li>专业操守</li>
</ul>
<p>毕业生及初级员工由经验丰富的地盘人员带领，把理论应用于日常施工。</p>
<h3 class="red-txt">在职培训</h3>
<p>华丰工程的同事接受在用道路作业培训，包括临时交通安排、夜间施工、机械操作及紧急出勤。</p>
<p>华丰建设工程的同事于建筑地盘受训，包括工种督导、进度控制及完工品质。</p>
<p>仁利工程的同事于渠务及土木保养工程受训，包括渠道及密闭空间作业、吊运，以及委托人举办的安全工作坊。</p>
<h3 class="red-txt">课程与实践</h3>
<p>同事会参加建造业议会、香港建造学院及职业安全健康局的课程，以及委托人工作坊。高风险工序交由受训督导人员负责，所学须在地盘实践。</p>
""",
}


def page_talent(lang: str) -> str:
    L = LABELS[lang]
    return inner_page("../images/banner/1.jpg", L["talent"], f"""
    <div class="about-content">{TALENT[lang]}</div>
""")


def news_sidebar(lang: str, current: str) -> str:
    lis = []
    opts = []
    for href, label in NEWS_CATES[lang]:
        cls = ' class="active"' if href == current else ""
        sel = " selected" if href == current else ""
        lis.append(f'<li{cls}><a href="{href}">{label}<i class="fa fa-angle-right" aria-hidden="true"></i></a></li>')
        opts.append(f'<option{sel} value="{href}">{label}</option>')
    return f"""
<div class="col-sm-3">
  <div class="news_cate">
    <div class="cate_list"><ul>{''.join(lis)}</ul></div>
    <div class="cate_select">
      <select onchange="window.location.href=this.value">{''.join(opts)}</select>
    </div>
  </div>
</div>
"""


NEWS_ORDER = [14, 15, 16, 18, 19, 20, 5, 2, 6, 13, 7, 8, 9, 10, 4, 3, 11, 12]


def existing_news_imgs(n: dict) -> list[str]:
    found = []
    for src in n.get("imgs") or []:
        rel = src[3:] if src.startswith("../") else src
        if (ROOT / rel).is_file():
            found.append(src)
    return found


def news_list_html(lang: str, ids: list[int]) -> str:
    L = LABELS[lang]
    items = []
    by_id = {n["id"]: n for n in NEWS}
    for nid in ids:
        n = by_id[nid]
        imgs = existing_news_imgs(n)
        thumb = ""
        extra = ""
        if imgs:
            thumb = (
                f'<div class="news_thumb">'
                f'<img src="{imgs[0]}" alt="" width="128" height="86" '
                f'style="width:128px;height:86px;object-fit:cover;display:block">'
                f"</div>"
            )
            extra = " news-has-img"
        items.append(f'''
        <div class="news_item"><div class="news{extra}">
          {thumb}
          <div class="news_copy">
            <div class="news_date">{n["date"][lang]}</div>
            <div class="news_title">{n[lang]["title"]}</div>
          </div>
          <div class="news_btn"><a href="news_detail_id-{n["id"]}.php">{L["details"]}</a></div>
        </div></div>''')
    return "".join(items)


def page_news(lang: str) -> str:
    L = LABELS[lang]
    return inner_page("../images/banner/5.jpg", L["latest"], f"""
  <div class="row">
    {news_sidebar(lang, "news.php")}
    <div class="col-sm-9"><div class="news_list">{news_list_html(lang, NEWS_ORDER)}</div></div>
  </div>
""")


def page_news_detail(lang: str, n: dict) -> str:
    L = LABELS[lang]
    pics = []
    for src in existing_news_imgs(n):
        pics.append(f'<p class="news_shot"><img src="{src}" alt=""></p>')
    return inner_page("../images/banner/5.jpg", L["latest"], f"""
    <div class="news_detail">
      <div class="news_detail_title"><p>{n[lang]["title"]}</p></div>
      <div class="news_detail_content">
        <p class="news_date">{n["date"][lang]}</p>
        {''.join(pics)}
        {n[lang]["body"]}
        <p class="news_back"><a href="news.php">{L["news_back"]}</a></p>
      </div>
    </div>
""")


RECRUIT = {
    "en": """
<h3 class="red-txt">Join Wah Fung</h3>
<p>Wah Fung is a Hong Kong civil and building contractor. We welcome applications from engineers, site agents, supervisors, safety personnel and experienced tradespeople who want to work on drainage, roads, site formation and building works.</p>
<p>Please send your curriculum vitae, relevant certificates and expected availability to <a href="mailto:enquiry@chdx-jv.com">enquiry@chdx-jv.com</a>. State the post you are applying for and when you can start.</p>
<p>Positions are offered according to project needs. Wah Fung is an equal opportunity employer. Personal data will be used only for recruitment.</p>
""",
    "tc": """
<h3 class="red-txt">加入華丰</h3>
<p>華丰為香港土木及建築承建商。歡迎工程師、地盤代理人、督導人員、安全人員及有經驗工種申請，參與渠務、道路、地盤平整及建築工程。</p><p>請將履歷、相關證書及可到任日期電郵至 <a href="mailto:enquiry@chdx-jv.com">enquiry@chdx-jv.com</a>，並註明申請職位及可上班日期。</p>
<p>職位視乎項目需要而設。華丰為平等機會僱主。個人資料只用於招聘用途。</p>
""",
    "sc": """
<h3 class="red-txt">加入华丰</h3>
<p>华丰为香港土木及建筑承建商。欢迎工程师、地盘代理人、督导人员、安全人员及有经验工种申请，参与渠务、道路、地盘平整及建筑工程。</p><p>请将履历、相关证书及可到任日期电邮至 <a href="mailto:enquiry@chdx-jv.com">enquiry@chdx-jv.com</a>，并注明申请职位及可上班日期。</p>
<p>职位视乎项目需要而设。华丰为平等机会雇主。个人资料只用于招聘用途。</p>
""",
}
INTEGRITY = {
    "en": """
<h3 class="red-txt">Integrity Management Policy</h3>
<p>Wah Fung is committed to honest, fair and lawful business. Bribery, collusion, bid-rigging and conflicts of interest are not tolerated. This applies to staff, subcontractors and anyone acting for the Company.</p>
<p>All employees shall comply with the Prevention of Bribery Ordinance and with the Company’s internal rules on gifts, entertainment and procurement. Favours, cash or advantages offered or accepted in connection with a contract must be refused and reported.</p>
<p>Staff and subcontractors may raise concerns through management without fear of reprisal. Wah Fung will look into reports and take disciplinary or legal action where needed.</p>
""",
    "tc": """
<h3 class="red-txt">誠信管理政策</h3>
<p>華丰堅守誠實、公平及合法經營。賄賂、串謀、圍標及利益衝突恕不寬貸。此政策適用於員工、分包商及任何代表公司行事的人士。</p>
<p>全體僱員須遵守《防止賄賂條例》，以及公司就饋贈、款待及採購訂立的內部規則。與合約有關的好處、現金或利益，不論給予或收受，均須拒絕並向上申報。</p>
<p>員工及分包商可向管理層反映關注事項，毋須擔心報復。華丰會跟進舉報，並在有需要時採取紀律或法律行動。</p>
""",
    "sc": """
<h3 class="red-txt">诚信管理政策</h3>
<p>华丰坚守诚实、公平及合法经营。贿赂、串谋、围标及利益冲突恕不宽贷。此政策适用于员工、分包商及任何代表公司行事的人士。</p>
<p>全体雇员须遵守《防止贿赂条例》，以及公司就馈赠、款待及采购订立的内部规则。与合约有关的好处、现金或利益，不论给予或收受，均须拒绝并向上申报。</p>
<p>员工及分包商可向管理层反映关注事项，毋须担心报复。华丰会跟进举报，并在有需要时采取纪律或法律行动。</p>
""",
}


def page_cate(lang: str, filename: str, inner: str) -> str:
    L = LABELS[lang]
    return inner_page("../images/banner/5.jpg", L["news"], f"""
  <div class="row">
    {news_sidebar(lang, filename)}
    <div class="col-sm-9"><div class="about-content">{inner}</div></div>
  </div>
""")


def page_contact(lang: str) -> str:
    L = LABELS[lang]
    return inner_page("../images/banner/6.jpg", L["contact"], f"""
        <div class="about-content">
          <div class="wf-block-title"><h2>{GROUP_TITLE[lang]}</h2></div>
          {company_list_html(lang)}
          <div class="row" style="margin-top:20px;">
            <div class="col-sm-7">
              <h3 class="red-txt">{L["office"]}</h3>
              <p>
              {L["address"]}
              </p>
              <p>
              {L["email"]}: <a href="mailto:{EMAIL}">{EMAIL}</a><br/>
              LinkedIn: <a href="{LINKEDIN}" target="_blank" rel="noopener">Wah Fung Engineering Company Limited</a>
              </p>
              <h3 class="red-txt">{DIXIE_LABEL[lang]}</h3>
              <p>{DIXIE_ADDR[lang]}</p>
            </div>
            <div class="col-sm-5">
              <iframe src="{MAPS_EMBED}" width="100%" height="300" frameborder="0" style="border:0;max-width:100%;" allowfullscreen></iframe>
            </div>
          </div>
        </div>
""")


def clean_old(lang_dir: Path) -> None:
    keep = {
        "index.html", "aboutus.html", "expertise.html", "projects.html",
        "sustainability.html", "talent.html", "news.html",
        "news_cate-10.html", "news_cate-13.html",
    }
    keep_ids = {str(p["id"]) for p in PROJECTS}
    keep_news = {str(n["id"]) for n in NEWS}
    for p in list(lang_dir.glob("*.php")) + list(lang_dir.glob("*.html")):
        name = p.name
        if name.endswith(".php"):
            p.unlink()
            continue
        if name in keep or name.startswith("news_cate-"):
            continue
        if name.startswith("projects-detail_id-"):
            if name.split("id-")[-1].split(".")[0] in keep_ids:
                continue
        if name.startswith("news_detail_id-"):
            if name.split("id-")[-1].split(".")[0] in keep_news:
                continue
        p.unlink()
        print("removed", p)


def set_site(site: dict) -> None:
    global CURRENT_SITE, COMPANY, COPYRIGHT
    CURRENT_SITE = site
    COMPANY = {lang: site[lang] for lang in ("en", "tc", "sc")}
    COPYRIGHT = {
        "en": f"© 2026 {site['en']}. All Rights Reserved.",
        "tc": f"© 2026 {site['tc']}。版權所有。",
        "sc": f"© 2026 {site['sc']}。版权所有。",
    }


def build_site(site: dict) -> None:
    set_site(site)
    for lang in ("en", "tc", "sc"):
        d = ROOT / site["slug"] / lang
        d.mkdir(parents=True, exist_ok=True)
        write_page(lang, "index.php", page_home(lang))
        write_page(lang, "aboutus.php", page_about(lang))
        write_page(lang, "expertise.php", page_expertise(lang))
        write_page(lang, "projects.php", page_projects(lang))
        write_page(lang, "sustainability.php", page_sust(lang))
        write_page(lang, "talent.php", page_talent(lang))
        write_page(lang, "news.php", page_news(lang))
        write_page(lang, "news_cate-10.php", page_cate(lang, "news_cate-10.php", RECRUIT[lang]))
        write_page(lang, "news_cate-13.php", page_cate(lang, "news_cate-13.php", INTEGRITY[lang]))
        for p in PROJECTS:
            write_page(lang, f'projects-detail_id-{p["id"]}.php', page_project_detail(lang, p))
        for n in NEWS:
            write_page(lang, f'news_detail_id-{n["id"]}.php', page_news_detail(lang, n))
        clean_old(d)
        print("built", site["slug"], lang)
    (ROOT / site["slug"] / "index.html").write_text(
        f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=en/index.html">
<title>{site["en"]}</title>
<meta name="description" content="{site["desc"]["en"]}">
</head>
<body><p><a href="en/index.html">English</a> · <a href="tc/index.html">繁</a> · <a href="sc/index.html">简</a></p></body></html>""",
        encoding="utf-8",
    )


def main() -> None:
    for site in SITES:
        build_site(site)
    for old in ("en", "tc", "sc"):
        d = ROOT / old
        if d.is_dir():
            shutil.rmtree(d)
    (ROOT / "index.html").write_text(
        """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wah Fung Engineering Company Limited · Wah Fung Building &amp; Engineering Limited · Dixie Engineering Company Limited</title>
</head>
<body>
<p><a href="engineering/en/index.html">Wah Fung Engineering Company Limited</a></p>
<p><a href="building/en/index.html">Wah Fung Building &amp; Engineering Limited</a></p>
<p><a href="dixie/en/index.html">Dixie Engineering Company Limited</a></p>
</body>
</html>
""",
        encoding="utf-8",
    )
    print("done")


if __name__ == "__main__":
    main()
