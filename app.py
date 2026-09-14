import streamlit as st
import requests
import time

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Free Website Audit Report Generator",
    page_icon="🔍",
    layout="centered"
)


# --------------------------------------------------
# Google Apps Script Web App URL
# --------------------------------------------------

GOOGLE_SCRIPT_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbywhys6Xkz5c6UCQbq-pF7FaugLmbqKjGTX6ZST9s0ooZ54ON9svHLq_ypF86u7LRSgQw"
    "/exec"
)


# --------------------------------------------------
# Utility Functions
# --------------------------------------------------

def normalize_url(url):
    """
    Add HTTPS if the user does not provide a protocol.
    """

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def is_valid_url(url):
    """
    Basic URL validation.
    """

    try:
        parsed = urlparse(url)

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
            and "." in parsed.netloc
        )

    except Exception:
        return False


def safe_text(value):
    """
    Convert empty or missing values into readable text.
    """

    if value is None:
        return ""

    return value.strip()


# --------------------------------------------------
# Real Website Audit Engine
# --------------------------------------------------

def run_audit(url):
    """
    Fetch the website and perform basic real HTML audits.
    """

    issues = []
    recommendations = []
    passed_checks = []

    score = 100
    audit_data = {}

    # ----------------------------------------------
    # URL Validation
    # ----------------------------------------------

    if not is_valid_url(url):
        return {
            "score": 0,
            "status": "Invalid URL",
            "issues": ["❌ The website URL is invalid."],
            "recommendations": [
                "👉 Enter a valid website URL such as https://example.com."
            ],
            "passed_checks": [],
            "audit_data": {}
        }

    # ----------------------------------------------
    # Fetch Website
    # ----------------------------------------------

    try:
        start_time = time.time()

        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (compatible; "
                    "WebsiteAuditBot/1.0; +https://example.com)"
                )
            },
            allow_redirects=True
        )

        response_time = round(time.time() - start_time, 2)

        final_url = response.url
        status_code = response.status_code
        page_size_kb = round(len(response.content) / 1024, 2)

        audit_data["Final URL"] = final_url
        audit_data["HTTP Status"] = status_code
        audit_data["Response Time"] = f"{response_time} seconds"
        audit_data["Page Size"] = f"{page_size_kb} KB"

    except requests.exceptions.Timeout:
        return {
            "score": 0,
            "status": "Timeout",
            "issues": [
                "❌ The website took too long to respond."
            ],
            "recommendations": [
                "👉 Check your hosting server, DNS settings, "
                "and website performance."
            ],
            "passed_checks": [],
            "audit_data": {}
        }

    except requests.exceptions.RequestException as error:
        return {
            "score": 0,
            "status": "Website Unreachable",
            "issues": [
                "❌ The website could not be reached successfully."
            ],
            "recommendations": [
                "👉 Confirm that the website is online and that "
                "the URL is correct."
            ],
            "passed_checks": [],
            "audit_data": {
                "Error": str(error)
            }
        }

    # ----------------------------------------------
    # HTTP Status Check
    # ----------------------------------------------

    if status_code == 200:
        passed_checks.append(
            "✅ Website is reachable and returned HTTP status 200."
        )
    elif 200 <= status_code < 400:
        score -= 5
        issues.append(
            f"⚠️ Website returned HTTP status {status_code}."
        )
        recommendations.append(
            "👉 Check redirects and confirm that the main page "
            "loads correctly."
        )
    else:
        score -= 20
        issues.append(
            f"❌ Website returned an error status: {status_code}."
        )
        recommendations.append(
            "👉 Check server configuration, hosting, DNS, "
            "and website availability."
        )

    # ----------------------------------------------
    # HTTPS Check
    # ----------------------------------------------

    parsed_url = urlparse(final_url)

    if parsed_url.scheme == "https":
        passed_checks.append(
            "✅ Secure HTTPS connection is active."
        )
    else:
        score -= 15
        issues.append(
            "❌ HTTPS is not active on the final website URL."
        )
        recommendations.append(
            "👉 Enable an SSL certificate and redirect HTTP traffic "
            "to HTTPS."
        )

    # ----------------------------------------------
    # Response Time Check
    # ----------------------------------------------

    if response_time <= 2:
        passed_checks.append(
            f"✅ Server response time is good: {response_time} seconds."
        )
    elif response_time <= 4:
        score -= 5
        issues.append(
            f"⚠️ Server response time is somewhat slow: "
            f"{response_time} seconds."
        )
        recommendations.append(
            "👉 Review hosting performance, caching, image sizes, "
            "and third-party scripts."
        )
    else:
        score -= 10
        issues.append(
            f"❌ Server response time is slow: {response_time} seconds."
        )
        recommendations.append(
            "👉 Consider improving hosting performance, enabling caching, "
            "and reducing heavy resources."
        )

    # ----------------------------------------------
    # Parse HTML
    # ----------------------------------------------

    soup = BeautifulSoup(response.text, "html.parser")

    # ----------------------------------------------
    # Page Title Check
    # ----------------------------------------------

    title_tag = soup.find("title")
    title = safe_text(title_tag.get_text()) if title_tag else ""

    audit_data["Page Title"] = title if title else "Not found"

    if not title:
        score -= 10
        issues.append(
            "❌ The page is missing a title tag."
        )
        recommendations.append(
            "👉 Add a unique, descriptive title tag that explains "
            "the page topic and includes the primary keyword naturally."
        )
    else:
        title_length = len(title)
        audit_data["Title Length"] = f"{title_length} characters"

        if 30 <= title_length <= 60:
            passed_checks.append(
                "✅ Page title exists and has a reasonable length."
            )
        elif title_length < 30:
            score -= 4
            issues.append(
                f"⚠️ Page title is short ({title_length} characters)."
            )
            recommendations.append(
                "👉 Make the title more descriptive while keeping it "
                "clear and relevant."
            )
        else:
            score -= 4
            issues.append(
                f"⚠️ Page title may be too long ({title_length} characters)."
            )
            recommendations.append(
                "👉 Shorten the title so the main topic is clear "
                "in search results."
            )

    # ----------------------------------------------
    # Meta Description Check
    # ----------------------------------------------

    meta_description_tag = soup.find(
        "meta",
        attrs={"name": lambda value: value and value.lower() == "description"}
    )

    meta_description = ""

    if meta_description_tag:
        meta_description = safe_text(
            meta_description_tag.get("content", "")
        )

    audit_data["Meta Description"] = (
        meta_description if meta_description else "Not found"
    )

    if not meta_description:
        score -= 8
        issues.append(
            "❌ Meta description is missing."
        )
        recommendations.append(
            "👉 Add a unique meta description that summarizes the page "
            "and encourages users to click."
        )
    else:
        meta_length = len(meta_description)
        audit_data["Meta Description Length"] = (
            f"{meta_length} characters"
        )

        if 70 <= meta_length <= 160:
            passed_checks.append(
                "✅ Meta description exists and has a reasonable length."
            )
        else:
            score -= 3
            issues.append(
                f"⚠️ Meta description length may need improvement "
                f"({meta_length} characters)."
            )
            recommendations.append(
                "👉 Rewrite the meta description to be concise, useful, "
                "and relevant to the page."
            )

    # ----------------------------------------------
    # H1 Check
    # ----------------------------------------------

    h1_tags = soup.find_all("h1")
    h1_count = len(h1_tags)

    audit_data["H1 Count"] = h1_count

    if h1_count == 0:
        score -= 8
        issues.append(
            "❌ No H1 heading was detected."
        )
        recommendations.append(
            "👉 Add one clear H1 heading that describes the main topic "
            "of the page."
        )
    elif h1_count == 1:
        passed_checks.append(
            "✅ One H1 heading was detected."
        )
    else:
        score -= 4
        issues.append(
            f"⚠️ Multiple H1 headings were detected ({h1_count})."
        )
        recommendations.append(
            "👉 Review the heading structure and use one primary H1 "
            "for the main page topic where appropriate."
        )

    # ----------------------------------------------
    # H2 and H3 Check
    # ----------------------------------------------

    h2_count = len(soup.find_all("h2"))
    h3_count = len(soup.find_all("h3"))

    audit_data["H2 Count"] = h2_count
    audit_data["H3 Count"] = h3_count

    if h2_count > 0:
        passed_checks.append(
            f"✅ Heading structure includes {h2_count} H2 heading(s)."
        )
    else:
        score -= 3
        issues.append(
            "⚠️ No H2 headings were detected."
        )
        recommendations.append(
            "👉 Use H2 headings to organize important sections "
            "and improve content readability."

        )

    # ----------------------------------------------
    # Image Alt Text Check
    # ----------------------------------------------

    images = soup.find_all("img")
    images_without_alt = []

    for image in images:
        alt_value = image.get("alt")

        if alt_value is None or not alt_value.strip():
            images_without_alt.append(image)

    total_images = len(images)
    missing_alt_count = len(images_without_alt)

    audit_data["Total Images"] = total_images
    audit_data["Images Missing Alt Text"] = missing_alt_count

    if total_images == 0:
        passed_checks.append(
            "✅ No images were detected on the page."
        )
    elif missing_alt_count == 0:
        passed_checks.append(
            "✅ All detected images have alt attributes."
        )
    else:
        score -= min(8, missing_alt_count * 2)
        issues.append(
            f"⚠️ {missing_alt_count} of {total_images} image(s) "
            "are missing alt text."
        )
        recommendations.append(
            "👉 Add meaningful alt text to informative images. "
            "Use empty alt text for purely decorative images."
        )

    # ----------------------------------------------
    # Mobile Viewport Check
    # ----------------------------------------------

    viewport_tag = soup.find(
        "meta",
        attrs={"name": lambda value: value and value.lower() == "viewport"}
    )

    if viewport_tag:
        passed_checks.append(
            "✅ Mobile viewport meta tag is present."
        )
    else:
        score -= 8
        issues.append(
            "❌ Mobile viewport meta tag is missing."
        )
        recommendations.append(
            "👉 Add a responsive viewport tag and verify the website "
            "on mobile devices."
        )

    # ----------------------------------------------
    # Canonical Tag Check
    # ----------------------------------------------

    canonical_tag = soup.find(
        "link",
        attrs={"rel": lambda value: value and "canonical" in value}
    )

    if canonical_tag and canonical_tag.get("href"):
        audit_data["Canonical URL"] = canonical_tag.get("href")
        passed_checks.append(
            "✅ Canonical tag is present."
        )
    else:
        audit_data["Canonical URL"] = "Not found"
        score -= 4
        issues.append(
            "⚠️ Canonical tag was not detected."
        )
        recommendations.append(
            "👉 Consider adding a correct canonical URL, especially "
            "for pages that may have duplicate URL versions."
        )

    # ----------------------------------------------
    # Robots Meta Check
    # ----------------------------------------------

    robots_tag = soup.find(
        "meta",
        attrs={"name": lambda value: value and value.lower() == "robots"}
    )

    robots_content = ""

    if robots_tag:
        robots_content = safe_text(
            robots_tag.get("content", "")
        ).lower()

    audit_data["Robots Meta"] = (
        robots_content if robots_content else "Not found"
    )

    if "noindex" in robots_content:
        score -= 10
        issues.append(
            "❌ A noindex directive was detected on this page."
        )
        recommendations.append(
            "👉 If this page should appear in search engines, "
            "review and remove the noindex directive."
        )
    else:
        passed_checks.append(
            "✅ No noindex directive was detected in the robots meta tag."
        )

    # ----------------------------------------------
    # Language Attribute Check
    # ----------------------------------------------

    html_tag = soup.find("html")
    language_value = ""

    if html_tag:
        language_value = safe_text(html_tag.get("lang", ""))

    audit_data["HTML Language"] = (
        language_value if language_value else "Not found"
    )

    if language_value:
        passed_checks.append(
            f"✅ HTML language attribute is present: {language_value}."
        )
    else:
        score -= 2
        issues.append(
            "⚠️ HTML language attribute was not detected."
        )
        recommendations.append(
            "👉 Add an appropriate lang attribute to the HTML element, "
            "such as lang=\"en\"."
        )

    # ----------------------------------------------
    # Open Graph Check
    # ----------------------------------------------

    og_title = soup.find(
        "meta",
        attrs={"property": "og:title"}
    )

    og_description = soup.find(
        "meta",
        attrs={"property": "og:description"}
    )

    og_image = soup.find(
        "meta",
        attrs={"property": "og:image"}
    )

    og_count = sum(
        1 for item in [og_title, og_description, og_image]
        if item is not None
    )

    audit_data["Open Graph Tags Found"] = og_count

    if og_count == 3:
        passed_checks.append(
            "✅ Essential Open Graph tags were detected."
        )
    else:
        score -= 3
        issues.append(
            "⚠️ Some essential Open Graph tags are missing."
        )
        recommendations.append(
            "👉 Add og:title, og:description, and og:image "
            "to improve social sharing previews."
        )

    # ----------------------------------------------
    # Basic Link Check
    # ----------------------------------------------

    links = soup.find_all("a", href=True)
    internal_links = 0
    external_links = 0

    base_domain = urlparse(final_url).netloc.lower()

    for link in links:
        href = link.get("href", "").strip()

        if not href:
            continue

        absolute_link = urljoin(final_url, href)
        link_domain = urlparse(absolute_link).netloc.lower()

        if link_domain == base_domain:
            internal_links += 1
        elif link_domain:
            external_links += 1

    audit_data["Internal Links"] = internal_links
    audit_data["External Links"] = external_links

    if internal_links > 0:
        passed_checks.append(
            f"✅ {internal_links} internal link(s) detected."
        )
    else:
        score -= 3
        issues.append(
            "⚠️ No internal links were detected on the page."
        )
        recommendations.append(
            "👉 Add relevant internal links to help users and search "
            "engines discover important pages."
        )

    # ----------------------------------------------
    # Basic Score Cleanup
    # ----------------------------------------------

    score = max(0, min(100, score))

    if score >= 85:
        audit_status = "Excellent"
    elif score >= 70:
        audit_status = "Good"
    elif score >= 50:
        audit_status = "Needs Improvement"
    else:
        audit_status = "Critical Improvements Needed"

    # If no issues were found
    if not issues:
        issues.append(
            "🎉 No major issues were detected in this basic audit."
        )

    if not recommendations:
        recommendations.append(
            "👉 Continue monitoring your website regularly "
            "and keep its content and technical setup updated."
        )

    return {
        "score": score,
        "status": audit_status,
        "issues": issues,
        "recommendations": recommendations,
        "passed_checks": passed_checks,
        "audit_data": audit_data
    }


# --------------------------------------------------
# Save Audit Report to Google Sheet and Email
# --------------------------------------------------

def save_audit_report(
    name,
    email,
    website_url,
    audit_score,
    audit_status,
    audit_issues,
    audit_recommendations
):
    """
    Send the audit report to Google Apps Script.
    """

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
                return True

        return False

    except Exception as error:
        print("Audit report error:", error)
        return False


# --------------------------------------------------
# Page Content
# --------------------------------------------------

st.title("🔍 Free Website Audit Report Generator")

st.write(
    "Enter your details below to receive a basic technical SEO "
    "and website health audit."
)

st.info(
    "This automated audit checks publicly accessible website HTML. "
    "It does not replace a complete manual SEO, security, or performance audit."
)


# --------------------------------------------------
# User Input Form
# --------------------------------------------------

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


# --------------------------------------------------
# Form Action
# --------------------------------------------------

if submit_button:

    if not name_input or not email_input or not url_input:
        st.error("Please fill in all fields.")

    elif "@" not in email_input or "." not in email_input:
        st.error("Please enter a valid email address.")

    else:

        website_url = normalize_url(url_input)

        if not is_valid_url(website_url):
            st.error(
                "Please enter a valid website URL, such as "
                "https://example.com"
            )

        else:

            with st.spinner(
                "Analyzing the website's technical structure..."
            ):

                audit_result = run_audit(website_url)

            final_score = audit_result["score"]
            audit_status = audit_result["status"]
            audit_issues = audit_result["issues"]
            audit_recs = audit_result["recommendations"]
            passed_checks = audit_result["passed_checks"]
            audit_data = audit_result["audit_data"]

            # ------------------------------------------
            # Display Report
            # ------------------------------------------

            st.success("🎉 Your audit report is ready!")

            st.metric(
                label="Overall Website Audit Score",
                value=f"{final_score}/100"
            )

            st.write(
                f"**Audit Status:** {audit_status}"
            )

            st.subheader("📊 Technical Audit Details")

            if audit_data:
                for key, value in audit_data.items():
                    st.write(f"**{key}:** {value}")

            st.subheader("✅ Checks Passed")

            if passed_checks:
                for item in passed_checks:
                    st.write(item)
            else:
                st.write("No successful checks were recorded.")

            st.subheader("📋 Audit Findings")

            for issue in audit_issues:
                st.write(issue)

            st.subheader("💡 Recommendations")

            for rec in audit_recs:
                st.markdown(rec)

            # ------------------------------------------
            # Send Report and Save Details
            # ------------------------------------------

            saved_successfully = save_audit_report(
                name=name_input,
                email=email_input,
                website_url=website_url,
                audit_score=final_score,
                audit_status=audit_status,
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
