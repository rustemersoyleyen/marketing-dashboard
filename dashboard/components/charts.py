"""
Chart Components
================
Grafik bileşenleri
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config.database import UTM_SOURCE_MAPPING


# Renk paleti
COLORS = {
    "google": "#4285F4",  # Google Blue
    "facebook": "#1877F2",  # Facebook Blue
    "apple": "#000000",  # Apple Black
    "revenue": "#28a745",  # Green
    "spend": "#dc3545",  # Red
    "leads": "#17a2b8"  # Cyan
}


def render_spend_vs_revenue_chart(metrics_by_source: dict):
    """
    Platform bazlı harcama vs ciro karşılaştırma grafiği
    """
    st.subheader("💰 Harcama vs Ciro Karşılaştırması")
    
    data = []
    for source, metrics in metrics_by_source.items():
        display_name = UTM_SOURCE_MAPPING.get(source, source)
        data.append({
            "Platform": display_name,
            "Harcama": metrics["spend"],
            "Ciro": metrics["revenue"],
            "source": source
        })
    
    df = pd.DataFrame(data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name="Harcama",
        x=df["Platform"],
        y=df["Harcama"],
        marker_color=COLORS["spend"],
        text=df["Harcama"].apply(lambda x: f"₺{x:,.0f}"),
        textposition="auto"
    ))
    
    fig.add_trace(go.Bar(
        name="Ciro",
        x=df["Platform"],
        y=df["Ciro"],
        marker_color=COLORS["revenue"],
        text=df["Ciro"].apply(lambda x: f"₺{x:,.0f}"),
        textposition="auto"
    ))
    
    fig.update_layout(
        barmode="group",
        xaxis_title="Platform",
        yaxis_title="Tutar (₺)",
        legend_title="Metrik",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_platform_pie_chart(metrics_by_source: dict, metric: str = "spend"):
    """
    Platform dağılımı pasta grafiği
    
    Args:
        metrics_by_source: Platform metrikleri
        metric: "spend", "leads", veya "revenue"
    """
    metric_labels = {
        "spend": "Harcama Dağılımı",
        "leads": "Lead Dağılımı",
        "revenue": "Ciro Dağılımı"
    }
    
    st.subheader(f"📊 {metric_labels.get(metric, 'Dağılım')}")
    
    data = []
    colors = []
    
    for source, metrics in metrics_by_source.items():
        display_name = UTM_SOURCE_MAPPING.get(source, source)
        value = metrics.get(metric, 0)
        if value > 0:
            data.append({
                "Platform": display_name,
                "Değer": value
            })
            colors.append(COLORS.get(source, "#666666"))
    
    if not data:
        st.info("📭 Gösterilecek veri yok")
        return
    
    df = pd.DataFrame(data)
    
    fig = px.pie(
        df,
        values="Değer",
        names="Platform",
        color_discrete_sequence=colors,
        hole=0.4
    )
    
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(height=350)
    
    st.plotly_chart(fig, use_container_width=True)


def render_daily_trend_chart(daily_data: pd.DataFrame, metric: str = "spend"):
    """
    Günlük trend çizgi grafiği
    
    Args:
        daily_data: DataFrame with date, source, and metric columns
        metric: "spend", "leads", "revenue"
    """
    metric_labels = {
        "spend": "Günlük Harcama Trendi",
        "LeadCount": "Günlük Lead Trendi",
        "TotalRevenue": "Günlük Ciro Trendi"
    }
    
    st.subheader(f"📈 {metric_labels.get(metric, 'Trend')}")
    
    if daily_data.empty:
        st.info("📭 Trend verisi bulunamadı")
        return
    
    # Tarih sütununu düzenle
    date_col = "date" if "date" in daily_data.columns else "Date"
    source_col = "source" if "source" in daily_data.columns else "UtmSource"
    
    if date_col not in daily_data.columns:
        st.error("Tarih sütunu bulunamadı")
        return
    
    # Source isimlerini güncelle
    daily_data = daily_data.copy()
    daily_data["Platform"] = daily_data[source_col].map(
        lambda x: UTM_SOURCE_MAPPING.get(x, x)
    )
    
    fig = px.line(
        daily_data,
        x=date_col,
        y=metric,
        color="Platform",
        markers=True,
        color_discrete_map={
            "Google Ads": COLORS["google"],
            "Facebook Ads": COLORS["facebook"],
            "Apple Ads": COLORS["apple"]
        }
    )
    
    fig.update_layout(
        xaxis_title="Tarih",
        yaxis_title="Değer",
        legend_title="Platform",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_content_performance_table(content_metrics: list):
    """
    UTM Content bazlı performans tablosu
    """
    st.subheader("📋 Kampanya/Content Performansı")
    
    if not content_metrics:
        st.info("📭 Kampanya verisi bulunamadı")
        return
    
    df = pd.DataFrame(content_metrics)
    
    # Sütun isimlerini Türkçeleştir
    df = df.rename(columns={
        "source": "Platform",
        "content": "Kampanya/Content",
        "spend": "Harcama (₺)",
        "leads": "Lead",
        "revenue": "Ciro (₺)",
        "cpa": "CPA (₺)",
        "roas": "ROAS"
    })
    
    # Platform isimlerini güncelle
    df["Platform"] = df["Platform"].map(lambda x: UTM_SOURCE_MAPPING.get(x, x))
    
    # Formatla
    df["Harcama (₺)"] = df["Harcama (₺)"].apply(lambda x: f"₺{x:,.0f}")
    df["Ciro (₺)"] = df["Ciro (₺)"].apply(lambda x: f"₺{x:,.0f}")
    df["CPA (₺)"] = df["CPA (₺)"].apply(lambda x: f"₺{x:,.0f}")
    df["ROAS"] = df["ROAS"].apply(lambda x: f"{x:.2f}x")
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


def render_roas_comparison_chart(metrics_by_source: dict):
    """
    Platform bazlı ROAS karşılaştırma grafiği
    """
    st.subheader("📊 ROAS Karşılaştırması")
    
    data = []
    colors = []
    
    for source, metrics in metrics_by_source.items():
        display_name = UTM_SOURCE_MAPPING.get(source, source)
        data.append({
            "Platform": display_name,
            "ROAS": metrics["roas"]
        })
        colors.append(COLORS.get(source, "#666666"))
    
    df = pd.DataFrame(data)
    
    fig = px.bar(
        df,
        x="Platform",
        y="ROAS",
        color="Platform",
        color_discrete_sequence=colors,
        text=df["ROAS"].apply(lambda x: f"{x:.2f}x")
    )
    
    # Breakeven çizgisi (ROAS = 1)
    fig.add_hline(
        y=1,
        line_dash="dash",
        line_color="red",
        annotation_text="Breakeven (1x)"
    )
    
    fig.update_traces(textposition="outside")
    fig.update_layout(
        showlegend=False,
        yaxis_title="ROAS",
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)
