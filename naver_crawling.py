from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve
from tqdm import tqdm
import time
import os
import zipfile

def get_images(keyword):

    print("접속중")
    driver = webdriver.Chrome(executable_path='/Users/namjjun/bin/chromedriver')
    driver.implicitly_wait(30)

    url='https://search.naver.com/search.naver?sm=tab_hty.top&where=image&query={}'.format(keyword)
    driver.get(url)

    #페이지 스크롤 다운
    body=driver.find_element_by_css_selector('body')
    for i in range(3):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1) #delay 주기

    #이미지 링크 수집
    imgs= driver.find_elements_by_css_selector("img._img")
    result=[]
    for img in tqdm(imgs):
        if 'http' in img.get_attribute('src'):
            result.append(img.get_attribute('src'))

    driver.close() # 크롬창 자동 종료
    print("수집 완료")

    #폴더생성
    print("폴더 생성")
    #폴더가 없을때만 생성
    if not os.path.isdir('./{}'.format(keyword)):
        os.mkdir('./{}'.format(keyword))

    #다운로드
    for index, link in tqdm(enumerate(result)): #tqdm은 작업현황을 알려줌.
        start=link.rfind('.') #뒤쪽부터 검사
        end=link.rfind('&')
        filetype=link[start:end] # .jpg , .png 같은게 뽑힘

        urlretrieve(link,'./{}/{}{}{}'.format(keyword,keyword,index,filetype))

    print('다운로드 완료')

    #압축 - 메일


    zip_file=zipfile.ZipFile('./{}.zip'.format(keyword),'w')

    for image in os.listdir('./{}'.format(keyword)): # Image는 파일명
        zip_file.write('./{}/{}'.format(keyword,image), compress_type=zipfile.ZIP_DEFLATED) #파일경로/파일명
    zip_file.close()
    print("압축완료")

if __name__ == '__main__':
    keyword=input("수집할 키워드를 입력하세요: ")
    get_images(keyword)
