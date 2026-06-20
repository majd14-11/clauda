# Statistical Analysis Report
## Gastrointestinal Symptoms and Associated Factors Among University Students During Exam Periods

**Design:** Cross-sectional online survey (Google Forms), self-administered, Arabic-language.
**Analytic sample:** N = 370 consenting university students.
**Analysis executed:** Following the pre-specified *Research Analysis Plan* (Phases 1–5).
**Significance level:** α = 0.05 (two-sided). Significance flags: `*` p<.05, `**` p<.01, `***` p<.001.

> **Important note on tooling.** The pre-specified plan was written for SPSS. The analysis
> environment here had no SPSS and no internet access to install statistical packages, so every
> procedure was re-implemented from first principles in pure Python (`statlib.py`) and validated
> against textbook reference values before use (e.g., χ²(1)=3.841→p=.05; ANOVA worked example
> F=10.4, p=.0046; Mann–Whitney, Kruskal–Wallis, Pearson, OLS, logistic and ordinal models all
> recovered known answers). The *methods, decision rules, variable definitions and models are
> exactly those in the plan*; only the software differs. Results are directly reproducible and can
> be re-run in SPSS using the exported `cleaned_data.csv`.

---

## 1. Methods

### 1.1 Data source and sample construction
The raw export contained **401 responses** and 78 columns (Google Forms quiz auto-scoring columns
were ignored). The analytic sample was built per the plan:

| Step | n removed | n remaining |
|---|---|---|
| Raw responses | — | 401 |
| Excluded: did not consent | 8 | 393 |
| Excluded: school students / non-university entries (توجيهي، مدرسة، ثانوية، …) | 23 | **370** |

> **Deviation from the plan (documented):** the plan states "work only on the 211 consenting
> responses." The dataset has since grown — there are now **393 consenting** responses, of which
> **370** are eligible university students after removing school-level respondents. The analysis
> therefore uses the **actual N = 370** rather than the historical figure of 211. This *increases*
> statistical power and does not change the planned procedure.

### 1.2 Data cleaning and recoding (Phase 1)
- **Category normalisation.** Many option values carried a stray bullet/whitespace prefix
  (`"·       …"`); these were stripped so that, e.g., `"·       1–2 مرات"` and `"1–2 مرات"` were
  treated as the same category.
- **College (الكلية).** Free-text entries (45 raw variants) were standardised into 9 faculties
  (Medicine & Health Sciences, Engineering & IT, Dentistry, Pharmacy, Nursing, Sciences,
  Humanities & Social Sciences, Arts & Media, Other). School-level entries were excluded.
- **Chronic GI disease.** Recoded to binary (0 = "لا"; 1 = any named GI condition — IBS, ulcerative
  colitis, celiac, gastritis, H. pylori, etc.). n = 24 (6.5%) positive.
- **13 GI symptoms.** Each rated لا يوجد=0 / خفيف=1 / متوسط=2 / شديد=3.
  - **Outcome 1 — GI_presence (binary):** 1 if any of the 13 symptoms > 0.
  - **Outcome 2 — GI_severity (continuous 0–39):** sum of the 13 severity codes.
- **Outcome 3 — symptom_increase (ordinal 1–4):** لا أعلم=1 / لا فرق=2 / أحيانًا=3 / نعم بوضوح=4.
- **GHQ-12 psychological stress (Section 4).** The form stored this as a 4-column grid; each of the
  12 items was mapped to its frequency level (أبدا=0 / أقل من المعتاد=1 / أكثر من المعتاد=2 / كثيرًا=3),
  giving the Likert GHQ score (range 0–36; Step 1.7 of the plan).
  - **Completeness handling:** 252 respondents answered all 12 items; others answered fewer.
    A respondent's score was computed only if **≥ 6 of 12** items were answered (50% rule) and was
    **prorated** to the 0–36 scale; respondents with < 6 items were set to missing. This yields a
    valid stress score for **n = 279** and leaves 91 missing — the main driver of the smaller n in
    the regression models.
  - **stress_level (binary):** median split (median = 20.0): High (>20) vs Low (≤20).
- **Ordinal ranks** were created for age, academic year, sleep hours, caffeine intake, eating-habit
  change, symptom frequency and study impact, exactly as specified.

### 1.3 Statistical methods
- **Phase 2 – Normality.** Shapiro–Wilk (Royston algorithm) and, as a cross-check, the
  D'Agostino–Pearson omnibus K² test, on the two continuous variables (GI_severity, stress_score).
- **Phase 3 – Descriptives.** n (%) for categorical; mean ± SD, median, IQR, range for continuous.
- **Phase 4 – Bivariate.** Test chosen by outcome type and the normality result:
  χ² (with Fisher's exact for 2×2) for GI_presence; Mann–Whitney U / Kruskal–Wallis H / Spearman ρ
  for the non-normal GI_severity and the ordinal symptom_increase.
- **Phase 5 – Regression.** Multiple linear (GI_severity), binary logistic (GI_presence) and ordinal
  proportional-odds logistic (symptom_increase), all entering predictors simultaneously (Enter
  method). For the regression models only, the 9 faculties were collapsed into 4 groups
  (Medicine & Health = reference; Engineering & IT; Other Health = Dentistry/Pharmacy/Nursing/Sciences;
  Non-Health = Humanities/Arts/Other) to avoid unstable estimates from very small faculty cells.

---

## 2. Results

### Phase 2 — Normality of continuous variables

| Variable | n | Mean ± SD | Median (IQR) | Range | Skew | Shapiro–Wilk | D'Agostino | Decision |
|---|---|---|---|---|---|---|---|---|
| GI_severity (0–39) | 370 | 10.31 ± 7.23 | 9.5 (4.0–15.0) | 0–33 | 0.46 | W=0.961, **p<.001** | K²=19.66, **p<.001** | **Non-normal → non-parametric** |
| Stress score (0–36) | 279 | 19.19 ± 9.28 | 20.0 (13.0–26.0) | 0–36 | −0.16 | W=0.980, **p<.001** | K²=13.95, **p<.001** | **Non-normal → non-parametric** |

Both continuous variables departed significantly from normality, so all subsequent comparisons
involving them use **non-parametric** tests (Mann–Whitney U, Kruskal–Wallis H, Spearman ρ), exactly
as the plan's decision rule dictates.

### Phase 3 — Descriptive statistics

**Table 3.1 Demographics (N = 370)**

| Variable | Category | n (%) |
|---|---|---|
| Age | <20 | 207 (55.9) |
|  | 20–24 | 150 (40.5) |
|  | 25–29 | 12 (3.2) |
|  | 30+ | 1 (0.3) |
| Gender | Female | 210 (56.8) |
|  | Male | 160 (43.2) |
| Academic year | 1st | 185 (50.0) |
|  | 2nd | 54 (14.6) |
|  | 3rd | 34 (9.2) |
|  | 4th | 37 (10.0) |
|  | 5th+ | 60 (16.2) |
| Chronic GI disease | No | 346 (93.5) |
|  | Yes | 24 (6.5) |
| College | Medicine & Health Sciences | 172 (46.5) |
|  | Engineering & IT | 91 (24.6) |
|  | Humanities & Social Sciences | 34 (9.2) |
|  | Dentistry | 21 (5.7) |
|  | Arts & Media | 14 (3.8) |
|  | Other | 13 (3.5) |
|  | Pharmacy | 10 (2.7) |
|  | Nursing | 9 (2.4) |
|  | Sciences | 6 (1.6) |

**Table 3.2 Severity of each GI symptom during exams** — n (%) per level

| Symptom | None | Mild | Moderate | Severe | Any (≥mild) |
|---|---|---|---|---|---|
| Abdominal pain / colic | 108 (29) | 107 (29) | 107 (29) | 48 (13) | **71%** |
| Bloating / fullness | 138 (37) | 97 (26) | 80 (22) | 55 (15) | 63% |
| Bothersome gas | 157 (42) | 80 (22) | 84 (23) | 49 (13) | 58% |
| Diarrhea | 225 (61) | 79 (21) | 47 (13) | 19 (5) | 39% |
| Constipation | 241 (65) | 63 (17) | 43 (12) | 23 (6) | 35% |
| Vomiting | 285 (77) | 46 (12) | 24 (6) | 15 (4) | 23% |
| Nausea | 186 (50) | 84 (23) | 60 (16) | 40 (11) | 50% |
| Heartburn / acidity | 151 (41) | 90 (24) | 86 (23) | 43 (12) | 59% |
| Appetite loss | 129 (35) | 74 (20) | 89 (24) | 78 (21) | **65%** |
| Difficulty swallowing | 256 (69) | 57 (15) | 42 (11) | 15 (4) | 31% |
| Rectal bleeding / blood in stool | 325 (88) | 21 (6) | 14 (4) | 10 (3) | 12% |
| Weight loss | 219 (59) | 64 (17) | 60 (16) | 27 (7) | 41% |
| Weight gain | 246 (66) | 55 (15) | 46 (12) | 23 (6) | 34% |

- **Outcome 1 — GI symptom presence:** **Yes = 334 (90.3%)**, No = 36 (9.7%).
- **Outcome 2 — GI severity score:** mean **10.31 ± 7.23**, median 9.5 (IQR 4–15), range 0–33.

**Table 3.3 Symptom characteristics**

| Variable | Category | n (%) |
|---|---|---|
| Frequency (last week) | Never 106 (28.6) · 1–2× 150 (40.5) · 3–4× 85 (23.0) · 5+× 29 (7.8) | |
| Impact on study | None 100 (27.0) · Mild 144 (38.9) · Moderate 89 (24.1) · Large 37 (10.0) | |
| Healthcare visit | No 308 (83.2) · **Yes 62 (16.8)** | |
| Medication / remedy use | No 322 (87.5) · **Yes 46 (12.5)** (n=368) | |

**Table 3.4 Lifestyle and self-reported comparison**

| Variable | Distribution n (%) |
|---|---|
| **Symptom increase vs normal days (Outcome 3)** | Don't know 51 (13.8) · No difference 60 (16.2) · Sometimes 103 (27.8) · **Yes, clearly 156 (42.2)** |
| Sleep / night | **<5h 150 (40.5)** · 5–6h 139 (37.6) · 6–7h 66 (17.8) · >7h 15 (4.1) |
| Daily caffeine | 0: 84 (22.7) · 1–2: 190 (51.4) · 3–4: 74 (20.0) · >4: 22 (5.9) |
| Eating-habit change | Better 16 (4.3) · No change 149 (40.3) · **Worse 205 (55.4)** |

**Table 3.5 Psychological stress (GHQ-12, 0–36; n = 279)**
- Total stress score: mean **19.19 ± 9.28**, median 20.0 (IQR 13–26), range 0–36.
- Stress level (median split at 20.0): Low 148 (53.0%), High 131 (47.0%).

> **Descriptive headline:** During exams, **9 in 10 students reported at least one GI symptom**, the
> commonest being abdominal pain/colic (71%), appetite loss (65%), bloating (63%) and heartburn (59%).
> **42% reported a clear increase** in symptoms versus normal days, **55% reported worsened eating
> habits**, and **41% slept under 5 hours/night**. Despite this, only 17% sought care and 13% took
> medication — pointing to a substantial, largely self-managed symptom burden.

### Phase 4 — Bivariate associations

Significance flags as above. For GI_severity (non-normal) and symptom_increase (ordinal),
non-parametric tests are used; Spearman ρ is reported for ordinal/continuous predictors.

**Table 4.1 Demographic predictors × 3 outcomes**

| Predictor | GI_presence | GI_severity | symptom_increase |
|---|---|---|---|
| **Gender (M vs F)** | χ²(1)=26.12, **p<.001*** | U, z=−5.73, **p<.001*** (F med 12 vs M 6.5) | U, z=−4.09, **p<.001*** (F med 4 vs M 3) |
| Age group | χ²(3)=8.10, p=.044* | ρ=.161, **p=.002**; H=9.59, p=.022* | ρ=.146, **p=.005**; H=9.78, p=.021* |
| College (9 grp) | χ²(8)=10.40, p=.238 | H(8)=16.88, p=.031* | H(8)=12.96, p=.113 |
| Academic year | χ²(4)=10.46, p=.033* | ρ=.180, **p<.001***; H=13.91, p=.008** | ρ=.162, **p=.002**; H=11.51, p=.021* |
| **Chronic GI disease** | χ²(1)=2.77, p=.096 | U, z=−5.18, **p<.001*** (med 9 vs 19) | U, z=−1.64, p=.101 |

**Table 4.2 Lifestyle / stress predictors × 3 outcomes**

| Predictor | GI_presence | GI_severity | symptom_increase |
|---|---|---|---|
| **Sleep hours** | χ²(3)=10.98, p=.012* | ρ=−.199, **p<.001***; H=14.84, p=.002** | ρ=−.243, **p<.001***; H=25.35, **p<.001*** |
| Caffeine intake | χ²(3)=8.92, p=.030* | ρ=.081, p=.121; H=13.44, p=.004** | ρ=.126, p=.015*; H=12.51, p=.006** |
| **Eating-habit change** | χ²(2)=24.87, **p<.001*** | ρ=**.333**, **p<.001***; H=44.96, **p<.001*** | ρ=**.401**, **p<.001***; H=60.51, **p<.001*** |
| **Stress level (Hi/Lo)** | χ²(1)=13.75, **p<.001*** | U, z=−6.27, **p<.001*** (med 7 vs 13) | U, z=−5.62, **p<.001*** |
| **Stress score (cont.)** | MWU z=−5.36, **p<.001*** (No med 5 vs Yes 21) | ρ=**.429**, **p<.001*** | ρ=**.342**, **p<.001*** |

> Some demographic cells (older ages, smaller faculties) had expected counts < 5, so the χ² results
> for age and college should be read cautiously (Fisher's exact agreed for all 2×2 tables).

### Phase 5 — Multivariable regression

All models use listwise deletion; analytic **n = 279** (limited by GHQ stress availability).
Faculties collapsed to 4 groups (ref = Medicine & Health).

**Model 2 — Multiple linear regression: predictors of GI_severity (0–39)**
R² = 0.351, Adjusted R² = 0.324, F(11,267) = 13.11, **p<.001**. All VIF < 3.2 (no multicollinearity).

| Predictor | B | SE | β | t | p | 95% CI (B) |
|---|---|---|---|---|---|---|
| Gender (Male vs Female) | −2.335 | 0.833 | −0.161 | −2.81 | **.005** | −3.97, −0.70 |
| Age group | 0.178 | 1.084 | 0.014 | 0.16 | .869 | −1.95, 2.30 |
| Academic year | 0.156 | 0.391 | 0.035 | 0.40 | .690 | −0.61, 0.92 |
| **Chronic GI disease (Yes)** | **6.702** | 1.339 | 0.257 | 5.01 | **<.001** | 4.08, 9.33 |
| Sleep hours (rank) | −0.595 | 0.436 | −0.071 | −1.36 | .174 | −1.45, 0.26 |
| Caffeine intake (rank) | −0.467 | 0.449 | −0.054 | −1.04 | .300 | −1.35, 0.41 |
| **Eating-habit change (rank)** | **2.371** | 0.735 | 0.182 | 3.23 | **.001** | 0.93, 3.81 |
| **Stress score (0–36)** | **0.211** | 0.044 | 0.278 | 4.75 | **<.001** | 0.12, 0.30 |
| College: Engineering & IT | −0.746 | 0.896 | −0.045 | −0.83 | .406 | −2.50, 1.01 |
| College: Other Health | −1.630 | 1.141 | −0.076 | −1.43 | .154 | −3.87, 0.61 |
| **College: Non-Health** | **−3.147** | 1.024 | −0.166 | −3.07 | **.002** | −5.15, −1.14 |

Independent predictors of **higher** severity: **chronic GI disease** (+6.7 points), **worsening eating
habits** (+2.4 per level), and **higher psychological stress** (+0.21 per GHQ point). **Female gender**
and being in a **non-health faculty** were associated with **lower** severity.

**Model 1 — Binary logistic regression: GI_presence** (events: Yes=257, No=22)
Maximum-likelihood estimation **did not converge** (quasi-complete separation: only 22 "No"
events for ~11 predictors, events-per-variable ≈ 2). A **ridge-penalised** logistic regression
(L2, λ=1.0, intercept unpenalised) is reported instead; estimates are shrunk toward the null and
are **exploratory only**. Full model: LR χ²(11)=57.81, p<.001, Nagelkerke R²=0.441.

| Predictor | B | OR | p | 95% CI (OR) |
|---|---|---|---|---|
| **Gender (Male vs Female)** | −1.289 | **0.276** | **.016** | 0.097–0.784 |
| **Stress score (0–36)** | 0.125 | **1.133** | **<.001** | 1.052–1.219 |
| Eating-habit change | 0.644 | 1.903 | .186 | 0.733–4.942 |
| Sleep hours | −0.429 | 0.651 | .112 | 0.384–1.105 |
| (other predictors n.s.) | | | | |

A parsimonious ridge model (gender, chronic GI, sleep, caffeine, eating, stress) agreed:
**Gender** OR=0.25 (**p=.008**) and **Stress** OR=1.13 (**p<.001**) remained the significant
predictors of having any symptom.

**Model 3 — Ordinal logistic (proportional odds): symptom_increase (1–4)** (n=279)
LR χ²(11)=82.07, **p<.001**, Nagelkerke R²=0.276. Parameterisation: a **positive B** means the
predictor raises the odds of being in a **higher** symptom-increase category.

| Predictor | B | OR | p | 95% CI (OR) |
|---|---|---|---|---|
| **Sleep hours (rank)** | −0.442 | **0.643** | **.002** | 0.486–0.849 |
| **Eating-habit change (rank)** | 0.885 | **2.423** | **<.001** | 1.517–3.872 |
| **Stress score (0–36)** | 0.039 | **1.040** | **.007** | 1.011–1.071 |
| **College: Non-Health** | −1.029 | **0.357** | **.002** | 0.187–0.685 |
| Gender (Male vs Female) | −0.450 | 0.638 | .093 | 0.377–1.077 |
| (age, year, chronic, caffeine, other college n.s.) | | | | |

Students who **slept less**, whose **eating worsened**, and who were **more stressed** had
significantly higher odds of reporting that their symptoms increased on exam days.

---

## 3. Key findings (interpretation)

1. **GI symptoms during exams are near-universal and burdensome.** 90% reported ≥1 symptom; 42%
   perceived a clear exam-related increase. The dominant complaints (abdominal pain, appetite loss,
   bloating, heartburn, nausea) are consistent with a stress/brain–gut mechanism rather than
   infection.
2. **Psychological stress is the most consistent modifiable correlate** — significant for all three
   outcomes in both bivariate and multivariable analyses (severity β=0.28; presence OR=1.13/GHQ point;
   increase OR=1.04/point).
3. **Worsening eating habits and reduced sleep** independently track with greater severity and a
   perceived exam-time increase — both are actionable behavioural targets.
4. **Chronic GI disease** strongly raises the severity score (+6.7 points), supporting the plan's
   suggestion to treat it as a covariate (it was retained in all models).
5. **Female students reported greater burden** (higher severity and higher odds of any symptom),
   a pattern widely reported in functional-GI literature.
6. **Faculty effects are weak and likely confounded;** the only consistent signal (lower burden in
   non-health faculties) should be interpreted cautiously given small cells.

## 4. Limitations
- **Cross-sectional, self-reported** data → associations are not causal; recall and social-desirability
  bias are possible.
- **GI_presence is highly skewed (90% "Yes")**, producing **separation** in the logistic model; its
  multivariable results are exploratory (ridge-penalised). The bivariate χ² findings are the more
  reliable evidence for Outcome 1.
- **GHQ completeness:** 91/370 (25%) had < 6 GHQ items and were excluded from stress-based analyses;
  the prorating rule and median split are pragmatic choices that should be stated in the manuscript.
- **Small faculty cells** required collapsing college for regression; the proportional-odds
  assumption (parallel lines) for Model 3 was not formally tested here and should be checked in SPSS.
- The plan's **GHQ "0–12"** label conflicts with its own Step 1.7 (sum = 0–36); the 0–36 Likert
  scoring (Step 1.7) was used and should be reported consistently.

## 5. Reproducibility / files
| File | Contents |
|---|---|
| `cleaned_data.csv` | Final analytic dataset (N=370) with all recoded variables — ready to import into SPSS |
| `statlib.py` | Pure-Python statistics library (all tests/models), validated against reference values |
| `analysis.py` | Phase-1 loading, cleaning and recoding |
| `run_phases.py` | Phases 2–3 (normality + descriptives) → `results.txt` |
| `run_phase4.py` | Phase 4 (bivariate) → `results_p4.txt` |
| `run_phase5.py` | Phase 5 (regression) → `results_p5.txt` |
| `protocol_clean.txt` | Plain-text extraction of the original analysis-plan document |

To reproduce in SPSS, import `cleaned_data.csv` and follow the SPSS menu paths listed in the original
plan; variable names match the plan (e.g., `GI_presence`, `GI_severity`, `symptom_increase`,
`stress_score`, `age_rank`, `sleep_rank`, etc.).
