from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright
from groq import Groq
import os

import uvicorn

mcp=FastMCP(
    name="mcp_job")

@mcp.tool()
async def job_search(search: str):
    """This tool searches for remote jobs based on user's search query and returns the 
    best job according to the search"""
    


    all_jobs=[]

    async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
            )

            page = await browser.new_page()
            await page.goto("https://remoteok.com", wait_until="domcontentloaded", timeout=60000)
            try:
                await page.locator("button").filter(has_text="x").click()
            except Exception:
                pass

            job_info = []
            await page.get_by_role("textbox", name="🔍 Search").fill(search)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(5000)

            job = page.locator("tr.job")
            for j in range(await job.count()):
                location = []
                job_title = await job.nth(j).locator("h2").inner_text()
                company = await job.nth(j).locator("h3[itemprop='name']").inner_text()
                for i in range(await job.nth(j).locator("div.location").count()):
                    location.append(await job.nth(j).locator("div.location").nth(i).inner_text())
                    for item in location:
                        if "salary" in item.lower():
                            location.remove(item)

                url = await job.nth(j).locator("a[itemprop='url']").get_attribute("href")
                url = "https://remoteok.com" + url

                job_info.append({
                    "title": job_title,
                    "company": company,
                    "location": location,
                    "url": url,
                })

                # print(job_info)
            # print("="*50)
            page = await browser.new_page()
            await page.goto("https://weworkremotely.com", wait_until="domcontentloaded", timeout=60000)
            await page.get_by_role("textbox", name="Search", exact=True).fill(search)
            await page.keyboard.press("Enter")
            await page.wait_for_load_state("load")
            view_all=page.locator("li.view-all")
            jobs=[]
            for i in range(await view_all.count()):
                await view_all.nth(i).click()
                await page.wait_for_load_state("domcontentloaded")
                job_listing=page.locator("li.new-listing-container")
                
                for j in range(await job_listing.count()):
                    job_title=await job_listing.nth(j).locator("h3").inner_text()
                    company=await job_listing.nth(j).locator("p.new-listing__company-name").inner_text()
                    info=await job_listing.nth(j).locator("div.new-listing__categories").inner_text()
                    info=info.split("\n")
                    ignore=["Featured","Top 100", "Boosted"]
                    info=[tag for tag in info if tag not in ignore]
                    try:
                        url=await job_listing.nth(j).locator("a.listing-link--unlocked").get_attribute("href")
                        url = "https://weworkremotely.com" + url
                        
                    except:    
                        # print("no url")
                        continue

                    jobs.append({
                            "title": job_title,
                            "company": company,
                            "location": info,
                            "info": url,
                        })
                    # print(jobs)
                await page.go_back()
                await page.wait_for_load_state("domcontentloaded")

            all_jobs=job_info+jobs
        
            # print(all_jobs)
            await browser.close()
            
                    


            client = Groq(
                api_key="GROQ_API_KEY"
            )
            ans1 = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "Choose the top 5 best job for the user from the list according the user search and given data, "
                        "return its url too and why is it best",
                    },
                    {
                        "role": "user",
                        "content": f"search: {search}, data: {job_info}",
                    },
                ],
            )
            gr1=ans1.choices[0].message.content
            # print(gr1)
        
        
            ans2 = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "Choose the top 5 best job for the user from the list according the user search and given data, "
                        "return its url too and why is it best",
                    },
                    {
                        "role": "user",
                        "content": f"search: {search}, data: {jobs[:100]}",
                    },
                ],
            )
            gr2=ans2.choices[0].message.content
            # print(gr2)
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "choose the best job according to user search only from the given data return the info of that job"
                        "also tell reason why is it best",
                    },
                    {
                        "role": "user",
                        "content": f"search: {search}, data: {gr1+gr2}",
                    },
                ],
            )

            best_jobs=response.choices[0].message.content
            return best_jobs
    
if __name__ == "__main__":
    app=mcp.sse_app()
    port=int(os.environ.get("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
    
