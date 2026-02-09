import requests
import json
import time
import csv

def scrape_shopee_search(keyword, pages=1):
    """
    精簡版蝦皮搜尋爬蟲 (技術展示)
    使用 Mobile API 以降低被攔截機率。
    """
    # 蝦皮 API 的 URL 隨版本更新可能變動，此為 v4 穩定版
    base_url = "https://shopee.tw/api/v4/search/search_items"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://shopee.tw/",
        "X-API-SOURCE": "pc",
        "Accept": "application/json",
    }
    
    items_list = []
    
    for i in range(pages):
        params = {
            "by": "relevancy",
            "keyword": keyword,
            "limit": 60,
            "newest": i * 60,
            "order": "desc",
            "page_type": "search",
            "scenario": "PAGE_GLOBAL_SEARCH",
            "version": "2"
        }
        
        # 建立一個測試用的 API 請求
        # 由於蝦皮有 Cloudflare 保護，這裡我們嘗試獲取數據
        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                if not items:
                    print("API 回傳成功但無資料，可能是觸發了人機驗證或該區域無搜尋結果。")
                    return []
                    
                for item in items:
                    info = item.get('item_basic', {})
                    items_list.append({
                        "name": info.get('name'),
                        "price": info.get('price') / 100000 if info.get('price') else 0,
                        "sold": info.get('historical_sold'),
                        "rating": info.get('item_rating', {}).get('rating_star'),
                        "location": info.get('shop_location'),
                        "url": f"https://shopee.tw/product/{info.get('shopid')}/{info.get('itemid')}"
                    })
            else:
                print(f"失敗，狀態碼: {response.status_code} (可能是被阻擋)")
                return []
        except Exception as e:
            print(f"發生錯誤: {e}")
            return []
            
        time.sleep(2) 
        
    return items_list

def save_to_csv(data, filename="shopee_results.csv"):
    if not data:
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

if __name__ == "__main__":
    # 測試執行
    keyword = "iPhone 15"
    results = scrape_shopee_search(keyword, pages=1)
    if results:
        print(f"成功抓取 {len(results)} 筆資料！範例：{results[0]['name']}")
        save_to_csv(results)
    else:
        print("未抓取到資料，建議檢查 Headers 或嘗試使用代理。")
