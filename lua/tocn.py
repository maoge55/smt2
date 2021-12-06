from os import path
from urllib.parse import quote
import requests
import execjs
import os

def get_sign(s):
    node=execjs.get()
    inx= __file__.rfind('\\')
    pp=__file__[:inx+1]+'baidu.js'
    with open(pp,'r',encoding='utf-8') as f:
        ctx=node.compile(f.read())
        js_code=f'''
        e('{s}')
        '''
        result=ctx.eval(js_code)
        
    return result


header={
    #'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'cookie':r'BIDUPSID=E53465E9CF1A07861F8CE42E377B1CBC; PSTM=1613727120; BDUSS=ZEdHgxVFRQcGZMUDYwb0oyTGlRaX5naTNqNWNOflB5VVctblJlY0FMUVRUVmRnSVFBQUFBJCQAAAAAAAAAAAEAAAAF3vVQue276sbfAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABPAL2ATwC9gbl; BDUSS_BFESS=ZEdHgxVFRQcGZMUDYwb0oyTGlRaX5naTNqNWNOflB5VVctblJlY0FMUVRUVmRnSVFBQUFBJCQAAAAAAAAAAAEAAAAF3vVQue276sbfAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABPAL2ATwC9gbl; H_WISE_SIDS=107317_110085_127969_131423_144966_154619_155932_156286_156927_159936_162371_162896_163568_164075_164163_164219_164326_164456_164635_165134_165136_165328_165617_165736_166025_166148_166184_166831_167296_167390_167422_168029_168403_168500_168541_168565_168570_168719_168768_168909_168914_168970_169060_169156_169308_169343_169373_169587_169661_169667; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; __yjs_duid=1_2bb7e7a965a5f6e8bde937a0c0ae8d591621515582173; BAIDUID=324859C4F51BCFB2C29A2C8E36412A34:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; MCITY=-:; delPer=0; PSINO=7; BAIDUID_BFESS=324859C4F51BCFB2C29A2C8E36412A34:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1629096219,1629252819,1629351587,1629355784; __yjs_st=2_N2FlMGM5M2M1ZjBjMGQ1YzQyOWMwYWQyYzBmYzJiNWU1ODU1NzRlODZmM2FiZWM0NjNkODhhYzM1OWQ0ZGYzNTNkMWM5MWZlZDdmMDEwY2NmNzE4NTc4YmY2NmIwNDdiNjM5NWE3NjYzNGIwYWJjMDJkNzk4MzA1YjU5NGYwMzEyODVhZTIzOTdhM2U4MjFjNjg3NjA4MTA5NWY2MzU4MTdmZjRjZTA5YWFmZmNmOGM1NmFhYWYzMGI4MDZlODQ2YWZkMzIxNDY5YWFhYjkxOTI0YTlkOTIxZDQ0MDNiMzZlOTgzNzI2ZTVkNTMwMTJmNzMxYTgwYjExNWVhZmU1Ml83X2VjMGY3YjM0; BCLID=11285537140260711596; BDSFRCVID=qVPOJexroG0YyvRHXCFEM2YymuweG7bTDYLEOwXPsp3LGJLVJeC6EG0Pts1-dEu-EHtdogKK3mOTHmKF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tR3aQ5rtKRTffjrnhPF3DJLzXP6-hnjy3bRkX4nvWPTThMOEDlrBhJLWbttf5q3RymJJ2-39LPO2hpRjyxv4y4Ldj4oxJpOJ-bCL0p5aHl51fbbvbURvDPug3-7LBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoCvt-5rDHJTg5DTjhPrMhH_OWMT-MTryKKJwM4QCOMnE34jYDlF-hqofKx-fKHnRhlRNB-3iV-OxDUvnyxAZyxomtfQxtNRJQKDE5p5hKq5S5-OobUPUDUc9LUvLW2cdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLtCvDqTrP-trf5DCShUFsJMjWB2Q-XPoO3KJZJtQ-yh7YXUtIDRr82RQf5mkf3fbgylRp8P3y0bb2DUA1y4vpBtQmJeTxoUJ2-KDVeh5Gqfo15-0ebPRiJ-r9QgbLahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hDvPKITD-tFO5eT22-us-PjW2hcHMPoosIJX2J7cyhk9bl7uJqc8a6Tf0l05KfbUoqRmXnJi0btQDPvxBf7pWDTm_q5TtUJMqIDzbMohqfLn5MOyKMnitKj9-pnEWhQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuDjRDKICV-frb-C62aKDs_pA2BhcqJ-ovQT3Z2Jkgyb7p0UnutH58W4555l0bHxbeWfvMXn-R0hbjJM7xWeJpaJ5nJq5nhMJmKTLVbML0qto7-P3y523iob6vQpnVOpQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0DjPVKgTa54cbb4o2WbCQ-xQm8pcN2b5oQT842qjNBpvm3eTuofTXa45beq06-lOUWfAkXpJvQnJjt2JxaqRCWJ5TMl5jDh3MKToDb-otexQ7bIny0hvctb6cShnzyUjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQh-p52f6_eJb-D3o; BCLID_BFESS=11285537140260711596; BDSFRCVID_BFESS=qVPOJexroG0YyvRHXCFEM2YymuweG7bTDYLEOwXPsp3LGJLVJeC6EG0Pts1-dEu-EHtdogKK3mOTHmKF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tR3aQ5rtKRTffjrnhPF3DJLzXP6-hnjy3bRkX4nvWPTThMOEDlrBhJLWbttf5q3RymJJ2-39LPO2hpRjyxv4y4Ldj4oxJpOJ-bCL0p5aHl51fbbvbURvDPug3-7LBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoCvt-5rDHJTg5DTjhPrMhH_OWMT-MTryKKJwM4QCOMnE34jYDlF-hqofKx-fKHnRhlRNB-3iV-OxDUvnyxAZyxomtfQxtNRJQKDE5p5hKq5S5-OobUPUDUc9LUvLW2cdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLtCvDqTrP-trf5DCShUFsJMjWB2Q-XPoO3KJZJtQ-yh7YXUtIDRr82RQf5mkf3fbgylRp8P3y0bb2DUA1y4vpBtQmJeTxoUJ2-KDVeh5Gqfo15-0ebPRiJ-r9QgbLahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hDvPKITD-tFO5eT22-us-PjW2hcHMPoosIJX2J7cyhk9bl7uJqc8a6Tf0l05KfbUoqRmXnJi0btQDPvxBf7pWDTm_q5TtUJMqIDzbMohqfLn5MOyKMnitKj9-pnEWhQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuDjRDKICV-frb-C62aKDs_pA2BhcqJ-ovQT3Z2Jkgyb7p0UnutH58W4555l0bHxbeWfvMXn-R0hbjJM7xWeJpaJ5nJq5nhMJmKTLVbML0qto7-P3y523iob6vQpnVOpQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0DjPVKgTa54cbb4o2WbCQ-xQm8pcN2b5oQT842qjNBpvm3eTuofTXa45beq06-lOUWfAkXpJvQnJjt2JxaqRCWJ5TMl5jDh3MKToDb-otexQ7bIny0hvctb6cShnzyUjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQh-p52f6_eJb-D3o; H_PS_PSSID=34434_34369_34145_34374_33848_34092_34094_26350_34323_22157_34390_34360; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1629375615; ab_sr=1.0.1_M2FhZjczNDVhZDBiMjA4NzMxZTQ0YmRmZWQ2NjYxMzVkZmRhNTEzOTRhYmNmZjUzZTNlMjg5ODMzMGNlNzM1MmIzOWUwZGY2MzM1NjBlYWYzMzUzNmRhNDM4Zjc0OTdiMmM5MDRhMGM4NjgzN2Y2Njg4ODFjYTEzMjQ5NTI3YWY2ZjI5YzUwMmMwZTkxYjMzNjg4OWRkMWIwN2VmNjE4NzNjY2M3NTIyYzMxZTRlYmUyY2U5MDQ2MjI0NjMxN2E0',
    #'Refer':r'https://fanyi.baidu.com/translate'
}

def fy(query):
    sign=get_sign(query.replace('\n',r'\n').replace(r"'",r"\'"))

    url=f'https://fanyi.baidu.com/v2transapi'
    data={
        'query':query,
        'from':'en',
        'to':'zh',
        'transtype': 'translang',
        'simple_means_flag': 3,
        'sign': sign,
        'token': '8a3163eda498dfd44b35d3d72822b7f6',
        'domain': 'common',
    }

    res=requests.post(url,headers=header,data=data)


    cot=res.json()
    datas=cot['trans_result']['data']
    trans_datas=[]

    for item in datas:
        trans_datas.append(item['dst'])
    
    return trans_datas