# 🔧 Python Scripts 폴더

## 📋 폴더 개요
이 폴더는 데이터 전처리 및 노트북 생성을 위한 Python 스크립트들을 포함합니다.

## 📁 파일 목록

### 1. `data_preprocessing.py` (기존)
- **파일 크기**: 7.1KB (194 lines)
- **생성일**: 2025-07-29
- **설명**: 원본 데이터를 전처리하여 분석용 데이터셋을 생성하는 스크립트

#### 🎯 주요 기능
1. **데이터 로딩**
   - `data/raw/Natural_Disaster_Risk.csv` 로딩
   - `data/raw/aged_housing_ratio.csv` 로딩
   - 파일 존재 여부 및 오류 처리

2. **자연재해 위험도 데이터 전처리**
   - 헤더 정리 (첫 번째, 두 번째 행을 컬럼명으로 설정)
   - 2023년 데이터만 선택
   - 숫자형 데이터 변환
   - 컬럼명 정리: `region`, `total_risk`, `high_risk`, `medium_risk`, `low_risk`

3. **노후주택 비율 데이터 전처리**
   - 헤더 정리 (첫 번째, 두 번째 행을 컬럼명으로 설정)
   - 2023.2 분기 데이터만 선택 (최신 데이터)
   - 숫자형 데이터 변환
   - 컬럼명 정리: `region`, `aged_housing_ratio`, `aged_housing_count`, `total_housing_count`

4. **데이터 통합**
   - 지역명 매핑 딕셔너리 사용
   - 두 데이터셋을 `region` 기준으로 통합 (inner join)
   - 지역명 통일 (예: '강원특별자치도' → '강원도')

5. **결과 저장**
   - `data/processed/processed_data.csv`로 저장
   - UTF-8 with BOM 인코딩 사용

#### 🛠️ 주요 함수
```python
def load_data()                    # 원본 데이터 로딩
def preprocess_disaster_data(df)   # 자연재해 위험도 전처리
def preprocess_housing_data(df)    # 노후주택 비율 전처리
def merge_data(disaster_data, housing_data)  # 데이터 통합
def save_processed_data(data, filename)      # 결과 저장
def main()                         # 메인 실행 함수
```

#### 🎯 실행 방법
```bash
# 프로젝트 루트에서 실행
python scripts/data_preprocessing.py

# 또는 scripts 폴더에서 실행
cd scripts
python data_preprocessing.py
```

#### 📊 출력 결과
- **성공 시**: 전처리된 데이터 정보 및 요약 통계 출력
- **실패 시**: 오류 메시지 출력
- **생성 파일**: `data/processed/processed_data.csv`

### 2. `preprocess_sewer_data.py` (신규)
- **파일 크기**: 3.7KB (94 lines)
- **생성일**: 2025-01-27
- **설명**: 하수도 보급률 데이터를 전처리하여 분석용 데이터셋을 생성하는 스크립트

#### 🎯 주요 기능
1. **데이터 로딩**
   - `data/raw/Sewer_Coverage_Rate.csv` 로딩
   - 파일 존재 여부 및 오류 처리

2. **컬럼 선택 및 정리**
   - 필요한 컬럼만 선택: 시도, 행정구역명, 총인구, 총면적, 하수도 관련 지표
   - 세종특별자치시 구군 컬럼 결측값 허용

3. **결측값 및 이상값 처리**
   - 결측값 제거 (구군 컬럼 제외)
   - 하수도 관련 지표 0-100% 범위 검증
   - 인구 밀도 이상값 처리 (50,000명/km² 이하)

4. **인구 밀도 계산**
   - 총인구 / 총면적으로 인구 밀도 계산
   - 단위: 명/km²

5. **결과 저장**
   - `data/processed/sewer_infrastructure_processed.csv`로 저장
   - UTF-8 with BOM 인코딩 사용

#### 🛠️ 주요 함수
```python
def preprocess_sewer_data()        # 메인 전처리 함수
def main()                         # 메인 실행 함수
```

#### 🎯 실행 방법
```bash
# 프로젝트 루트에서 실행
python scripts/preprocess_sewer_data.py

# 또는 scripts 폴더에서 실행
cd scripts
python preprocess_sewer_data.py
```

#### 📊 출력 결과
- **성공 시**: 전처리된 데이터 정보 및 시도별 데이터 개수 출력
- **실패 시**: 오류 메시지 출력
- **생성 파일**: `data/processed/sewer_infrastructure_processed.csv`

### 3. `sewer_infrastructure_index.py` (신규)
- **파일 크기**: 10KB (260 lines)
- **생성일**: 2025-01-27
- **설명**: 하수도 인프라 지수를 계산하고 분석하는 클래스 기반 스크립트

#### 🎯 주요 기능
1. **데이터 로딩 및 탐색**
   - 전처리된 하수도 데이터 로딩
   - 데이터 기본 정보 및 기술통계 확인

2. **데이터 정제**
   - 결측값 처리
   - 이상값 제거
   - 데이터 타입 변환

3. **인프라 지수 계산**
   - 가중치 기반 종합 지수 계산
   - MinMaxScaler를 사용한 정규화
   - 등급별 분류

4. **지역별 분석**
   - 시도별 통계 계산
   - 상위/하위 지역 분석
   - 등급별 분포 분석

5. **시각화**
   - 히스토그램, 파이차트, 바차트 등
   - 상관관계 히트맵
   - 산점도

6. **결과 저장**
   - 분석 결과 CSV 파일 저장
   - 시각화 이미지 저장

#### 🛠️ 주요 클래스 및 함수
```python
class SewerInfrastructureIndex:
    def __init__(self, data_path)           # 초기화
    def load_data(self)                     # 데이터 로딩
    def explore_data(self)                  # 데이터 탐색
    def clean_data(self)                    # 데이터 정제
    def calculate_infrastructure_index(self, weights=None)  # 지수 계산
    def analyze_by_region(self)             # 지역별 분석
    def create_visualizations(self, save_path)  # 시각화
    def save_results(self, output_path)     # 결과 저장
```

#### 🎯 실행 방법
```bash
# 프로젝트 루트에서 실행
python scripts/sewer_infrastructure_index.py

# 또는 scripts 폴더에서 실행
cd scripts
python sewer_infrastructure_index.py
```

### 4. `create_social_vulnerability_notebook.py` (신규)
- **파일 크기**: 18KB (386 lines)
- **생성일**: 2025-01-27
- **설명**: 사회취약지수 분석을 위한 Jupyter Notebook을 생성하는 스크립트

#### 🎯 주요 기능
1. **노트북 구조 생성**
   - `json` 형식으로 노트북 구조 생성
   - 마크다운 셀과 코드 셀 조합
   - 메타데이터 설정

2. **분석 코드 포함**
   - 데이터 로드 및 전처리
   - 사회취약지수 계산
   - 다양한 시각화
   - 인터랙티브 지도 생성
   - 결과 요약 및 저장

3. **절대 경로 사용**
   - 크로스 플랫폼 호환성을 위한 절대 경로 설정
   - 파일 존재 여부 확인 로직 포함

#### 🛠️ 주요 함수
```python
def create_social_vulnerability_notebook()  # 노트북 생성 메인 함수
def main()                                  # 메인 실행 함수
```

#### 🎯 실행 방법
```bash
# 프로젝트 루트에서 실행
python scripts/create_social_vulnerability_notebook.py

# 또는 scripts 폴더에서 실행
cd scripts
python create_social_vulnerability_notebook.py
```

#### 📊 출력 결과
- **생성 파일**: `notebooks/01_social_vulnerability_analysis.ipynb`
- **노트북 내용**: 완전한 분석 워크플로우 포함

### 5. `create_sewer_infrastructure_notebook.py` (신규)
- **파일 크기**: 18KB (375 lines)
- **생성일**: 2025-01-27
- **설명**: 하수도 인프라 분석을 위한 Jupyter Notebook을 생성하는 스크립트

#### 🎯 주요 기능
1. **노트북 구조 생성**
   - `json` 형식으로 노트북 구조 생성
   - 마크다운 셀과 코드 셀 조합
   - 메타데이터 설정

2. **분석 코드 포함**
   - 전처리된 데이터 로드
   - 하수도 인프라 지수 계산
   - 다양한 시각화
   - 상위/하위 지역 분석
   - 시도별 분석
   - 결과 저장

3. **절대 경로 사용**
   - 크로스 플랫폼 호환성을 위한 절대 경로 설정
   - 파일 존재 여부 확인 로직 포함
   - 세종특별자치시 데이터 포함 처리

#### 🛠️ 주요 함수
```python
def create_sewer_infrastructure_notebook()  # 노트북 생성 메인 함수
def main()                                  # 메인 실행 함수
```

#### 🎯 실행 방법
```bash
# 프로젝트 루트에서 실행
python scripts/create_sewer_infrastructure_notebook.py

# 또는 scripts 폴더에서 실행
cd scripts
python create_sewer_infrastructure_notebook.py
```

#### 📊 출력 결과
- **생성 파일**: `notebooks/02_sewer_infrastructure_analysis.ipynb`
- **노트북 내용**: 완전한 하수도 인프라 분석 워크플로우 포함

## 🔧 기술적 세부사항

### 사용된 라이브러리
```python
# 공통 라이브러리
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# 전처리 관련
from sklearn.preprocessing import MinMaxScaler

# 노트북 생성 관련
import json

# 시각화 관련
import matplotlib.pyplot as plt
import seaborn as sns
```

### 파일 경로 관리
- **절대 경로 사용**: 크로스 플랫폼 호환성을 위해 절대 경로 사용
- **Path 객체**: 크로스 플랫폼 호환성
- **자동 디렉토리 생성**: `os.makedirs(path, exist_ok=True)`

### 오류 처리
- **try-except 블록**: 각 단계별 오류 처리
- **상세한 오류 메시지**: 디버깅 용이성
- **단계별 검증**: 데이터 품질 보장
- **파일 존재 여부 확인**: 실행 전 파일 경로 검증

## 🚨 주의사항

### 공통 사항
1. **실행 위치**: 프로젝트 루트에서 실행 권장
2. **원본 데이터**: `data/raw/` 폴더에 원본 파일 필요
3. **결과 덮어쓰기**: 기존 파일 덮어씀
4. **인코딩**: UTF-8 with BOM 사용 (한글 호환성)

### 하수도 인프라 관련
1. **세종특별자치시**: 구군 컬럼이 없는 특수 행정구역으로 처리
2. **이상값 처리**: 인구 밀도 50,000명/km² 이하로 제한
3. **가중치 설정**: 하수도설치율(30%), 공공하수처리구역(30%), 고도처리(20%), 인구밀도(20%)

### 노트북 생성 관련
1. **의존성**: `json` 라이브러리 사용
2. **절대 경로**: Windows 경로 형식 사용
3. **한글 폰트**: `DejaVu Sans` 폰트 설정 포함

## 📞 문제 해결

### 일반적인 오류
1. **FileNotFoundError**: 원본 데이터 파일 경로 확인
2. **ImportError**: 필요한 라이브러리 설치 확인
3. **PermissionError**: 파일 쓰기 권한 확인
4. **경로 문제**: 절대 경로 설정 확인

### 해결 방법
```bash
# 라이브러리 설치
pip install pandas numpy scikit-learn matplotlib seaborn

# 권한 문제 해결 (Linux/macOS)
chmod +x scripts/*.py

# 경로 문제 해결
python -c "import os; print('현재 작업 디렉토리:', os.getcwd())"
```

## 🔄 워크플로우

### 전체 분석 과정
```bash
# 1. 기존 데이터 전처리
python scripts/data_preprocessing.py

# 2. 하수도 데이터 전처리
python scripts/preprocess_sewer_data.py

# 3. 노트북 생성
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

## 📊 분석 지표

### 사회취약지수 (기존)
- 전체 위험도 (40%)
- 고위험도 (30%)
- 노후주택비율 (30%)

### 하수도 인프라 지수 (신규)
- 하수도설치율 (30%)
- 공공하수처리구역 인구보급률 (30%)
- 고도처리인구 보급률 (20%)
- 인구밀도 정규화 (20%)

---
**마지막 업데이트**: 2025-07-30 
**스크립트 버전**: 2.0 (하수도 인프라 분석 추가) 