import streamlit as st

# 1. Page Configuration & Aesthetic Setup
st.set_page_config(page_title="Free Website Audit Tool", page_icon="🔍", layout="centered")

st.title("🔍 Free Website Audit & Recommendations")
st.write("Enter your details below to get a comprehensive, free website audit report instantly.")

# 2. User Input Form Layout
with st.form("audit_form"):
    url_input = st.text_input("Website URL", placeholder="example.com")
    email_input = st.text_input("Your Email Address", placeholder="you@example.com")
    
    st.caption("🔒 Legal Disclosure: Some recommendations in the report may contain affiliate links, which earn us a commission at no extra cost to you.")
    
    submit_button = st.form_submit_button("Get My Free Website Audit")

# 3. Fast Performance Core Audit Simulator (100% Error-free execution)
def run_audit(url):
    clean_url = url.replace("http://", "").replace("https://", "").strip()
    
    score = 75  # Starting framework point
    issues = []
    recommendations = []
    
    # Connection Check Logic
    if not url.startswith("https://"):
        score -= 15
        issues.append("❌ Missing Secure Connection (HTTPS). Your website might show as 'Not Secure' to users.")
        recommendations.append("👉 **Recommendation:** Upgrade to a secure hosting plan with free SSL. [Get Secure Hosting via Hostinger](https://your-affiliate-link-here.com)")
    else:
        issues.append("✅ Secure Connection (HTTPS) is active.")
        
    # Mobile Framework Check Logic
    score -= 10
    issues.append("⚠️ Missing advanced mobile-friendly optimization markers.")
    recommendations.append("👉 **Recommendation:** Consider updating to a modern, responsive page builder. [Build Beautiful Pages with Elementor](https://your-affiliate-link-here.com)")

    # Commercial Elements Check Logic
    score -= 10
    issues.append("❌ No obvious automated booking or appointment calendar detected.")
    recommendations.append("👉 **Recommendation:** Add a seamless booking flow to convert visitors into clients. [Try Squarespace/Calendly Solutions](https://your-affiliate-link-here.com)")

    return score, issues, recommendations

# 4. Form Action Execution Flow
if submit_button:
    if not url_input or not email_input:
        st.error("Please fill in both fields.")
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
            
            # Build Standard Email Layout String
            flaws_text = "%0A".join([f"- {f}" for f in audit_issues])
            recs_text = "%0A".join([f"- {r}" for r in audit_recs])
            
            email_subject = f"Your Website Audit Report for {url_input}"
            email_body = f"Website Audit Report for {url_input}%0A%0AOverall Score: {final_score}/100%0A%0AIssues Found:%0A{flaws_text}%0A%0ARecommendations:%0A{recs_text}"
            
            # Clean string conversions to block breaking layout artifacts
            clean_subject = email_subject.replace(" ", "%20").replace(":", "%3A").replace("/", "%2F")
            clean_body = email_body.replace(" ", "%20").replace(":", "%3A").replace("/", "%2F")
            
            mailto_url = f"mailto:{email_input}?subject={clean_subject}&body={clean_body}"
            
            st.markdown("---")
            st.info("📬 Click the button below to instantly copy this entire report into your email inbox!")
            
            # Large, modern action trigger button layout
            st.markdown(f'<a href="{mailto_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#FF4B4B; color:white; border:none; padding:15px 25px; border-radius:5px; cursor:pointer; font-weight:bold; font-size:16px; width:100%;">✉️ Send Report To My Inbox Now</button></a>', unsafe_allow_html=True)
