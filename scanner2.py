import requests
from bs4 import BeautifulSoup

url = input("Enter Website URL: ").strip("/")

risk = 0

try:
    response = requests.get(url, timeout=10)

    print("\nWebsite Reachable\n")

    headers = response.headers

    security_headers = [
        "X-Frame-Options",
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-XSS-Protection"
    ]

    print("=== Security Headers ===")

    for header in security_headers:

        if header in headers:
            print(f"[✓] {header}")
        else:
            print(f"[✗] {header}")
            risk += 1

    soup = BeautifulSoup(response.text, "html.parser")

    forms = soup.find_all("form")

    print(f"\nForms Found: {len(forms)}")

    login_keywords = ["login", "signin", "sign-in"]

    if any(word in response.text.lower() for word in login_keywords):
        print("[!] Possible Login Page Found")
        risk += 1

    print("\n=== Admin Panel Check ===")

    admin_paths = [
        "/admin",
        "/administrator",
        "/login",
        "/admin/login"
    ]

    for path in admin_paths:

        try:
            r = requests.get(url + path, timeout=5)

            if r.status_code == 200:
                print(f"[FOUND] {path}")
                risk += 1

        except:
            pass

    print("\n=== robots.txt Check ===")

    try:
        robots = requests.get(url + "/robots.txt")

        if robots.status_code == 200:
            print("[✓] robots.txt Found")
        else:
            print("[✗] robots.txt Missing")

    except:
        pass

    print("\n=== sitemap.xml Check ===")

    try:
        sitemap = requests.get(url + "/sitemap.xml")

        if sitemap.status_code == 200:
            print("[✓] sitemap.xml Found")
        else:
            print("[✗] sitemap.xml Missing")

    except:
        pass

    if risk <= 2:
        level = "LOW"

    elif risk <= 5:
        level = "MEDIUM"

    else:
        level = "HIGH"

    print(f"\nRisk Score: {risk}")
    print(f"Risk Level: {level}")

    with open("report.txt", "w", encoding="utf-8") as report:

        report.write("WEB SECURITY REPORT\n")
        report.write("===================\n")
        report.write(f"Target: {url}\n")
        report.write(f"Forms Found: {len(forms)}\n")
        report.write(f"Risk Score: {risk}\n")
        report.write(f"Risk Level: {level}\n")

    print("\nReport Saved: report.txt")

except Exception as e:
    print("Error:", e)