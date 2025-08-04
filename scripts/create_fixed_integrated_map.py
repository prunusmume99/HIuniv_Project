#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
통합 취약지수 지도 생성 (등급 매핑 수정 버전)
주거취약지수, 수도인프라지수, 사회취약지수를 통합하여 시각화
"""

import pandas as pd
import folium
import json
import numpy as np
from folium import plugins
import branca.colormap as cm
import os

print("🚀 통합 취약지수 지도 생성 시작")

# ---------------------------
# 1) GeoJSON 데이터 로드
# ---------------------------
print("📁 GeoJSON 데이터 로드 중...")

# 모든 시도의 GeoJSON 파일 경로
geo_paths = {
    '서울': 'data/raw/hangjeongdong_서울특별시.geojson',
    '부산': 'data/raw/hangjeongdong_부산광역시.geojson',
    '대구': 'data/raw/hangjeongdong_대구광역시.geojson',
    '인천': 'data/raw/hangjeongdong_인천광역시.geojson',
    '광주': 'data/raw/hangjeongdong_광주광역시.geojson',
    '대전': 'data/raw/hangjeongdong_대전광역시.geojson',
    '울산': 'data/raw/hangjeongdong_울산광역시.geojson',
    '세종': 'data/raw/hangjeongdong_세종특별자치시.geojson',
    '경기': 'data/raw/hangjeongdong_경기도.geojson',
    '강원': 'data/raw/hangjeongdong_강원도.geojson',
    '충북': 'data/raw/hangjeongdong_충청북도.geojson',
    '충남': 'data/raw/hangjeongdong_충청남도.geojson',
    '전북': 'data/raw/hangjeongdong_전라북도.geojson',
    '전남': 'data/raw/hangjeongdong_전라남도.geojson',
    '경북': 'data/raw/hangjeongdong_경상북도.geojson',
    '경남': 'data/raw/hangjeongdong_경상남도.geojson',
    '제주': 'data/raw/hangjeongdong_제주특별자치도.geojson'
}

# GeoJSON 파일들 로드
geos = []
for sido, path in geo_paths.items():
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            geo_data = json.load(f)
            geos.append(geo_data)
            print(f"✅ {sido}: {len(geo_data['features'])}개 행정동")
    else:
        print(f"❌ {sido}: 파일 없음 ({path})")

# 모든 GeoJSON 병합
geo_all = {
    "type": "FeatureCollection",
    "features": [f for g in geos for f in g['features']]
}

print(f"✅ GeoJSON 로드 완료: {len(geo_all['features'])}개 행정동")

# ---------------------------
# 2) 데이터 로드 및 전처리
# ---------------------------

# 주거취약지수 데이터 로드 (시도별 데이터)
housing_data = pd.read_csv('results/yunjin/housing_vulnerability_analysis.csv')
print(f"🏠 주거취약지수 데이터: {len(housing_data)}개 행")

# 수도인프라지수 데이터 로드 (시군구별 데이터)
sewer_data = pd.read_csv('results/yunjin/sewer_infrastructure_analysis_summary.csv')
print(f"💧 수도인프라지수 데이터: {len(sewer_data)}개 행")

# 사회취약지수 데이터 로드 (읍면동별 데이터)
social_data = pd.read_csv('data/processed/202506_읍면동_사회취약계층표.csv')
print(f"👥 사회취약지수 데이터: {len(social_data)}개 행")

# 데이터 전처리
housing_data['주거취약지수'] = housing_data['vulnerability_normalized']

# 등급 계산 함수
def calculate_grade(value, bins):
    if pd.isna(value):
        return 1
    for i in range(1, len(bins)):
        if value < bins[i]:
            return i
    return len(bins) - 1

# 주거취약지수 등급 (70/50/30/10 기준으로 5등급)
housing_bins = [0, 10, 30, 50, 70, 100]
housing_data['주거취약등급'] = housing_data['주거취약지수'].apply(lambda x: calculate_grade(x, housing_bins))

# 수도인프라지수 등급 (80/60/40 기준으로 4등급)
sewer_bins = [0, 40, 60, 80, 100]
sewer_data['수도인프라등급'] = sewer_data['하수도_인프라_지수'].apply(lambda x: calculate_grade(x, sewer_bins))

# 사회취약지수 등급 (25/50/75 기준으로 4등급)
social_bins = [0, 25, 50, 75, 100]
social_data['사회취약등급'] = social_data['사회취약지수'].apply(lambda x: calculate_grade(x, social_bins))

print("📊 등급 계산 완료")

# 등급별 라벨 매핑
def get_grade_label(grade, grade_type):
    if grade_type == "주거취약":
        labels = {1: "매우 낮음", 2: "낮음", 3: "보통", 4: "높음", 5: "매우 높음"}
    elif grade_type == "수도인프라":
        labels = {1: "매우 낮음", 2: "낮음", 3: "보통", 4: "높음"}
    else:  # 사회취약
        labels = {1: "매우 낮음", 2: "낮음", 3: "보통", 4: "높음"}
    return labels.get(grade, "보통")

# 등급 라벨 추가
housing_data['주거취약등급라벨'] = housing_data['주거취약등급'].apply(lambda x: get_grade_label(x, "주거취약"))
sewer_data['수도인프라등급라벨'] = sewer_data['수도인프라등급'].apply(lambda x: get_grade_label(x, "수도인프라"))
social_data['사회취약등급라벨'] = social_data['사회취약등급'].apply(lambda x: get_grade_label(x, "사회취약"))

print("📊 등급 라벨 매핑 완료")

# 시도명 매핑 함수
def map_sido_name(sido_name):
    mapping = {
        '서울': '서울특별시',
        '부산': '부산광역시',
        '대구': '대구광역시',
        '인천': '인천광역시',
        '광주': '광주광역시',
        '대전': '대전광역시',
        '울산': '울산광역시',
        '세종': '세종특별자치시',
        '경기': '경기도',
        '강원': '강원도',
        '충북': '충청북도',
        '충남': '충청남도',
        '전북': '전라북도',
        '전남': '전라남도',
        '경북': '경상북도',
        '경남': '경상남도',
        '제주': '제주특별자치도'
    }
    return mapping.get(sido_name, sido_name)

# 시도명 매핑 적용
housing_data['region'] = housing_data['region'].apply(map_sido_name)

# ---------------------------
# 3) GeoJSON feature에 데이터 속성 병합
# ---------------------------

# 데이터를 딕셔너리로 변환 (중복 제거)
housing_dict = housing_data.set_index('region').to_dict(orient='index')

# 수도인프라지수: 중복 제거 후 딕셔너리 생성
sewer_data_unique = sewer_data.drop_duplicates(subset=['시도', '행정구역명']).copy()
# 시도명과 행정구역명을 문자열로 변환
sewer_data_unique['시도'] = sewer_data_unique['시도'].astype(str)
sewer_data_unique['행정구역명'] = sewer_data_unique['행정구역명'].astype(str)
sewer_dict = sewer_data_unique.set_index(['시도', '행정구역명']).to_dict(orient='index')

# 시도별 평균 수도인프라지수 계산 (매핑되지 않은 지역용)
sewer_sido_avg = sewer_data_unique.groupby('시도')['하수도_인프라_지수'].mean().to_dict()

# 시도별 평균 등급 계산
sewer_sido_grade_avg = sewer_data_unique.groupby('시도')['등급_숫자'].mean().round().astype(int).to_dict()

# 시군구명 정규화 함수
def normalize_sgg_name(sgg_name):
    """시군구명을 정규화하여 매핑을 개선"""
    if not sgg_name:
        return sgg_name
    
    # 일반적인 패턴들
    patterns = {
        # 구분자 추가
        '수원시장안구': '수원시 장안구',
        '수원시권선구': '수원시 권선구', 
        '수원시팔달구': '수원시 팔달구',
        '수원시영통구': '수원시 영통구',
        '성남시수정구': '성남시 수정구',
        '성남시중원구': '성남시 중원구',
        '성남시분당구': '성남시 분당구',
        '안양시만안구': '안양시 만안구',
        '안양시동안구': '안양시 동안구',
        '부천시원미구': '부천시 원미구',
        '부천시소사구': '부천시 소사구',
        '부천시오정구': '부천시 오정구',
        '광명시': '광명시',
        '평택시': '평택시',
        '동두천시': '동두천시',
        '안산시상록구': '안산시 상록구',
        '안산시단원구': '안산시 단원구',
        '고양시덕양구': '고양시 덕양구',
        '고양시일산동구': '고양시 일산동구',
        '고양시일산서구': '고양시 일산서구',
        '과천시': '과천시',
        '구리시': '구리시',
        '남양주시': '남양주시',
        '오산시': '오산시',
        '시흥시': '시흥시',
        '군포시': '군포시',
        '의왕시': '의왕시',
        '하남시': '하남시',
        '용인시처인구': '용인시 처인구',
        '용인시기흥구': '용인시 기흥구',
        '용인시수지구': '용인시 수지구',
        '파주시': '파주시',
        '이천시': '이천시',
        '안성시': '안성시',
        '김포시': '김포시',
        '화성시': '화성시',
        '광주시': '광주시',
        '여주시': '여주시',
        '부천시': '부천시',
        '고양시': '고양시',
        '안산시': '안산시',
        '용인시': '용인시',
        
        # 시도명 정규화
        '세종시': '세종특별자치시',
    }
    
    return patterns.get(sgg_name, sgg_name)

def flexible_sewer_mapping(sidonm, sggnm, sewer_dict, sewer_data_unique):
    """유연한 수도인프라지수 매핑 함수"""
    if not sggnm:
        return None
    
    # 시도명 정규화
    sido_mapping = {
        '서울': '서울특별시',
        '부산': '부산광역시',
        '대구': '대구광역시',
        '인천': '인천광역시',
        '광주': '광주광역시',
        '대전': '대전광역시',
        '울산': '울산광역시',
        '세종': '세종특별자치시',
        '경기': '경기도',
        '강원': '강원도',
        '충북': '충청북도',
        '충남': '충청남도',
        '전북': '전라북도',
        '전남': '전라남도',
        '경북': '경상북도',
        '경남': '경상남도',
        '제주': '제주특별자치도'
    }
    
    # 시도명 매핑 적용
    mapped_sido = sido_mapping.get(sidonm, sidonm)
    
    # 1단계: 정확한 매칭 시도 (원본 시도명)
    exact_key = (sidonm, sggnm)
    if exact_key in sewer_dict:
        return sewer_dict[exact_key]
    
    # 2단계: 매핑된 시도명으로 정확한 매칭 시도
    if mapped_sido != sidonm:
        mapped_key = (mapped_sido, sggnm)
        if mapped_key in sewer_dict:
            return sewer_dict[mapped_key]
    
    # 3단계: 정규화된 시군구명으로 매칭
    normalized_sggnm = normalize_sgg_name(sggnm)
    normalized_key = (mapped_sido, normalized_sggnm)
    if normalized_key in sewer_dict:
        return sewer_dict[normalized_key]
    
    # 4단계: 부분 단어 매칭 (시군구명에 포함된 키워드로 검색)
    sggnm_clean = sggnm.replace(' ', '').replace('시', '').replace('구', '').replace('군', '').replace('읍', '').replace('면', '').replace('동', '')
    
    # 데이터에서 해당 시도의 모든 행정구역명 확인
    sido_data = sewer_data_unique[sewer_data_unique['시도'] == mapped_sido]
    
    for _, row in sido_data.iterrows():
        data_sggnm = str(row['행정구역명'])
        data_sggnm_clean = data_sggnm.replace(' ', '').replace('시', '').replace('구', '').replace('군', '').replace('읍', '').replace('면', '').replace('동', '')
        
        # 부분 매칭 시도 (양방향)
        if (sggnm_clean in data_sggnm_clean or data_sggnm_clean in sggnm_clean or
            sggnm in data_sggnm or data_sggnm in sggnm):
            return row.to_dict()
    
    # 5단계: 세종특별자치시 특별 처리
    if mapped_sido == '세종특별자치시':
        # 세종시 데이터 찾기 (시군구명에 '세종'이 포함된 경우)
        for _, row in sewer_data_unique.iterrows():
            if '세종' in str(row['행정구역명']):
                return row.to_dict()
    
    # 6단계: 시군구명에서 주요 키워드만 추출하여 매칭
    # 예: "수원시 장안구" -> "장안", "수원"
    sggnm_parts = sggnm.replace('시', ' ').replace('구', ' ').replace('군', ' ').split()
    
    for _, row in sido_data.iterrows():
        data_sggnm = str(row['행정구역명'])
        data_sggnm_parts = data_sggnm.replace('시', ' ').replace('구', ' ').replace('군', ' ').split()
        
        # 공통 키워드가 있는지 확인
        common_parts = set(sggnm_parts) & set(data_sggnm_parts)
        if len(common_parts) > 0:
            return row.to_dict()
    
    return None

def extract_sgg_name(adm_nm):
    """행정구역명에서 시군구명만 추출"""
    if not adm_nm:
        return adm_nm
    
    # 공백으로 분리
    parts = adm_nm.split()
    
    # 시도명 제거하고 시군구명만 반환
    if len(parts) >= 2:
        # 첫 번째 부분이 시도명이므로 제거
        return ' '.join(parts[1:])
    else:
        return adm_nm

# 수도인프라지수 데이터에 정규화된 시군구명 추가
sewer_data_unique['행정구역명_정규화'] = sewer_data_unique['행정구역명'].apply(normalize_sgg_name)

# 정규화 결과 디버깅
print("\n=== 정규화 디버깅 ===")
print("원본 시군구명 샘플:")
for sgg in sewer_data_unique['행정구역명'].head(10):
    print(f"  {sgg}")

print("\n정규화된 시군구명 샘플:")
for sgg in sewer_data_unique['행정구역명_정규화'].head(10):
    print(f"  {sgg}")

# 정규화된 시군구명으로도 딕셔너리 생성
sewer_dict_normalized = sewer_data_unique.set_index(['시도', '행정구역명_정규화']).to_dict(orient='index')

# 사회취약지수: 중복 제거 후 딕셔너리 생성
social_data_unique = social_data.drop_duplicates(subset=['행정동코드']).copy()
# 행정동코드를 문자열로 변환
social_data_unique['행정동코드'] = social_data_unique['행정동코드'].astype(str)
social_dict = social_data_unique.set_index('행정동코드').to_dict(orient='index')

# 시군구별 매핑 통계를 위한 집계
sgg_mapping_stats = {}

print(f"📊 딕셔너리 생성 완료:")
print(f"  - 주거취약지수: {len(housing_dict)}개")
print(f"  - 수도인프라지수 (원본): {len(sewer_dict)}개")
print(f"  - 수도인프라지수 (정규화): {len(sewer_dict_normalized)}개")
print(f"  - 사회취약지수: {len(social_dict)}개")
print(f"  - 시도별 평균 수도인프라지수: {len(sewer_sido_avg)}개")

# 디버깅: 샘플 매핑 확인
print("\n=== 디버깅: 수도인프라지수 매핑 샘플 ===")
sample_keys = list(sewer_dict.keys())[:5]
print("수도인프라지수 딕셔너리 키 샘플:")
for key in sample_keys:
    print(f"  {key}")

print("\nGeoJSON 시군구 샘플:")
for i, feat in enumerate(geo_all['features'][:5]):
    sidonm = feat['properties'].get('sidonm', '')
    sggnm = feat['properties'].get('sggnm', '')
    print(f"  {i+1}. {sidonm} {sggnm}")

print(f"\n매핑 시도:")
sample_feat = geo_all['features'][0]
sidonm = sample_feat['properties'].get('sidonm', '')
sggnm = sample_feat['properties'].get('sggnm', '')
print(f"  GeoJSON: {sidonm} {sggnm}")
print(f"  딕셔너리에서 찾기: {(sidonm, sggnm) in sewer_dict}")
if (sidonm, sggnm) in sewer_dict:
    print(f"  찾음: {sewer_dict[(sidonm, sggnm)]}")
else:
    print(f"  못찾음")
    print(f"  딕셔너리 키 타입: {type(list(sewer_dict.keys())[0])}")
    print(f"  찾는 키 타입: {type((sidonm, sggnm))}")

# 매핑 성공/실패 통계
mapping_stats = {
    'social_success': 0,
    'social_failed': 0,
    'sewer_success': 0,
    'sewer_failed': 0,
    'sewer_sido_avg_used': 0,
    'housing_success': 0,
    'housing_failed': 0
}

print("🔄 GeoJSON 데이터 병합 중...")

for feat in geo_all['features']:
    # 기본 정보 추출
    adm_cd2 = str(feat['properties'].get('adm_cd2', ''))
    adm_nm = feat['properties'].get('adm_nm', '')
    sidonm = feat['properties'].get('sidonm', '')
    sggnm = feat['properties'].get('sggnm', '')
    
    # 주거취약지수 (시도별)
    housing_row = housing_dict.get(sidonm)
    if housing_row:
        housing_vuln = housing_row.get('주거취약지수', 50)
        housing_grade = housing_row.get('주거취약등급', 3)
        housing_grade_label = housing_row.get('주거취약등급라벨', '보통')
        mapping_stats['housing_success'] += 1
    else:
        housing_vuln = 50
        housing_grade = 3
        housing_grade_label = '보통'
        mapping_stats['housing_failed'] += 1
    
    # 수도인프라지수 (시도+시군구별, 실패시 시도 평균 사용)
    # GeoJSON에서 시군구명 추출
    extracted_sggnm = extract_sgg_name(adm_nm)
    
    # 유연한 매핑 함수 사용
    sewer_row = flexible_sewer_mapping(sidonm, extracted_sggnm, sewer_dict, sewer_data_unique)
    
    if sewer_row:
        sewer_vuln = sewer_row.get('하수도_인프라_지수', 50)
        sewer_grade = sewer_row.get('등급_숫자', 3)
        sewer_grade_label = sewer_row.get('인프라_등급', '보통')
        mapping_stats['sewer_success'] += 1
        
        # 시군구별 매핑 통계
        sgg_key = f"{sidonm}_{sggnm}"
        if sgg_key not in sgg_mapping_stats:
            sgg_mapping_stats[sgg_key] = {'success': 0, 'total': 0}
        sgg_mapping_stats[sgg_key]['success'] += 1
        sgg_mapping_stats[sgg_key]['total'] += 1
    else:
        # 4단계: 시도별 평균값 사용
        sewer_vuln = sewer_sido_avg.get(sidonm, 50)
        sewer_grade = sewer_sido_grade_avg.get(sidonm, 3)
        # 등급 라벨 매핑
        if sewer_grade == 1:
            sewer_grade_label = "매우 낮음"
        elif sewer_grade == 2:
            sewer_grade_label = "낮음"
        elif sewer_grade == 3:
            sewer_grade_label = "보통"
        elif sewer_grade == 4:
            sewer_grade_label = "높음"
        else:
            sewer_grade_label = "매우 높음"
        mapping_stats['sewer_sido_avg_used'] += 1
        mapping_stats['sewer_failed'] += 1
        
        # 시군구별 매핑 통계
        sgg_key = f"{sidonm}_{sggnm}"
        if sgg_key not in sgg_mapping_stats:
            sgg_mapping_stats[sgg_key] = {'success': 0, 'total': 0}
        sgg_mapping_stats[sgg_key]['total'] += 1
    
    # 사회취약지수 (읍면동별 개별 데이터)
    social_row = social_dict.get(adm_cd2)
    if social_row:
        social_vuln = social_row.get('사회취약지수', 50)
        social_grade = social_row.get('사회취약등급', 3)
        social_grade_label = social_row.get('사회취약등급라벨', '보통')
        mapping_stats['social_success'] += 1
    else:
        # 행정동코드 형식이 다를 수 있으므로 다른 형식도 시도
        # 10자리 -> 8자리 변환 시도
        if len(adm_cd2) == 10:
            adm_cd2_8 = adm_cd2[2:]  # 앞 2자리 제거
            social_row = social_dict.get(adm_cd2_8)
            if social_row:
                social_vuln = social_row.get('사회취약지수', 50)
                social_grade = social_row.get('사회취약등급', 3)
                social_grade_label = social_row.get('사회취약등급라벨', '보통')
                mapping_stats['social_success'] += 1
            else:
                social_vuln = 50
                social_grade = 3
                social_grade_label = '보통'
                mapping_stats['social_failed'] += 1
        else:
            social_vuln = 50
            social_grade = 3
            social_grade_label = '보통'
            mapping_stats['social_failed'] += 1
    
    # 통합 취약도 계산 (가중 평균)
    integrated_score = (housing_vuln * 0.4 + sewer_vuln * 0.3 + social_vuln * 0.3)
    
    # 통합 등급 계산
    if integrated_score < 30:
        integrated_grade = 1
        integrated_label = "매우 낮음"
    elif integrated_score < 50:
        integrated_grade = 2
        integrated_label = "낮음"
    elif integrated_score < 70:
        integrated_grade = 3
        integrated_label = "보통"
    elif integrated_score < 85:
        integrated_grade = 4
        integrated_label = "높음"
    else:
        integrated_grade = 5
        integrated_label = "매우 높음"
    
    # GeoJSON 속성에 데이터 추가
    feat['properties'].update({
        '주거취약지수': round(housing_vuln, 2),
        '주거취약등급': housing_grade,
        '주거취약등급라벨': housing_grade_label,
        '수도인프라지수': round(sewer_vuln, 2),
        '수도인프라등급': sewer_grade,
        '수도인프라등급라벨': sewer_grade_label,
        '사회취약지수': round(social_vuln, 2),
        '사회취약등급': social_grade,
        '사회취약등급라벨': social_grade_label,
        '통합취약도': round(integrated_score, 2),
        '통합등급': integrated_grade,
        '통합등급라벨': integrated_label
    })

print(f"✅ 매핑 완료:")
print(f"  - 사회취약지수: {mapping_stats['social_success']}개 성공, {mapping_stats['social_failed']}개 실패")
print(f"  - 수도인프라지수: {mapping_stats['sewer_success']}개 성공, {mapping_stats['sewer_failed']}개 실패")
print(f"  - 주거취약지수: {mapping_stats['housing_success']}개 성공, {mapping_stats['housing_failed']}개 실패")
print(f"  - 시도별 평균 수도인프라지수 사용: {mapping_stats['sewer_sido_avg_used']}개")

# 시군구별 매핑 통계 출력
print(f"\n=== 시군구별 수도인프라지수 매핑 통계 ===")
failed_sgg = []
for sgg_key, stats in sgg_mapping_stats.items():
    if stats['success'] == 0 and stats['total'] > 0:
        failed_sgg.append(sgg_key)
    elif stats['success'] > 0:
        success_rate = (stats['success'] / stats['total']) * 100
        print(f"  {sgg_key}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")

if failed_sgg:
    print(f"\n매핑 실패한 시군구 ({len(failed_sgg)}개):")
    for sgg in failed_sgg[:10]:  # 처음 10개만 출력
        print(f"  - {sgg}")
    if len(failed_sgg) > 10:
        print(f"  ... 외 {len(failed_sgg) - 10}개")

# ---------------------------
# 4) 지도 생성
# ---------------------------
print("🗺️ 지도 생성 중...")

# 중심점 계산
center_lat = 36.5
center_lon = 127.5

# 기본 지도 생성
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=7,
    tiles='OpenStreetMap'
)

# 각 지수별 색상 팔레트 정의 (다른 색상 사용)
housing_colors = ['#fee5d9', '#fcae91', '#fb6a4a', '#de2d26', '#a50f15']  # 빨간색 계열
sewer_colors = ['#edf8e9', '#bae4b3', '#74c476', '#31a354', '#006d2c']    # 초록색 계열
social_colors = ['#fde0dd', '#fcc5c0', '#fa9fb5', '#f768a1', '#c51b8a']   # 분홍색 계열
integrated_colors = ['#f7f7f7', '#cccccc', '#969696', '#525252', '#252525']  # 회색 계열

# 색상 매핑 함수
def get_color(value, colors):
    if pd.isna(value) or value < 1:
        return colors[0]
    elif value >= len(colors):
        return colors[-1]
    else:
        return colors[int(value) - 1]

# 주거취약지수 레이어
housing_layer = folium.FeatureGroup(name='주거취약지수', show=True)
for feat in geo_all['features']:
    grade = feat['properties'].get('주거취약등급', 3)
    color = get_color(grade, housing_colors)
    
    folium.GeoJson(
        feat,
        style_function=lambda x, color=color: {
            'fillColor': color,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        },
        tooltip=folium.Tooltip(
            f"<b>{feat['properties'].get('adm_nm', '')}</b><br>"
            f"주거취약지수: {feat['properties'].get('주거취약지수', 0):.1f}<br>"
            f"등급: {feat['properties'].get('주거취약등급라벨', '보통')}",
            style="font-size: 12px;"
        )
    ).add_to(housing_layer)
housing_layer.add_to(m)

# 수도인프라지수 레이어
sewer_layer = folium.FeatureGroup(name='수도인프라지수', show=False)
for feat in geo_all['features']:
    grade = feat['properties'].get('수도인프라등급', 3)
    color = get_color(grade, sewer_colors)
    
    folium.GeoJson(
        feat,
        style_function=lambda x, color=color: {
            'fillColor': color,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        },
        tooltip=folium.Tooltip(
            f"<b>{feat['properties'].get('adm_nm', '')}</b><br>"
            f"수도인프라지수: {feat['properties'].get('수도인프라지수', 0):.1f}<br>"
            f"등급: {feat['properties'].get('수도인프라등급라벨', '보통')}",
            style="font-size: 12px;"
        )
    ).add_to(sewer_layer)
sewer_layer.add_to(m)

# 사회취약지수 레이어
social_layer = folium.FeatureGroup(name='사회취약지수', show=False)
for feat in geo_all['features']:
    grade = feat['properties'].get('사회취약등급', 3)
    color = get_color(grade, social_colors)
    
    folium.GeoJson(
        feat,
        style_function=lambda x, color=color: {
            'fillColor': color,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        },
        tooltip=folium.Tooltip(
            f"<b>{feat['properties'].get('adm_nm', '')}</b><br>"
            f"사회취약지수: {feat['properties'].get('사회취약지수', 0):.1f}<br>"
            f"등급: {feat['properties'].get('사회취약등급라벨', '보통')}",
            style="font-size: 12px;"
        )
    ).add_to(social_layer)
social_layer.add_to(m)

# 통합취약지수 레이어
integrated_layer = folium.FeatureGroup(name='통합취약지수', show=False)
for feat in geo_all['features']:
    grade = feat['properties'].get('통합등급', 3)
    color = get_color(grade, integrated_colors)
    
    folium.GeoJson(
        feat,
        style_function=lambda x, color=color: {
            'fillColor': color,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        },
        tooltip=folium.Tooltip(
            f"<b>{feat['properties'].get('adm_nm', '')}</b><br>"
            f"통합취약도: {feat['properties'].get('통합취약도', 0):.1f}<br>"
            f"등급: {feat['properties'].get('통합등급라벨', '보통')}<br>"
            f"주거: {feat['properties'].get('주거취약지수', 0):.1f}<br>"
            f"수도: {feat['properties'].get('수도인프라지수', 0):.1f}<br>"
            f"사회: {feat['properties'].get('사회취약지수', 0):.1f}",
            style="font-size: 12px;"
        )
    ).add_to(integrated_layer)
integrated_layer.add_to(m)

# 레이어 컨트롤 추가
folium.LayerControl().add_to(m)

# 전체 화면 버튼 추가
plugins.Fullscreen().add_to(m)

print("🗺️ 지도 생성 완료")

# ---------------------------
# 6) HTML 파일 저장
# ---------------------------
output_path = 'results/integrated_housing_sewer_social_map_fixed.html'
m.save(output_path)

print(f"💾 지도 저장 완료: {output_path}")

# ---------------------------
# 7) 등급 분포 통계 출력
# ---------------------------
print("\n=== 등급 분포 통계 ===")

# 주거취약등급 분포
housing_grade_counts = housing_data['주거취약등급라벨'].value_counts()
print("주거취약등급 분포:")
for grade, count in housing_grade_counts.items():
    print(f"  {grade}: {count}개")

# 수도인프라등급 분포
sewer_grade_counts = sewer_data['수도인프라등급라벨'].value_counts()
print("\n수도인프라등급 분포:")
for grade, count in sewer_grade_counts.items():
    print(f"  {grade}: {count}개")

# 사회취약등급 분포
social_grade_counts = social_data['사회취약등급라벨'].value_counts()
print("\n사회취약등급 분포:")
for grade, count in social_grade_counts.items():
    print(f"  {grade}: {count}개")

print("\n🎉 통합 취약지수 지도 생성 완료!") 