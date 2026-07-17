from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.user import User
from app.models.news import News
from app.models.privilege import Privilege
from app.models.legislation import Legislation
from app.utils.auth import get_password_hash


def populate_db():
    db: Session = SessionLocal()
    try:
        # 1. Create Default Admin User if none exists
        admin_exists = db.query(User).filter(User.username == "admin").first()
        if not admin_exists:
            hashed_pwd = get_password_hash("admin123")
            admin_user = User(username="admin", hashed_password=hashed_pwd)
            db.add(admin_user)
            db.commit()
            print("Default admin user created: admin / admin123")

        # 2. Create Default News if none exists
        news_count = db.query(News).count()
        if news_count == 0:
            demo_news = [
                News(
                    title="Uzeltexsanoat Kasaba Uyushmasi yangi jamoa shartnomasini imzoladi",
                    content="Bugun Uzeltexsanoat uyushmasi va korxonalar ma'muriyati o'rtasida 2026-2029 yillarga mo'ljallangan yangi tarmoq kelishuvi imzolandi. Ushbu shartnoma xodimlarning mehnat sharoitlarini yaxshilash, ijtimoiy kafolatlarini kengaytirish hamda mehnat muhofazasini yuqori bosqichga ko'tarishga qaratilgan bir qator muhim bandlarni o'z ichiga oladi.",
                    image_url=""
                ),
                News(
                    title="Sanatoriylarga imtiyozli yo'llanmalar topshirildi",
                    content="Yozgi sog'lomlashtirish mavsumi munosabati bilan tarmoq korxonalarining 50 dan ortiq xodimlariga oila a'zolari bilan birgalikda dam olishlari uchun O'zbekistonning yetakchi sanatoriylariga 50% va 70% imtiyozli yo'llanmalar tantanali ravishda topshirildi.",
                    image_url=""
                ),
                News(
                    title="Yosh mutaxassislar uchun huquqiy seminar o'tkazildi",
                    content="Kasaba uyushmasi yuristlari tomonidan yosh ishchi-xodimlarning mehnat sohasidagi huquqiy savodxonligini oshirish maqsadida 'Yangi Mehnat Kodeksi va Yoshlarning Huquqlari' mavzusida interaktiv seminar tashkil etildi. Seminar davomida ishtirokchilar o'zlarini qiziqtirgan savollarga javob olishdi.",
                    image_url=""
                )
            ]
            db.add_all(demo_news)
            db.commit()
            print("Demo news populated.")

        # 3. Create Default Privileges if none exists
        privilege_count = db.query(Privilege).count()
        if privilege_count == 0:
            demo_privileges = [
                Privilege(
                    title="Sanatoriyga imtiyozli yo'llanmalar",
                    description="Kasaba a'zolari va ularning oila a'zolari uchun 50% gacha imtiyozli dam olish maskanlari yo'llanmalari.",
                    icon="🏥",
                    content="Yo'llanma olish tartibi:\n1. Arizachi kasaba uyushmasiga ariza bilan murojaat qiladi.\n2. Shifokorning 070-U shaklidagi ma'lumotnomasi taqdim etiladi.\n3. Arizalar ro'yxatga olinib, navbatga muvofiq sanatoriy yo'llanmasi taqdim etiladi.\n\nEslatma: Yo'llanmalar asosan O'zbekiston kasaba uyushmalari federatsiyasi tasarrufidagi sanatoriylar (masalan, Chinobod, Chimyon, Humson va hk.) uchun amal qiladi."
                ),
                Privilege(
                    title="Bir martalik moddiy yordam",
                    description="Bemorlik, to'y marosimi yoki og'ir ijtimoiy sharoitlar yuzaga kelganda moddiy yordam ajratish tizimi.",
                    icon="💰",
                    content="Moddiy yordam olish shartlari:\n- Salomatlik bilan bog'liq jarrohlik yoki uzoq muddatli davolanish talab etilganda.\n- Oilada yuzaga kelgan fors-major holatlari (yong'in, tabiiy ofat) yuz berganda.\n- Birinchi marta nikohdan o'tish yoki oila a'zolaridan birining vafoti holatida.\n\nHujjatlar: Ariza, pasport nusxasi, kasallik varaqasi yoki tegishli dalolatnoma/guvohnomalar."
                ),
                Privilege(
                    title="Bolalar oromgohlari",
                    description="Yozgi mavsumda xodimlarning farzandlarini oromgohlarga yuborish xarajatlarini qisman qoplash.",
                    icon="🧸",
                    content="Yozgi ta'tilda 7 yoshdan 14 yoshgacha bo'lgan bolalarni sog'lomlashtirish oromgohlariga yuborish tartibi:\n1. Bahor oylarida arizalar yig'iladi.\n2. Yo'llanma xarajatlarining 50-70% qismi kasaba uyushmasi budjeti hisobidan to'lanadi.\n3. Qolgan qismi ish beruvchi yoki ota-onaning o'zi tomonidan to'lanishi mumkin.\n\nTegishli hujjatlar: Ariza, tug'ilganlik haqidagi guvohnoma nusxasi, tibbiy ma'lumotnoma."
                )
            ]
            db.add_all(demo_privileges)
            db.commit()
            print("Demo privileges populated.")

        # 4. Create Default Legislation if none exists
        legislation_count = db.query(Legislation).count()
        if legislation_count == 0:
            demo_legislations = [
                Legislation(
                    title="O'zbekiston Respublikasining Mehnat Kodeksi (Yangi tahriri)",
                    description="Xodimlar va ish beruvchilar o'rtasidagi munosabatlarni tartibga soluvchi bosh qonun hujjati.",
                    category="Qonun",
                    file_url=""
                ),
                Legislation(
                    title="O'zbekiston Respublikasining 'Kasaba uyushmalari to'g'risida'gi Qonuni",
                    description="Kasaba uyushmalarining huquqlari, majburiyatlari va kafolatlarini belgilovchi qonun.",
                    category="Qonun",
                    file_url=""
                ),
                Legislation(
                    title="Kasaba uyushmalari faoliyatini yanada takomillashtirish chora-tadbirlari to'g'risidagi qaror",
                    description="Tashkiliy tuzilmani isloh qilish bo'yicha hukumat qarori.",
                    category="Qaror",
                    file_url=""
                ),
                Legislation(
                    title="Elektrotexnika sanoati korxonalari tarmog'ining tarif-malaka ma'lumotnomasi",
                    description="Ishchilarning lavozimlari, toifalari va maosh stavkalarini belgilovchi ichki tarmoq yo'riqnomasi.",
                    category="Nizom",
                    file_url=""
                )
            ]
            db.add_all(demo_legislations)
            db.commit()
            print("Demo legislations populated.")

    finally:
        db.close()
