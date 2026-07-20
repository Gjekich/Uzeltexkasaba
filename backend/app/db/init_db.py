from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.user import User
from app.models.news import News
from app.models.privilege import Privilege
from app.models.legislation import Legislation
from app.models.staff import Staff
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
                    title="\"O'zeltexsanoat\" uyushmasi yangi jamoa shartnomasini imzoladi",
                    content="Bugun \"O'zeltexsanoat\" uyushmasi va korxonalar ma'muriyati o'rtasida 2026-2029 yillarga mo'ljallangan yangi tarmoq kelishuvi imzolandi. Ushbu shartnoma xodimlarning mehnat sharoitlarini yaxshilash, ijtimoiy kafolatlarini kengaytirish hamda mehnat muhofazasini yuqori bosqichga ko'tarishga qaratilgan bir qator muhim bandlarni o'z ichiga oladi.",
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
                    content="""Yo'llanma olish tartibi va sanatoriylar ro'yxati:

Kasaba a'zolari va ularning oila a'zolari uchun 50% gacha imtiyozli narxlarda Federatsiya tasarrufidagi quyidagi yetakchi sanatoriylarga yo'llanmalar beriladi:

1. "ZOMIN" SANATORIYSI (Jizzax viloyati)
- Ixtisoslashuvi: Nafas yo'llari, nevrologiya, tayanch-harakat a'zolari kasalliklari. Tog'li toza havo va iqlimiy davolash.

2. "CHINOBOD" SANATORIYSI (Toshkent shahri)
- Ixtisoslashuvi: Oshqozon-ichak trakti, jigar, o't yo'llari, ginekologiya va qandli diabet kasalliklari. Issiq mineral suv va shifobaxsh loylar.

3. "TURON" SANATORIYSI (Toshkent shahri)
- Ixtisoslashuvi: Yurak-qon tomir tizimi, asab kasalliklari, qon aylanish a'zolari kasalliklari. Balneologik muolajalar.

4. "OQTOSH" SANATORIYSI (Toshkent viloyati)
- Ixtisoslashuvi: Nafas olish a'zolarining surunkali o'ziga xos bo'lmagan kasalliklari (astma va bronxit). Tinch tog' havosi.

5. "BO'STON" SANATORIYSI (Toshkent viloyati)
- Ixtisoslashuvi: Yurak-qon tomir, nevrologik, tayanch-harakat a'zolari va ginekologik kasalliklar.

6. "CHORTOQ" SANATORIYSI (Namangan viloyati)
- Ixtisoslashuvi: Mineral suvlar yordamida oshqozon-ichak, tayanch-harakat, teri va asab tizimi kasalliklarini davolash.

7. "CHIMYON" SANATORIYSI (Farg'ona viloyati)
- Ixtisoslashuvi: Vodorod sulfidli suvlar va loy yordamida tayanch-harakat, yurak-qon tomir va asab tizimini sog'lomlashtirish.

8. "SITORAI MOHI XOSA" SANATORIYSI (Buxoro viloyati)
- Ixtisoslashuvi: Buyrak va siydik yo'llari kasalliklari, asab tizimi va tayanch-harakat a'zolari. Tarixiy yozgi saroy iqlimi.

Imtiyozli yo'llanma olish uchun zarur hujjatlar:
1. Korxonangiz boshlang'ich kasaba uyushmasi tashkiloti raisi nomiga ariza.
2. Davolovchi shifokor tomonidan berilgan 070-U shaklidagi tibbiy ma'lumotnoma (yo'llanma tavsifnomasi).
3. Kasaba uyushmasi a'zoligi tasdiqlangan guvohnoma yoki ma'lumotnoma."""
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
                    description="Xodimlar va ish beruvchilar o'rtasidagi munosabatlarni tartibga soluvchi bosh qonun hujjati. (Lex.uz rasmiy havolasi)",
                    category="Qonun",
                    file_url="https://lex.uz/docs/6257288"
                ),
                Legislation(
                    title="O'zbekiston Respublikasining 'Kasaba uyushmalari to'g'risida'gi Qonuni",
                    description="Kasaba uyushmalarining huquqlari, majburiyatlari va kafolatlarini belgilovchi qonun. (Lex.uz rasmiy havolasi)",
                    category="Qonun",
                    file_url="https://lex.uz/docs/4638365"
                ),
                Legislation(
                    title="Kasaba uyushmalari faoliyatini yanada takomillashtirish chora-tadbirlari to'g'risidagi qaror",
                    description="Tashkiliy tuzilmani isloh qilish bo'yicha hukumat qarori. (Lex.uz rasmiy havolasi)",
                    category="Qaror",
                    file_url="https://lex.uz/docs/5049306"
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

        # 5. Create Default Staff if none exists
        staff_count = db.query(Staff).count()
        if staff_count == 0:
            demo_staff = [
                Staff(
                    full_name="Eshmatov Qobiljon Abdullayevich",
                    position="Tarmoq kasaba uyushmasi raisi",
                    phone="+998 (71) 200-11-22",
                    email="q.eshmatov@uzeltexkasaba.uz"
                ),
                Staff(
                    full_name="Karimov Jamshid Shavkatovich",
                    position="Rais o'rinbosari",
                    phone="+998 (71) 200-11-23",
                    email="j.karimov@uzeltexkasaba.uz"
                ),
                Staff(
                    full_name="Sodiqov Dilshod Rustamovich",
                    position="Bosh huquqshunos",
                    phone="+998 (71) 200-11-24",
                    email="d.sodiqov@uzeltexkasaba.uz"
                ),
                Staff(
                    full_name="Nasimova Lola Murodovna",
                    position="Moliyaviy bo'lim mudiri",
                    phone="+998 (71) 200-11-25",
                    email="l.nasimova@uzeltexkasaba.uz"
                ),
                Staff(
                    full_name="Xasanov Alisher Baxtiyorovich",
                    position="Mehnat muhofazasi bo'limi bosh mutaxassisi",
                    phone="+998 (71) 200-11-26",
                    email="a.xasanov@uzeltexkasaba.uz"
                )
            ]
            db.add_all(demo_staff)
            db.commit()
            print("Demo staff populated.")

    finally:
        db.close()
