import os
from dotenv import load_dotenv, dotenv_values
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup as bs
import csv
from jinja2 import Template
from combo import opt_team

load_dotenv()

def main():
    with sync_playwright() as p:
        # Login
        print("Logging into APA members page...")
        browser = p.chromium.launch(headless=True) # set headless=False if you want to see what's going on
        page = browser.new_page()

        page.goto("https://accounts.poolplayers.com/login")
        page.get_by_label("email").fill(os.getenv("email"))
        page.get_by_label("password").fill(os.getenv("password"))
        page.get_by_role("button").dispatch_event("click")
        time.sleep(2)
        page.get_by_role("button").dispatch_event("click")
        time.sleep(2)
        page.get_by_text("No Thanks").click()
        page_url = page.url
        

        # Scrape 8-ball team stats
        print("Scraping team 8-ball stats...")
        page8_url = page.url.replace("dashboard", os.getenv("page8"))
        page.goto(page8_url)
        time.sleep(3)
        soup8 = bs(page.content(), "html.parser")
        head8 = soup8.table.thead.find_all("span")
        row8 = soup8.table.tbody.find_all("td")
        name8 = soup8.table.tbody.find_all("a")

        headers8 = []
        for i in head8:
            headers8.append(i.string)

        names8 = []
        for i in name8:
            names8.append(i.string)
        
        rows8 = []
        index8 = 0
        for i in row8:
            if i.string == None:
                i = names8[index8]
                index8 += 1
                rows8.append(i)
            else:
                rows8.append(i.string)
        
        
        # 8-ball team stat csv creation
        print("Creating team 8-ball stats csv file...")
        n = 6
        csv8_rows = [rows8[i:i + n] for i in range(0, len(rows8), n)]
        with open("team_8_stats.csv", "w", newline='') as f:
            write = csv.writer(f)
            write.writerow(headers8)
            write.writerows(csv8_rows)
        
        time.sleep(3)


        # Scrape 9-ball team stats
        print("Scraping team 9-ball stats...")
        page9_url = page.url.replace(os.getenv("page8"), os.getenv("page9"))
        page.goto(page9_url)
        time.sleep(3)
        soup9 = bs(page.content(), "html.parser")
        head9 = soup9.table.thead.find_all("span")
        row9 = soup9.table.tbody.find_all("td")
        name9 = soup9.table.tbody.find_all("a")

        headers9 = []
        for i in head9:
            headers9.append(i.string)

        names9 = []
        for i in name9:
            names9.append(i.string)
        
        rows9 = []
        index9 = 0
        for i in row9:
            if i.string == None:
                i = names9[index9]
                index9 += 1
                rows9.append(i)
            else:
                rows9.append(i.string)
        
        
        # 9-ball team stat csv creation
        print("Creating team 9-ball stats csv file...")
        csv9_rows = [rows9[i:i + n] for i in range(0, len(rows9), n)]
        with open("team_9_stats.csv", "w", newline='') as f:
            write = csv.writer(f)
            write.writerow(headers9)
            write.writerows(csv9_rows)
        
        time.sleep(3)
        
        
        # Pull this week's matchup
        print("Pulling 8/9-ball matchup for the week...")
        page.goto(page_url.replace("dashboard", os.getenv("matchup")))
        time.sleep(2)
        page.locator(".card-box").get_by_role("link").nth(0).click()
        time.sleep(3)
        soup_m8 = bs(page.content(), "html.parser")
        tables8 = soup_m8.find_all('table')
        home8 = tables8[0]
        away8 = tables8[1]
        
        time.sleep(2)
        
        page.goto(page_url.replace("dashboard", os.getenv("matchup")))
        time.sleep(2)
        page.locator(".card-box").get_by_role("link").nth(2).click()
        time.sleep(3)
        soup_m9 = bs(page.content(), "html.parser")
        tables9 = soup_m9.find_all('table')
        home9 = tables9[0]
        away9 = tables9[1]

        time.sleep(2)
        browser.close()


        # Create webpage for matchup stats
        print("Creating html page for the week's matchup...")
        template = Template('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <link rel="stylesheet" href="style.css">
            <link href='https://fonts.googleapis.com/css?family=JetBrains Mono' rel='stylesheet'>
            <title>{{ title }}</title>
        </head>
        <body>

            <div class="container">
            <h1>{{ header1 }}</h1>
            <div class="tcontainer">{{ table_h8 }}{{ table_a8 }}</div>
            <h2>{{ combos }}</h2>
            <div class="combo">{{ combo8 }}</div>
            </div>
            <div class="container">
            <h1>{{ header2 }}</h1>
            <div class="tcontainer">{{ table_h9 }}{{ table_a9 }}</div>
            <h2>{{ combos }}</h2>
            <div class="combo">{{ combo9 }}</div>
            </div>
        </body>
        </html>
        ''')

        combos = opt_team()
        
        html_content = template.render(
            title="This Week's Matchup", 
            header1='8-Ball Matchup', 
            table_h8=home8, table_a8=away8, 
            header2='9-Ball Matchup', 
            table_h9=home9, 
            table_a9=away9,
            combos="Possible Combos",
            combo8='<br>'.join([combo for combo in combos[0]]),
            combo9='<br>'.join([combo for combo in combos[1]])
            )

        with open('matchup.html', 'w') as file:
            file.write(html_content)
        
if __name__ == "__main__":
    main()