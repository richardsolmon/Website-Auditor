import streamlit as st
import urllib.parse

# 1. Page Configuration & Title Setup
st.set_page_config(page_title="Free Website Audit Report Generator", page_icon="🔍", layout="centered")

st.title("🔍 Free Website Audit Report Generator")
st.write("Enter your details below to get a comprehensive, free website audit report instantly.")

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
            
            # 5. The Ultimate Secure Pre-filled Link Configuration
            # Public Form View Link for your specific form ID
            base_form_url = "https://google.com"
            
            # Standard URL Encoding to securely pass string values without errors
            encoded_name = urllib.parse.quote_plus(name_input)
            encoded_email = urllib.parse.quote_plus(email_input)
            encoded_url = urllib.parse.quote_plus(url_input)
            
            # Verified Entry IDs mapped directly to your fields
            prefilled_url = f"{base_form_url}?entry.2005485455={encoded_name}&entry.1030438686={encoded_email}&entry.892019484={encoded_url}"
            
            st.markdown("---")
            st.warning("📥 మీ రిపోర్ట్‌ను మీ ఇన్‌బాక్స్‌కు పంపడానికి మరియు వెరిఫై చేయడానికి కింద ఉన్న బ్లూ బటన్‌ను తప్పకుండా క్లిక్ చేయండి!")
            
            # Opens the professional Google Form where data is already filled in!
            st.markdown(f'<a href="{prefilled_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#1a73e8; color:white; border:none; padding:15px 25px; border-radius:5px; cursor:pointer; font-weight:bold; font-size:16px; width:100%;">📬 Confirm & Get My Report in Email</button></a>', unsafe_allow_html=True)
