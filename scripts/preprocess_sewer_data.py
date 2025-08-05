#!/usr/bin/env python3
"""
하수도 인프라 데이터 전처리 스크립트
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

def preprocess_sewer_data():
    """
    하수도 보급률 데이터를 전처리하여 분석용 데이터로 변환
    """
    print("=== 하수도 인프라 데이터 전처리 시작 ===")
    
    # 데이터 로드
    print("1. 데이터 로드 중...")
    df = pd.read_csv('data/raw/Sewer_Coverage_Rate.csv', encoding='utf-8')
    print(f"   원본 데이터: {len(df)}개 행, {len(df.columns)}개 컬럼")
    
    # 필요한 컬럼만 선택
    print("2. 필요한 컬럼 선택 중...")
    essential_cols = [
        '시도', '구군', '행정구역명', '총인구(명)', '총면적',
        '하수도설치율', '공공하수처리구역 인구보급률', '고도처리인구 보급률'
    ]
    
    processed_df = df[essential_cols].copy()
    
    # 결측값 처리 (구군 컬럼 제외)
    # 세종특별자치시는 구군이 없으므로 필요한 컬럼만 선택 후 결측값 처리
    print("3. 결측값 처리 중...")
    essential_cols_for_cleaning = [
        '시도', '행정구역명', '총인구(명)', '총면적',
        '하수도설치율', '공공하수처리구역 인구보급률', '고도처리인구 보급률'
    ]
    processed_df = processed_df[essential_cols_for_cleaning].dropna()
    print(f"   결측값 제거 후: {len(processed_df)}개 행")
    
    # 이상값 처리 (0보다 작거나 100보다 큰 값)
    print("4. 이상값 처리 중...")
    for col in ['하수도설치율', '공공하수처리구역 인구보급률', '고도처리인구 보급률']:
        processed_df = processed_df[
            (processed_df[col] >= 0) & (processed_df[col] <= 100)
        ]
    
    # 인구 밀도 계산 (명/km²)
    print("5. 인구 밀도 계산 중...")
    processed_df['인구밀도'] = processed_df['총인구(명)'] / processed_df['총면적']
    
    # 인구 밀도 이상값 처리 (너무 높은 값 제거)
    processed_df = processed_df[processed_df['인구밀도'] <= 50000]
    
    print(f"   정제 후 데이터: {len(processed_df)}개 행")
    
    # 시도별 데이터 개수 확인
    print("6. 시도별 데이터 개수:")
    region_counts = processed_df['시도'].value_counts()
    print(region_counts)
    
    # 세종특별자치시 포함 여부 확인
    if '세종특별자치시' in processed_df['시도'].values:
        sejong_count = len(processed_df[processed_df['시도'] == '세종특별자치시'])
        print(f"   ✅ 세종특별자치시: {sejong_count}개 행정구역 포함")
    else:
        print("   ❌ 세종특별자치시 데이터가 누락됨")
    
    # 결과 디렉토리 생성
    os.makedirs('data/processed', exist_ok=True)
    
    # 전처리된 데이터 저장
    output_path = 'data/processed/sewer_infrastructure_processed.csv'
    processed_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"\n=== 전처리 완료 ===")
    print(f"전처리된 데이터 저장: {output_path}")
    print(f"총 {len(processed_df)}개 행정구역 데이터 준비 완료")
    
    return processed_df, output_path

def main():
    """메인 실행 함수"""
    try:
        processed_df, output_path = preprocess_sewer_data()
        print(f"\n✅ 전처리 성공!")
        print(f"📁 저장 위치: {output_path}")
        print(f"📊 데이터 크기: {len(processed_df)}개 행, {len(processed_df.columns)}개 컬럼")
        
    except Exception as e:
        print(f"❌ 전처리 중 오류 발생: {str(e)}")
        return None

if __name__ == "__main__":
    main() 