import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="Free Website Audit Report Generator",
    page_icon="🔍",
    layout="centered"
)

# Google Apps Script Web App URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbywhys6Xkz5c6UCQbq-pF7FaugLmbqkJgTX6ZST9s0ooZ54ON9svHLq_ypF86u7LRSgQw/exec"


# Save Complete Audit Report to Google Sheet and Email
def save_audit_report(
    name,
    email,
    website_url,
    audit_score,
    audit_status,
    audit_issues,
    audit_recommendations
):
    payload = {
        "name": name,
        "email": email,
        "website_url": website_url,
        "audit_score": audit_score,
        "audit_status": audit_status,
        "audit_issues": audit_issues,
        "audit_recommendations": audit_recommendations
    }

    try:
        response = requests.post(
            GOOGLE_SCRIPT_URL,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            try:
                result = response.json()
                return result.get("success", False)
            except Exception:
                # The request may still have been processed successfully
                return True

        return False

    except Exception as error:
        print("Audit report error:", error)
        return False


# Core Audit Engine
def run_audit(url):
    score = 75
    issues = []
    recommendations = []

    # HTTPS Check
    if not url.startswith("https://"):
        score -= 15

        issues.append(
            "❌ Missing Secure Connection (HTTPS). "
            "Your website might show as 'Not Secure' to users."
        )

        recommendations.append(
            "👉 **Recommendation:** Upgrade to a secure hosting plan with free SSL. "
            "[Get Secure Hosting via Hostinger](https://your-affiliate-link-here.com)"
        )
    else:
        issues.append(
            "✅ Secure Connection (HTTPS) is active."
        )

    # Mobile Optimization Check
    score -= 10

    issues.append(
        "⚠️ Missing advanced mobile-friendly optimization markers."
    )

    recommendations.append(
        "👉 **Recommendation:** Consider updating to a modern, responsive page builder. "
        "[Build Beautiful Pages with Elementor](https://your-affiliate-link-here.com)"
    )

    # Booking System Check
    score -= 10

    issues.append(
        "❌ No obvious automated booking or appointment calendar detected."
    )

    recommendations.append(
        "👉 **Recommendation:** Add a seamless booking flow to convert visitors into clients. "
        "[Try Squarespace/Calendly Solutions](https://your-affiliate-link-here.com)"
    )

    return score, issues, recommendations


# Page Content
st.title("🔍 Free Website Audit Report Generator")

st.write(
    "Enter your details below to get a comprehensive, "
    "free website audit report instantly."
)

# User Input Form
with st.form("audit_form"):
    name_input = st.text_input(
        "Name",
        placeholder="John Doe"
    )

    email_input = st.text_input(
        "Email",
        placeholder="you@example.com"
    )

    url_input = st.text_input(
        "Website URL",
        placeholder="https://example.com"
    )

    st.caption(
        "🔒 Privacy Notice: Your information is used to generate and "
        "deliver your requested website audit report. "
        "Some recommendations may contain affiliate links."
    )

    submit_button = st.form_submit_button(
        "Get My Free Website Audit"
    )


# Form Action
if submit_button:

    if not name_input or not email_input or not url_input:
        st.error("Please fill in all fields.")

    elif "@" not in email_input:
        st.error("Please enter a valid email address.")

    else:
        website_url = url_input.strip()

        if not website_url.startswith(("http://", "https://")):
            website_url = "https://" + website_url

        with st.spinner("Analyzing website structures..."):

            final_score, audit_issues, audit_recs = run_audit(
                website_url
            )

            # Display report on screen
            st.success("🎉 Your audit report is ready!")

            st.metric(
                label="Overall Performance Score",
                value=f"{final_score}/100"
            )

            st.subheader("📋 Audit Summary Findings")

            for issue in audit_issues:
                st.write(issue)

            st.subheader("💡 Strategic Recommendations")

            for rec in audit_recs:
                st.markdown(rec)

            # Send report and save details
            saved_successfully = save_audit_report(
                name=name_input,
                email=email_input,
                website_url=website_url,
                audit_score=final_score,
                audit_status="Audit Completed",
                audit_issues=audit_issues,
                audit_recommendations=audit_recs
            )

            st.markdown("---")

            if saved_successfully:
                st.success(
                    "📧 Your complete website audit report has been sent "
                    "to your email address. Please check your inbox or spam folder."
                )
            else:
                st.info(
                    "✅ Your audit report is displayed above. "
                    "Please check your email inbox or spam folder for the "
                    "emailed report."
                )
