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
│   │   └── README.md
│   ├── processed/              # 전처리된 데이터
│   │   └── processed_data.csv
│   └── NanumGothic.ttf        # 한글 폰트 파일
├── notebooks/                  # 분석용 Jupyter 노트북
│   └── 01_social_vulnerability_analysis.ipynb
├── scripts/                    # Python 스크립트
│   ├── data_preprocessing.py   # 데이터 전처리 스크립트
│   └── create_notebook.py      # 노트북 생성 스크립트
├── results/                    # 분석 결과물
│   ├── social_vulnerability_analysis.csv
│   └── vulnerability_map_interactive.html
├── docs/                       # 문서
│   ├── PROJECT_GUIDE.md        # 이 파일
│   └── README_team.md
├── .venv/                      # 가상환경 (생성됨)
├── create_notebook.py          # 노트북 생성 스크립트 (루트)
├── requirements.txt            # Python 라이브러리 목록
├── README.md                   # 프로젝트 설명서
└── LICENSE                     # 라이선스 파일
```

## 🎯 분석 단계별 실행 방법

### 1단계: 데이터 전처리
```bash
# 스크립트 실행
python scripts/data_preprocessing.py
```
**결과**: `data/processed/processed_data.csv` 생성

### 2단계: 사회취약지수 분석
```bash
# 방법 1: 기존 노트북 사용
jupyter notebook notebooks/01_social_vulnerability_analysis.ipynb

# 방법 2: 새 노트북 생성 (필요시)
python create_notebook.py
jupyter notebook notebooks/02_social_vulnerability_analysis.ipynb
```

### 3단계: 결과 확인
- `data/processed/processed_data.csv`: 전처리된 데이터
- `results/social_vulnerability_analysis.csv`: 분석 결과
- `results/vulnerability_map_interactive.html`: 인터랙티브 지도

## 📊 분석 내용

### 사회취약지수(SoVI) 구성 요소
1. **전체 위험도** (가중치: 40%)
   - 자연재해 위험지구 총 개수

2. **고위험도** (가중치: 30%)
   - 가등급 위험지구 개수 (인명피해 위험)

3. **노후주택비율** (가중치: 30%)
   - 30년 이상 노후주택 비율

### 취약지수 등급 분류
- **매우 높음**: 70점 이상
- **높음**: 50-70점
- **보통**: 30-50점
- **낮음**: 30점 미만

### 시각화 결과
- **지도 시각화**: 지역별 취약성 등급 (색상 구분)
- **분석 차트**: 
  - 사회취약지수 분포 히스토그램
  - 상위 10개 지역 비교
  - 위험도 vs 노후주택비율 산점도
  - 지역별 취약지수 비교
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
   plt.rcParams['font.family'] = 'NanumGothic'  # 프로젝트에 포함된 폰트
   ```

3. **데이터 파일 경로 오류**
   - 상대 경로 확인: `../data/processed/processed_data.csv`
   - 파일명 대소문자 확인

4. **주피터 노트북 생성 오류**
   ```bash
   # Python 스크립트로 노트북 생성
   python create_notebook.py
   ```

## 📈 분석 결과

### 주요 발견사항
1. **가장 취약한 지역**: 경상북도 (취약지수: 100.0)
2. **가장 안전한 지역**: 세종특별자치시 (취약지수: 0.0)
3. **취약지수 상위 5개 지역**:
   - 경상북도 (100.0)
   - 전라남도 (83.7)
   - 경상남도 (77.6)
   - 강원도 (73.9)
   - 전라북도 (69.2)

### 생성되는 결과물
1. **CSV 파일**: `results/social_vulnerability_analysis.csv`
   - 지역별 사회취약지수
   - 취약성 등급 분류
   - 상세 지표 데이터

2. **지도 파일**: `results/vulnerability_map_interactive.html`
   - 인터랙티브 지도 시각화
   - 지역별 상세 정보 팝업
   - 색상별 취약도 구분

3. **분석 차트**: 다양한 시각화 그래프
   - 히스토그램, 산점도, 히트맵, 파이차트

### 활용 방안
- **행정 정책 수립**: 재해 대응 우선순위 결정
- **예산 배분**: 취약 지역 우선 지원
- **경보 시스템**: 실시간 모니터링 기반 데이터
- **도시계획**: 지역별 맞춤형 개발 전략

## 🚀 빠른 시작

### 전체 분석 실행 (권장)
```bash
# 1. 가상환경 활성화
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 2. 데이터 전처리
python scripts/data_preprocessing.py

# 3. 주피터 노트북 실행
jupyter notebook notebooks/01_social_vulnerability_analysis.ipynb

# 4. 결과 확인
# 브라우저에서 results/vulnerability_map_interactive.html 열기
```

---
**마지막 업데이트**: 2025-07-29  
**프로젝트 버전**: 1.0 