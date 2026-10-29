"""
Write data/dialogues/heldout.yaml (15) and dev.yaml (25).

Each dialogue is what an applicant types into the optional chat assistant. `expected` is derived BY HAND
from the text (see NUMBER_WORDS.md). The metric is per-field exact match on amount, term_months and
monthly_income (3 fields per dialogue); when the text is genuinely ambiguous the expected value is null and
the expected action is ask_again (the system must ask, never guess).
Dialect labels are our best approximation and need a native reader's review before freezing.
"""
import os
import yaml

ROOT = os.path.dirname(os.path.abspath(__file__))


def d(id_, dialect, turns, amount, term, income, action="confirm", note=None):
    x = {"id": id_, "dialect": dialect, "turns": turns,
         "expected": {"amount": amount, "term_months": term, "monthly_income": income, "action": action}}
    if note:
        x["note"] = note
    return x


HELDOUT = [
    d("HO-DLG-01", "baghdadi", ["هلا، اريد قرض مليون ونص، أسدده بسنة ونص", "دخلي بالشهر حدود ثمنميه ألف"], 1_500_000, 18, 800_000),
    d("HO-DLG-02", "baghdadi", ["شكد گدر آخذ قرض؟ اريد نص مليون بس، وأرجعه بستة شهور", "أشتغل سواق تكسي، يطلع لي بالشهر ميتين وخمسين ألف"], 500_000, 6, 250_000),
    d("HO-DLG-03", "baghdadi", ["اريد مليونين ونص، اسدده بسنتين", "دخلي مليون وربع بالشهر"], 2_500_000, 24, 1_250_000),
    d("HO-DLG-04", "baghdadi", ["اريد قرض حتى اوسّع المحل، بس ما أدري شكد اگدر آخذ"], None, None, None, "ask_again", "no amount, term or income given"),
    d("HO-DLG-05", "basrawi", ["هلا ويّاك، اريد قرض مليون وربع، واسدّه بسنة", "دخلي بالشهر هواي مو ثابت، تقريباً ستميه ألف"], 1_250_000, 12, 600_000),
    d("HO-DLG-06", "basrawi", ["اريد ثلاث ملايين، اسدّدهم بسنة وثمان شهور", "آخذ بالشهر مليون وخمسميّة"], 3_000_000, 20, 1_500_000),
    d("HO-DLG-07", "basrawi", ["اريد مبلغ زين، بس مو هواي. اشوكت اگدر اخذه؟"], None, None, None, "ask_again", "'a decent amount, not a lot' is not a figure"),
    d("HO-DLG-08", "mosuli", ["السلام عليكم، آني اريد قرض مليون إلا ربع، أسدّده بثمان شهور", "دخلي بالشهر خمسمية ألف"], 750_000, 8, 500_000),
    d("HO-DLG-09", "mosuli", ["هسّة محتاج مليونين لأجل المحل، وأسدّدهم بسنة", "الشغل كلّش متقلّب، بس بالمتوسط ثمنمية ألف"], 2_000_000, 12, 800_000),
    d("HO-DLG-10", "mosuli", ["اريد قرض مليون وأسدّده بسنة", "دخلي خمسمية ألف بالشهر", "لا لحظة، يمكن مليون ونص بالشهر، ما أدري بالضبط"], 1_000_000, 12, None, "ask_again", "contradictory income (X3): must be re-asked, not stored"),
    d("HO-DLG-11", "arabizi", ["hala, areed qarid milyon w nos, w asaddid b sana w nos", "dakhli b shahar 800 alf"], 1_500_000, 18, 800_000),
    d("HO-DLG-12", "arabizi", ["salam, areed 500 alf bs, arjeaa b sitta shhor", "dakhli hdood 350 alf"], 500_000, 6, 350_000),
    d("HO-DLG-13", "arabizi", ["shlonkum, areed rub3 milyon, w asaddid b 4 shhor", "m3ash 400 alf b shahar"], 250_000, 4, 400_000),
    d("HO-DLG-14", "msa", ["السلام عليكم، أرغب في الحصول على قرض بقيمة مليون وخمسمئة ألف دينار، وأود سداده خلال ثمانية عشر شهراً.", "دخلي الشهري الصافي حوالي تسعمئة ألف دينار."], 1_500_000, 18, 900_000),
    d("HO-DLG-15", "msa", ["أحتاج إلى قرض قدره ثلاثة ملايين دينار لمدة سنتين.", "يبلغ صافي دخلي الشهري مليوناً ومئتي ألف دينار."], 3_000_000, 24, 1_200_000),
]

DEV = [
    d("DEV-DLG-01", "baghdadi", ["أريد أخذ قرض نص مليون، وأرجّعه بأربع شهور", "راتبي من الشغل حدود تلتمية ألف"], 500_000, 4, 300_000),
    d("DEV-DLG-02", "baghdadi", ["شكد گدر آخذ إذا أريد مليون وربع؟ أسدده بسنة", "دخلي بالشهر مليون إلا ربع"], 1_250_000, 12, 750_000),
    d("DEV-DLG-03", "baghdadi", ["اريد قرض مليونين، اسدده بسنتين", "الدخل الصافي حوالي مليون ومية ألف"], 2_000_000, 24, 1_100_000),
    d("DEV-DLG-04", "baghdadi", ["آني بقال، اريد قرض ثلاث ملايين حتى اشتري بضاعة، واسدده بسنة ونص", "دخلي مليون وثمنميه ألف بالشهر"], 3_000_000, 18, 1_800_000),
    d("DEV-DLG-05", "baghdadi", ["اريد 750 ألف، وارجّعهم بثمان شهور", "دخلي نص مليون بالشهر"], 750_000, 8, 500_000),
    d("DEV-DLG-06", "baghdadi", ["اريد قرض كم مليون بس مو متأكد شكد، وارجّعه بسنة تقريباً"], None, 12, None, "ask_again", "amount is 'a few millions': must ask"),
    d("DEV-DLG-07", "baghdadi", ["هلا، محتاج ربع مليون بس، ارجعهم بثلاث شهور", "دخلي مية وخمسين ألف"], 250_000, 3, 150_000),
    d("DEV-DLG-08", "basrawi", ["اريد قرض مليون ونص، واسدّه بسنتين", "دخلي بالشهر ثمنميّة وخمسين ألف"], 1_500_000, 24, 850_000),
    d("DEV-DLG-09", "basrawi", ["هلا، اريد مليونين، لا لحظة، مليونين وربع، اسدّه بسنة ونص", "اربح بالشهر مليون إلا ربع"], 2_250_000, 18, 750_000),
    d("DEV-DLG-10", "basrawi", ["اريد نص مليون، وارجعه بخمس شهور", "دخلي حدود أربعمية ألف"], 500_000, 5, 400_000),
    d("DEV-DLG-11", "basrawi", ["اريد قرض مليونين، بس شكد مدة لازم اسدّه؟", "دخلي بالشهر مليون"], 2_000_000, None, 1_000_000, "ask_again", "term missing: must ask"),
    d("DEV-DLG-12", "basrawi", ["اريد أربع ملايين، أسدّه بسنة وثمان شهور", "دخلي مليونين بالشهر"], 4_000_000, 20, 2_000_000),
    d("DEV-DLG-13", "mosuli", ["آني عندي مطعم صغير، اريد قرض ثلاث ملايين، واسدّده بسنتين", "الدخل الصافي مليون ونص"], 3_000_000, 24, 1_500_000),
    d("DEV-DLG-14", "mosuli", ["هسّة اريد مليون وربع، بثمان شهور", "دخلي كلّش قليل، حدود خمسمية وخمسين ألف"], 1_250_000, 8, 550_000),
    d("DEV-DLG-15", "mosuli", ["اريد قرض نص مليون واسدّه بستة شهور", "راتبي ثلاثمية ألف"], 500_000, 6, 300_000),
    d("DEV-DLG-16", "mosuli", ["اريد مبلغ حتى اجدّد المحل، شو الأفضل؟"], None, None, None, "ask_again", "no figures"),
    d("DEV-DLG-17", "arabizi", ["salam, areed milyon w rub3, asaddidhom b sana", "dakhli 700 alf"], 1_250_000, 12, 700_000),
    d("DEV-DLG-18", "arabizi", ["areed qarid 2 milyon w nos, b sanateen", "dakhli milyon b shahar"], 2_500_000, 24, 1_000_000),
    d("DEV-DLG-19", "arabizi", ["hala areed 300 alf, arjaa3hom b 5 shhor", "dakhli 450 alf"], 300_000, 5, 450_000),
    d("DEV-DLG-20", "arabizi", ["areed milyon ila rub3 w asaddid b sana w nos", "dakhli b shahar 600 alf"], 750_000, 18, 600_000),
    d("DEV-DLG-21", "arabizi", ["areed qarid, bs ma a3raf shgad"], None, None, None, "ask_again", "no figures"),
    d("DEV-DLG-22", "msa", ["أرغب في قرض بمبلغ مليونين وخمسمئة ألف دينار لمدة اثني عشر شهراً.", "دخلي الشهري ثمانمئة ألف دينار."], 2_500_000, 12, 800_000),
    d("DEV-DLG-23", "msa", ["أحتاج إلى قرض قدره مليون دينار يسدد خلال ستة أشهر.", "يبلغ دخلي الشهري ستمئة وخمسين ألف دينار."], 1_000_000, 6, 650_000),
    d("DEV-DLG-24", "msa", ["أرغب بالحصول على ثمانية ملايين دينار لمدة سبعة عشر شهراً.", "صافي دخلي الشهري مليونان وخمسمئة ألف."], 8_000_000, 17, 2_500_000),
    d("DEV-DLG-25", "msa", ["قرض بقيمة ربع مليون دينار، سداد خلال أربعة أشهر، ودخلي الشهري ثلاثمئة ألف."], 250_000, 4, 300_000),
]

HEADER = ("# Synthetic application dialogues. Expected values were derived by hand from the text.\n"
          "# Dialect labels are approximate; a native reader should review before the set is frozen.\n")


def write(name, items, split):
    for x in items:
        x["split"] = split
    with open(os.path.join(ROOT, "dialogues", name), "w", encoding="utf-8") as f:
        f.write(HEADER)
        yaml.safe_dump(items, f, allow_unicode=True, sort_keys=False, width=110)


if __name__ == "__main__":
    write("heldout.yaml", HELDOUT, "heldout")
    write("dev.yaml", DEV, "dev")
    from collections import Counter
    for nm, it in (("held-out", HELDOUT), ("dev", DEV)):
        print(nm, len(it), dict(Counter(x["dialect"] for x in it)),
              "ambiguous:", sum(x["expected"]["action"] == "ask_again" for x in it))
