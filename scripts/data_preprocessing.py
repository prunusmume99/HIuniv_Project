#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
데이터 전처리 스크립트
자연재해위험도와 노후주택비율 데이터를 전처리하여 사회취약지수 계산에 활용
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

def load_data():
    """원본 데이터 로딩"""
    try:
        # 데이터 경로 설정
        data_path = Path("data/raw")
        
        # 데이터 로딩
        disaster_risk = pd.read_csv(data_path / "Natural_Disaster_Risk.csv")
        housing_ratio = pd.read_csv(data_path / "aged_housing_ratio.csv")
        
        print("✅ 데이터 로딩 완료")
        print(f"   - 자연재해위험 데이터: {disaster_risk.shape}")
        print(f"   - 노후주택비율 데이터: {housing_ratio.shape}")
        
        return disaster_risk, housing_ratio
    
    except FileNotFoundError as e:
        print(f"❌ 데이터 파일을 찾을 수 없습니다: {e}")
        return None, None
    except Exception as e:
        print(f"❌ 데이터 로딩 중 오류 발생: {e}")
        return None, None

def preprocess_disaster_data(df):
    """자연재해위험 데이터 전처리"""
    try:
        df_clean = df.copy()
        
        # 첫 번째 행을 컬럼명으로 설정
        df_clean.columns = df_clean.iloc[0]
        df_clean = df_clean.iloc[1:].reset_index(drop=True)
        
        # 두 번째 행을 컬럼명으로 설정
        df_clean.columns = df_clean.iloc[0]
        df_clean = df_clean.iloc[1:].reset_index(drop=True)
        
        # 2023년 데이터만 선택 (첫 번째 컬럼이 지역명, 나머지가 데이터)
        df_2023 = df_clean.iloc[:, [0, 1, 2, 3, 4]].copy()
        
        # 숫자형으로 변환
        numeric_columns = df_2023.columns[1:]  # 첫 번째 컬럼(지역명) 제외
        for col in numeric_columns:
            df_2023[col] = pd.to_numeric(df_2023[col], errors='coerce')
        
        # 컬럼명 정리
        df_2023.columns = ['region', 'total_risk', 'high_risk', 'medium_risk', 'low_risk']
        
        print("✅ 자연재해위험 데이터 전처리 완료")
        return df_2023
    
    except Exception as e:
        print(f"❌ 자연재해위험 데이터 전처리 중 오류: {e}")
        return None

def preprocess_housing_data(df):
    """노후주택비율 데이터 전처리"""
    try:
        df_clean = df.copy()
        
        # 첫 번째 행을 컬럼명으로 설정
        df_clean.columns = df_clean.iloc[0]
        df_clean = df_clean.iloc[1:].reset_index(drop=True)
        
        # 두 번째 행을 컬럼명으로 설정
        df_clean.columns = df_clean.iloc[0]
        df_clean = df_clean.iloc[1:].reset_index(drop=True)
        
        # 2023년 데이터만 선택 (2023.2 분기 - 마지막 3개 컬럼)
        # 컬럼 구조: 지역명, 2023, 2023.1, 2023.2 (각각 비율, 노후주택수, 전체주택수)
        housing_2023 = df_clean.iloc[:, [0, -3, -2, -1]].copy()  # 지역명, 2023.2의 3개 컬럼
        
        # 숫자형으로 변환
        numeric_columns = housing_2023.columns[1:]  # 첫 번째 컬럼(지역명) 제외
        for col in numeric_columns:
            housing_2023[col] = pd.to_numeric(housing_2023[col], errors='coerce')
        
        # 컬럼명 정리
        housing_2023.columns = ['region', 'aged_housing_ratio', 'aged_housing_count', 'total_housing_count']
        
        print("✅ 노후주택비율 데이터 전처리 완료")
        return housing_2023
    
    except Exception as e:
        print(f"❌ 노후주택비율 데이터 전처리 중 오류: {e}")
        return None

def merge_data(disaster_data, housing_data):
    """데이터 통합"""
    try:
        # 지역명 매핑 딕셔너리
        region_mapping = {
            '서울특별시': '서울특별시',
            '부산광역시': '부산광역시',
            '대구광역시': '대구광역시',
            '인천광역시': '인천광역시',
            '광주광역시': '광주광역시',
            '대전광역시': '대전광역시',
            '울산광역시': '울산광역시',
            '세종특별자치시': '세종특별자치시',
            '경기도': '경기도',
            '강원특별자치도': '강원도',
            '충청북도': '충청북도',
            '충청남도': '충청남도',
            '전북특별자치도': '전라북도',
            '전라남도': '전라남도',
            '경상북도': '경상북도',
            '경상남도': '경상남도',
            '제주특별자치도': '제주특별자치도'
        }
        
        # 지역명 통일
        disaster_data['region'] = disaster_data['region'].map(region_mapping)
        housing_data['region'] = housing_data['region'].map(region_mapping)
        
        # 데이터 통합
        merged_data = pd.merge(disaster_data, housing_data, on='region', how='inner')
        
        print("✅ 데이터 통합 완료")
        print(f"   - 통합된 데이터: {merged_data.shape}")
        
        return merged_data
    
    except Exception as e:
        print(f"❌ 데이터 통합 중 오류: {e}")
        return None

def save_processed_data(data, filename):
    """전처리된 데이터 저장"""
    try:
        # 저장 경로 생성
        save_path = Path("data/processed")
        save_path.mkdir(parents=True, exist_ok=True)
        
        # 데이터 저장
        file_path = save_path / filename
        data.to_csv(file_path, index=False, encoding='utf-8-sig')
        
        print(f"✅ 데이터 저장 완료: {file_path}")
        return True
    
    except Exception as e:
        print(f"❌ 데이터 저장 중 오류: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 데이터 전처리 시작...")
    
    # 1. 데이터 로딩
    disaster_risk, housing_ratio = load_data()
    if disaster_risk is None or housing_ratio is None:
        return
    
    # 2. 데이터 전처리
    disaster_clean = preprocess_disaster_data(disaster_risk)
    housing_clean = preprocess_housing_data(housing_ratio)
    
    if disaster_clean is None or housing_clean is None:
        return
    
    # 3. 데이터 통합
    merged_data = merge_data(disaster_clean, housing_clean)
    if merged_data is None:
        return
    
    # 4. 데이터 저장
    success = save_processed_data(merged_data, "processed_data.csv")
    
    if success:
        print("\n🎉 데이터 전처리 완료!")
        print("\n📊 전처리 결과:")
        print(merged_data.head())
        print(f"\n📈 데이터 요약:")
        print(f"   - 총 지역 수: {len(merged_data)}")
        print(f"   - 평균 자연재해위험지구: {merged_data['total_risk'].mean():.1f}개")
        print(f"   - 평균 노후주택비율: {merged_data['aged_housing_ratio'].mean():.1f}%")
    else:
        print("\n❌ 데이터 전처리 실패")

if __name__ == "__main__":
    main() 