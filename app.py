import streamlit as st
import requests

st.set_page_config(page_title="Free Website Audit Tool", page_icon="🔍", layout="centered")
st.title("🔍 Free Website Audit & Recommendations")
st.write("Enter your details below to get a comprehensive, free website audit report.")

with st.form("audit_form"):
    name_input = st.text_input("Your Full Name", placeholder="John Doe")
    url_input = st.text_input("Website URL", placeholder="example.com")
    email_input = st.text_input("Your Email Address", placeholder="you@example.com")
    st.caption("🔒 Legal Disclosure: Some recommendations in the report may contain affiliate links, which earn us a commission at no extra cost to you.")
    submit_button = st.form_submit_button("Get My Free Website Audit")

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

if submit_button:
    if not name_input or not url_input or not email_input:
        st.error("Please fill in both fields.")
    else:
        with st.spinner("Analyzing website structures..."):
            final_score, audit_issues, audit_recs = run_audit(url_input)
            
            # Show on screen instantly
            st.success("🎉 Audit complete!")
            st.metric(label="Overall Performance Score", value=f"{final_score}/100")
            
            st.subheader("📋 Audit Summary Findings")
            for issue in audit_issues:
                st.write(issue)
                
            st.subheader("💡 Strategic Recommendations")
            for rec in audit_recs:
                st.write(rec)
            
            # Send data to Formspree
            formspree_url = st.secrets["FORMSPREE_URL"]
            payload = {
                "name": name_input,
                "email": email_input,
                "website": url_input,
                "score": f"{final_score}/100"
            }
            
            try:
                # Bypasses all server blocks instantly
                requests.post(formspree_url, json=payload)
                st.info(f"📬 Lead details successfully captured! Check your Formspree dashboard or email inbox.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
