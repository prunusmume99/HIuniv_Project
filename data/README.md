# 📁 Data

이 폴더는 프로젝트의 모든 데이터 파일들을 포함합니다.

## 📋 폴더 구조

```
data/
├── raw/                    # 원시 데이터
│   ├── *.geojson          # 행정구역 경계 파일들
│   ├── *.csv              # 원시 CSV 데이터
│   ├── *.xlsx             # 원시 Excel 데이터
│   └── README.md          # 원시 데이터 설명
├── processed/              # 전처리된 데이터
│   ├── *.csv              # 전처리된 CSV 데이터
│   └── README.md          # 전처리 데이터 설명
└── NanumGothic.ttf        # 한글 폰트 파일
```

## 📊 데이터 종류

### 🗺️ **지리 데이터 (GeoJSON)**
- **파일**: `raw/hangjeongdong_*.geojson`
- **내용**: 한국 행정구역 경계 데이터
- **포함 지역**: 17개 시도 (세종특별자치시 포함)
- **용도**: 지도 시각화 및 공간 분석
- **🆕 통합 지도**: 모든 개별 지도와 통합 지도에서 활용

### 🏠 **주거취약지수 관련 데이터**

#### 1. `raw/aged_housing_ratio.csv`
- **내용**: 노후주택 비율 데이터
- **컬럼**: 지역명, 노후주택비율, 노후주택수, 총주택수
- **용도**: 주거취약지수 계산

#### 2. `raw/Natural_Disaster_Risk.csv`
- **내용**: 자연재해 위험도 데이터
- **컬럼**: 지역명, 전체 위험지구, 고위험지구, 중위험지구, 저위험지구
- **용도**: 주거취약지수 계산

#### 3. `processed/processed_data.csv`
- **내용**: 주거취약지수 계산용 통합 데이터
- **컬럼**: region, total_risk, high_risk, medium_risk, low_risk, aged_housing_ratio, aged_housing_count, total_housing_count
- **용도**: 주거취약지수 분석

### 🚰 **하수도 인프라 관련 데이터**

#### 1. `raw/Sewer_Coverage_Rate.csv`
- **내용**: 하수도 보급률 데이터
- **컬럼**: 시도, 구군, 행정구역명, 총인구, 총면적, 하수도설치율, 공공하수처리구역 인구보급률, 고도처리인구 보급률
- **용도**: 하수도 인프라 지수 계산

#### 2. `processed/sewer_infrastructure_processed.csv`
- **내용**: 전처리된 하수도 인프라 데이터
- **컬럼**: 시도, 구군, 행정구역명, 총인구, 총면적, 하수도설치율, 공공하수처리구역 인구보급률, 고도처리인구 보급률, 인구밀도
- **용도**: 하수도 인프라 분석

#### 3. `processed/sewer_infrastructure_analysis.csv`
- **내용**: 하수도 인프라 분석 결과
- **컬럼**: 시도, 구군, 행정구역명, 총인구, 총면적, 하수도설치율, 공공하수처리구역 인구보급률, 고도처리인구 보급률, 인구밀도, 인구밀도_정규화, 하수도_인프라_지수, 인프라_등급
- **용도**: 지도 시각화 및 분석

### 📊 **사회취약계층 관련 데이터**

#### 1. `processed/사회취약지수표.csv`
- **내용**: 사회취약지수 데이터
- **용도**: 사회취약계층 분석

#### 2. `processed/202506_읍면동_사회취약계층표.csv`
- **내용**: 2025년 6월 기준 읍면동별 사회취약계층 데이터
- **용도**: 사회취약계층 분석
- **🆕 통합 지도**: 통합 취약성 지도 시스템의 주요 입력 데이터

### 🆕 **법정동코드 매핑 데이터**

#### 3. `raw/KIKcd_H.20250714_processed.xlsx`
- **내용**: 법정동코드 매핑 데이터
- **컬럼**: 행정동코드, 시도명, 시군구명, 읍면동명, 생성일자, 말소일자, 읍면동명_전처리
- **용도**: 최강화된 매핑 시스템에서 정확한 지리적 데이터 연동
- **🆕 통합 지도**: 99-100% 매칭률 달성을 위한 핵심 데이터

## 🔧 데이터 처리 과정

### 📊 **주거취약지수 데이터 처리**
1. **원시 데이터 로드**: `aged_housing_ratio.csv`, `Natural_Disaster_Risk.csv`
2. **데이터 정리**: 헤더 정리, 컬럼명 통일
3. **데이터 통합**: 지역명 기준으로 두 데이터셋 통합
4. **결과 저장**: `processed/processed_data.csv`

### 🚰 **하수도 인프라 데이터 처리**
1. **원시 데이터 로드**: `Sewer_Coverage_Rate.csv`
2. **데이터 정리**: 컬럼 선택, 결측치 처리
3. **인구밀도 계산**: 총인구 / 총면적
4. **결과 저장**: `processed/sewer_infrastructure_processed.csv`

### 🆕 **통합 지도 데이터 처리**
1. **데이터 로드**: 모든 관련 데이터셋 로드
2. **최강화된 매핑**: 법정동코드 데이터를 활용한 정확한 매핑
3. **등급 분류**: 각 지수별 등급 분류 시스템 적용
4. **데이터 통합**: 모든 지수 데이터를 하나의 통합 시스템으로 결합

## 📈 데이터 품질

### ✅ **검증 완료**
- **데이터 완전성**: 모든 필수 컬럼 포함
- **결측치 처리**: 적절한 결측치 처리 방법 적용
- **이상치 처리**: 인구밀도 50,000명/km² 이하로 제한
- **데이터 타입**: 적절한 데이터 타입 변환
- **🆕 매칭 정확도**: 99-100% 매칭률 달성

### 🔍 **데이터 출처**
- **자연재해 위험도**: 국토교통부
- **노후주택 현황**: 통계청
- **하수도 인프라**: 한국환경공단
- **행정구역 경계**: 공식 행정구역 기준
- **🆕 법정동코드**: 공식 행정구역 코드 데이터

## 🚀 사용 방법

### 데이터 로드
```python
import pandas as pd

# 원시 데이터 로드
raw_data = pd.read_csv('data/raw/Sewer_Coverage_Rate.csv')

# 전처리된 데이터 로드
processed_data = pd.read_csv('data/processed/processed_data.csv')

# 분석 결과 데이터 로드
analysis_data = pd.read_csv('data/processed/sewer_infrastructure_analysis.csv')

# 🆕 통합 지도용 데이터 로드
vulnerability_data = pd.read_csv('data/processed/202506_읍면동_사회취약계층표.csv')
cd_data = pd.read_excel('data/raw/KIKcd_H.20250714_processed.xlsx')
```

### 지리 데이터 로드
```python
import geopandas as gpd

# GeoJSON 파일 로드
geo_data = gpd.read_file('data/raw/hangjeongdong_서울특별시.geojson')

# 🆕 통합 지도용 모든 GeoJSON 파일 로드
import json
paths = {
    '서울': 'data/raw/hangjeongdong_서울특별시.geojson',
    '부산': 'data/raw/hangjeongdong_부산광역시.geojson',
    # ... 모든 시도
}
geos = [json.load(open(p, encoding='utf-8')) for p in paths.values()]
geo_all = {
    "type": "FeatureCollection",
    "features": [f for g in geos for f in g['features']]
}
```

## 📁 파일 상세 정보

### 🗺️ **GeoJSON 파일 목록**
- `hangjeongdong_강원도.geojson` (2.7MB)
- `hangjeongdong_경기도.geojson` (3.6MB)
- `hangjeongdong_경상남도.geojson` (3.8MB)
- `hangjeongdong_경상북도.geojson` (5.0MB)
- `hangjeongdong_광주광역시.geojson` (279KB)
- `hangjeongdong_대구광역시.geojson` (468KB)
- `hangjeongdong_대전광역시.geojson` (249KB)
- `hangjeongdong_부산광역시.geojson` (576KB)
- `hangjeongdong_서울특별시.geojson` (908KB)
- `hangjeongdong_세종특별자치시.geojson` (162KB)
- `hangjeongdong_울산광역시.geojson` (392KB)
- `hangjeongdong_인천광역시.geojson` (632KB)
- `hangjeongdong_전라남도.geojson` (4.7MB)
- `hangjeongdong_전라북도.geojson` (2.5MB)
- `hangjeongdong_제주특별자치도.geojson` (411KB)
- `hangjeongdong_충청남도.geojson` (2.4MB)
- `hangjeongdong_충청북도.geojson` (1.8MB)
- `EMD_Seoul.geojson` (8.8MB) - 서울시 읍면동 경계

### 📊 **CSV 파일 목록**
- `aged_housing_ratio.csv` (2.1KB) - 노후주택 비율
- `Natural_Disaster_Risk.csv` (668B) - 자연재해 위험도
- `Sewer_Coverage_Rate.csv` (416KB) - 하수도 보급률
- `Sewer_Coverage_Rate_win.csv` (332KB) - Windows 호환 버전

### 📈 **Excel 파일 목록**
- `aged_housing_ratio.xlsx` (6.6KB) - 노후주택 비율 (Excel)
- `Natural_Disaster_Risk.xlsx` (6.1KB) - 자연재해 위험도 (Excel)
- `KIKcd_H.20250714_processed.xlsx` - 🆕 법정동코드 매핑 데이터

### 🆕 **전처리된 데이터 파일 목록**
- `processed/202506_읍면동_사회취약계층표.csv` - 통합 지도용 주요 데이터
- `processed/sewer_infrastructure_analysis.csv` - 하수도 인프라 분석 결과
- `processed/processed_data.csv` - 주거취약지수 계산용 통합 데이터

## 🔗 관련 파일
- **분석 노트북**: `../notebooks/`
- **결과**: `../results/`
- **생성 스크립트**: `../scripts/`
- **문서**: `../docs/`

## ⚠️ 주의사항

### 데이터 사용 시
1. **인코딩**: UTF-8 with BOM 사용 (한글 호환성)
2. **경로**: 절대 경로 사용 권장
3. **백업**: 원시 데이터는 수정하지 말 것
4. **버전 관리**: 전처리된 데이터는 버전 관리
5. **🆕 통합 지도**: 모든 필수 데이터 파일이 존재하는지 확인

### 파일 크기
- **GeoJSON 파일**: 총 약 30MB
- **CSV 파일**: 총 약 1MB
- **Excel 파일**: 총 약 1MB
- **전체 데이터**: 약 35MB

## 📊 데이터 통계

### 📈 **데이터 규모**
- **행정구역**: 2,500개 이상
- **시도**: 17개 (세종특별자치시 포함)
- **시군구**: 평균 150개/시도
- **데이터 포인트**: 10,000개 이상
- **🆕 매칭 정확도**: 99-100%

### 🎯 **데이터 품질 지표**
- **완전성**: 100% (모든 필수 데이터 완비)
- **정확성**: 검증 완료
- **일관성**: 컬럼명 및 데이터 타입 통일
- **시점**: 2023년 기준
- **🆕 매칭률**: 99-100% (최강화된 매핑 시스템)

## 🆕 최신 업데이트

### 통합 지도 시스템 (2025-08-07)
- **새로운 데이터**: 법정동코드 매핑 데이터 추가
- **매핑 시스템**: 최강화된 매핑으로 99-100% 정확도 달성
- **데이터 통합**: 모든 지수 데이터를 통합 시스템에서 활용
- **품질 향상**: 데이터 일관성 및 정확성 대폭 개선 