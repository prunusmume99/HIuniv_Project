# 🔧 Scripts

이 폴더는 프로젝트의 Python 스크립트들을 포함합니다.

## 📋 스크립트 목록

### 📊 **데이터 처리 스크립트**

#### 1. `preprocess_sewer_data.py`
- **목적**: 하수도 인프라 데이터 전처리
- **기능**:
  - 원시 하수도 데이터 로드 및 정리
  - 데이터 타입 변환 및 결측치 처리
  - 인구밀도 계산 및 정규화
  - 전처리된 데이터를 `data/processed/sewer_infrastructure_processed.csv`로 저장
- **입력**: `data/raw/Sewer_Coverage_Rate.csv`
- **출력**: `data/processed/sewer_infrastructure_processed.csv`

#### 2. `sewer_infrastructure_index.py`
- **목적**: 하수도 인프라 지수 계산
- **기능**:
  - 하수도 인프라 지수 계산 (가중치 기반)
  - 인프라 등급 분류
  - 결과를 `data/processed/sewer_infrastructure_analysis.csv`로 저장
- **입력**: `data/processed/sewer_infrastructure_processed.csv`
- **출력**: `data/processed/sewer_infrastructure_analysis.csv`

### 📓 **노트북 생성 스크립트**

#### 3. `create_housing_vulnerability_notebook.py`
- **목적**: 주거취약지수 분석 노트북 생성
- **기능**:
  - 주거취약지수 분석을 위한 Jupyter 노트북 자동 생성
  - 데이터 로드, 분석, 시각화 코드 포함
  - 결과를 `notebooks/01_housing_vulnerability_analysis.ipynb`로 저장
- **출력**: `notebooks/01_housing_vulnerability_analysis.ipynb`

#### 4. `create_sewer_infrastructure_notebook.py`
- **목적**: 하수도 인프라 분석 노트북 생성
- **기능**:
  - 하수도 인프라 분석을 위한 Jupyter 노트북 자동 생성
  - 데이터 전처리, 지수 계산, 시각화 코드 포함
  - 결과를 `notebooks/02_sewer_infrastructure_analysis.ipynb`로 저장
- **출력**: `notebooks/02_sewer_infrastructure_analysis.ipynb`

#### 5. `create_housing_vulnerability_map_notebook.py`
- **목적**: 주거취약지수 지도 시각화 노트북 생성
- **기능**:
  - 주거취약지수 지도 시각화를 위한 Jupyter 노트북 자동 생성
  - 최강화된 매칭 시스템 포함
  - Folium 기반 인터랙티브 지도 생성 코드
  - 결과를 `notebooks/04_housing_vulnerability_map_visualization.ipynb`로 저장
- **출력**: `notebooks/04_housing_vulnerability_map_visualization.ipynb`

#### 6. `create_sewer_map_visualization_notebook.py`
- **목적**: 하수도 인프라 지도 시각화 노트북 생성
- **기능**:
  - 하수도 인프라 지도 시각화를 위한 Jupyter 노트북 자동 생성
  - 최강화된 매칭 시스템 포함
  - Folium 기반 인터랙티브 지도 생성 코드
  - 결과를 `notebooks/03_sewer_infrastructure_map_visualization.ipynb`로 저장
- **출력**: `notebooks/03_sewer_infrastructure_map_visualization.ipynb`

## 🚀 사용 방법

### 환경 설정
```bash
# 필요한 패키지 설치
pip install -r ../requirements.txt

# Python 스크립트 실행
python scripts/[스크립트명].py
```

### 실행 순서
1. **데이터 전처리**: `preprocess_sewer_data.py`
2. **지수 계산**: `sewer_infrastructure_index.py`
3. **노트북 생성**: `create_*.py` 스크립트들
4. **분석 실행**: 생성된 노트북 실행

### 개별 실행 예시
```bash
# 하수도 데이터 전처리
python scripts/preprocess_sewer_data.py

# 하수도 인프라 지수 계산
python scripts/sewer_infrastructure_index.py

# 주거취약지수 분석 노트북 생성
python scripts/create_housing_vulnerability_notebook.py

# 하수도 인프라 분석 노트북 생성
python scripts/create_sewer_infrastructure_notebook.py

# 주거취약지수 지도 시각화 노트북 생성
python scripts/create_housing_vulnerability_map_notebook.py

# 하수도 인프라 지도 시각화 노트북 생성
python scripts/create_sewer_map_visualization_notebook.py
```

## 🔧 주요 기능

### 📊 **데이터 처리**
- 안전한 데이터 타입 변환
- 결측치 처리
- 정규화 및 표준화
- 인구밀도 계산

### 🎯 **지수 계산**
- 가중치 기반 복합 지수 계산
- 등급 분류 시스템
- 정규화 및 표준화

### 📓 **노트북 생성**
- 자동화된 Jupyter 노트북 생성
- 완전한 분석 워크플로우 포함
- 시각화 코드 자동 생성

### 🗺️ **지도 시각화**
- 최강화된 매칭 시스템 (10단계)
- Folium 기반 인터랙티브 지도
- 색상별 등급 표시
- 상세한 툴팁 정보

## 📁 파일 구조
```
scripts/
├── preprocess_sewer_data.py                    # 하수도 데이터 전처리
├── sewer_infrastructure_index.py               # 하수도 인프라 지수 계산
├── create_housing_vulnerability_notebook.py    # 주거취약지수 분석 노트북 생성
├── create_sewer_infrastructure_notebook.py     # 하수도 인프라 분석 노트북 생성
├── create_housing_vulnerability_map_notebook.py # 주거취약지수 지도 시각화 노트북 생성
├── create_sewer_map_visualization_notebook.py  # 하수도 인프라 지도 시각화 노트북 생성
└── README.md                                   # 이 파일
```

## 🔗 관련 파일
- **데이터**: `../data/`
- **노트북**: `../notebooks/`
- **결과**: `../results/`
- **문서**: `../docs/`

## ⚠️ 주의사항

### 실행 전 확인사항
1. **Python 환경**: Python 3.8 이상 필요
2. **필수 패키지**: `requirements.txt`의 모든 패키지 설치
3. **데이터 파일**: 원시 데이터 파일들이 `data/raw/`에 존재하는지 확인
4. **경로 설정**: Windows 경로 형식 사용 (`C:\Users\...`)

### 오류 해결
```python
# 경로 문제 해결
import os
print("현재 작업 디렉토리:", os.getcwd())

# 파일 존재 여부 확인
file_path = "data/raw/Sewer_Coverage_Rate.csv"
print(f"파일 존재 여부: {os.path.exists(file_path)}")

# 패키지 설치 확인
try:
    import pandas as pd
    import folium
    print("필수 패키지 설치 완료")
except ImportError as e:
    print(f"패키지 설치 필요: {e}")
``` 