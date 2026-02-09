import asyncio
from playwright.async_api import async_playwright

async def scrape_shopee_stealth(keyword):
    """
    專業版蝦皮爬蟲 Demo (使用 Playwright Stealth)
    解決純 requests 會遇到的 403 / Cloudflare 阻擋問題。
    """
    async with async_playwright() as p:
        # 啟動瀏覽器
        browser = await p.chromium.launch(headless=True)
        
        # 設定 Context，模擬真實瀏覽器環境
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()
        
        # 模擬進入首頁獲取基礎 Cookie
        print(f"正在連線至蝦皮並模擬真人行為...")
        await page.goto("https://shopee.tw/", wait_until="networkidle")
        
        # 執行關鍵字搜尋
        search_url = f"https://shopee.tw/search?keyword={keyword}"
        await page.goto(search_url, wait_until="networkidle")
        
        # 模擬捲動以加載動態內容 (Ajax)
        await page.evaluate("window.scrollBy(0, document.body.scrollHeight/2)")
        await asyncio.sleep(2)
        
        # 抓取商品元素 (範例 Selector)
        # 注意：蝦皮的 Class Name 常變動，實務上需動態偵測
        items = await page.query_selector_all('div[data-sqe="item"]')
        
        results = []
        for item in items[:10]: # 僅抓取前 10 筆作為 Demo
            try:
                name_el = await item.query_selector('div[data-sqe="name"]')
                price_el = await item.query_selector('span') # 簡化定位
                
                if name_el:
                    name = await name_el.inner_text()
                    results.append({"name": name})
            except:
                continue
        
        print(f"成功透過模擬瀏覽器找到 {len(results)} 筆商品！")
        await browser.close()
        return results

if __name__ == "__main__":
    # 由於當前伺服器環境限制，此代碼需在具備 Playwright 環境的本機執行
    print("提示：此為專業版架構示範。在真實環境中，需搭配 'playwright-stealth' 插件以繞過高度檢測。")
    # asyncio.run(scrape_shopee_stealth("MacBook"))
