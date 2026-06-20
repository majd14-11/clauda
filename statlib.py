"""
Pure-Python statistics library for the GI-symptoms research analysis.
No third-party dependencies (no numpy/scipy) - everything implemented from scratch.
Implements: special functions, normality tests (Shapiro-Wilk Royston + D'Agostino),
chi-square/Fisher, t-test, ANOVA, Mann-Whitney U, Kruskal-Wallis H,
Pearson/Spearman correlation, and OLS / logistic / ordinal (proportional-odds) regression.
"""
import math

# ----------------------------------------------------------------------------
# Special functions
# ----------------------------------------------------------------------------

def norm_cdf(x):
    return 0.5 * math.erfc(-x / math.sqrt(2.0))

def norm_pdf(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)

def norm_ppf(p):
    """Inverse normal CDF (Acklam's algorithm)."""
    if p <= 0.0:
        return -math.inf
    if p >= 1.0:
        return math.inf
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow = 0.02425
    phigh = 1 - plow
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        x = (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
            ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    elif p <= phigh:
        q = p - 0.5
        r = q*q
        x = (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
            (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    else:
        q = math.sqrt(-2*math.log(1-p))
        x = -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
             ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    # one Halley refinement
    e = norm_cdf(x) - p
    u = e * math.sqrt(2*math.pi) * math.exp(x*x/2)
    x = x - u/(1 + x*u/2)
    return x

def _gammainc_lower_reg(a, x):
    """Regularized lower incomplete gamma P(a,x)."""
    if x < 0 or a <= 0:
        return 0.0
    if x == 0:
        return 0.0
    if x < a + 1.0:
        # series
        ap = a
        s = 1.0 / a
        d = s
        for _ in range(1000):
            ap += 1
            d *= x / ap
            s += d
            if abs(d) < abs(s) * 1e-15:
                break
        return s * math.exp(-x + a * math.log(x) - math.lgamma(a))
    else:
        # continued fraction for Q, then P = 1 - Q
        fpmin = 1e-300
        b = x + 1.0 - a
        c = 1.0 / fpmin
        d = 1.0 / b
        h = d
        for i in range(1, 1000):
            an = -i * (i - a)
            b += 2.0
            d = an * d + b
            if abs(d) < fpmin:
                d = fpmin
            c = b + an / c
            if abs(c) < fpmin:
                c = fpmin
            d = 1.0 / d
            delta = d * c
            h *= delta
            if abs(delta - 1.0) < 1e-15:
                break
        q = math.exp(-x + a * math.log(x) - math.lgamma(a)) * h
        return 1.0 - q

def chi2_sf(x, df):
    """Upper tail (survival) of chi-square."""
    if x <= 0:
        return 1.0
    return 1.0 - _gammainc_lower_reg(df / 2.0, x / 2.0)

def _betacf(a, b, x):
    fpmin = 1e-300
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-15:
            break
    return h

def betai(a, b, x):
    """Regularized incomplete beta I_x(a,b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                  + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    else:
        return 1.0 - bt * _betacf(b, a, 1.0 - x) / b

def t_sf(t, df):
    """Upper tail of Student's t."""
    x = df / (df + t * t)
    ib = 0.5 * betai(df / 2.0, 0.5, x)
    if t >= 0:
        return ib
    else:
        return 1.0 - ib

def t_two_sided_p(t, df):
    return 2.0 * t_sf(abs(t), df)

def f_sf(f, df1, df2):
    """Upper tail of F distribution."""
    if f <= 0:
        return 1.0
    x = df2 / (df2 + df1 * f)
    return betai(df2 / 2.0, df1 / 2.0, x)

# ----------------------------------------------------------------------------
# Descriptives
# ----------------------------------------------------------------------------

def mean(v):
    return sum(v) / len(v)

def variance(v, ddof=1):
    if len(v) <= ddof:
        return float('nan')
    m = mean(v)
    return sum((x - m) ** 2 for x in v) / (len(v) - ddof)

def sd(v, ddof=1):
    return math.sqrt(variance(v, ddof))

def median(v):
    s = sorted(v)
    n = len(s)
    if n == 0:
        return float('nan')
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2.0

def percentile(v, q):
    """Linear interpolation percentile (q in 0..100)."""
    s = sorted(v)
    n = len(s)
    if n == 0:
        return float('nan')
    if n == 1:
        return s[0]
    pos = (q / 100.0) * (n - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return s[lo]
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)

def skewness(v):
    n = len(v)
    m = mean(v)
    s = sd(v, ddof=1)
    if s == 0 or n < 3:
        return float('nan')
    return (n / ((n - 1) * (n - 2))) * sum(((x - m) / s) ** 3 for x in v)

def kurtosis_excess(v):
    n = len(v)
    m = mean(v)
    s = sd(v, ddof=1)
    if s == 0 or n < 4:
        return float('nan')
    g = sum(((x - m) / s) ** 4 for x in v)
    return ((n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3))) * g - \
           (3 * (n - 1) ** 2) / ((n - 2) * (n - 3))

# ----------------------------------------------------------------------------
# Normality tests
# ----------------------------------------------------------------------------

def dagostino_pearson(v):
    """D'Agostino-Pearson omnibus K^2 normality test. Returns (K2, p)."""
    n = len(v)
    if n < 20:
        return (float('nan'), float('nan'))
    b1 = skewness_biased(v)
    b2 = kurtosis_biased(v)
    # skewness test (D'Agostino)
    y = b1 * math.sqrt((n + 1) * (n + 3) / (6.0 * (n - 2)))
    beta2 = 3.0 * (n * n + 27 * n - 70) * (n + 1) * (n + 3) / \
            ((n - 2) * (n + 5) * (n + 7) * (n + 9))
    w2 = -1 + math.sqrt(2 * (beta2 - 1))
    delta = 1.0 / math.sqrt(0.5 * math.log(w2))
    alpha = math.sqrt(2.0 / (w2 - 1))
    if y == 0:
        zb1 = 0.0
    else:
        zb1 = delta * math.log(y / alpha + math.sqrt((y / alpha) ** 2 + 1))
    # kurtosis test (Anscombe-Glynn)
    eb2 = 3.0 * (n - 1) / (n + 1)
    varb2 = 24.0 * n * (n - 2) * (n - 3) / ((n + 1) ** 2 * (n + 3) * (n + 5))
    x = (b2 - eb2) / math.sqrt(varb2)
    sqrtbeta1 = 6.0 * (n * n - 5 * n + 2) / ((n + 7) * (n + 9)) * \
                math.sqrt(6.0 * (n + 3) * (n + 5) / (n * (n - 2) * (n - 3)))
    a = 6.0 + 8.0 / sqrtbeta1 * (2.0 / sqrtbeta1 + math.sqrt(1 + 4.0 / (sqrtbeta1 ** 2)))
    term = 1 - 2.0 / a
    denom = 1 + x * math.sqrt(2.0 / (a - 4.0))
    zb2 = ((term) - ((1 - 2.0 / a) / denom) ** (1.0 / 3.0)) / math.sqrt(2.0 / (9.0 * a))
    k2 = zb1 * zb1 + zb2 * zb2
    p = chi2_sf(k2, 2)
    return (k2, p)

def skewness_biased(v):
    n = len(v)
    m = mean(v)
    m2 = sum((x - m) ** 2 for x in v) / n
    m3 = sum((x - m) ** 3 for x in v) / n
    if m2 == 0:
        return 0.0
    return m3 / (m2 ** 1.5)

def kurtosis_biased(v):
    n = len(v)
    m = mean(v)
    m2 = sum((x - m) ** 2 for x in v) / n
    m4 = sum((x - m) ** 4 for x in v) / n
    if m2 == 0:
        return 0.0
    return m4 / (m2 ** 2)

def shapiro_wilk(x):
    """Shapiro-Wilk W test using Royston (1992/1995, AS R94). Valid 3<=n<=5000.
    Returns (W, p)."""
    n = len(x)
    if n < 3:
        return (float('nan'), float('nan'))
    xs = sorted(x)
    # normal scores m_i
    m = [norm_ppf((i + 1 - 0.375) / (n + 0.25)) for i in range(n)]
    ssm2 = sum(mi * mi for mi in m)
    rsn = 1.0 / math.sqrt(n)
    # polynomial coefficients (Royston)
    c1 = [0.0, 0.221157, -0.147981, -2.071190, 4.434685, -2.706056]
    c2 = [0.0, 0.042981, -0.293762, -1.752461, 5.682633, -3.582633]
    def poly(c, t):
        return sum(c[j] * t ** j for j in range(len(c)))
    a = [0.0] * n
    if n > 5:
        an = m[n - 1] / math.sqrt(ssm2)
        an1 = m[n - 2] / math.sqrt(ssm2)
        a_n = poly(c1, rsn) + an   # a[n-1] (largest)
        a_n1 = poly(c2, rsn) + an1
        phi = (ssm2 - 2.0 * m[n - 1] ** 2 - 2.0 * m[n - 2] ** 2) / \
              (1.0 - 2.0 * a_n ** 2 - 2.0 * a_n1 ** 2)
        a[n - 1] = a_n
        a[0] = -a_n
        a[n - 2] = a_n1
        a[1] = -a_n1
        for i in range(2, n - 2):
            a[i] = m[i] / math.sqrt(phi)
    else:
        an = m[n - 1] / math.sqrt(ssm2)
        a_n = poly(c1, rsn) + an
        phi = (ssm2 - 2.0 * m[n - 1] ** 2) / (1.0 - 2.0 * a_n ** 2)
        a[n - 1] = a_n
        a[0] = -a_n
        for i in range(1, n - 1):
            a[i] = m[i] / math.sqrt(phi)
    xbar = mean(xs)
    num = sum(a[i] * xs[i] for i in range(n)) ** 2
    den = sum((xi - xbar) ** 2 for xi in xs)
    if den == 0:
        return (float('nan'), float('nan'))
    W = num / den
    # p-value (Royston approximations)
    if n == 3:
        pi6 = 6.0 / math.pi
        stqr = math.asin(math.sqrt(0.75))
        p = pi6 * (math.asin(math.sqrt(W)) - stqr)
        return (W, max(0.0, min(1.0, 1 - p if p < 0.5 else p)))  # crude for n=3
    if n <= 11:
        gamma = -2.273 + 0.459 * n
        w1 = -math.log(gamma - math.log(1 - W))
        mu = 0.5440 - 0.39978 * n + 0.025054 * n ** 2 - 0.0006714 * n ** 3
        sigma = math.exp(1.3822 - 0.77857 * n + 0.062767 * n ** 2 - 0.0020322 * n ** 3)
    else:
        ln_n = math.log(n)
        w1 = math.log(1 - W)
        mu = -1.5861 - 0.31082 * ln_n - 0.083751 * ln_n ** 2 + 0.0038915 * ln_n ** 3
        sigma = math.exp(-0.4803 - 0.082676 * ln_n + 0.0030302 * ln_n ** 2)
    z = (w1 - mu) / sigma
    p = 1.0 - norm_cdf(z)
    return (W, p)

# ----------------------------------------------------------------------------
# Ranks (with ties -> average ranks)
# ----------------------------------------------------------------------------

def rankdata(v):
    n = len(v)
    order = sorted(range(n), key=lambda i: v[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j + 2) / 2.0  # average of ranks (1-based)
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks

def tie_correction(v):
    from collections import Counter
    c = Counter(v)
    return sum(t ** 3 - t for t in c.values())

# ----------------------------------------------------------------------------
# Two/multi-group tests
# ----------------------------------------------------------------------------

def ttest_ind(a, b):
    """Independent samples t-test. Returns dict with Student & Welch."""
    na, nb = len(a), len(b)
    ma, mb = mean(a), mean(b)
    va, vb = variance(a), variance(b)
    # Student (pooled)
    sp2 = ((na - 1) * va + (nb - 1) * vb) / (na + nb - 2)
    se_p = math.sqrt(sp2 * (1.0 / na + 1.0 / nb))
    t_p = (ma - mb) / se_p if se_p > 0 else float('nan')
    df_p = na + nb - 2
    p_p = t_two_sided_p(t_p, df_p)
    # Welch
    se_w = math.sqrt(va / na + vb / nb)
    t_w = (ma - mb) / se_w if se_w > 0 else float('nan')
    df_w = (va / na + vb / nb) ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
    p_w = t_two_sided_p(t_w, df_w)
    return {'mean_a': ma, 'mean_b': mb, 'sd_a': math.sqrt(va), 'sd_b': math.sqrt(vb),
            'n_a': na, 'n_b': nb,
            't_student': t_p, 'df_student': df_p, 'p_student': p_p,
            't_welch': t_w, 'df_welch': df_w, 'p_welch': p_w}

def anova_oneway(groups):
    """One-way ANOVA. groups = list of lists."""
    k = len(groups)
    N = sum(len(g) for g in groups)
    grand = mean([x for g in groups for x in g])
    ssb = sum(len(g) * (mean(g) - grand) ** 2 for g in groups)
    ssw = sum(sum((x - mean(g)) ** 2 for x in g) for g in groups)
    dfb = k - 1
    dfw = N - k
    msb = ssb / dfb
    msw = ssw / dfw if dfw > 0 else float('nan')
    F = msb / msw if msw > 0 else float('nan')
    p = f_sf(F, dfb, dfw)
    return {'F': F, 'df1': dfb, 'df2': dfw, 'p': p}

def mannwhitney_u(a, b):
    """Mann-Whitney U test, normal approximation with tie correction (two-sided)."""
    na, nb = len(a), len(b)
    combined = a + b
    ranks = rankdata(combined)
    Ra = sum(ranks[:na])
    U1 = Ra - na * (na + 1) / 2.0
    U2 = na * nb - U1
    U = min(U1, U2)
    mu = na * nb / 2.0
    n = na + nb
    tc = tie_correction(combined)
    sigma = math.sqrt((na * nb / 12.0) * ((n + 1) - tc / (n * (n - 1))))
    if sigma == 0:
        return {'U': U, 'z': float('nan'), 'p': float('nan'),
                'median_a': median(a), 'median_b': median(b), 'n_a': na, 'n_b': nb}
    z = (U - mu) / sigma
    # continuity correction
    zc = (abs(U - mu) - 0.5) / sigma
    p = 2.0 * (1.0 - norm_cdf(zc))
    p = min(1.0, p)
    return {'U': U, 'U1': U1, 'z': z, 'p': p,
            'median_a': median(a), 'median_b': median(b), 'n_a': na, 'n_b': nb,
            'mean_rank_a': Ra / na, 'mean_rank_b': (sum(ranks) - Ra) / nb}

def kruskal_wallis(groups):
    """Kruskal-Wallis H test with tie correction."""
    all_vals = [x for g in groups for x in g]
    N = len(all_vals)
    ranks = rankdata(all_vals)
    idx = 0
    H_sum = 0.0
    rank_groups = []
    for g in groups:
        rg = ranks[idx:idx + len(g)]
        rank_groups.append(rg)
        idx += len(g)
        H_sum += (sum(rg) ** 2) / len(g)
    H = 12.0 / (N * (N + 1)) * H_sum - 3.0 * (N + 1)
    tc = tie_correction(all_vals)
    correction = 1.0 - tc / (N ** 3 - N)
    if correction != 0:
        H = H / correction
    df = len(groups) - 1
    p = chi2_sf(H, df)
    return {'H': H, 'df': df, 'p': p,
            'mean_ranks': [sum(rg) / len(rg) for rg in rank_groups]}

# ----------------------------------------------------------------------------
# Correlation
# ----------------------------------------------------------------------------

def pearson_r(x, y):
    n = len(x)
    mx, my = mean(x), mean(y)
    sxy = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    sxx = sum((xi - mx) ** 2 for xi in x)
    syy = sum((yi - my) ** 2 for yi in y)
    if sxx == 0 or syy == 0:
        return {'r': float('nan'), 'p': float('nan'), 'n': n}
    r = sxy / math.sqrt(sxx * syy)
    if abs(r) >= 1.0:
        return {'r': r, 'p': 0.0, 'n': n}
    t = r * math.sqrt((n - 2) / (1 - r * r))
    p = t_two_sided_p(t, n - 2)
    return {'r': r, 'p': p, 'n': n, 't': t}

def spearman_r(x, y):
    rx = rankdata(x)
    ry = rankdata(y)
    res = pearson_r(rx, ry)
    return {'rho': res['r'], 'p': res['p'], 'n': res['n']}

# ----------------------------------------------------------------------------
# Categorical tests
# ----------------------------------------------------------------------------

def chi2_independence(table):
    """Pearson chi-square test of independence. table = list of rows (counts)."""
    nrows = len(table)
    ncols = len(table[0])
    row_tot = [sum(r) for r in table]
    col_tot = [sum(table[i][j] for i in range(nrows)) for j in range(ncols)]
    N = sum(row_tot)
    chi2 = 0.0
    min_exp = float('inf')
    n_low = 0
    ncells = nrows * ncols
    for i in range(nrows):
        for j in range(ncols):
            exp = row_tot[i] * col_tot[j] / N
            min_exp = min(min_exp, exp)
            if exp < 5:
                n_low += 1
            if exp > 0:
                chi2 += (table[i][j] - exp) ** 2 / exp
    df = (nrows - 1) * (ncols - 1)
    p = chi2_sf(chi2, df)
    return {'chi2': chi2, 'df': df, 'p': p, 'N': N,
            'min_expected': min_exp, 'pct_cells_low': 100.0 * n_low / ncells}

def fisher_exact_2x2(table):
    """Two-sided Fisher's exact test for a 2x2 table [[a,b],[c,d]]."""
    a, b = table[0]
    c, d = table[1]
    r1 = a + b; r2 = c + d
    c1 = a + c; c2 = b + d
    n = a + b + c + d
    def logfact(x):
        return math.lgamma(x + 1)
    def hyperg(a_):
        b_ = r1 - a_
        c_ = c1 - a_
        d_ = r2 - c_
        if b_ < 0 or c_ < 0 or d_ < 0:
            return 0.0
        logp = (logfact(r1) + logfact(r2) + logfact(c1) + logfact(c2)
                - logfact(n) - logfact(a_) - logfact(b_) - logfact(c_) - logfact(d_))
        return math.exp(logp)
    p_obs = hyperg(a)
    amin = max(0, c1 - r2)
    amax = min(r1, c1)
    p = 0.0
    for av in range(amin, amax + 1):
        pv = hyperg(av)
        if pv <= p_obs * (1 + 1e-7):
            p += pv
    return {'p': min(1.0, p), 'odds_ratio': (a * d) / (b * c) if b * c > 0 else float('inf')}

# ----------------------------------------------------------------------------
# Linear algebra
# ----------------------------------------------------------------------------

def mat_T(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

def mat_mul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    C = [[0.0] * p for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        for k in range(m):
            aik = Ai[k]
            if aik == 0:
                continue
            Bk = B[k]
            Ci = C[i]
            for j in range(p):
                Ci[j] += aik * Bk[j]
    return C

def mat_vec(A, x):
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]

def mat_inv(A):
    """Gauss-Jordan inverse."""
    n = len(A)
    M = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-14:
            raise ValueError("Singular matrix")
        M[col], M[piv] = M[piv], M[col]
        pivval = M[col][col]
        M[col] = [v / pivval for v in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                factor = M[r][col]
                M[r] = [M[r][k] - factor * M[col][k] for k in range(2 * n)]
    return [row[n:] for row in M]

# ----------------------------------------------------------------------------
# OLS multiple linear regression
# ----------------------------------------------------------------------------

def ols(X, y, names):
    """X includes intercept column. Returns coefficients with SE, t, p, plus R2 etc."""
    n = len(X); k = len(X[0])
    Xt = mat_T(X)
    XtX = mat_mul(Xt, X)
    XtX_inv = mat_inv(XtX)
    Xty = mat_vec(Xt, y)
    beta = mat_vec(XtX_inv, Xty)
    yhat = mat_vec(X, beta)
    resid = [y[i] - yhat[i] for i in range(n)]
    sse = sum(r * r for r in resid)
    ybar = mean(y)
    sst = sum((yi - ybar) ** 2 for yi in y)
    df_res = n - k
    mse = sse / df_res
    r2 = 1 - sse / sst
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - k)
    se = [math.sqrt(mse * XtX_inv[j][j]) for j in range(k)]
    tvals = [beta[j] / se[j] if se[j] > 0 else float('nan') for j in range(k)]
    pvals = [t_two_sided_p(tvals[j], df_res) for j in range(k)]
    ci = [(beta[j] - 1.96 * se[j], beta[j] + 1.96 * se[j]) for j in range(k)]
    # standardized beta
    sy = sd(y)
    std_beta = []
    for j in range(k):
        col = [X[i][j] for i in range(n)]
        sx = sd(col) if len(set(col)) > 1 else 0.0
        std_beta.append(beta[j] * sx / sy if sy > 0 else float('nan'))
    df_model = k - 1
    F = (r2 / df_model) / ((1 - r2) / df_res) if (1 - r2) > 0 else float('inf')
    Fp = f_sf(F, df_model, df_res)
    # VIF
    vif = compute_vif(X, names)
    return {'names': names, 'beta': beta, 'se': se, 't': tvals, 'p': pvals, 'ci': ci,
            'std_beta': std_beta, 'r2': r2, 'adj_r2': adj_r2, 'F': F, 'Fp': Fp,
            'df_model': df_model, 'df_res': df_res, 'n': n, 'sse': sse, 'mse': mse}

def compute_vif(X, names):
    """VIF for each non-intercept predictor."""
    n = len(X); k = len(X[0])
    vifs = {}
    for j in range(1, k):
        yj = [X[i][j] for i in range(n)]
        # regress column j on all others (incl intercept)
        Xo = [[X[i][c] for c in range(k) if c != j] for i in range(n)]
        try:
            Xt = mat_T(Xo)
            b = mat_vec(mat_inv(mat_mul(Xt, Xo)), mat_vec(Xt, yj))
            yhat = mat_vec(Xo, b)
            ybar = mean(yj)
            sst = sum((v - ybar) ** 2 for v in yj)
            sse = sum((yj[i] - yhat[i]) ** 2 for i in range(n))
            r2 = 1 - sse / sst if sst > 0 else 0.0
            vifs[names[j]] = 1.0 / (1.0 - r2) if r2 < 1 else float('inf')
        except Exception:
            vifs[names[j]] = float('nan')
    return vifs

# ----------------------------------------------------------------------------
# Binary logistic regression (IRLS / Newton-Raphson)
# ----------------------------------------------------------------------------

def logistic_regression(X, y, names, max_iter=100, tol=1e-8, ridge=0.0):
    """Binary logistic regression via IRLS. Optional L2 (ridge) penalty `ridge`
    on all coefficients EXCEPT the intercept (column 0). Ridge stabilises the
    fit under (quasi-)complete separation."""
    n = len(X); k = len(X[0])
    beta = [0.0] * k
    ll_old = None
    for _ in range(max_iter):
        eta = mat_vec(X, beta)
        p = [1.0 / (1.0 + math.exp(-max(-35, min(35, e)))) for e in eta]
        W = [pi * (1 - pi) for pi in p]
        # penalised gradient X'(y-p) - ridge*beta (no penalty on intercept)
        grad = [sum(X[i][j] * (y[i] - p[i]) for i in range(n)) - (ridge * beta[j] if j > 0 else 0.0)
                for j in range(k)]
        # Hessian X' W X + ridge*I (no penalty on intercept)
        XtWX = [[0.0] * k for _ in range(k)]
        for i in range(n):
            wi = W[i]
            if wi < 1e-12:
                wi = 1e-12
            Xi = X[i]
            for a in range(k):
                xa = Xi[a] * wi
                for b in range(k):
                    XtWX[a][b] += xa * Xi[b]
        for j in range(1, k):
            XtWX[j][j] += ridge
        try:
            H_inv = mat_inv(XtWX)
        except ValueError:
            break
        delta = mat_vec(H_inv, grad)
        # step-halving to keep |beta| bounded
        beta = [beta[j] + delta[j] for j in range(k)]
        beta = [max(-30.0, min(30.0, b)) for b in beta]
        ll = sum((y[i] * math.log(p[i] + 1e-300) + (1 - y[i]) * math.log(1 - p[i] + 1e-300)) for i in range(n))
        if ll_old is not None and abs(ll - ll_old) < tol:
            break
        ll_old = ll
    eta = mat_vec(X, beta)
    p = [1.0 / (1.0 + math.exp(-max(-35, min(35, e)))) for e in eta]
    W = [max(pi * (1 - pi), 1e-12) for pi in p]
    XtWX = [[0.0] * k for _ in range(k)]
    for i in range(n):
        wi = W[i]; Xi = X[i]
        for a in range(k):
            xa = Xi[a] * wi
            for b in range(k):
                XtWX[a][b] += xa * Xi[b]
    for j in range(1, k):
        XtWX[j][j] += ridge
    cov = mat_inv(XtWX)
    se = [math.sqrt(abs(cov[j][j])) for j in range(k)]
    z = [beta[j] / se[j] if se[j] > 0 else float('nan') for j in range(k)]
    pv = [2.0 * (1.0 - norm_cdf(abs(zj))) for zj in z]
    OR = [math.exp(max(-30, min(30, beta[j]))) for j in range(k)]
    ci = [(math.exp(max(-30, min(30, beta[j] - 1.96 * se[j]))),
           math.exp(max(-30, min(30, beta[j] + 1.96 * se[j])))) for j in range(k)]
    ll_model = sum((y[i] * math.log(p[i] + 1e-300) + (1 - y[i]) * math.log(1 - p[i] + 1e-300)) for i in range(n))
    ybar = mean(y)
    ll_null = sum((y[i] * math.log(ybar + 1e-300) + (1 - y[i]) * math.log(1 - ybar + 1e-300)) for i in range(n))
    lr_chi2 = 2 * (ll_model - ll_null)
    lr_p = chi2_sf(lr_chi2, k - 1)
    cox = 1 - math.exp(2 * (ll_null - ll_model) / n)
    nagel = cox / (1 - math.exp(2 * ll_null / n))
    return {'names': names, 'beta': beta, 'se': se, 'z': z, 'p': pv, 'OR': OR, 'ci': ci,
            'll_model': ll_model, 'll_null': ll_null, 'lr_chi2': lr_chi2, 'lr_p': lr_p,
            'nagelkerke': nagel, 'cox_snell': cox, 'n': n, 'events': int(sum(y))}

# ----------------------------------------------------------------------------
# Ordinal logistic regression (proportional odds), Newton-Raphson w/ numeric Hessian
# ----------------------------------------------------------------------------

def ordinal_logistic(Xcov, y, names, max_iter=200, tol=1e-7):
    """Proportional odds model. y in {1..J} (consecutive ints). Xcov has NO intercept.
    Parameter vector = [thresholds(J-1), betas(p)]. logit P(Y<=j) = theta_j - x'beta."""
    n = len(Xcov)
    p = len(Xcov[0]) if n > 0 else 0
    cats = sorted(set(y))
    J = len(cats)
    cat_index = {c: i for i, c in enumerate(cats)}
    yy = [cat_index[v] for v in y]  # 0..J-1
    nth = J - 1

    def negloglik(par):
        theta = par[:nth]
        beta = par[nth:]
        # ensure increasing thresholds via penalty
        ll = 0.0
        for i in range(n):
            xb = sum(Xcov[i][j] * beta[j] for j in range(p))
            yi = yy[i]
            # cumulative: P(Y<=j) = sigma(theta_j - xb)
            def cum(j):
                if j < 0:
                    return 0.0
                if j >= nth:
                    return 1.0
                z = theta[j] - xb
                z = max(-35, min(35, z))
                return 1.0 / (1.0 + math.exp(-z))
            pr = cum(yi) - cum(yi - 1)
            if pr < 1e-12:
                pr = 1e-12
            ll += math.log(pr)
        return -ll

    # init thresholds from cumulative proportions, betas=0
    par = []
    cumc = 0
    for j in range(nth):
        cumc += sum(1 for v in yy if v == j)
        frac = cumc / n
        frac = min(max(frac, 1e-3), 1 - 1e-3)
        par.append(math.log(frac / (1 - frac)))
    par += [0.0] * p
    npar = len(par)

    def grad_hess(par):
        eps = 1e-5
        f0 = negloglik(par)
        g = [0.0] * npar
        for i in range(npar):
            pp = par[:]; pp[i] += eps
            pm = par[:]; pm[i] -= eps
            g[i] = (negloglik(pp) - negloglik(pm)) / (2 * eps)
        Hm = [[0.0] * npar for _ in range(npar)]
        for i in range(npar):
            for j in range(i, npar):
                pp = par[:]; pp[i] += eps; pp[j] += eps
                pm = par[:]; pm[i] += eps; pm[j] -= eps
                mp = par[:]; mp[i] -= eps; mp[j] += eps
                mm = par[:]; mm[i] -= eps; mm[j] -= eps
                val = (negloglik(pp) - negloglik(pm) - negloglik(mp) + negloglik(mm)) / (4 * eps * eps)
                Hm[i][j] = val; Hm[j][i] = val
        return g, Hm, f0

    f_old = negloglik(par)
    for _ in range(max_iter):
        g, Hm, f0 = grad_hess(par)
        try:
            step = mat_vec(mat_inv(Hm), g)
        except ValueError:
            break
        lam = 1.0
        improved = False
        for _ls in range(30):
            newpar = [par[i] - lam * step[i] for i in range(npar)]
            th = newpar[:nth]
            if all(th[i] < th[i + 1] for i in range(nth - 1)):
                fn = negloglik(newpar)
                if fn < f0:
                    par = newpar; improved = True; break
            lam *= 0.5
        if not improved:
            break
        if abs(f_old - f0) < tol:
            f_old = f0
            break
        f_old = f0
    # final covariance from Hessian
    g, Hm, f0 = grad_hess(par)
    try:
        cov = mat_inv(Hm)
        se = [math.sqrt(abs(cov[i][i])) for i in range(npar)]
    except ValueError:
        se = [float('nan')] * npar
    beta = par[nth:]
    se_beta = se[nth:]
    z = [beta[j] / se_beta[j] if se_beta[j] > 0 else float('nan') for j in range(p)]
    pv = [2.0 * (1.0 - norm_cdf(abs(zj))) for zj in z]
    OR = [math.exp(b) for b in beta]
    ci = [(math.exp(beta[j] - 1.96 * se_beta[j]), math.exp(beta[j] + 1.96 * se_beta[j])) for j in range(p)]
    ll_model = -f0
    # null model: thresholds only
    def negloglik_null(th):
        ll = 0.0
        for i in range(n):
            yi = yy[i]
            def cum(j):
                if j < 0: return 0.0
                if j >= nth: return 1.0
                z = max(-35, min(35, th[j]))
                return 1.0 / (1.0 + math.exp(-z))
            pr = cum(yi) - cum(yi - 1)
            if pr < 1e-12: pr = 1e-12
            ll += math.log(pr)
        return -ll
    th0 = []
    cumc = 0
    for j in range(nth):
        cumc += sum(1 for v in yy if v == j)
        frac = min(max(cumc / n, 1e-3), 1 - 1e-3)
        th0.append(math.log(frac / (1 - frac)))
    ll_null = -negloglik_null(th0)
    lr_chi2 = 2 * (ll_model - ll_null)
    lr_p = chi2_sf(lr_chi2, p)
    cox = 1 - math.exp(2 * (ll_null - ll_model) / n)
    nagel = cox / (1 - math.exp(2 * ll_null / n))
    return {'names': names, 'beta': beta, 'se': se_beta, 'z': z, 'p': pv, 'OR': OR, 'ci': ci,
            'thresholds': par[:nth], 'll_model': ll_model, 'll_null': ll_null,
            'lr_chi2': lr_chi2, 'lr_p': lr_p, 'nagelkerke': nagel, 'n': n, 'J': J}
