"""
Self-test for llm/forbidden_terms.txt: patterns must flag decision language and must NOT flag the
legitimate wording we rely on (consent, accepted documents, safe replies).
Run: python llm/forbidden_terms_selftest.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_AR = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ة": "ه", "ـ": ""})


def norm(s):
    s = re.sub(r"[\u064B-\u0652]", "", s).translate(_AR)
    return s


def load():
    pats = []
    for line in open(os.path.join(HERE, "forbidden_terms.txt"), encoding="utf-8"):
        line = line.rstrip("\n")
        if line and not line.startswith("#"):
            pats.append(re.compile(norm(line), re.I))
    return pats


def flagged(text, pats):
    t = norm(text)
    return any(p.search(t) for p in pats)


MUST_FLAG = [
    "Your loan is approved.", "We have declined your application", "Application rejected", "Congratulations!",
    "تمت الموافقة على طلبك", "وافقنا على قرضك", "طلبك مرفوض", "تم رفض الطلب", "موافق", "مبروك عليك القرض",
    "نوافق على الطلب", "تم قبول طلبك", "I can approve this for you",
]
MUST_PASS = [
    "القرار يعود لموظف القروض، وأنا أجهّز لك الملف وأوضح ما ينقصه",
    "قبل أن نقرأ حركات المحفظة نحتاج موافقتك على تحليل الحركات، ويمكنك الاكتفاء بالمستندات",
    "المستندات المقبولة: عقد الإيجار، إجازة المشروع، فواتير الشراء",
    "The file is ready for the loan officer's review; a field visit is required.",
    "Your monthly installment would be 212,000 IQD, which is 50.1% of your income.",
    "ممكن تقلل المبلغ إلى 1,800,000 أو تمدد المدة إلى 12 شهر",
    "ينقص الملف: الضمان (كفيل أو وثيقة رهن)",
]

if __name__ == "__main__":
    pats = load()
    bad = [t for t in MUST_FLAG if not flagged(t, pats)] + [t for t in MUST_PASS if flagged(t, pats)]
    for t in bad:
        print("WRONG:", t)
    print(f"{len(pats)} patterns; {len(MUST_FLAG)} must-flag and {len(MUST_PASS)} must-pass phrases;",
          "FAILURES:" if bad else "all correct", len(bad) or "")
    sys.exit(1 if bad else 0)
