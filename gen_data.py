# Synthetic, template-based corpus of investment scam vs genuine messages (English / Hindi / Hinglish).
# Every row carries a "type" so evaluation can hold out whole scam families (leave-one-type-out).
import random, csv
random.seed(7)
PL=["WhatsApp","Telegram"]; BR=["Zerodha","Groww","Upstox","Angel One","Paytm Money"]
FAKE={"Zerodha":["zerodha-pro.in","zer0dha.com","zerodha-kyc.net"],"Groww":["groww-india.xyz","grow.co.in","groww-app.in"],"Upstox":["upstox-login.in","upst0x.com"],"Angel One":["angelone-kyc.com","angel0ne.in"],"Paytm Money":["paytmmoney-pro.in","paytm-money.xyz"]}
S={ # scam families: list of fragments (en, hi, hinglish mixed)
"tips_group":["Join our VIP {pl} group for sure shot intraday tips and daily calls.","Get insider stock tips from our expert team in the premium {pl} channel.","Our operator group gives jackpot stock calls every morning, join now.","हमारे VIP {pl} ग्रुप में जुड़ें, रोज़ पक्के इंट्राडे टिप्स मिलेंगे।","एक्सपर्ट टीम से रोज़ जैकपॉट स्टॉक कॉल्स पाएँ, ग्रुप जॉइन करें।","Hamare VIP {pl} group me join karo, daily sure shot tips milenge.","Aaj ka jackpot stock call chahiye? Premium group join karo."],
"guaranteed":["Invest {amt} and get guaranteed {pct}% returns every month.","100% assured profit, zero risk, withdraw anytime.","Double your money in {n} days, guaranteed by our fund manager.","{amt} लगाइए और हर महीने {pct}% का गारंटीड मुनाफ़ा पाइए।","पैसा दोगुना करें, कोई रिस्क नहीं, पक्का रिटर्न।","{amt} lagao aur har mahine {pct}% pakka profit pao, risk zero.","Paisa double in {n} din, guarantee ke saath."],
"fake_app":["Download our trading app from this link to start earning: {apk}","Install the new official app {apk} and get a free bonus.","कमाई शुरू करने के लिए हमारा ऐप डाउनलोड करें: {apk}","Earning start karne ke liye ye app install karo: {apk}"],
"fake_broker":["Your {b} account needs urgent update. Login at {f} to avoid suspension.","{b} Pro offers special IPO allotment. Register at {f}.","आपका {b} अकाउंट अपडेट करें वरना बंद हो जाएगा: {f}","Aapka {b} account band hone wala hai, abhi update karo: {f}"],
"otp_vishing":["To release your profit, share the OTP received and install AnyDesk so our agent can help.","Send your PIN and OTP to complete KYC verification now.","मुनाफ़ा निकालने के लिए आपके फोन पर आया OTP बताइए और AnyDesk इंस्टॉल करें।","Profit withdraw karne ke liye OTP bhejo aur TeamViewer install karo."],
"preipo":["Pre-IPO shares at 40% discount through our institutional account, allotment guaranteed.","Block deal opportunity in unlisted shares, limited slots, invest before listing.","प्री-IPO शेयर 40% सस्ते, इंस्टिट्यूशनल अकाउंट से अलॉटमेंट पक्का।","Pre-IPO shares sasta mil raha hai, allotment pakka, sirf kuch slots."],
"fee_scam":["Pay a registration fee of {amt} on UPI {upi} to activate your account.","Processing fee {amt} required to unlock your profit, send to {upi}.","अकाउंट चालू करने के लिए {amt} रजिस्ट्रेशन फीस UPI {upi} पर भेजें।","Account activate karne ke liye {amt} fee UPI {upi} pe bhejo."]}
MOD=["Only {k} seats left, hurry!","Offer ends today.","Last chance, join now.","सिर्फ़ {k} सीट बाकी, आज ही!","ऑफ़र आज खत्म, जल्दी करें।","Sirf {k} seats bachi, jaldi karo!","SEBI registered.","100% SEBI approved expert.","सेबी रजिस्टर्ड एक्सपर्ट।","Limited slots. Reply YES to confirm.","Bit.ly/{x} par details dekho.","Details: t.me/{x}"]
OPEN=["Congratulations!","Dear investor,","Namaste,","सुनिए,","Hello sir,","Hi,","बधाई हो!","Dear sir/madam,","","","Hello bhai,"]
L={ # genuine families, includes hard negatives (genuine OTP, SEBI warnings, offers, chat)
"sip":["Your SIP of {amt} in {fund} will be processed on {d}. Please maintain sufficient balance.","आपकी {amt} की SIP {d} तारीख को कटेगी। खाते में बैलेंस रखें।","SIP ka {amt} {d} ko katega, balance rakhna."],
"contract_note":["Contract note for trades done on {d} has been sent to your registered email. Check your app for details.","{d} के ट्रेड का कॉन्ट्रैक्ट नोट आपके रजिस्टर्ड ईमेल पर भेजा गया है।","Aapke {d} ke trades ka contract note email par bhej diya gaya hai."],
"kyc":["Please complete your KYC at our official website or nearest branch. Do not share OTP with anyone.","KYC पूरा करने के लिए आधिकारिक वेबसाइट या नज़दीकी शाखा जाएँ। OTP किसी को न बताएँ।","KYC pura karne ke liye branch jaye ya official site dekhe. OTP kisi ko na de."],
"nav":["NAV of {fund} as on {d} is Rs {nav}. Mutual fund investments are subject to market risks, read all scheme related documents carefully.","{d} को {fund} का NAV Rs {nav} है। म्यूचुअल फंड निवेश बाज़ार जोखिमों के अधीन हैं।"],
"bank":["Rs {amt2} debited from A/c XX{k} on {d}. If not you, call the bank helpline. Never share OTP.","OTP for your transaction is {otp}. Do not share it with anyone. Valid for 10 minutes.","आपके खाते XX{k} से Rs {amt2} {d} को डेबिट हुए। OTP किसी से साझा न करें।","Your UPI payment of Rs {amt2} to the merchant was successful on {d}."],
"advisory":["SEBI advisory: Beware of guaranteed returns and unregistered tips groups. Verify advisers on the SEBI website.","सावधान: गारंटीड रिटर्न और टिप्स वाले ग्रुप से बचें। SEBI की वेबसाइट पर सलाहकार जाँचें।","Fake apps and sure shot tips are scams. Never share OTP. Report fraud on 1930 or cybercrime.gov.in.","Dhokhe se bacho: pakka profit ka vaada karne wale group se door rahe. Sirf SEBI registered se milo."],
"chat":["Beta, did you check the mutual fund statement? Call me in the evening.","पापा, म्यूचुअल फंड की स्टेटमेंट देखी क्या? शाम को फोन करना।","Bhai kal milte hai, SIP ke baare me baat karni hai.","Happy Diwali! Wishing you and family a prosperous year.","Meeting at 5 pm, please bring the demat account documents."],
"amc_offer":["New fund offer from {fund} opens on {d}. Please read the offer document. Visit the official website.","Limited period: exit load waiver till {d} on {fund}. Mutual fund investments are subject to market risks.","{fund} का नया फंड ऑफर {d} से खुल रहा है। ऑफर डॉक्यूमेंट ध्यान से पढ़ें।"],
"education":["Learn what a nominee is in your demat account. Add a nominee online through your DP.","Nominee kaise add kare demat account me? Apne DP ki website par jaye.","डीमैट अकाउंट में नॉमिनी जोड़ना क्यों ज़रूरी है, जानिए आधिकारिक वेबसाइट पर।"]}
def fill(t):
    b=random.choice(BR)
    return t.format(pl=random.choice(PL),amt=random.choice(["₹5,000","Rs 10000","₹25,000","₹50,000","10 हज़ार"]),pct=random.choice([10,15,20,30,50,300]),n=random.choice([7,10,15,30]),apk=random.choice(["bit.ly/inv%d"%random.randint(10,99),"trade-"+str(random.randint(10,99))+".apk","dl.profitapp.in/app.apk"]),b=b,f=random.choice(FAKE[b]),upi=random.choice(["98%08d@paytm"%random.randint(0,99999999),"investpro%d@ybl"%random.randint(1,99)]),k=random.randint(2,9),x="inv%d"%random.randint(100,999),fund=random.choice(["HDFC Flexi Cap","SBI Bluechip","Axis Midcap","Nippon Small Cap","Parag Parikh Flexi Cap"]),d=random.choice(["5th","12 Oct","3 Nov","25/09","1st"]),nav=round(random.uniform(20,400),2),amt2=random.randint(100,9999),otp=random.randint(100000,999999))
def noise(s):
    if random.random()<.15:s=s.upper()
    if random.random()<.2:s+=random.choice([" 🚀"," 💰"," 👍",""])
    return s
rows=[]
for t,fr in S.items():
    for _ in range(260):
        parts=[random.choice(fr)]
        if random.random()<.4:
            t2=random.choice([k for k in S if k!=t]);parts.append(random.choice(S[t2]))
        for m in random.sample(MOD,random.choice([0,1,1,2])):parts.append(m)
        rows.append((noise(fill(random.choice(OPEN)+" "+" ".join(parts)).strip()),1,t))
for t,fr in L.items():
    for _ in range(205):
        parts=[random.choice(fr)]
        if random.random()<.3:parts.append(random.choice(fr))
        pre=random.choice(["","","VK-INFO: ","Dear customer, ","प्रिय ग्राहक, ","Hi, "])
        rows.append((noise(fill(pre+" ".join(parts))),0,t))
random.shuffle(rows)
with open("dataset.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow(["text","label","type"]);w.writerows(rows)
print(len(rows),sum(r[1] for r in rows))
