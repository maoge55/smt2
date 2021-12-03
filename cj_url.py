from pyppeteer import launch
from lxml import etree
import time,re
import asyncio
from sql import insert, select, update

dcj_keywords=[]
pat_pid=re.compile(r'/item/(\d+?).html[?]')
baurl=r'https://www.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText={0}&ltype=wholesale&SortType=default&page={1}'
async def cj_urls(sep,w,h):
    async with sep:
        global dcj_keywords
        browser = await launch(
        headless=False,
        #userDataDir='./userdata3',
        args=['--disable-infobars','--start-maximized']
        )
        page = await browser.newPage()
        await page.setViewport({'width': w, 'height':h}) #设置窗口大小
        # 设置浏览器
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36')
        
        # 防止被识别，将webdriver设置为false
        await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')

        while True:

            if len(dcj_keywords)==0:
                print('所有网址采集完毕')
                break
            aurls=0
            kw=dcj_keywords.pop(0)
            search_text=f'{kw["fcname"]} {kw["cname"]}'

            for pc in range(kw['cpcount'],kw['cpage']+1):
            #for pc in range(1,3):
                try:
                    liurl=baurl.format(search_text,pc)
                    for jj in range(3):
                        try: 
                            await page.goto(liurl)
                            break
                        except Exception as e:
                            pass

                    ifzero=await page.J('div.zero-list ')
                    if ifzero:
                        print(f'第{pc}页无内容直接跳过')
                        continue
                    await page.waitForSelector('div.product-container')
                    await page.mouse.move(w-10,20)
                    await page.mouse.down()
                    await page.mouse.move(w,h, {'steps': 20})
                    await page.mouse.up()
                    await asyncio.sleep(1)
                    cot=await page.content()
                    urls= etree.HTML(cot).xpath('//div[@class="product-container"]/div[@class="JIIxO"]/a/@href')
                    if not urls:
                        urls= etree.HTML(cot).xpath('//div[@class="product-container"]/div[@class="JIIxO"]/div/a[1]/@href')
                    aurls+=len(urls)
                    objd=[{'url':f'https://www.aliexpress.com{href}','pid':pat_pid.search(href).group(1),'pcid':kw["cid"]} for href in urls]
                    res000=insert(objd,'pids')
                    print(f'{kw["cname"]},第{pc}页 => {len(urls)},存入情况:{res000}')
                    update(f'cpcount={pc+1}',f'cid={kw["cid"]}','class')
                except Exception as e:
                    print(f'{kw["cname"]},第{pc}页 出现错误=> {e}')
            
            #print(aurls)
            #res=insert(aurls,'pids')
            #print(f'存入表pids结果:{res}')
            update('cstate=1',f'cid={kw["cid"]}','class')
            print(f'关键词{kw["cname"]}采集完毕,共采集{aurls}个网址')
            
        await page.close()
        await browser.close()

async def begin_cj_urls(w,h,k,cids):
    try:
        strat_time=time.time()
        sep=asyncio.Semaphore(k)
        tasks=[]
        kw1s=select('grade=1','class')
        if cids==-1:
            kw2s=select('grade=2 and cstate=0','class')
        else:
            kw2s=select(f'cid in {cids} and grade=2 and cstate=0','class')
        print(f'{len(kw2s)}个二级类目待采集')

        global dcj_keywords
        for item0 in kw2s:
            for item1 in kw1s:
                if item0['cfid']==item1['cid']:
                    fc=item1['cname']
                    break
            
            dcj_keywords.append({
                'fcname':fc,
                'cname':item0['cname'],
                'cid':item0['cid'], 
                'cpage':item0['cpage'],
                'cpcount':item0['cpcount']
            })

        for j in range(k):
            tasks.append(asyncio.create_task(cj_urls(sep,w,h)))
        
        await asyncio.gather(*tasks)

        end_time=time.time()
        time_cost=f'{(end_time-strat_time):2f}s'
        print(f'协程数:{k},耗时:{time_cost}')
        return 1

    except Exception as e:
        print(f'网址采集错误 => {e}')
        return 0 

