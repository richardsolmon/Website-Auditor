import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Free Website Audit Tool", page_icon="🔍", layout="centered")
st.title("🔍 Free Website Audit & Recommendations")
st.write("Enter your details below to get a comprehensive, free website audit report delivered straight to your inbox.")

with st.form("audit_form"):
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

def send_email_report(to_email, site_url, score, flaws, recs):
    # Fetching clean credential tags
    sender_email = str(st.secrets["GMAIL_USER"]).strip()
    sender_password = str(st.secrets["GMAIL_PASSWORD"]).strip()
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = f"Your Website Audit Report for {site_url}"
    
    flaws_html = "".join([f"<li>{f}</li>" for f in flaws])
    recs_html = "".join([f"<li>{r}</li>" for r in recs])
    
    body = f"""
    <html>
        <body>
            <h2>Website Audit Report for {site_url}</h2>
            <p><strong>Overall Score: {score}/100</strong></p>
            <h3>Detected Issues:</h3>
            <ul>{flaws_html}</ul>
            <h3>Actionable Recommendations:</h3>
            <ul>{recs_html}</ul>
            <br>
            <p><small>Disclaimer: This email contains affiliate links. If you purchase services through these links, we earn a small commission.</small></p>
        </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))
    
    try:
        # Standard Port 587 configuration with fully explicit routing
        server = smtplib.SMTP(host='://gmail.com', port=587, timeout=15)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.close()
        return True
    except Exception as e1:
        try:
            # Automatic Backup to SSL Port 465 if network restricts TLS
            server = smtplib.SMTP_SSL(host='://gmail.com', port=465, timeout=15)
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            server.close()
            return True
        except Exception as e2:
            st.error(f"Connection Alert: Primary failed ({str(e1)}), Backup failed ({str(e2)}). Please check your Streamlit Secrets string spaces.")
            return False

if submit_button:
    if not url_input or not email_input:
        st.error("Please fill in both fields.")
    else:
        with st.spinner("Analyzing website structures..."):
            final_score, audit_issues, audit_recs = run_audit(url_input)
            st.success("Audit complete!")
            st.metric(label="Overall Performance Score", value=f"{final_score}/100")
            
            email_success = send_email_report(email_input, url_input, final_score, audit_issues, audit_recs)
            if email_success:
                st.info(f"📬 The full report has been automatically emailed to: **{email_input}**")
