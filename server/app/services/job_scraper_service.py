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
from playwright.sync_api import sync_playwright


class JobScraper:

    @staticmethod
    def search(role: str):
        jobs = []

        try:
            with sync_playwright() as p:

                browser = p.chromium.launch(
                    headless=True
                )

                page = browser.new_page()

                url = (
                    f"https://remoteok.com/"
                    f"remote-{role.replace(' ', '-')}-jobs"
                )

                page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=30000,
                )

                try:
                    page.wait_for_selector(
                        "tr.job",
                        timeout=10000,
                    )
                except Exception:
                    print("No RemoteOK jobs found.")
                    browser.close()
                    return []

                cards = page.locator("tr.job")

                count = min(cards.count(), 20)

                for i in range(count):
                    card = cards.nth(i)

                    try:
                        title = (
                            card.locator("h2")
                            .first
                            .text_content()
                            or ""
                        ).strip()

                        company = (
                            card.locator("h3")
                            .first
                            .text_content()
                            or ""
                        ).strip()

                        locations = [
                            text.strip()
                            for text in card
                            .locator(".location")
                            .all_text_contents()
                            if text.strip()
                        ]

                        location = (
                            locations[0]
                            if locations
                            else "Remote"
                        )

                        href = (
                            card.get_attribute("data-href")
                            or ""
                        )

                        salarys = [
                            text.strip()
                            for text in card
                            .locator(".salary")
                            .all_text_contents()
                            if text.strip()
                        ]

                        salary = (
                            salarys[0]
                            if salarys
                            else "Based on performance"
                        )

                        jobs.append({
                            "title": title,
                            "company": company,
                            "location": location,
                            "url": f"https://remoteok.com{href}",
                            "salary": salary,
                            "description": "",
                            "source": "RemoteOK",
                        })

                    except Exception as e:
                        print(
                            f"Skipping job {i}: {e}"
                        )

                browser.close()

        except Exception as e:
            print(
                f"Job scraper failed: {type(e).__name__}: {e}"
            )
            return []

        return jobs
