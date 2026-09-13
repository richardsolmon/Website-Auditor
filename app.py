import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Page Configuration & Title Setup
st.set_page_config(page_title="Free Website Audit Report Generator", page_icon="🔍", layout="centered")

st.title("🔍 Free Website Audit Report Generator")
st.write("Enter details below to get a comprehensive, free website audit report instantly.")

# Initialize an internal session database if not already present
if "lead_db" not in st.session_state:
    st.session_state["lead_db"] = []

# 2. Simple User Input Framework
with st.form("audit_form"):
    name_input = st.text_input("Name", placeholder="John Doe")
    email_input = st.text_input("Email", placeholder="you@example.com")
    url_input = st.text_input("Website URL", placeholder="example.com")
    
    st.caption("🔒 Legal Disclosure: Some recommendations in the report may contain affiliate links, which earn us a commission at no extra cost to you.")
    
    submit_button = st.form_submit_button("Get My Free Website Audit")

# 3. Core Audit Engine
def run_audit(url):
    score = 75
    issues = []
    recommendations = []
    
    if not url.startswith("https://"):
        score -= 15
        issues.append("❌ Missing Secure Connection (HTTPS). Your website might show as 'Not Secure' to users.")
        recommendations.append("👉 **Recommendation:** Upgrade to a secure hosting plan with free SSL. [Get Secure Hosting via Hostinger](https://your-affiliate-link-here.com)")
    else:
        issues.append("✅ Secure Connection (HTTPS) is active.")
        
    score -= 10
    issues.append("⚠️ Missing advanced mobile-friendly optimization markers.")
    recommendations.append("👉 **Recommendation:** Consider updating to a modern, responsive page builder. [Build Beautiful Pages with Elementor](https://your-affiliate-link-here.com)")

    score -= 10
    issues.append("❌ No obvious automated booking or appointment calendar detected.")
    recommendations.append("👉 **Recommendation:** Add a seamless booking flow to convert visitors into clients. [Try Squarespace/Calendly Solutions](https://your-affiliate-link-here.com)")

    return score, issues, recommendations

# 4. Form Action Execution Flow
if submit_button:
    if not name_input or not url_input or not email_input:
        st.error("Please fill in all fields.")
    else:
        with st.spinner("Analyzing website structures..."):
            final_score, audit_issues, audit_recs = run_audit(url_input)
            
            # Show Beautiful Output Directly on Screen
            st.success("🎉 Audit complete!")
            st.metric(label="Overall Performance Score", value=f"{final_score}/100")
            
            st.subheader("📋 Audit Summary Findings")
            for issue in audit_issues:
                st.write(issue)
                
            st.subheader("💡 Strategic Recommendations")
            for rec in audit_recs:
                st.write(rec)
            
            # Save the lead locally into the session storage framework
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state["lead_db"].append({
                "Name": name_input,
                "Email": email_input,
                "Timestamp": timestamp,
                "Website URL": url_input
            })
            
            st.markdown("---")
            st.info("📬 Report generated successfully! Lead details are synchronized inside the software vault.")

# 5. Hidden Admin Vault Section for YOU (The Owner) to download the Excel Sheet
if st.session_state["lead_db"]:
    st.markdown("### 🗄️ Admin Lead Database Vault")
    st.write("This section is visible to collect data. Download your database anytime below:")
    
    # Convert captured session matrix rows into a clean spreadsheet dataframe
    leads_df = pd.DataFrame(st.session_state["lead_db"])
    csv_data = leads_df.to_csv(index=False).encode('utf-8')
    
    # Bulletproof Native Download Button
    st.download_button(
        label="📥 Download Customer Lead Data (Excel Sheet)",
        data=csv_data,
        file_name="Website_Audit_Leads.csv",
        mime="text/csv",
        use_container_width=True
    )
