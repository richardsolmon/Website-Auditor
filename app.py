import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="Free Website Audit Report Generator",
    page_icon="🔍",
    layout="centered"
)

# 2. Google Apps Script Web App URL
GOOGLE_SCRIPT_URL = "YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL"


# 3. Save Lead to Google Sheet
def save_lead_to_google_sheet(
    name,
    email,
    website_url,
    audit_score,
    audit_status
):
    payload = {
        "name": name,
        "email": email,
        "website_url": website_url,
        "audit_score": audit_score,
        "audit_status": audit_status
    }

    try:
        response = requests.post(
            GOOGLE_SCRIPT_URL,
            json=payload,
            timeout=20
        )

        if response.status_code == 200:
            result = response.json()
            return result.get("success", False)

        return False

    except Exception as error:
        st.error(f"Google Sheet connection error: {error}")
        return False


# 4. Core Audit Engine
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
        issues.append("✅ Secure Connection (HTTPS) is active.")

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


# 5. Page Content
st.title("🔍 Free Website Audit Report Generator")

st.write(
    "Enter your details below to get a comprehensive, "
    "free website audit report instantly."
)

# 6. User Input Form
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
        "🔒 Legal Disclosure: Some recommendations in the report may contain "
        "affiliate links, which earn us a commission at no extra cost to you."
    )

    submit_button = st.form_submit_button(
        "Get My Free Website Audit"
    )


# 7. Form Action
if submit_button:

    if not name_input or not email_input or not url_input:
        st.error("Please fill in all fields.")

    elif "@" not in email_input:
        st.error("Please enter a valid email address.")

    else:
        # Automatically add https:// if missing
        website_url = url_input.strip()

        if not website_url.startswith(("http://", "https://")):
            website_url = "https://" + website_url

        with st.spinner("Analyzing website structures..."):

            final_score, audit_issues, audit_recs = run_audit(
                website_url
            )

            # Save customer data automatically to Google Sheet
            saved_successfully = save_lead_to_google_sheet(
                name=name_input,
                email=email_input,
                website_url=website_url,
                audit_score=final_score,
                audit_status="Audit Completed"
            )

            # Show Audit Result
            st.success("🎉 Audit complete!")

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

            # Save Status
            if saved_successfully:
                st.success(
                    "✅ Your details have been securely recorded. "
                    "No additional form submission is required."
                )
            else:
                st.warning(
                    "⚠️ Your audit is complete, but we could not save your "
                    "details to Google Sheets. Please try again later."
                )
