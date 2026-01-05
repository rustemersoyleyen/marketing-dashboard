"""
Metrics Service
===============
CPA, ROAS ve diğer metrikleri hesaplar
"""

from datetime import date
from services.lead_service import get_total_leads, get_leads_by_source, get_lead_count_by_source_content
from services.revenue_service import get_total_revenue, get_revenue_by_source, get_revenue_summary_by_source_content
from services.ad_spend_service import get_total_spend, get_spend_by_source, get_spend_by_content
from config.database import SUPPORTED_PLATFORMS


def calculate_overall_metrics(start_date: date, end_date: date) -> dict:
    """
    Genel performans metriklerini hesaplar
    
    Returns:
        dict: {
            total_spend, total_leads, total_revenue,
            cpa, roas, conversion_rate
        }
    """
    total_spend = float(get_total_spend(start_date, end_date) or 0)
    total_leads = int(get_total_leads(start_date, end_date) or 0)
    total_revenue = float(get_total_revenue(start_date, end_date) or 0)
    
    # CPA (Cost per Acquisition/Lead)
    cpa = total_spend / total_leads if total_leads > 0 else 0
    
    # ROAS (Return on Ad Spend)
    roas = total_revenue / total_spend if total_spend > 0 else 0
    
    # Conversion rate (estimate based on leads)
    # Not: Gerçek dönüşüm için satış/lead oranı kullanılabilir
    
    return {
        "total_spend": round(float(total_spend), 2),
        "total_leads": total_leads,
        "total_revenue": round(float(total_revenue), 2),
        "cpa": round(float(cpa), 2),
        "roas": round(float(roas), 2),
        "roas_percentage": round(float(roas) * 100, 1)
    }


def calculate_metrics_by_source(start_date: date, end_date: date) -> dict:
    """
    Platform bazlı metrikleri hesaplar
    
    Returns:
        dict: {
            "google": {spend, leads, revenue, cpa, roas},
            "facebook": {spend, leads, revenue, cpa, roas}
        }
    """
    spend_by_source = get_spend_by_source(start_date, end_date)
    leads_by_source = get_leads_by_source(start_date, end_date)
    revenue_by_source = get_revenue_by_source(start_date, end_date)
    
    metrics = {}
    
    for source in SUPPORTED_PLATFORMS:
        spend = float(spend_by_source.get(source, 0) or 0)
        leads = int(leads_by_source.get(source, 0) or 0)
        revenue = float(revenue_by_source.get(source, 0) or 0)
        
        cpa = spend / leads if leads > 0 else 0
        roas = revenue / spend if spend > 0 else 0
        
        metrics[source] = {
            "spend": round(float(spend), 2),
            "leads": leads,
            "revenue": round(float(revenue), 2),
            "cpa": round(float(cpa), 2),
            "roas": round(float(roas), 2),
            "roas_percentage": round(float(roas) * 100, 1)
        }
    
    return metrics


def calculate_metrics_by_content(start_date: date, end_date: date) -> list:
    """
    UTM Content bazlı metrikleri hesaplar
    
    Returns:
        list: [{source, content, spend, leads, revenue, cpa, roas}, ...]
    """
    spend_df = get_spend_by_content(start_date, end_date)
    leads_df = get_lead_count_by_source_content(start_date, end_date)
    revenue_df = get_revenue_summary_by_source_content(start_date, end_date)
    
    if spend_df.empty:
        return []
    
    # Veriyi birleştir
    results = []
    
    for _, row in spend_df.iterrows():
        source = row["source"]
        content = row["utm_content"]
        spend = float(row["spend"] or 0)
        
        # Lead sayısı
        lead_match = leads_df[
            (leads_df["UtmSource"] == source) & 
            (leads_df["UtmContent"] == content)
        ]
        leads = int(lead_match["LeadCount"].sum()) if not lead_match.empty else 0
        
        # Ciro
        revenue_match = revenue_df[
            (revenue_df["UtmSource"] == source) & 
            (revenue_df["UtmContent"] == content)
        ]
        revenue = float(revenue_match["TotalRevenue"].sum()) if not revenue_match.empty else 0
        
        cpa = spend / leads if leads > 0 else 0
        roas = revenue / spend if spend > 0 else 0
        
        results.append({
            "source": source,
            "content": content,
            "spend": round(float(spend), 2),
            "leads": leads,
            "revenue": round(float(revenue), 2),
            "cpa": round(float(cpa), 2),
            "roas": round(float(roas), 2)
        })
    
    # ROAS'a göre sırala
    return sorted(results, key=lambda x: x["roas"], reverse=True)


def get_dashboard_summary(start_date: date, end_date: date) -> dict:
    """
    Dashboard için özet veriler döner
    
    Returns:
        dict: {
            overall: {...},
            by_source: {...},
            by_content: [...]
        }
    """
    return {
        "overall": calculate_overall_metrics(start_date, end_date),
        "by_source": calculate_metrics_by_source(start_date, end_date),
        "by_content": calculate_metrics_by_content(start_date, end_date)
    }


def format_currency(value: float) -> str:
    """Para birimini formatlar"""
    return f"₺{value:,.2f}"


def format_percentage(value: float) -> str:
    """Yüzdeyi formatlar"""
    return f"%{value:.1f}"
