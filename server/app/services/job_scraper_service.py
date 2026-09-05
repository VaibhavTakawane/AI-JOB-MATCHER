# from playwright.sync_api import sync_playwright

# class JobScraper:

#     @staticmethod
#     def search(role: str):
#         jobs = []

#         with sync_playwright() as p:
#             browser = p.chromium.launch(headless=True)
#             page = browser.new_page()

#             page.goto(
#                 f"https://remoteok.com/remote-{role.replace(' ', '-')}-jobs", wait_until="domcontentloaded")

#             page.wait_for_selector("tr.job")
#             cards = page.locator("tr.job")

#             count = min(cards.count(), 20)

#             for i in range(count):
#                 card = cards.nth(i)

#                 try:
#                     title = (card.locator(
#                         "h2").first.text_content() or "").strip()
#                     company = (card.locator(
#                         "h3").first.text_content() or "").strip()
#                     locations = [
#                         text.strip()
#                         for text in card.locator(".location").all_text_contents()
#                         if text.strip()
#                     ]
#                     location = locations[0] if locations else "Remote"

#                     href = card.get_attribute("data-href") or ""

#                     salarys = [
#                         text.strip()
#                         for text in card.locator(".salary").all_text_contents()
#                         if text.strip()
#                     ]
#                     salary = salarys[0] if salarys else "Based on performance"

#                     # # Try to get a short description from the card itself first
#                     # description = ""
#                     # try:
#                     #     desc_loc = card.locator(".description")
#                     #     if desc_loc.count() > 0:
#                     #         description = (
#                     #             desc_loc.first.text_content() or "").strip()
#                     # except Exception:
#                     #     description = ""

#                     # # If no description on the card, open the job detail page and try common selectors
#                     # if not description and href:
#                     #     detail = browser.new_page()
#                     #     try:
#                     #         detail.goto(
#                     #             f"https://remoteok.com{href}", wait_until="domcontentloaded")
#                     #         desc_selectors = [
#                     #             ".description",
#                     #             "div.job-description",
#                     #             ".job__description",
#                     #             "#job-description",
#                     #             ".jobdesc",
#                     #             "article",
#                     #         ]
#                     #         for sel in desc_selectors:
#                     #             try:
#                     #                 loc = detail.locator(sel)
#                     #                 if loc.count() > 0:
#                     #                     description = (
#                     #                         loc.first.text_content() or "").strip()
#                     #                     if description:
#                     #                         break
#                     #             except Exception:
#                     #                 continue
#                     #     except Exception:
#                     #         description = ""
#                     #     finally:
#                     #         detail.close()

#                     jobs.append({
#                         "title": title,
#                         "company": company,
#                         "location": location,
#                         "url": f"https://remoteok.com{href}",
#                         "salary": salary,
#                         "description": "description",
#                         "source": "RemoteOK",
#                     })
#                 except Exception as e:
#                     print(f"Skipping job: {e}")

#             browser.close()
#         return jobs



# -----------------------------------------------------------
import requests


class JobScraper:

    API_URL = "https://remoteok.com/api"

    @staticmethod
    def search(role: str):
        try:
            response = requests.get(
                JobScraper.API_URL,
                headers={
                    "User-Agent": "AI-Job-Matcher/1.0"
                },
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            if not isinstance(data, list):
                print("RemoteOK returned unexpected data")
                return []

            role_words = {
                word.lower()
                for word in role.split()
                if len(word) > 2
            }

            jobs = []

            for item in data:

                if not isinstance(item, dict):
                    continue

                # Skip RemoteOK API metadata
                if "position" not in item:
                    continue

                title = (
                    item.get("position")
                    or ""
                ).strip()

                company = (
                    item.get("company")
                    or ""
                ).strip()

                location = (
                    item.get("location")
                    or "Remote"
                ).strip()

                url = (
                    item.get("url")
                    or ""
                ).strip()

                description = (
                    item.get("description")
                    or ""
                ).strip()

                salary_min = item.get("salary_min")
                salary_max = item.get("salary_max")

                if salary_min and salary_max:
                    salary = f"${salary_min} - ${salary_max}"
                elif salary_min:
                    salary = f"From ${salary_min}"
                elif salary_max:
                    salary = f"Up to ${salary_max}"
                else:
                    salary = "Based on performance"

                # Search title + tags + description
                searchable_text = " ".join([
                    title,
                    str(item.get("tags") or ""),
                    description,
                ]).lower()

                # Match role keywords
                if role_words:
                    matched = any(
                        word in searchable_text
                        for word in role_words
                    )

                    if not matched:
                        continue

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "url": url,
                    "salary": salary,
                    "description": description,
                    "source": "RemoteOK",
                })

                if len(jobs) >= 20:
                    break

            print(
                f"RemoteOK: found {len(jobs)} jobs "
                f"for role '{role}'"
            )

            return jobs

        except requests.RequestException as e:
            print(f"RemoteOK request failed: {e}")
            return []

        except Exception as e:
            print(
                f"RemoteOK scraper failed: "
                f"{type(e).__name__}: {e}"
            )
            return []
