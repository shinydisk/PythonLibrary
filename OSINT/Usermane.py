import requests
from concurrent.futures import ThreadPoolExecutor

# Liste de services à tester (ajoutez-en autant que vous voulez)
SITES = {
    "GitHub": "https://github.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Pinterest": "https://www.pinterest.com/{}/",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "Dev.to": "https://dev.to/{}"
}

def check_username(site, url_template, username):
    url = url_template.format(username)
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return (site, url)
    except requests.RequestException:
        pass
    return None

def osint_username(username):
    print(f"🔍 Recherche du pseudo : {username}")
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(check_username, site, url_template, username)
            for site, url_template in SITES.items()
        ]
        for future in futures:
            result = future.result()
            if result:
                results.append(result)

    if results:
        print("\n✅ Utilisateur trouvé sur :")
        for site, url in results:
            print(f" - {site}: {url}")
    else:
        print("❌ Aucune présence trouvée.")

if __name__ == "__main__":
    username = input("\nEntrez un nom d'utilisateur à rechercher : ").strip()
    osint_username(username)
