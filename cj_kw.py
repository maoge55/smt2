from pyppeteer import launch
from lxml import etree
from sql import *
# import asyncio


async def begin_cj_kw(w=1600,h=900):
    try:
        browser = await launch(
        headless=True,
        #userDataDir='./userdata0',
        args=['--disable-infobars','--start-maximized']
        )

        url='https://www.aliexpress.com/'

        page = await browser.newPage()

        await page.setViewport({'width': w, 'height': h}) #设置窗口大小
            # 设置浏览器
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36')
        for j in range(10):
            try:
                await page.goto(url,options={'timeout':5000})
                break
            except Exception as e:
                pass
        
        await page.waitForSelector('div.categories-list-box')
        els=await page.JJ('dt.cate-name')
        for item in els:
            await item.hover()
            await page.waitFor(300)
        
        await page.waitFor(300)

        cot= await page.content()
        
        html= etree.HTML(cot)

        cl_items=html.xpath('//div[@class="categories-list-box"]/dl')
        kw_fist=[]
        kw_second=[]
        for el in cl_items:
            txts=el.xpath('./dt[@class="cate-name"]/span//text()')
            txts0=el.xpath('./dd[@class="sub-cate"]/div[@class="sub-cate-main"]/div[@class="sub-cate-content"]//dd/a/text()')
            
            kw_fist.append(''.join(txts))
            kw_second.append(txts0)

        datas0=[{'cname':kw,'grade':1} for kw in kw_fist]
        insert(datas0,'class')
        res=select('grade=1','class')
        for j in range(len(kw_fist)):
            fcname=kw_fist[j]
            for item in res:
                if item['cname']==fcname:
                    cid=item['cid']
                    break
            datas=[]
            for kw in kw_second[j]:
                datas.append({'grade':2,'cfid':cid,'cname':kw})
            insert(datas,'class')
            
        await page.close()
        await browser.close()
        return 1

    except Exception as e:
        print(f'运行出错 => {e}')
        await page.close()
        await browser.close()
        return 0


# if __name__=='__main__':
#     loop=asyncio.get_event_loop()
#     loop.run_until_complete(begin_cj_kw())