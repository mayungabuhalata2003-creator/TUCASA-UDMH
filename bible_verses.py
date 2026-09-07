"""Mistari ya Biblia ya kila siku (Daily Bible verses in Swahili)."""
from datetime import date

VERSES = [
    {
        "reference": "Yeremia 29:11",
        "text": "Maana nayajua mawazo ninayowawazia ninyi, asema Bwana, ni mawazo ya amani wala si ya mabaya, kuwapa ninyi tumaini siku zenu za mwisho.",
    },
    {
        "reference": "Zaburi 23:1",
        "text": "Bwana ndiye mchungaji wangu, sitapungukiwa na kitu.",
    },
    {
        "reference": "Wafilipi 4:13",
        "text": "Naweza kufanya mambo yote katika yeye anitiaye nguvu.",
    },
    {
        "reference": "Mithali 3:5-6",
        "text": "Mtumaini Bwana kwa moyo wako wote, wala usizitegemee akili zako mwenyewe. Katika njia zako zote mkiri yeye, naye atayanyosha mapito yako.",
    },
    {
        "reference": "Yoshua 1:9",
        "text": "Je! Sikuamuru mimi? Uwe hodari na moyo wa ushujaa; usifadhaike wala usifadhaishwe, kwa kuwa Bwana Mungu wako yu pamoja nawe kila uendako.",
    },
    {
        "reference": "Warumi 8:28",
        "text": "Nasi twajua ya kuwa katika mambo yote Mungu hufanya kazi pamoja na wale wampendao katika kuwapatia mema, yaani, wale walioitwa kwa kusudi lake.",
    },
    {
        "reference": "Isaya 41:10",
        "text": "Usiogope, kwa maana mimi ni pamoja nawe; usifadhaike, kwa maana mimi ni Mungu wako; nitakutia nguvu, naam, nitakusaidia, naam, nitakushika kwa mkono wa kuume wa haki yangu.",
    },
    {
        "reference": "Mathayo 11:28",
        "text": "Njoni kwangu, ninyi nyote msumbukao na kulemewa na mizigo, nami nitawapumzisha.",
    },
    {
        "reference": "2 Timotheo 1:7",
        "text": "Maana Mungu hakutupa roho ya woga, bali ya nguvu na ya upendo na ya moyo wa kiasi.",
    },
    {
        "reference": "Zaburi 46:1",
        "text": "Mungu ni kimbilio letu na nguvu yetu, msaada utakaoonekana tele wakati wa mateso.",
    },
    {
        "reference": "Yohana 3:16",
        "text": "Kwa maana jinsi hii Mungu aliupenda ulimwengu, hata akamtoa Mwanawe pekee, ili kila mtu amwaminiye asipotee, bali awe na uzima wa milele.",
    },
    {
        "reference": "Waebrania 11:1",
        "text": "Basi imani ni kuwa na hakika ya mambo yatarajiwayo, ni bayana ya mambo yasiyoonekana.",
    },
]


def get_daily_verse_index():
    """Return the index for today's verse within the rotating list."""
    day_of_year = date.today().timetuple().tm_yday
    return day_of_year % len(VERSES)


def get_daily_verse():
    """Return today's verse based on day-of-year, cycling through the list."""
    return VERSES[get_daily_verse_index()]
