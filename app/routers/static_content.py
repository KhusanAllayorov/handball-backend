"""
Statik kontent (sessiyalar, kutubxona, bilim bazasi).
Bu ma'lumotlar o'zgarmaydi — DB ga saqlash shart emas.
Flutter api_service.dart: fetchSessions(), fetchLibrary(), fetchKnowledge()
"""
from fastapi import APIRouter, Query

router = APIRouter(tags=["content"])

# ── 36 sessiya ────────────────────────────────────────────────────────────────

_WEEK_TOPICS = [
    "To'p bilan tanishish, ushlash texnikasi",
    "Ushlash mustahkamlash + dribling asoslari",
    "Tashlash va uzatishga kirish",
    "Uzatish turlari va aniqlik",
    "Tashlash-uzatish takomili",
    "Tashlash-ilish + harakat birlashuvi",
    "Hujum-himoya juftlik o'yinlari",
    "Hujum-himoya muvozanati",
    "Harakatda ilish va dribling",
    "Tezkor hujum va o'tish",
    "Murakkab o'yin vaziyatlari",
    "Integratsiya — to'liq o'yinlar",
]

_PHASES = {
    (1, 2): "To'p bilan tanishish va ushlash",
    (3, 5): "To'pni tashlash va uzatish",
    (6, 8): "Tashlash-ilish + harakat",
    (9, 11): "Harakatda ilish va dribling",
    (12, 12): "Kichik maydonli o'yinlar (integratsiya)",
}


def _phase_for_week(w: int) -> str:
    for (lo, hi), title in _PHASES.items():
        if lo <= w <= hi:
            return title
    return ""


def _build_sessions():
    sessions = []
    for w in range(1, 13):
        phase = _phase_for_week(w)
        topic = _WEEK_TOPICS[w - 1]
        for d in range(1, 4):
            n = (w - 1) * 3 + d
            sessions.append({
                "number": n,
                "week": w,
                "topic": topic,
                "phase": phase,
                "exercises": [
                    {
                        "name": "Qo'l koordinatsiyasi mashqi",
                        "description": "Sessiya bosqichiga mos to'p bilan ishlash mashqi.",
                        "load": "10–12 daq",
                        "goal": "Qo'llar chaqqonligini rivojlantirish",
                        "domainId": 1,
                    },
                    {
                        "name": "Uzatish va tutib olish mashqi",
                        "description": "Juftlik yoki guruhda uzatish-qabul qilish.",
                        "load": "10–12 daq",
                        "goal": "Vizuomotor integratsiya, antitsipatsiya",
                        "domainId": 2,
                    },
                    {
                        "name": "Muvozanat mashqi",
                        "description": "Statik yoki dinamik muvozanat.",
                        "load": "8–10 daq",
                        "goal": "Muvozanat va tana nazorati",
                        "domainId": 3,
                    },
                ],
            })
    return sessions


_SESSIONS = _build_sessions()

_LIBRARY = [
    {"name": "To'pni ushlash", "domainId": 1},
    {"name": "To'pni uzatish", "domainId": 2},
    {"name": "Joyida dribling", "domainId": 1},
    {"name": "Harakatda dribling", "domainId": 1},
    {"name": "Ko'krakdan uzatish", "domainId": 2},
    {"name": "Pastdan uzatish", "domainId": 2},
    {"name": "Yuqoridan uzatish", "domainId": 2},
    {"name": "Bir qo'llab uzatish", "domainId": 2},
    {"name": "Sakrab to'p otish", "domainId": 2},
    {"name": "Oyoqlar orasida «8» son", "domainId": 1},
    {"name": "Tana atrofida aylantirish", "domainId": 1},
    {"name": "Devorga uloqtirish", "domainId": 2},
    {"name": "Skameyka ustida dribling", "domainId": 3},
    {"name": "To'siqlar orasida dribling", "domainId": 3},
    {"name": "Bir oyoqda muvozanat", "domainId": 3},
    {"name": "Halqaga sakratib uzatish", "domainId": 2},
    {"name": "Ikki to'p bilan ishlash", "domainId": 1},
    {"name": "Estafeta", "domainId": 1},
]

_KNOWLEDGE = [
    {
        "emoji": "🧠",
        "category": "Nazariya",
        "title": "DCD nima?",
        "summary": "Rivojlanishdagi koordinatsiya buzilishi haqida",
        "body": (
            "DCD (Developmental Coordination Disorder) — koordinatsion harakat "
            "ko'nikmalarini o'rganish va qo'llashda sezilarli kechikish bilan "
            "tavsiflanadigan neyrorivojlanish buzilishidir. Asosiy belgilar: "
            "qo'pollik, motor bosqichlarni kech egallash, yozuv va predmet bilan "
            "ishlashda qiyinchilik, muvozanat muammolari. "
            "Maktab yoshidagi bolalarning taxminan 5–6%ida uchraydi."
        ),
    },
    {
        "emoji": "📋",
        "category": "Metodika",
        "title": "MABC-2 testi",
        "summary": "Baholash metodikasi va protsentil kesimlari",
        "body": (
            "Movement Assessment Battery for Children – Second Edition (MABC-2) "
            "uch domen bo'yicha baholaydi: qo'llar chaqqonligi, tutib olish va "
            "uzatish, muvozanat. Protsentil kesimlari: 5%-dan past — DCD; "
            "6–15% — DCD xavfi (r-DCD); 16%-dan yuqori — tipik rivojlanish."
        ),
    },
    {
        "emoji": "🤾",
        "category": "Metodika",
        "title": "Mini-gandbol metodikasi",
        "summary": "Nima uchun ochiq-ko'nikmali sport samaraliroq",
        "body": (
            "Mini-gandbol ochiq-ko'nikmali (open-skill) sport bo'lib, u tez qaror "
            "qabul qilish, strategik rejalashtirish va harakat moslashuvchanligini "
            "talab qiladi. Bu dinamik talablar bir vaqtning o'zida motor va kognitiv "
            "rivojlanishni rag'batlantiradi."
        ),
    },
    {
        "emoji": "🏠",
        "category": "Ota-onaga",
        "title": "Ota-onalar uchun maslahatlar",
        "summary": "Uyda farzandga qanday yordam berish",
        "body": (
            "Uyda oddiy mashqlar bilan farzandingizni qo'llab-quvvatlang: devorga "
            "to'p uloqtirish, bir oyoqda turib muvozanat, tana atrofida to'p "
            "aylantirish. Eng muhimi — ijobiy muhit va rag'batlantirish."
        ),
    },
    {
        "emoji": "📚",
        "category": "Nazariya",
        "title": "Ilmiy asoslar",
        "summary": "Tadqiqot natijalari va adabiyotlar",
        "body": (
            "Metodika ekologik dinamika, idrok-harakat bog'liqligi va bosqichli motor "
            "o'rganish nazariyalariga asoslanadi. Tadqiqotlar mini-gandbolning DCD "
            "bolalarida koordinatsiyani rivojlantirishdagi samaradorligini tasdiqlaydi."
        ),
    },
    {
        "emoji": "⚠️",
        "category": "Amaliyot",
        "title": "Xavfsizlik qoidalari",
        "summary": "Mashg'ulot davomida e'tibor berish kerak",
        "body": (
            "Yumshoq to'pdan boshlang. Masofani asta oshiring. Bolani xato uchun "
            "jazolamang. Har bir kichik yutuqni rag'batlantiring. Mashg'ulot maydoni "
            "xavfsiz va to'siqlardan xoli bo'lsin."
        ),
    },
]


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("/sessions")
def get_sessions():
    return _SESSIONS


@router.get("/library")
def get_library(domain_id: int | None = Query(None, alias="domainId")):
    if domain_id is None:
        return _LIBRARY
    return [i for i in _LIBRARY if i["domainId"] == domain_id]


@router.get("/knowledge")
def get_knowledge():
    return _KNOWLEDGE
