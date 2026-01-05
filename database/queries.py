"""
SQL Queries
===========
Lead ve Ciro sorguları
"""


# Lead sorgusu - MemberForm tablosundan
LEAD_QUERY = """
SELECT 
    MemberId,
    UtmSource,
    UtmMedium,
    UtmTerm,
    UtmContent,
    CreateDate
FROM MemberPrime..MemberForm
WHERE UtmSource IN ({sources})
  AND BrandId = 1
  AND CreateDate BETWEEN ? AND ?
ORDER BY CreateDate DESC
"""


# Lead sayısı - kaynak ve content bazlı gruplandırma
LEAD_COUNT_BY_SOURCE_CONTENT = """
SELECT 
    UtmSource,
    UtmContent,
    COUNT(DISTINCT MemberId) as LeadCount,
    CAST(MIN(CreateDate) as DATE) as FirstLeadDate,
    CAST(MAX(CreateDate) as DATE) as LastLeadDate
FROM MemberPrime..MemberForm
WHERE UtmSource IN ({sources})
  AND BrandId = 1
  AND CreateDate BETWEEN ? AND ?
GROUP BY UtmSource, UtmContent
ORDER BY LeadCount DESC
"""


# Lead sayısı - günlük trend
LEAD_DAILY_TREND = """
SELECT 
    CAST(CreateDate as DATE) as Date,
    UtmSource,
    COUNT(DISTINCT MemberId) as LeadCount
FROM MemberPrime..MemberForm
WHERE UtmSource IN ({sources})
  AND BrandId = 1
  AND CreateDate BETWEEN ? AND ?
GROUP BY CAST(CreateDate as DATE), UtmSource
ORDER BY Date ASC
"""


# Ciro sorgusu - MemberForm ile Join yaparak UTM verileri ile eşleştirilmiş
REVENUE_QUERY = """
SELECT 
    mf.MemberId,
    mf.UtmSource,
    mf.UtmMedium,
    mf.UtmContent,
    T.StudentName,
    T.StudentNo,
    T.BeginDate,
    P.Title AS Product,
    T.Status,
    T.LessonDuration,
    O.Price,
    O.TotalPrice,
    CONVERT(DECIMAL(10, 2), (O.TotalPrice / 1.1)) as NetPrice,
    O.CreateDate AS OrderDate,
    T.CreateDate AS TermDate
FROM MemberPrime..MemberForm mf
INNER JOIN (
    SELECT MemberId, MAX(CreateDate) as MaxCreateDate
    FROM MemberPrime..MemberForm
    GROUP BY MemberId
) mf_latest ON mf.MemberId = mf_latest.MemberId AND mf.CreateDate = mf_latest.MaxCreateDate
INNER JOIN TERM T ON T.MemberId = mf.MemberId
INNER JOIN MEMBER M ON M.ID = T.MemberId
INNER JOIN EmployeeMember EM ON T.MemberId = EM.MemberId AND EM.Status = 1 AND EM.EmployeeTypeId = 4
INNER JOIN [OrderTermDetail] OTD ON OTD.TermId = T.ID
INNER JOIN [ORDER] O ON O.Id = OTD.OrderId
INNER JOIN Product P ON P.ID = T.ProductId
INNER JOIN Payment PM ON PM.OrderId = OTD.OrderId
WHERE mf.UtmSource IN ({sources})
  AND O.CreateDate BETWEEN ? AND ?
  AND T.SalesType = 1
  AND O.TotalPrice > 0
  AND PM.Status = 1
ORDER BY O.CreateDate DESC
"""


# Ciro özeti - kaynak ve content bazlı
REVENUE_SUMMARY_BY_SOURCE_CONTENT = """
SELECT 
    mf.UtmSource,
    mf.UtmContent,
    COUNT(DISTINCT O.Id) as OrderCount,
    SUM(O.TotalPrice) as TotalRevenue,
    SUM(CONVERT(DECIMAL(10, 2), (O.TotalPrice / 1.1))) as NetRevenue,
    AVG(O.TotalPrice) as AvgOrderValue
FROM MemberPrime..MemberForm mf
INNER JOIN (
    SELECT MemberId, MAX(CreateDate) as MaxCreateDate
    FROM MemberPrime..MemberForm
    GROUP BY MemberId
) mf_latest ON mf.MemberId = mf_latest.MemberId AND mf.CreateDate = mf_latest.MaxCreateDate
INNER JOIN TERM T ON T.MemberId = mf.MemberId
INNER JOIN [OrderTermDetail] OTD ON OTD.TermId = T.ID
INNER JOIN [ORDER] O ON O.Id = OTD.OrderId
INNER JOIN Payment PM ON PM.OrderId = OTD.OrderId
WHERE mf.UtmSource IN ({sources})
  AND O.CreateDate BETWEEN ? AND ?
  AND T.SalesType = 1
  AND O.TotalPrice > 0
  AND PM.Status = 1
GROUP BY mf.UtmSource, mf.UtmContent
ORDER BY TotalRevenue DESC
"""


# Günlük ciro trendi
REVENUE_DAILY_TREND = """
SELECT 
    CAST(O.CreateDate as DATE) as Date,
    mf.UtmSource,
    SUM(O.TotalPrice) as TotalRevenue,
    COUNT(DISTINCT O.Id) as OrderCount
FROM MemberPrime..MemberForm mf
INNER JOIN (
    SELECT MemberId, MAX(CreateDate) as MaxCreateDate
    FROM MemberPrime..MemberForm
    GROUP BY MemberId
) mf_latest ON mf.MemberId = mf_latest.MemberId AND mf.CreateDate = mf_latest.MaxCreateDate
INNER JOIN TERM T ON T.MemberId = mf.MemberId
INNER JOIN [OrderTermDetail] OTD ON OTD.TermId = T.ID
INNER JOIN [ORDER] O ON O.Id = OTD.OrderId
INNER JOIN Payment PM ON PM.OrderId = OTD.OrderId
WHERE mf.UtmSource IN ({sources})
  AND O.CreateDate BETWEEN ? AND ?
  AND T.SalesType = 1
  AND O.TotalPrice > 0
  AND PM.Status = 1
GROUP BY CAST(O.CreateDate as DATE), mf.UtmSource
ORDER BY Date ASC
"""


def format_sources(sources: list) -> str:
    """Source listesini SQL IN clause formatına çevirir"""
    return ", ".join([f"'{s}'" for s in sources])
