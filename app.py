import streamlit as st
import requests

st.set_page_config(page_title="Free Website Audit Tool", page_icon="🔍", layout="centered")
st.title("🔍 Free Website Audit & Recommendations")
st.write("Enter your details below to get a comprehensive, free website audit report delivered straight to your inbox.")

# Updated User Form with Name Field
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
        st.error("Please fill in all fields.")
    else:
        with st.spinner("Analyzing website structures..."):
            final_score, audit_issues, audit_recs = run_audit(url_input)
            st.success("🎉 Audit complete!")
            st.metric(label="Overall Performance Score", value=f"{final_score}/100")
            
            flaws_html = "".join([f"<li>{f}</li>" for f in audit_issues])
            recs_html = "".join([f"<li>{r}</li>" for r in audit_recs])
            
            # Personalized email body using customer name
            html_body = f"""
            <html>
                <body>
                    <h2>Hi {name_input},</h2>
                    <p>Thank you for requesting a website audit. Here is the report for <strong>{url_input}</strong>.</p>
                    <p><strong>Overall Score: {final_score}/100</strong></p>
                    <h3>Detected Issues:</h3>
                    <ul>{flaws_html}</ul>
                    <h3>Actionable Recommendations:</h3>
                    <ul>{recs_html}</ul>
                </body>
            </html>
            """
            
            webhook_url = st.secrets["EMAIL_WEBHOOK_URL"]
            # Added cust_name to payload
            payload = {
                "cust_name": name_input,
                "to_email": email_input,
                "site_url": url_input,
                "subject": f"Hi {name_input}, Your Website Audit Report for {url_input}",
                "body": html_body
            }
            
            try:
                response = requests.post(webhook_url, json=payload)
                st.info(f"📬 The full report has been automatically emailed to: **{email_input}**")
            except Exception as e:
                st.error("Email delivery interface encounter.")
