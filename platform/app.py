"""Minimal Streamlit landing page for Project Serendib v2."""

from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="Project Serendib v2", page_icon="📚", layout="centered")

st.title("Project Serendib v2")
st.caption("Sovereign Sinhala Data Ecosystem")

st.write("This is a quiet, long-term faculty seed project.")

st.subheader("3 Pillars")
st.markdown(
    """
- **Education & Human Development** (`pillar-education-human-development/`)
- **Economy & Enterprise** (`pillar-economy-enterprise/`)
- **Society & Environment** (`pillar-society-environment/`)
"""
)

st.subheader("Shared Links")
st.markdown(
    """
- Argilla workspace: `shared/argilla/`
- OCR pipeline: `shared/ocr-pipeline/`
- Proposal v2: `PROPOSAL-v2.md`
"""
)

st.info("Start by choosing a pillar folder and contributing within a visible sub-pillar.")
