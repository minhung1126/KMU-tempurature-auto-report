import sys
from random import randint
import requests
from bs4 import BeautifulSoup


def log_in(acc: str, pwd: str) -> requests.Session:
    rs = requests.Session()
    rs.headers.update({'Accept-Language': 'zh-TW,zh;q=0.9'})

    # login page
    stu_login_page_url = "https://wac.kmu.edu.tw/loginnew.php?PNO=indexstuv2.php&usertype=stu&lang=zh"
    resp = rs.get(stu_login_page_url)
    if not resp.ok:
        ...

    # post login
    log_in_data = {
        'userid': acc,
        'pwd': pwd,
        'usertype': 'stu',
        'PNO': 'indexstuv2.php',
        'paras': '',
    }
    stu_login_request_url = "https://wac.kmu.edu.tw/loginchk.php"
    resp = rs.post(stu_login_request_url, data=log_in_data)
    if not resp.ok:
        ...

    # Verify
    verify_url = "https://wac.kmu.edu.tw/stu/stuaca/stum0021.php"
    resp = rs.get(verify_url)
    if not resp.ok:
        ...

    if acc in resp.text:
        print('Verified')
    else:
        print('Unverified')

    return rs


def report(rs: requests.Session):
    report_url = "https://wac.kmu.edu.tw/stu/stusch/stum2906.php"
    resp = rs.get(report_url)

    # New
    requests_new_post_data = {'m_Action': '新增'.encode('cp950')}
    resp = rs.post(report_url, data=requests_new_post_data)
    if not resp.ok:
        ...

    soup = BeautifulSoup(resp.text, 'html.parser')
    post_tempurature_data = {
        '_CD_CELAYOUT': 'C',
        'm_CurRec': '0',
        'm_UPDMode': '1',
        'SCHBODYTEMP_SPNO': soup.select_one('input[name="SCHBODYTEMP_SPNO"]').get('value'),
        'SCHBODYTEMP_SNO': '自動'.encode('cp950'),
        'SCHBODYTEMP_TEL': soup.select_one('input[name="SCHBODYTEMP_TEL"]').get('value'),
        'SCHBODYTEMP_IS_FEVER': 'N',
        'SCHBODYTEMP_IS_COUGH': 'N',
        'SCHBODYTEMP_TMPTYPE': '0',
        'SCHBODYTEMP_TEMP': randint(355, 365) / 10,
        'SCHBODYTEMP_IS_MED': 'N',
        'SCHBODYTEMP_STATE': '1',
        'm_Action': '存檔'.encode('cp950'),
    }
    resp = rs.post(report_url, data=post_tempurature_data)
    if not resp.ok:
        ...
    print('Success')


def main():
    acc, pwd = sys.argv[1:3]
    rs = log_in(acc, pwd)
    report(rs)


if __name__ == "__main__":
    main()
