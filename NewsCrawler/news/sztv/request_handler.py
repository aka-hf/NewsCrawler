# -*- coding: utf-8 -*-
from base.base_request import RequestHandler

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authorization': 'hmac username="onesz", algorithm="hmac-sha512", headers="x-date @request-target host nonce", signature="v95FVEAnTP5FR9tkg0iTR5ejZtohYL9jkJDAm4PpkojIDOLXzZ/kNh0UEa0xS1AWOsKrz9NE8gWF3hlZlrzOPA=="',
    'nonce': 'o5yvkf4GqEaWPjCfMghbLhb3bR4qumi0',
    'origin': 'https://www.sztv.com.cn',
    'priority': 'u=0, i',
    'referer': 'https://www.sztv.com.cn/',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'x-date': 'Sat, 05 Jul 2025 09:58:50 GMT',
}
cookies = {
    "H_BDCLCKID_SF_BFESS": "tRk8oI0aJDvDqTrP-trf5DCShUFsBfodB2Q-XPoO3M3fKq7OKPPM0qDAK47bL5jiW5cpoMbgylRp8P3y0bb2DUA1y4vpa-T-aeTxoUJ2abjne-53qtnWeMLebPRiXTj9QgbwahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hD0wD5thj6PVKgTa54cbb4o2WbCQLPK28pcN2b5oQp-Oqtn9b-4JLCjPQqneQKovOPQKDpOUWfAkXpJvQnJjt2JxaqRC2bcqDl5jDh3MhP_1bhode4ROfgTy0hvcyIocShn8yUjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDHt8JT-tJJ3aQ5rtKRTffjrnhPF3QUPUXP6-hnjy3avbsl7v-bAMVJTaKx7f3TDUypjpJh3RymJ42-39LPO2hpRjyxv4MPI8h4oxJpOJaK6x0P57HR7Wbh5vbURvW5Dg3-7wBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoC0XtI0hMCvnh-nhbKC3bfT2K46JHD7yWCvqthvcOR59K4nn3P3DXPne253I2GTHanb6tqvvfxLR3MOZXMQ0MM6ky5o2KHntLUQo2J5_sq0x0bOo-f-O5JPL2bkO3COMahv9tq7xOhroQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3YjjTBeHKet58HtR3X043bHtjaKROvhjRG2jkgyxomtjjC5gOwbRcb2qjmjJ5L5M7Eef3LMG-qLUkqKCOfLtjpBpv48xODKMvTM4oyQttj2t5ufIkja-5cWPbzDJ7TyURiDx47y-Ti0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OOJRQ2QJ8BJILaMKbP",
    "Hm_lpvt_b408fb96e1915fe02831d4b48a2f25c8": "1751709530",
    "Hm_lvt_b408fb96e1915fe02831d4b48a2f25c8": "1751268682",
    "HMACCOUNT": "02F45A56821D1CF5",
    "HMACCOUNT_BFESS": "02F45A56821D1CF5",
    "BDUSS": "VNVUmtRZ1JHaVFielFHdFY3MFN5aXpucTJ2TnN3eVZMam9JTnlsNFYtTDhha2xvSVFBQUFBJCQAAAAAAAAAAAEAAADG3oZA2LzYvGVuZNi82LwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPzdIWj83SFod",
    "BDUSS_BFESS": "VNVUmtRZ1JHaVFielFHdFY3MFN5aXpucTJ2TnN3eVZMam9JTnlsNFYtTDhha2xvSVFBQUFBJCQAAAAAAAAAAAEAAADG3oZA2LzYvGVuZNi82LwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPzdIWj83SFod",
    "BDORZ": "B490B5EBF6F3CD402E515D22BCDA1598",
    "BDRCVFR[feWj1Vr5u3D]": "I67x6TjHwwYf0",
    "BDSFRCVID": "Qy8OJeC62AdONQjsjAPieZtHi9D1j36TH6aowvqALKVNSFpLCja3EG0nfM8g0KuKHtImogKKX2OTHNKF_2uxOjjg8UtVJeC6EG0Ptf8g0x5",
    "BDSFRCVID_BFESS": "Qy8OJeC62AdONQjsjAPieZtHi9D1j36TH6aowvqALKVNSFpLCja3EG0nfM8g0KuKHtImogKKX2OTHNKF_2uxOjjg8UtVJeC6EG0Ptf8g0x5",
    "BCLID": "9156461317718688762",
    "BCLID_BFESS": "9156461317718688762",
    "67_vq": "9",
    "BA_HECTOR": "ah05040laka5208k2h0k8g852184841k6hftp24",
    "BAIDUID": "00A56A9FB2CD2CC7B6A405AA4E3C5E31:FG=1",
    "BAIDUID_BFESS": "00A56A9FB2CD2CC7B6A405AA4E3C5E31:FG=1",
}


sztv_request_handler = RequestHandler(headers=headers, cookies=cookies)  

