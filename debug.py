import asyncio
# import pandas as pd
from playwright.async_api import async_playwright

async def fetch_data():
    async with async_playwright() as p:
        # 启动浏览器
        # 显式指定使用已安装的 chromium 路径
        import os
        # executable_path = "/home/ubuntu/.cache/ms-playwright/chromium-1187/chrome-linux/chrome"
        # browser = await p.chromium.launch(headless=True, executable_path=executable_path)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        url = "https://standards.cencenelec.eu/ords/f?p=CEN:105"
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="networkidle")
        
        # 输入关键字 62443 并回车
        print("Entering keyword '62443'...")
        await page.fill("#KEYWORDS_AND", "62443")
        await page.press("#KEYWORDS_AND", "Enter")
        
        # 等待结果加载
        print("Waiting for results to load...")
        # 等待表格出现
        try:
            await page.wait_for_selector("table", timeout=60000)
        except Exception as e:
            print(f"Timeout waiting for table: {e}")
            await browser.close()
            return

        # 稍微等待一下确保内容渲染完成
        await asyncio.sleep(5)
        
        # 提取表格数据
        # 使用 evaluate 在浏览器环境中执行 JS 提取逻辑
        data = await page.evaluate("""() => {
            const tables = Array.from(document.querySelectorAll('table'));
            const resultTable = tables.find(t => t.innerText.includes('Committee') && t.innerText.includes('Reference, Title'));
            
            if (!resultTable) return null;
            
            const rows = Array.from(resultTable.querySelectorAll('tr'));
            return rows.map(row => {
                const cells = Array.from(row.querySelectorAll('th, td'));
                return cells.map(cell => cell.innerText.trim());
            });
        }""")
        
        if not data:
            print("Table not found or no data extracted.")
            await browser.close()
            return
        
        print(f"Extracted {len(data)} rows of data.")
        print("Sample data:", data[:10])  # 打印前5行数据
        # 保存为 CSV
        header = data[0]
        # df = pd.DataFrame(data[1:], columns=header)
        # output_file = "cenelec_standards_62443_playwright.csv"
        # df.to_csv(output_file, index=False)
        # print(f"Successfully fetched {len(df)} rows and saved to {output_file}")
        
        await browser.close()
        # return df

if __name__ == "__main__":
    asyncio.run(fetch_data())
