# -*- coding: utf-8 -*-
"""
Full statistical analysis pipeline for:
"Gastrointestinal Symptoms and Associated Factors Among University Students
 During Exam Periods"
Follows the pre-specified analysis plan (Phases 1-5).
Pure Python + statlib.py (no numpy/scipy/SPSS required).
"""
import csv, re, math, sys
import statlib as S
from collections import Counter, OrderedDict

CSV = "نموذج بدون عنوان (1).csv"

def norm(s):
    if s is None:
        return ""
    s = s.replace('·', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return s

# ----- column indices -----
C_CONSENT = 2
C_AGE = 5
C_GENDER = 8
C_COLLEGE = 11
C_YEAR = 14
C_CHRONIC = 17
SYM_IDX = list(range(20, 45, 2))   # 13 symptom columns
SYM_LABELS = ["AbdPain_colic", "Bloating", "Gas", "Diarrhea", "Constipation",
              "Vomiting", "Nausea", "Heartburn", "Appetite_loss", "Dysphagia",
              "Rectal_bleed", "Weight_loss", "Weight_gain"]
SYM_AR = ["ألم بطني أو مغص", "انتفاخ/امتلاء", "غازات", "إسهال", "إمساك", "قيء",
          "غثيان", "حرقة/حموضة", "فقدان شهية", "صعوبة بلع", "نزيف شرجي",
          "فقدان وزن", "زيادة وزن"]
C_FREQ = 46
C_IMPACT = 49
C_VISIT = 52
C_MED = 55
C_INCREASE = 58
C_SLEEP = 61
C_CAFFEINE = 64
C_EATING = 67
GHQ_COLS = [(70, 0), (72, 1), (74, 2), (76, 3)]  # (col, level)

SEV = {"لا يوجد": 0, "خفيف": 1, "متوسط": 2, "شديد": 3}

def age_rank(v):
    v = norm(v)
    if not v: return None
    if "أقل من 20" in v: return 1
    if "20" in v and "24" in v: return 2
    if "25" in v and "29" in v: return 3
    if "30" in v: return 4
    return None

def year_rank(v):
    v = norm(v)
    for kw, r in [("أولى", 1), ("ثانية", 2), ("ثالثة", 3), ("رابعة", 4), ("خامسة", 5)]:
        if kw in v: return r
    return None

def sleep_rank(v):
    v = norm(v)
    if not v: return None
    if "أقل من 5" in v: return 1
    if "أكثر من 7" in v: return 4
    if "5" in v and "6" in v: return 2
    if "6" in v and "7" in v: return 3
    return None

def caffeine_rank(v):
    v = norm(v)
    if v == "": return None
    if "أكثر من 4" in v: return 4
    if v == "0" or v.strip() == "0": return 1
    if "1" in v and "2" in v: return 2
    if "3" in v and "4" in v: return 3
    if v == "0": return 1
    return None

def freq_rank(v):
    v = norm(v)
    if not v: return None
    if "لم تحدث" in v: return 1
    if "5" in v and ("أكثر" in v or "اكثر" in v): return 4
    if "1" in v and "2" in v: return 2
    if "3" in v and "4" in v: return 3
    return None

def impact_rank(v):
    v = norm(v)
    if not v: return None
    if "لا تأثير" in v: return 1
    if "بسيط" in v: return 2
    if "متوسط" in v: return 3
    if "كبير" in v: return 4
    return None

def eating_rank(v):
    v = norm(v)
    if not v: return None
    if "الأفضل" in v or "الافضل" in v: return 1
    if "لم تتغير" in v: return 2
    if "أسوأ" in v or "اسوأ" in v or "اسوا" in v: return 3
    return None

def increase_rank(v):
    v = norm(v)
    if not v: return None
    if "لا أعلم" in v or "لا ألاحظ" in v or "لا اعلم" in v: return 1
    if "لا فرق" in v: return 2
    if "أحيان" in v or "احيان" in v: return 3
    if "نعم" in v: return 4
    return None

def yesno(v):
    v = norm(v)
    if v == "": return None
    if v == "لا": return 0
    if v == "نعم": return 1
    return None

def med_bin(v):
    v = norm(v)
    if v == "": return None
    if v in (",", "?", "...", "."): return None
    if v == "لا": return 0
    return 1

def chronic_bin(v):
    v = norm(v)
    if v == "": return None
    if v == "لا": return 0
    return 1

# ----- college recode -----
def college_clean(v):
    v = norm(v)
    if v == "": return None
    # exclude school students / non-university
    excl_kw = ["توجيهي", "مدرسة", "مدرسه", "ثانوي", "ثانوية", "مش بكلية", "school",
               "طالبة ثانوية", "هندسة زراعية", "..."]
    if v in ("...",): return "EXCLUDE"
    for kw in excl_kw:
        if kw in v:
            return "EXCLUDE"
    if "اسنان" in v or "الفم" in v:
        return "Dentistry"
    if "تمريض" in v:
        return "Nursing"
    if "صيدلة" in v:
        return "Pharmacy"
    if "الطب وعلوم الصحة" in v or "طب وعلوم الصحة" in v:
        return "Medicine & Health Sciences"
    if "هندسة" in v:   # remaining engineering (agric. already excluded)
        return "Engineering & IT"
    if "العلوم الإنسانية" in v or "الاقتصاد" in v or "التربية" in v or "الآداب" in v or "الاداب" in v:
        return "Humanities & Social Sciences"
    if "الفنون" in v or v == "فنون":
        return "Arts & Media"
    if v == "كلية العلوم" or v == "العلوم":
        return "Sciences"
    # everything else -> Other (law, security, allied professions, military med, etc.)
    return "Other"

GHQ_ITEMS = [
    "هل واجهت صعوبة في التركيز؟",
    "هل فقدت النوم بسبب القلق؟",
    "هل شعرت أنك لا تقوم بدور مفيد؟",
    "هل واجهت صعوبة في اتخاذ القرارات؟",
    "هل شعرت أنك تحت ضغط مستمر؟",
    "هل واجهت صعوبة في التغلب على المشاكل؟",
    "هل واجهت صعوبة في الاستمتاع بالأنشطة اليومية؟",
    "هل شعرت أنك غير قادر على مواجهة المشاكل؟",
    "هل شعرت بالحزن أو الاكتئاب؟",
    "هل شعرت أنك فقدت الثقة بنفسك؟",
    "هل شعرت أنك بلا قيمة؟",
    "هل شعرت أنك غير سعيد عمومًا؟",
]
GHQ_SET = set(GHQ_ITEMS)

def parse_ghq(row):
    """Return (stress_score 0-36 prorated, n_answered) or (None, n_answered)."""
    item_levels = {}
    for col, level in GHQ_COLS:
        cell = row[col]
        if not cell:
            continue
        for part in cell.split(';'):
            it = norm(part)
            if it in GHQ_SET:
                if it in item_levels:
                    item_levels[it] = max(item_levels[it], level)
                else:
                    item_levels[it] = level
    n_ans = len(item_levels)
    if n_ans >= 6:
        total = sum(item_levels.values())
        prorated = total / n_ans * 12.0
        return prorated, n_ans, item_levels
    return None, n_ans, item_levels


def load():
    with open(CSV, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    header, data = rows[0], rows[1:]
    recs = []
    n_total = len(data)
    n_noconsent = 0
    n_excl_college = 0
    for row in data:
        rec = {}
        consent = norm(row[C_CONSENT])
        if consent != "نعم ,أوافق بشدة" and "نعم" not in consent:
            n_noconsent += 1
            continue
        col = college_clean(row[C_COLLEGE])
        if col is None or col == "EXCLUDE":
            n_excl_college += 1
            continue
        rec['college'] = col
        rec['age_rank'] = age_rank(row[C_AGE])
        rec['gender'] = norm(row[C_GENDER])  # ذكر/أنثى
        rec['gender_male'] = 1 if rec['gender'] == "ذكر" else (0 if rec['gender'] == "أنثى" else None)
        rec['year_rank'] = year_rank(row[C_YEAR])
        rec['chronic_GI'] = chronic_bin(row[C_CHRONIC])
        # symptoms
        codes = []
        ok = True
        for idx in SYM_IDX:
            v = norm(row[idx])
            codes.append(SEV.get(v, None))
        rec['sym_codes'] = codes
        valid_codes = [c for c in codes if c is not None]
        if valid_codes:
            rec['GI_severity'] = sum(valid_codes)
            rec['GI_presence'] = 1 if any(c > 0 for c in valid_codes) else 0
            rec['n_sym_valid'] = len(valid_codes)
        else:
            rec['GI_severity'] = None
            rec['GI_presence'] = None
            rec['n_sym_valid'] = 0
        rec['freq_rank'] = freq_rank(row[C_FREQ])
        rec['impact_rank'] = impact_rank(row[C_IMPACT])
        rec['visit'] = yesno(row[C_VISIT])
        rec['med'] = med_bin(row[C_MED])
        rec['symptom_increase'] = increase_rank(row[C_INCREASE])
        rec['sleep_rank'] = sleep_rank(row[C_SLEEP])
        rec['caffeine_rank'] = caffeine_rank(row[C_CAFFEINE])
        rec['eating_rank'] = eating_rank(row[C_EATING])
        ss, nans, items = parse_ghq(row)
        rec['stress_score'] = ss
        rec['ghq_n'] = nans
        recs.append(rec)
    info = {'n_total': n_total, 'n_noconsent': n_noconsent,
            'n_excl_college': n_excl_college, 'n_final': len(recs)}
    return recs, info


def fmtp(p):
    if p is None or (isinstance(p, float) and math.isnan(p)):
        return "n/a"
    if p < 0.001:
        return "<0.001"
    return f"{p:.3f}"

def star(p):
    if p is None or (isinstance(p, float) and math.isnan(p)):
        return ""
    if p < 0.001: return "***"
    if p < 0.01: return "**"
    if p < 0.05: return "*"
    return ""

if __name__ == "__main__":
    recs, info = load()
    print("DATA LOADING SUMMARY")
    print(f"  Total raw responses          : {info['n_total']}")
    print(f"  Excluded - did not consent   : {info['n_noconsent']}")
    print(f"  Excluded - school/non-univ.  : {info['n_excl_college']}")
    print(f"  Final analytic sample (N)    : {info['n_final']}")
    # stress availability
    ss_ok = sum(1 for r in recs if r['stress_score'] is not None)
    print(f"  GHQ stress score available   : {ss_ok} (>=6 of 12 items answered)")
    import pickle
    with open("recs.pkl", "wb") as f:
        pickle.dump((recs, info), f)
    print("Saved recs.pkl")
