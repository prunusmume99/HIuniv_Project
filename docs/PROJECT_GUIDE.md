# 🚀 프로젝트 실행 가이드

## 📋 프로젝트 개요
홍익대학교 세종캠퍼스 빅데이터 분석 역량 강화 프로젝트  
**"우선대응지도: 극한 강우와 사회취약도 기반 지역 분석"**

## 🛠️ 환경 설정

### 1. Python 환경 설정
```bash
# 가상환경 생성 (권장)
python -m venv .venv

# 가상환경 활성화
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 필요한 라이브러리 설치
pip install -r requirements.txt
```

### 2. Jupyter Notebook 설치 및 실행
```bash
# Jupyter 설치 (이미 requirements.txt에 포함됨)
pip install jupyter

# Jupyter Notebook 실행
jupyter notebook
```

## 📁 프로젝트 구조
```
HIuniv_Project/
├── data/
│   ├── raw/                    # 원본 데이터
│   │   ├── Natural_Disaster_Risk.csv
│   │   ├── Natural_Disaster_Risk.xlsx
│   │   ├── aged_housing_ratio.csv
│   │   ├── aged_housing_ratio.xlsx
│   │   ├── Sewer_Coverage_Rate.csv
│   │   ├── Sewer_Coverage_Rate_win.csv
│   │   └── README.md
│   ├── processed/              # 전처리된 데이터
│   │   ├── processed_data.csv
│   │   ├── sewer_infrastructure_processed.csv
│   │   └── sewer_infrastructure_analysis.csv
│   └── NanumGothic.ttf        # 한글 폰트 파일
├── notebooks/                  # 분석용 Jupyter 노트북
│   ├── 01_social_vulnerability_analysis.ipynb
│   ├── 02_sewer_infrastructure_analysis.ipynb
│   └── README.md
├── scripts/                    # Python 스크립트
│   ├── data_preprocessing.py   # 기존 데이터 전처리 스크립트
│   ├── preprocess_sewer_data.py # 하수도 데이터 전처리 스크립트
│   ├── sewer_infrastructure_index.py # 하수도 인프라 지수 계산
│   ├── create_social_vulnerability_notebook.py # 사회취약도 노트북 생성
│   ├── create_sewer_infrastructure_notebook.py # 하수도 인프라 노트북 생성
│   └── README.md
├── results/                    # 분석 결과물
│   ├── social_vulnerability_analysis.csv
│   ├── vulnerability_map_interactive.html
│   ├── sewer_infrastructure_by_region.csv
│   └── sewer_infrastructure_analysis.csv
├── docs/                       # 문서
│   ├── PROJECT_GUIDE.md        # 이 파일
│   └── README_team.md
├── .venv/                      # 가상환경 (생성됨)
├── requirements.txt            # Python 라이브러리 목록
├── README.md                   # 프로젝트 설명서
└── LICENSE                     # 라이선스 파일
```

## 🎯 분석 단계별 실행 방법

### 1단계: 기존 데이터 전처리
```bash
# 기존 데이터 전처리 (자연재해 위험도 + 노후주택 비율)
python scripts/data_preprocessing.py
```
**결과**: `data/processed/processed_data.csv` 생성

### 2단계: 하수도 데이터 전처리 (신규)
```bash
# 하수도 인프라 데이터 전처리
python scripts/preprocess_sewer_data.py
```
**결과**: `data/processed/sewer_infrastructure_processed.csv` 생성

### 3단계: 노트북 생성 (선택사항)
```bash
# 사회취약도 분석 노트북 생성
python scripts/create_social_vulnerability_notebook.py

# 하수도 인프라 분석 노트북 생성
python scripts/create_sewer_infrastructure_notebook.py
```

### 4단계: 분석 실행
```bash
# 방법 1: 기존 노트북 사용
jupyter notebook notebooks/01_social_vulnerability_analysis.ipynb
jupyter notebook notebooks/02_sewer_infrastructure_analysis.ipynb

# 방법 2: 새로 생성된 노트북 사용 (위 3단계 실행 후)
jupyter notebook notebooks/01_social_vulnerability_analysis.ipynb
jupyter notebook notebooks/02_sewer_infrastructure_analysis.ipynb
```

### 5단계: 결과 확인
- `data/processed/processed_data.csv`: 기존 전처리된 데이터
- `data/processed/sewer_infrastructure_processed.csv`: 하수도 전처리된 데이터
- `results/social_vulnerability_analysis.csv`: 사회취약도 분석 결과
- `results/sewer_infrastructure_by_region.csv`: 하수도 인프라 시도별 통계
- `results/vulnerability_map_interactive.html`: 인터랙티브 지도

## 📊 분석 내용

### 사회취약지수(SoVI) 구성 요소 (기존)
1. **전체 위험도** (가중치: 40%)
   - 자연재해 위험지구 총 개수

2. **고위험도** (가중치: 30%)
   - 가등급 위험지구 개수 (인명피해 위험)

3. **노후주택비율** (가중치: 30%)
   - 30년 이상 노후주택 비율

### 하수도 인프라 지수 구성 요소 (신규)
1. **하수도설치율** (가중치: 30%)
   - 하수관거가 설치된 지역의 면적 비율

2. **공공하수처리구역 인구보급률** (가중치: 30%)
   - 공공하수처리시설 처리구역 내 인구 비율

3. **고도처리인구 보급률** (가중치: 20%)
   - 고도처리시설을 통해 처리되는 하수를 사용하는 인구 비율

4. **인구밀도 정규화** (가중치: 20%)
   - MinMaxScaler를 사용한 0-100 스케일 정규화

### 취약지수 등급 분류
- **매우 높음/높음**: 60점 이상
- **보통**: 40-60점
- **낮음/매우 낮음**: 40점 미만

### 시각화 결과
- **지도 시각화**: 지역별 취약성 및 인프라 등급 (색상 구분)
- **분석 차트**: 
  - 사회취약지수/하수도 인프라 지수 분포 히스토그램
  - 상위/하위 지역 비교
  - 위험도 vs 노후주택비율 산점도
  - 인구 밀도 vs 인프라 지수 산점도
  - 지역별 지수 비교
  - 변수 간 상관관계 히트맵
  - 등급별 분포 파이차트

## 🔧 문제 해결

### 일반적인 오류 및 해결방법

1. **라이브러리 설치 오류**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

2. **한글 폰트 오류**
   ```python
   # matplotlib 한글 폰트 설정
   import matplotlib.pyplot as plt
   plt.rcParams['font.family'] = 'DejaVu Sans'  # 하수도 인프라 노트북
   plt.rcParams['font.family'] = 'NanumGothic'  # 사회취약도 노트북
   ```

3. **데이터 파일 경로 오류**
   - 절대 경로 사용: `C:\Users\MakerSpace\Desktop\HIuniv_Project\data\processed\`
   - 파일명 대소문자 확인
   - 파일 존재 여부 확인

4. **세종특별자치시 데이터 오류**
   ```python
   # 세종특별자치시는 구군 컬럼이 없는 특수 행정구역
   # 전처리 스크립트에서 이미 처리됨
   ```

5. **주피터 노트북 생성 오류**
   ```bash
   # Python 스크립트로 노트북 생성
   python scripts/create_social_vulnerability_notebook.py
   python scripts/create_sewer_infrastructure_notebook.py
   ```

## 📈 분석 결과

### 사회취약지수 주요 발견사항 (기존)
1. **가장 취약한 지역**: 경상북도 (취약지수: 100.0)
2. **가장 안전한 지역**: 세종특별자치시 (취약지수: 0.0)
3. **취약지수 상위 5개 지역**:
   - 경상북도 (100.0)
   - 전라남도 (83.7)
   - 경상남도 (77.6)
   - 강원도 (73.9)
   - 전라북도 (69.2)

### 하수도 인프라 지수 주요 발견사항 (신규)
1. **세종특별자치시 포함**: 특수 행정구역으로 처리하여 분석에 포함
2. **절대 경로 시스템**: 크로스 플랫폼 호환성을 위한 안정적인 파일 로딩
3. **전처리된 데이터 활용**: 별도 전처리 스크립트로 생성된 데이터 사용

### 생성되는 결과물
1. **CSV 파일들**:
   - `results/social_vulnerability_analysis.csv`: 사회취약도 분석 결과
   - `results/sewer_infrastructure_by_region.csv`: 하수도 인프라 시도별 통계
   - `data/processed/sewer_infrastructure_analysis.csv`: 하수도 인프라 전체 분석 결과

2. **지도 파일**: `results/vulnerability_map_interactive.html`
   - 인터랙티브 지도 시각화
   - 지역별 상세 정보 팝업
   - 색상별 취약도 구분

3. **분석 차트**: 다양한 시각화 그래프
   - 히스토그램, 산점도, 히트맵, 파이차트, 박스플롯

### 활용 방안
- **행정 정책 수립**: 재해 대응 및 인프라 투자 우선순위 결정
- **예산 배분**: 취약 지역 및 인프라 부족 지역 우선 지원
- **경보 시스템**: 실시간 모니터링 기반 데이터
- **도시계획**: 지역별 맞춤형 개발 전략
- **하수도 인프라 투자**: 지역별 인프라 격차 해소를 위한 투자 계획

## 🚀 빠른 시작

### 전체 분석 실행 (권장)
```bash
# 1. 가상환경 활성화
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 2. 기존 데이터 전처리
python scripts/data_preprocessing.py

# 3. 하수도 데이터 전처리
python scripts/preprocess_sewer_data.py

# 4. 노트북 생성 (선택사항)
python scripts/create_social_vulnerability_notebook.py
python scripts/create_sewer_infrastructure_notebook.py

# 5. 주피터 노트북 실행
jupyter notebook notebooks/01_social_vulnerability_analysis.ipynb
jupyter notebook notebooks/02_sewer_infrastructure_analysis.ipynb

# 6. 결과 확인
# 브라우저에서 results/vulnerability_map_interactive.html 열기
```

### 개별 분석 실행
```bash
# 사회취약도 분석만 실행
python scripts/data_preprocessing.py
jupyter notebook notebooks/01_social_vulnerability_analysis.ipynb

# 하수도 인프라 분석만 실행
python scripts/preprocess_sewer_data.py
jupyter notebook notebooks/02_sewer_infrastructure_analysis.ipynb
```

## 🔄 워크플로우

### 전체 분석 과정
```bash
# 1. 기존 데이터 전처리
python scripts/data_preprocessing.py

# 2. 하수도 데이터 전처리
python scripts/preprocess_sewer_data.py

# 3. 노트북 생성 (선택사항)
python scripts/create_social_vulnerability_notebook.py
python scripts/create_sewer_infrastructure_notebook.py

# 4. 분석 실행
jupyter notebook notebooks/01_social_vulnerability_analysis.ipynb
jupyter notebook notebooks/02_sewer_infrastructure_analysis.ipynb
```

### 개별 실행
```bash
# 전처리만 실행
python scripts/data_preprocessing.py
python scripts/preprocess_sewer_data.py

# 노트북 생성만 실행
python scripts/create_social_vulnerability_notebook.py
python scripts/create_sewer_infrastructure_notebook.py

# 인프라 지수 분석만 실행
python scripts/sewer_infrastructure_index.py
```

## 📊 분석 지표 비교

### 사회취약지수 (01_social_vulnerability_analysis.ipynb)
- **목적**: 자연재해 위험도와 주거 취약성 종합 평가
- **구성**: 전체 위험도(40%) + 고위험도(30%) + 노후주택비율(30%)
- **범위**: 시도 단위 (17개 지역)

### 하수도 인프라 지수 (02_sewer_infrastructure_analysis.ipynb)
- **목적**: 하수도 인프라 현황 및 투자 우선순위 평가
- **구성**: 하수도설치율(30%) + 공공하수처리구역(30%) + 고도처리(20%) + 인구밀도(20%)
- **범위**: 시군구 단위 (세종특별자치시 포함)

---
**마지막 업데이트**: 2025-07-30  
**프로젝트 버전**: 2.0 (하수도 인프라 분석 추가) 