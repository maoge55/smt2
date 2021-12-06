from pyppeteer import launch
from lxml import etree
from sql import *
import asyncio,re,json

pat_category1=re.compile(r'www\.aliexpress\.com/category/(\d+?)[/.]')
pat_category2=re.compile(r'www\.aliexpress\.com.*?category/(\d+?)[/.]')

async def begin_cj_kw(w=1600,h=900):
    try:
        browser = await launch(
        headless=False,
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
        await page.reload()
        await page.reload()
        await page.waitForSelector('div.categories-list-box')
        els=await page.JJ('dt.cate-name')
        for item in els:
            await item.hover()
            await page.waitFor(300)
        
        await page.waitFor(300)

        cot= await page.content()
        
        html= etree.HTML(cot)

        cl_one_items=html.xpath('//div[@class="categories-list-box"]/dl')
        for el in cl_one_items:
            txts=el.xpath('./dt[@class="cate-name"]/span//text()')
            cur_one_hrefs=el.xpath('./dt[@class="cate-name"]/span/a/@href')
            cur_one_cname=''.join(txts)
            cur_one_urls=[f'https:{href}' for href in cur_one_hrefs]
            cur_one_categorys=[pat_category1.search(href).group(1) for href in cur_one_hrefs]
            res_one=insert([{
                'cname':cur_one_cname,
                'curl':json.dumps(cur_one_urls),
                'grade':1,
                'category':json.dumps(cur_one_categorys),
                'isup':0
            }],'class')

            if res_one['success']:
                cur_first_class=exe_sql2(f"select * from class where cname =%s and grade=%s",(cur_one_cname,1))[0]
                cur_one_cid=cur_first_class["cid"]
                print(f'{cur_one_cname},存入成功,cid为{cur_one_cid}')
                cl_second_items=el.xpath('./dd[@class="sub-cate"]/div[@class="sub-cate-main"]/div[@class="sub-cate-content"]/div[@class="sub-cate-row"]/dl')
                for el2 in cl_second_items:
                    cur_second_cname=el2.xpath('./dt/a/text()')[0]
                    cur_second_url=f"https:{el2.xpath('./dt/a/@href')[0]}"
                    mat_securl=pat_category2.search(cur_second_url)
                    if not mat_securl:
                        mat_securl=re.search(r'CatId=(\d+)',cur_second_url)
                    cur_second_category=mat_securl.group(1)
                    res_two=insert([{
                        'cname':cur_second_cname,
                        'curl':cur_second_url,
                        'grade':2,
                        'cfid':cur_one_cid,
                        'category':cur_second_category,
                        'fidlist':json.dumps([cur_one_cid]),
                        'cfname':cur_one_cname,
                        'isup':0,
                    }],'class')

                    if res_two['fail']:
                        cur_second_category=f'{cur_second_category}_2'
                        res_two=insert([{
                            'cname':cur_second_cname,
                            'curl':cur_second_url,
                            'grade':2,
                            'cfid':cur_one_cid,
                            'category':cur_second_category,
                            'fidlist':json.dumps([cur_one_cid]),
                            'cfname':cur_one_cname,
                            'isup':0,
                        }],'class')
                    
                    cur_second_class=exe_sql2(f"select * from class where category=%s and grade=%s",(cur_second_category,2))[0]
                    cur_second_cid=cur_second_class['cid']
                    cl_third_items=el2.xpath('./dd/a')
                    third_datas=[]
                    for el3 in cl_third_items:

                        cur_third_url=f"https:{el3.xpath('./@href')[0]}"
                        opos=el3.xpath('./text()')
                        if opos:
                            cur_third_cname=opos[0]
                        else:
                            mat_opos=re.search(r'//www\.aliexpress\.com/category/\d+/(.*?)\.html',cur_third_url)
                            if mat_opos:
                                cur_third_cname=mat_opos.group(1)
                            else:
                                continue
                        print(cur_third_cname)
                        mat_thrurl=pat_category1.search(cur_third_url)
                        if not mat_thrurl:
                            mat_thrurl=re.search(r'CatId=(\d+)',cur_third_url,flags=re.I)
                        
                        if not mat_thrurl:
                            continue
                        cur_third_category=mat_thrurl.group(1)
                        third_datas.append({
                            'cname':cur_third_cname,
                            'curl':cur_third_url,
                            'grade':3,
                            'cfid':cur_second_cid,
                            'category':cur_third_category,
                            'fidlist':json.dumps([cur_one_cid,cur_second_cid]),
                            'cfname':cur_second_cname,
                            'isup':0,
                        })
                    
                    res_three=insert(third_datas,'class')
                    print(res_three)

            else:
                print(f'{cur_one_cname},存入失败')
                
            
        await page.close()
        await browser.close()
        return 1

    except Exception as e:
        print(f'运行出错 => {e}')
        await page.close()
        await browser.close()
        return 0


if __name__=='__main__':
    loop=asyncio.get_event_loop()
    loop.run_until_complete(begin_cj_kw())