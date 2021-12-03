from pyppeteer import launch
from lxml import etree
import time,json,re
import asyncio

from sql import insert, select, update


dcj_urls=[]
async def cj_prd(sep,w,h):
    async with sep:
        global dcj_urls
        browser = await launch(
        headless=False,
        #userDataDir='./userdata3',
        args=['--disable-infobars','--start-maximized']
        )
        page = await browser.newPage()
        await page.setViewport({'width': w, 'height': h}) #设置窗口大小
        # 设置浏览器
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36')
        
        # 防止被识别，将webdriver设置为false

        await page.evaluate(

        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
        while True:
            try:
                if len(dcj_urls)==0:
                    break
                pobj=dcj_urls.pop(0)
                url=pobj['url']
                for jj in range(3):
                    try:
                        await page.goto(url)
                        break
                    except Exception as e:
                        pass
                await page.waitForSelector('h1.product-title-text')
                await page.mouse.move(w-10,20)
                await page.mouse.down()
                await page.mouse.move(h,1000, {'steps': 50})
                await page.mouse.up()
                await asyncio.sleep(1)
                await page.hover('div.sku-wrap')
                cot= await page.content()
                html=etree.HTML(cot)

                #获取seo
                seo={}
                title=html.xpath('//head/title/text()')[0]
                keywords=html.xpath('//head/meta[@name="keywords"]/@content')[0]
                description=html.xpath('//head/meta[@name="description"]/@content')[0]

                seo['title']=title
                seo['keywords']=[kw for kw in keywords.split(',') if kw!=' ']
                seo['description']=description
                #print(f'seo => {seo}')

                #获取产品名称
                pname=html.xpath('//div[@class="product-title"]/h1[@class="product-title-text"]/text()')[0]
                #print(f'pname => {pname}')

                #获取产品主图以及轮播图
                pimg={}
                imgs_lb=html.xpath('//div[@class="images-view-wrap"]/ul/li/div[@class="images-view-item"]/img/@src')
                img_main=[item.replace('50x50','Q90') for item in imgs_lb]
                pimg['lb']=imgs_lb
                pimg['main']=img_main
                #print(f'pimg=>{pimg}')

                #获取description
                prodes={}
                des_text=html.xpath('//div[@id="product-description"]/div[@class="origin-part box-sizing"]//text()')
                des_img=html.xpath('//div[@id="product-description"]/div[@class="origin-part box-sizing"]//img/@src')
                prodes['text']=[item for item in des_text if len(item)>=30 and 'window.adminAccountId=' not in item]
                prodes['imgs']=des_img

                #print(f'prodes => {prodes}')

                #获取product-sku
                el_sku_propertys=html.xpath('//div[@class="sku-wrap"]/div[@class="sku-property"]')
                product_sku=[]
                for item in el_sku_propertys:
                    cursku={}
                    sku_title=item.xpath('./div[@class="sku-title"]/text()')[0]
                    curtit=re.search(r'(.*?):(.*)',sku_title).group(2)
                    sku_title=re.search(r'(.*?):',sku_title).group(1)
                    cursku["title"]=sku_title
                    property_list=item.xpath('./ul[@class="sku-property-list"]/li')
                    if property_list:
                        text_list=item.xpath('./ul[@class="sku-property-list"]/li/div[@class="sku-property-text"]//text()')
                        if not text_list:
                            text_list=img_list=item.xpath('./ul[@class="sku-property-list"]/li/div[@class="sku-property-image"]//img/@title')
                        img_list=item.xpath('./ul[@class="sku-property-list"]/li/div[@class="sku-property-image"]//img/@src')
                        cursku["texts"]= text_list
                        cursku['imgs']=img_list
                    else:
                        cursku["texts"]= [curtit]
                    product_sku.append(cursku)
                #print(f'product_sku => {product_sku}')

                #获取sku_price
                sku_price={}
                sku_propertys=await page.xpath('//div[@class="sku-wrap"]/div[@class="sku-property"]')
                sku_nums=len(sku_propertys)
                async def get_price(n,p,l,t=[]):
                    '''
                        获取价格sku
                        n:计数器用来控制递归数
                        p:当前页面
                        l:递归总数
                        t:记录sku组合的index
                    '''
                    if n==1:
                        sku=await p.xpath(f'//div[@class="sku-wrap"]/div[{l-n+1}]/ul/li')
                        cot= await p.content()
                        clss_sku=etree.HTML(cot).xpath(f'//div[@class="sku-wrap"]/div[{l-n+1}]/ul/li/@class')
                        for k in range(len(clss_sku)):
                            if 'disabled' not in clss_sku[k]:
                                if 'sku-size-info' not in clss_sku[k]:
                                    await sku[k].click()
                                    await asyncio.sleep(0.1)
                                    tt=t[:]
                                    tt.append(k)
                                    cot= await p.content()
                                    ps=etree.HTML(cot).xpath('//div[@class="product-price-current"]/span[1]/text()')
                                    if not ps:
                                        ps=etree.HTML(cot).xpath('//span[@class="uniform-banner-box-price"]/text()')
                                    
                                    tt_key='_'.join([str(item)for item in tt])
                                    sku_price[tt_key]=ps[0]
                    else:
                        sku=await p.xpath(f'//div[@class="sku-wrap"]/div[{l-n+1}]/ul/li')

                        if sku:
                            cot= await p.content()
                            clss_sku=etree.HTML(cot).xpath(f'//div[@class="sku-wrap"]/div[{l-n+1}]/ul/li/@class')
                            for k in range(len(clss_sku)):
                                if 'disabled' not in clss_sku[k]:
                                    if 'sku-size-info' not in clss_sku[k]:
                                        await sku[k].click()
                                        await asyncio.sleep(0.1)
                                        tt=t[:]
                                        tt.append(k)
                                        await get_price(n-1,p,l,tt)                    
                        else:
                            await get_price(n-1,p,l,t[:])
                await get_price(sku_nums,page,sku_nums)
                #print(f'sku_price => {sku_price}')
                
                #获取描述规格
                prodes['dec_gg']=[]
                el_tab=await page.JJ('div.detail-extend-tab>div.detail-tab-bar>ul>li')
                if el_tab:
                    for j0 in range(len(el_tab)):
                        txts=html.xpath(f'//div[@class="detail-extend-tab"]/div[@class="detail-tab-bar"]/ul/li[{j0+1}]//text()')
                        txts_str=''.join(txts)
                        if 'SPECIFICATIONS' in txts_str:
                            #await el_tab[j0].hover()
                            await el_tab[j0].click()
                            await page.waitFor(300)
                            cur_cot=await page.content()
                            el_ul=etree.HTML(cur_cot).xpath('//div[@class="tab-content"]/div/div[@class="product-specs"]/ul')[0]
                            gg_names=el_ul.xpath('./li/span[@class="property-title"]/text()')
                            gg_values=el_ul.xpath('./li/span[@title]/@title')
                            l0=len(gg_values)
                            for j1 in range(len(gg_names)):
                                if j1<l0:
                                    gg_name=gg_names[j1].strip().strip(':')
                                    prodes['dec_gg'].append({'name':gg_name,'value':gg_values[j1]})
                            break

                pdata={
                    'pid':pobj['pid'],
                    'pcid':pobj['pcid'],
                    'pname':pname,
                    'psku':json.dumps(product_sku),
                    'pprice':json.dumps(sku_price),
                    'pprint':json.dumps(pimg),
                    'pseo':json.dumps(seo),
                    'pdec':json.dumps(prodes)
                }

                #print(pdata)
                res00=insert([pdata],'product')
                #print(f'{pobj["pid"]} => {res00}')
                if (res00['success']!=0):
                    update('pstate=1',f"pid='{pobj['pid']}'",'pids')
                    print(f'成功采集产品{pobj["pid"]},并存入数据库,剩余{len(dcj_urls)}')

            except Exception as e:
                print(f'{pobj["pid"]}出现错误=>{e}')
        
        await page.close()
        await browser.close()

async def begin_cj_content(w,h,k,cids):
    try:
        global dcj_urls
        strat_time=time.time()
        sep=asyncio.Semaphore(k)
        tasks=[]
        if cids==-1:
            dcj_urls= select('pstate=0','pids')
        else:
            dcj_urls=select(f'pcid in {cids} and pstate=0','pids')

        print(f'数据库共{len(dcj_urls)}个待采集网址')

        for y in range(k):
            tasks.append(asyncio.create_task(cj_prd(sep,w,h)))

        await asyncio.gather(*tasks)
        end_time=time.time()
        time_cost=f'{(end_time-strat_time):2f}s'
        print(f'协程数:{k},耗时:{time_cost}')
        return 1
    
    except Exception as e:
        print(f'主程序错误 => {e}')
        return 0

