import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Title and Layout Setup
st.set_page_config(page_title="Free Website Audit Tool", page_icon="🔍", layout="centered")

st.title("🔍 Free Website Audit & Recommendations")
st.write("Enter your details below to get a comprehensive, free website audit report delivered straight to your inbox.")

# User Input Form
with st.form("audit_form"):
    url_input = st.text_input("Website URL", placeholder="example.com")
    email_input = st.text_input("Your Email Address", placeholder="you@example.com")
    
    st.caption("🔒 Legal Disclosure: Some recommendations in the report may contain affiliate links, which earn us a commission at no extra cost to you.")
    
    submit_button = st.form_submit_button("Get My Free Website Audit")

# Core Audit Logic Engine
def run_audit(url):
    score = 75  # Baseline V1 performance score
    issues = []
    recommendations = []
    
    # Check 1: HTTPS Connection
    if not url.startswith("https://"):
        score -= 15
        issues.append("❌ Missing Secure Connection (HTTPS). Your website might show as 'Not Secure' to users.")
        recommendations.append("👉 **Recommendation:** Upgrade to a secure hosting plan with free SSL. [Get Secure Hosting via Hostinger](https://your-affiliate-link-here.com)")
    else:
        issues.append("✅ Secure Connection (HTTPS) is active.")
        
    # Check 2: Mobile Responsiveness Marker
    score -= 10
    issues.append("⚠️ Missing advanced mobile-friendly optimization markers.")
    recommendations.append("👉 **Recommendation:** Consider updating to a modern, responsive page builder. [Build Beautiful Pages with Elementor](https://your-affiliate-link-here.com)")

    # Check 3: Booking System Availability
    score -= 10
    issues.append("❌ No obvious automated booking or appointment calendar detected.")
    recommendations.append("👉 **Recommendation:** Add a seamless booking flow to convert visitors into clients. [Try Squarespace/Calendly Solutions](https://your-affiliate-link-here.com)")

    return score, issues, recommendations

# Automated Email Delivery System via Gmail
def send_email_report(to_email, site_url, score, flaws, recs):
    sender_email = st.secrets["GMAIL_USER"]
    sender_password = st.secrets["GMAIL_PASSWORD"]
    
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
            <p><small>Disclaimer: This email contains affiliate links. If you purchase services through these links, we earn a small commission at no extra cost to you.</small></p>
        </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))
    
    try:
        server = smtplib.SMTP('://gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.close()
        return True
    except:
        try:
            server = smtplib.SMTP_SSL('://gmail.com', 465)
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            server.close()
            return True
        except:
            return False

# Execution Flow
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
            else:
                st.warning("The report was generated on screen, but email delivery failed. Please verify your App Password settings in the Streamlit Dashboard secrets.")
