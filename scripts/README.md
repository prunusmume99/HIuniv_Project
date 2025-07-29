# 🔧 Python Scripts 폴더

## 📋 폴더 개요
이 폴더는 데이터 전처리 및 노트북 생성을 위한 Python 스크립트들을 포함합니다.

## 📁 파일 목록

### 1. `data_preprocessing.py`
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

### 2. `create_notebook.py`
- **파일 크기**: 15KB (406 lines)
- **생성일**: 2025-07-29
- **설명**: 사회취약지수 분석을 위한 Jupyter Notebook을 프로그래밍 방식으로 생성하는 스크립트

#### 🎯 주요 기능
1. **노트북 구조 생성**
   - `nbformat` 라이브러리 사용
   - 마크다운 셀과 코드 셀 조합
   - 메타데이터 설정

2. **분석 코드 포함**
   - 데이터 로드 및 전처리
   - 사회취약지수 계산
   - 다양한 시각화 (히스토그램, 산점도, 히트맵, 파이차트)
   - 인터랙티브 지도 생성
   - 결과 요약 및 저장

3. **셀 구성**
   - **마크다운 셀**: 제목, 섹션 구분, 설명
   - **코드 셀**: 실제 분석 코드
   - **총 21개 셀**: 체계적인 분석 흐름

#### 🛠️ 주요 함수
```python
def create_social_vulnerability_notebook()  # 노트북 생성 메인 함수
```

#### 🎯 실행 방법
```bash
# 프로젝트 루트에서 실행
python scripts/create_notebook.py

# 또는 scripts 폴더에서 실행
cd scripts
python create_notebook.py
```

#### 📊 출력 결과
- **생성 파일**: `notebooks/02_social_vulnerability_analysis.ipynb`
- **노트북 내용**: 완전한 분석 워크플로우 포함

## 🔧 기술적 세부사항

### 사용된 라이브러리
```python
# data_preprocessing.py
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# create_notebook.py
import nbformat as nbf
from pathlib import Path
```

### 파일 경로 관리
- **상대 경로 사용**: 프로젝트 루트 기준
- **Path 객체**: 크로스 플랫폼 호환성
- **자동 디렉토리 생성**: `mkdir(parents=True, exist_ok=True)`

### 오류 처리
- **try-except 블록**: 각 단계별 오류 처리
- **상세한 오류 메시지**: 디버깅 용이성
- **단계별 검증**: 데이터 품질 보장

## 🚨 주의사항

### data_preprocessing.py
1. **실행 위치**: 프로젝트 루트에서 실행 권장
2. **원본 데이터**: `data/raw/` 폴더에 원본 파일 필요
3. **결과 덮어쓰기**: 기존 `processed_data.csv` 파일 덮어씀
4. **인코딩**: UTF-8 with BOM 사용 (한글 호환성)

### create_notebook.py
1. **의존성**: `nbformat` 라이브러리 필요
2. **결과 덮어쓰기**: 기존 노트북 파일 덮어씀
3. **경로 설정**: 노트북 내 상대 경로 사용
4. **한글 폰트**: `NanumGothic` 폰트 설정 포함

## 📞 문제 해결

### 일반적인 오류
1. **FileNotFoundError**: 원본 데이터 파일 경로 확인
2. **ImportError**: 필요한 라이브러리 설치 확인
3. **PermissionError**: 파일 쓰기 권한 확인

### 해결 방법
```bash
# 라이브러리 설치
pip install pandas numpy nbformat

# 권한 문제 해결 (Linux/macOS)
chmod +x scripts/*.py

# 경로 문제 해결
python -c "import sys; print(sys.path)"
```

## 🔄 워크플로우

### 전체 분석 과정
```bash
# 1. 데이터 전처리
python scripts/data_preprocessing.py

# 2. 노트북 생성 (선택사항)
python scripts/create_notebook.py

# 3. 분석 실행
jupyter notebook notebooks/01_social_vulnerability_analysis.ipynb
```

### 개별 실행
```bash
# 전처리만 실행
python scripts/data_preprocessing.py

# 노트북 생성만 실행
python scripts/create_notebook.py
```

---
**마지막 업데이트**: 2025-07-29  
**스크립트 버전**: 1.0 