# 📓 Jupyter Notebooks 폴더

## 📋 폴더 개요
이 폴더는 주거취약지수 분석과 하수도 인프라 분석을 위한 Jupyter Notebook 파일들을 포함합니다.

## 📁 파일 목록

### 1. `01_housing_vulnerability_analysis.ipynb` (기존)
- **파일 크기**: 13KB (351 lines)
- **생성일**: 2025-07-29
- **설명**: 주거취약지수 분석 및 지도 시각화를 위한 메인 분석 노트북

#### 📊 분석 내용
1. **데이터 로드 및 전처리**
   - `processed_data.csv` 파일 로딩
   - 데이터 정보 확인 및 기술통계
   - 결측치 처리 (대전광역시 low_risk → 0)

2. **주거취약지수 계산**
   - 가중치 기반 취약지수 계산:
     - 전체 위험도 (40%)
     - 고위험도 (30%)
     - 노후주택비율 (30%)
   - 0-100 스케일로 정규화
   - 등급별 분류 (매우 높음/높음/보통/낮음)

3. **데이터 시각화**
   - 취약지수 분포 히스토그램
   - 상위 10개 지역 비교 차트
   - 위험도 vs 노후주택비율 산점도
   - 지역별 취약지수 비교 차트
   - 변수 간 상관관계 히트맵
   - 등급별 분포 파이차트

4. **인터랙티브 지도 생성**
   - Folium을 사용한 한국 지도 시각화
   - 지역별 원형 마커 (색상 및 크기로 취약도 표현)
   - 상세 정보 팝업
   - 범례 포함

5. **결과 요약 및 저장**
   - 분석 결과 요약
   - CSV 파일로 결과 저장
   - HTML 지도 파일 저장

#### 🛠️ 사용된 라이브러리
- **pandas**: 데이터 처리 및 분석
- **numpy**: 수치 계산
- **matplotlib**: 기본 시각화
- **seaborn**: 고급 시각화
- **folium**: 인터랙티브 지도 생성
- **pathlib**: 파일 경로 관리

#### 🎯 실행 방법
```bash
# Jupyter Notebook 실행
jupyter notebook notebooks/01_social_vulnerability_analysis.ipynb

# 또는 Jupyter Lab 사용
jupyter lab notebooks/01_housing_vulnerability_analysis.ipynb
```

#### 📈 주요 결과
- **가장 취약한 지역**: 경상북도 (취약지수: 100.0)
- **가장 안전한 지역**: 세종특별자치시 (취약지수: 0.0)
- **취약지수 상위 5개 지역**: 경상북도, 전라남도, 경상남도, 강원도, 전라북도

#### 💾 생성되는 결과물
- `results/housing_vulnerability_analysis.csv`: 분석 결과 데이터
- `results/vulnerability_map_interactive.html`: 인터랙티브 지도

### 2. `02_sewer_infrastructure_analysis.ipynb` (신규)
- **파일 크기**: 411KB (2042 lines)
- **생성일**: 2025-07-30
- **최종 수정**: 2025-01-27 (인터랙티브 지도 시각화 추가)
- **설명**: 하수도 인프라 지수 분석 및 인터랙티브 지도 시각화를 위한 메인 분석 노트북

#### 📊 분석 내용
1. **전처리된 데이터 로드**
   - `sewer_infrastructure_processed.csv` 파일 로딩
   - 절대 경로를 사용한 안정적인 파일 로딩
   - 데이터 정보 확인 및 기술통계
   - 시도별 데이터 개수 확인

2. **하수도 인프라 지수 계산**
   - 가중치 기반 인프라 지수 계산:
     - 하수도설치율 (30%)
     - 공공하수처리구역 인구보급률 (30%)
     - 고도처리인구 보급률 (20%)
     - 인구밀도 정규화 (20%)
   - MinMaxScaler를 사용한 인구 밀도 정규화
   - 등급별 분류 (매우 낮음/낮음/보통/높음)

3. **데이터 시각화**
   - 인프라 지수 분포 히스토그램
   - 등급별 분포 파이차트
   - 시도별 평균 지수 수평 막대차트
   - 지표별 상관관계 히트맵
   - 인구 밀도 vs 인프라 지수 산점도
   - 등급별 인구 밀도 박스플롯

4. **상위/하위 지역 분석**
   - 상위 20개 지역 분석
   - 하위 20개 지역 분석
   - 지역별 인프라 현황 비교

5. **시도별 분석**
   - 시도별 통계 계산 (평균, 표준편차, 최소값, 최대값, 지역수)
   - 시도별 인프라 등급 분포 분석
   - 지역간 인프라 격차 분석

6. **인터랙티브 지도 시각화**
   - Folium 기반 Choropleth 지도 생성
   - 시도별 하수도 인프라 지수를 색상으로 표현
   - 마우스 호버 시 상세 정보 툴팁 표시
   - 확대/축소 및 레이어 컨트롤 기능
   - HTML 파일로 저장하여 웹 브라우저에서 확인 가능

7. **결과 저장**
   - 분석 결과 CSV 파일 저장
   - 시도별 통계 CSV 파일 저장
   - 인터랙티브 지도 HTML 파일 저장
   - 세종특별자치시 포함 여부 확인

#### 🛠️ 사용된 라이브러리
- **pandas**: 데이터 처리 및 분석
- **numpy**: 수치 계산
- **matplotlib**: 기본 시각화
- **seaborn**: 고급 시각화
- **sklearn.preprocessing**: MinMaxScaler 정규화
- **folium**: 인터랙티브 지도 시각화
- **geopandas**: 지리 데이터 처리
- **os**: 파일 경로 관리

#### 🎯 실행 방법
```bash
# Jupyter Notebook 실행
jupyter notebook notebooks/02_sewer_infrastructure_analysis.ipynb

# 또는 Jupyter Lab 사용
jupyter lab notebooks/02_sewer_infrastructure_analysis.ipynb
```

#### 📈 주요 결과
- **세종특별자치시 포함**: 특수 행정구역으로 처리하여 분석에 포함
- **절대 경로 사용**: 크로스 플랫폼 호환성을 위한 안정적인 파일 로딩
- **전처리된 데이터 활용**: 별도 전처리 스크립트로 생성된 데이터 사용

#### 💾 생성되는 결과물
- `data/processed/sewer_infrastructure_analysis.csv`: 전체 분석 결과 데이터
- `results/sewer_infrastructure_by_region.csv`: 시도별 통계 데이터
- `results/sewer_infrastructure_map.html`: 인터랙티브 지도 파일

## 🔧 노트북 실행 환경

### 필수 라이브러리
```python
# requirements.txt에 포함된 라이브러리들
pandas>=1.5.0
numpy>=1.21.0
matplotlib>=3.5.0
seaborn>=0.11.0
folium>=0.14.0
scikit-learn>=1.1.0
jupyter>=1.0.0
```

### 한글 폰트 설정
```python
# 노트북 내에서 한글 폰트 설정
import matplotlib.font_manager as fm

# 나눔고딕 폰트 경로 설정
font_path = r'C:\Users\f4141\Desktop\HIuniv_Project\data\NanumGothic.ttf'

# 폰트 등록 및 설정
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False
```

## 🚨 주의사항

### 공통 사항
1. **파일 경로**: 노트북은 절대 경로를 사용하여 안정적인 파일 로딩
2. **결과 저장**: 분석 결과는 `results/` 폴더에 저장됩니다
3. **한글 폰트**: `data/NanumGothic.ttf` 폰트 파일이 필요합니다
4. **인터넷 연결**: Folium 지도 시각화를 위해 인터넷 연결이 필요합니다

### 하수도 인프라 분석 노트북
1. **전처리된 데이터**: `scripts/preprocess_sewer_data.py`로 생성된 데이터 사용
2. **세종특별자치시**: 구군 컬럼이 없는 특수 행정구역으로 처리
3. **절대 경로**: Windows 경로 형식을 사용하여 안정성 확보
4. **인터랙티브 지도**: Folium 기반 Choropleth 지도로 시도별 인프라 현황 시각화
5. **한글 폰트**: 나눔고딕 폰트 적용으로 한글 시각화 최적화

### 주거취약도 분석 노트북
1. **상대 경로**: `../data/processed/processed_data.csv` 경로에서 데이터를 로드
2. **결과 저장**: `../results/` 폴더에 저장

## 📞 문제 해결

### 일반적인 오류
1. **FileNotFoundError**: 데이터 파일 경로 확인
2. **한글 깨짐**: 폰트 설정 확인
3. **지도 로딩 실패**: 인터넷 연결 확인
4. **경로 문제**: 절대 경로 설정 확인

### 해결 방법
```python
# 경로 문제 해결
import os
print("현재 작업 디렉토리:", os.getcwd())

# 폰트 문제 해결
import matplotlib.font_manager as fm
print("사용 가능한 폰트:", [f.name for f in fm.fontManager.ttflist if 'Nanum' in f.name])

# 파일 존재 여부 확인
import os
file_path = "data/processed/sewer_infrastructure_processed.csv"
print(f"파일 존재 여부: {os.path.exists(file_path)}")
```

## 🔄 워크플로우

### 전체 분석 과정
```bash
# 1. 데이터 전처리
python scripts/data_preprocessing.py
python scripts/preprocess_sewer_data.py

# 2. 노트북 생성 (선택사항)
python scripts/create_housing_vulnerability_notebook.py
python scripts/create_sewer_infrastructure_notebook.py

# 3. 분석 실행
jupyter notebook notebooks/01_housing_vulnerability_analysis.ipynb
jupyter notebook notebooks/02_sewer_infrastructure_analysis.ipynb
```

### 개별 실행
```bash
# 주거취약도 분석만 실행
jupyter notebook notebooks/01_housing_vulnerability_analysis.ipynb

# 하수도 인프라 분석만 실행
jupyter notebook notebooks/02_sewer_infrastructure_analysis.ipynb
```

## 📊 분석 지표 비교

### 주거취약지수 (01_housing_vulnerability_analysis.ipynb)
- **목적**: 자연재해 위험도와 주거 취약성 종합 평가
- **구성**: 전체 위험도(40%) + 고위험도(30%) + 노후주택비율(30%)
- **범위**: 시도 단위 (17개 지역)

### 하수도 인프라 지수 (02_sewer_infrastructure_analysis.ipynb)
- **목적**: 하수도 인프라 현황 및 투자 우선순위 평가
- **구성**: 하수도설치율(30%) + 공공하수처리구역(30%) + 고도처리(20%) + 인구밀도(20%)
- **범위**: 시군구 단위 (세종특별자치시 포함)

## 🚀 최신 업데이트 (2025-07-30)

### ✅ 추가된 기능
1. **하수도 인프라 분석 노트북**: 완전한 하수도 인프라 분석 워크플로우
2. **절대 경로 시스템**: 크로스 플랫폼 호환성을 위한 안정적인 파일 로딩
3. **세종특별자치시 처리**: 특수 행정구역 데이터 포함 처리
4. **모듈화된 구조**: 각 분석 영역별 독립적인 노트북 구성

### 🔧 기술적 개선사항
- 절대 경로 기반 파일 시스템으로 안정성 향상
- 전처리된 데이터 활용으로 분석 효율성 증대
- 세종특별자치시 특수 케이스 처리 로직 추가

---
**마지막 업데이트**: 2025-07-30  
**노트북 버전**: 2.0 (하수도 인프라 분석 추가) 