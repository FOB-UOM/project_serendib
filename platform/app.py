"""Streamlit landing page for Project Serendib v2."""

from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="Project Serendib v2",
    page_icon="🌱",
    layout="wide",
)

ARGILLA_URL = "https://argilla.example.com/project-serendib-v2"

PILLARS = [
    {
        "name_en": "Education & Human Development",
        "name_si": "අධ්‍යාපන හා මානව සංවර්ධනය",
        "desc_en": "Teacher capacity, learner mindset, and cultural literacy.",
        "desc_si": "ගුරු ශක්තිමත් කිරීම, ඉගෙනුම් මනෝභාවය සහ සංස්කෘතික දැනුම.",
        "subpillars": [
            "teacher-empowerment",
            "philosophy-psychology-personality",
            "art-literature-culture",
        ],
    },
    {
        "name_en": "Economy & Enterprise",
        "name_si": "ආර්ථිකය හා ව්‍යවසාය",
        "desc_en": "SMEs, financial literacy, and policy-aware economic thinking.",
        "desc_si": "කුඩා ව්‍යාපාර, මූල්‍ය දැනුම සහ ප්‍රතිපත්ති සබඳ ආර්ථික සිතුවිලි.",
        "subpillars": [
            "business-sme-bpm",
            "finance-financial-literacy",
            "political-economy",
        ],
    },
    {
        "name_en": "Society & Environment",
        "name_si": "සමාජය හා පරිසරය",
        "desc_en": "Social trust, inclusion, and climate resilience.",
        "desc_si": "සමාජ විශ්වාසය, ඇතුළත්භාවය සහ දේශගුණ තිරසාරභාවය.",
        "subpillars": [
            "sociology-social-dynamics",
            "sustainability-climate",
        ],
    },
]

st.markdown(
    """
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2.5rem;
    max-width: 1100px;
}
.hero {
    background: linear-gradient(135deg, #e8f5e9 0%, #fff8e1 100%);
    border: 1px solid #d7e8d7;
    border-radius: 18px;
    padding: 1.2rem 1.2rem 1rem 1.2rem;
    margin-bottom: 1rem;
}
.card {
    background: #ffffff;
    border: 1px solid #e3e8ef;
    border-radius: 16px;
    padding: 1rem;
    height: 100%;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
}
.card h3 {
    margin-top: 0;
    margin-bottom: 0.2rem;
}
.subpillars {
    margin-top: 0.5rem;
    padding-left: 1rem;
    font-size: 0.94rem;
}
@media (max-width: 768px) {
    .hero { padding: 1rem; }
    .card { margin-bottom: 0.8rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
  <h1 style="margin:0 0 0.3rem 0;">Project Serendib v2</h1>
  <p style="margin:0; font-size:1.02rem;">
    Welcome to the Sinhala-first data ecosystem. <strong>PROPOSAL-v2.md</strong> is the project blueprint.
    <br/>
    සිංහල කේන්ද්‍රීය දත්ත පද්ධතියට සාදරයෙන් පිළිගනිමු. ව්‍යාපෘතියේ මූල සැලැස්ම <strong>PROPOSAL-v2.md</strong> තුළ ඇත.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

col_a, col_b = st.columns([2.2, 1])
with col_a:
    st.subheader("Three Pillars | ප්‍රධාන ස්ථම්භ තුන")
with col_b:
    st.link_button("Contribute Now", ARGILLA_URL, type="primary", use_container_width=True)

cols = st.columns(3)
for index, pillar in enumerate(PILLARS):
    with cols[index]:
        subpillars_html = "".join(f"<li>{item}</li>" for item in pillar["subpillars"])
        st.markdown(
            f"""
<div class="card">
  <h3>{pillar['name_en']}</h3>
  <div style="font-weight:600; margin-bottom:0.4rem;">{pillar['name_si']}</div>
  <div style="font-size:0.94rem;">{pillar['desc_en']}</div>
  <div style="font-size:0.94rem; margin-top:0.2rem;">{pillar['desc_si']}</div>
  <ul class="subpillars">{subpillars_html}</ul>
</div>
""",
            unsafe_allow_html=True,
        )

st.caption(
    "Reference: PROPOSAL-v2.md | Argilla link is a placeholder and can be replaced in platform/app.py"
)
