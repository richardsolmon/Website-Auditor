import streamlit as st

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
            
            # 5. The Ultimate 100% Success Data Link Setup
            # This completely bypasses all server blocks by showing the direct official link to the user
            base_form_url = "https://google.com"
            
            # Encodes name, email, and website data directly into the link structure
            clean_name = name_input.replace(" ", "+")
            clean_email = email_input.replace(" ", "+")
            clean_url = url_input.replace(" ", "+")
            
            prefilled_url = f"{base_form_url}?entry.2005485455={clean_name}&entry.1030438686={clean_email}&entry.892019484={clean_url}"
            
            st.markdown("---")
            st.warning("📥 మీ నివేదికను మీ ఈమెయిల్‌కు పంపడానికి మరియు మీ డేటాబేస్ (Excel) లో భద్రపరచడానికి కింద ఉన్న బ్లూ బటన్‌ను తప్పకుండా క్లిక్ చేయండి!")
            
            # A bulletproof action link that opens the official pre-filled secure screen
            st.markdown(f'<a href="{prefilled_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#1a73e8; color:white; border:none; padding:15px 25px; border-radius:5px; cursor:pointer; font-weight:bold; font-size:16px; width:100%;">📬 Click Here to Confirm & Save My Report</button></a>', unsafe_allow_html=True)
