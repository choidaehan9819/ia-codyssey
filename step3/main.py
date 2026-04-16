import json  # 외부 JSON 파일을 읽고 파싱(해석)하기 위한 라이브러리
import time  # 성능 측정(연산 시간 계산)을 위해 고정밀 타이머를 제공하는 라이브러리

# ==========================================
# 1. 코어 연산 및 유틸리티 함수 (알고리즘 엔진부)
# ==========================================

def normalize_label(label):
    # 입력된 문자열을 소문자로 싹 변환하여 대소문자 차이로 인한 오류 방지
    label_lower = label.lower() 
    
    # 리스트 안에 해당 문자열이 포함되어 있는지 확인 (OR 연산과 동일)
    if label_lower in ['+', 'cross']:
        return 'Cross'
    elif label_lower in ['x']:
        return 'X'
    return 'UNDECIDED'

def mac_2d(pattern, filter_matrix, size):
    score = 0.0  # 점수를 누적할 변수 초기화 (float 타입)
    
    # 2차원 배열을 순회하기 위한 이중 반복문 (가로 세로 교차점 탐색)
    for i in range(size):          # 행(Row) 탐색
        for j in range(size):      # 열(Column) 탐색
            # 위치가 일치하는 패턴 값과 필터 값을 곱한 뒤 score에 누적합(+=)
            score += pattern[i][j] * filter_matrix[i][j]
    return score

def mac_1d(pattern_1d, filter_1d, length):
    score = 0.0
    # 2차원과 달리 행/열 구분이 없으므로 단일 반복문으로 한 번에 쭉 스캔
    for i in range(length):
        score += pattern_1d[i] * filter_1d[i]
    return score

def flatten_matrix(matrix):
    # 리스트 컴프리헨션(List Comprehension): 파이썬 특유의 빠르고 간결한 문법
    # 2차원 matrix 안의 row를 꺼내고, 다시 그 row 안의 element를 꺼내 1차원 리스트로 쭉 나열함
    return [element for row in matrix for element in row]

def compare_scores(score_cross, score_x):
    epsilon = 1e-9  # 10의 -9승 (0.000000001). 부동소수점 연산 오차를 무시하기 위한 데드존(Deadzone)
    
    # 두 점수의 차이의 절댓값(abs)이 epsilon보다 작으면 사실상 같은 값으로 취급
    if abs(score_cross - score_x) < epsilon:
        return 'UNDECIDED'
    # 삼항 연산자: score_cross가 크면 'Cross' 반환, 아니면 'X' 반환
    return 'Cross' if score_cross > score_x else 'X'

def measure_performance(func, pattern, filter_matrix, size, iterations=10):
    # time.perf_counter(): OS의 가장 정밀한 시계를 가져옴 (밀리초 단위 측정용)
    start_time = time.perf_counter() 
    
    # 지정된 반복 횟수(iterations)만큼 함수를 빈틈없이 연속 실행하여 부하를 줌
    for _ in range(iterations):
        func(pattern, filter_matrix, size)
        
    end_time = time.perf_counter()
    
    # 총 걸린 시간을 반복 횟수로 나누어 1회당 평균 시간을 구하고, 1000을 곱해 ms(밀리초) 단위로 변환
    avg_time_ms = ((end_time - start_time) / iterations) * 1000
    return avg_time_ms

# ==========================================
# 2. 보너스 과제: 패턴 생성기
# ==========================================

def generate_pattern(size, pattern_type):
    # 크기 size x size이며 모든 값이 0인 2차원 리스트 생성
    matrix = [[0] * size for _ in range(size)]
    mid = size // 2  # 중심점(인덱스) 계산 (예: 5 // 2 = 2)
    
    if pattern_type == 'Cross':
        for i in range(size):
            matrix[i][mid] = 1  # 세로줄 가운데를 1로 켬
            matrix[mid][i] = 1  # 가로줄 가운데를 1로 켬
    elif pattern_type == 'X':
        for i in range(size):
            matrix[i][i] = 1             # 좌상단 -> 우하단 대각선 1로 켬
            matrix[i][size - 1 - i] = 1  # 우상단 -> 좌하단 대각선 1로 켬
    return matrix

# ==========================================
# 3. 모드 1: 사용자 입력 (3x3)
# ==========================================

def get_user_matrix(name, size=3):
    print(f"\n[{name}] {size}x{size} 행렬을 한 줄씩 공백으로 구분하여 입력하세요:")
    matrix = []
    
    for i in range(size):
        while True: # 올바른 값을 입력할 때까지 무한 반복 (입력 방어 로직)
            try:
                # 1. input(): 사용자 입력 문자열 받음 (예: "1 0 1")
                # 2. split(): 공백 기준으로 쪼갬 (['1', '0', '1'])
                # 3. map(float, ...): 쪼개진 문자열을 실수형으로 변환 (아까 얘기한 그 맵 함수!)
                # 4. list(): 변환된 값들을 최종적으로 리스트로 묶음 ([1.0, 0.0, 1.0])
                row = list(map(float, input(f" - {i+1}번째 줄: ").split()))
                
                # 입력된 숫자의 개수가 지정된 size(3)와 다르면 에러 처리 후 다시 입력받음
                if len(row) != size:
                    print(f"입력 형식 오류: 정확히 {size}개의 숫자를 입력해야 합니다.")
                    continue
                    
                matrix.append(row) # 정상 통과 시 matrix 배열에 한 줄 추가
                break # while 루프 탈출, 다음 줄 입력으로 넘어감
                
            except ValueError:
                # 숫자가 아닌 문자('A', '가' 등)가 들어와서 float 변환이 실패할 경우의 예외 처리
                print("입력 형식 오류: 숫자만 입력 가능합니다.")
    return matrix

def mode_1_user_input():
    # 콘솔 출력 및 입력 함수들을 순서대로 호출
    print("\n--- [모드 1] 사용자 입력 (3x3) ---")
    filter_cross = get_user_matrix("Cross 필터")
    filter_x = get_user_matrix("X 필터")
    pattern = get_user_matrix("검사할 패턴")
    
    # 입력받은 행렬들로 2D MAC 연산 함수 호출
    score_cross = mac_2d(pattern, filter_cross, 3)
    score_x = mac_2d(pattern, filter_x, 3)
    
    # 판정 함수 호출
    result = compare_scores(score_cross, score_x)
    
    print(f"\n[결과] Cross 점수: {score_cross}, X 점수: {score_x}")
    print(f"판정: {result}")
    
    # 시간 측정 함수를 호출할 때 함수 이름(mac_2d) 자체를 변수처럼 넘겨줌 (콜백)
    avg_time = measure_performance(mac_2d, pattern, filter_cross, 3)
    print(f"연산 시간(평균): {avg_time:.6f} ms")

# ==========================================
# 4. 모드 2: JSON 로드 및 분석
# ==========================================

def mode_2_json_analysis():
    print("\n--- [모드 2] data.json 분석 및 성능 측정 ---")
    
    # 파일 입출력 처리. 'with' 문을 쓰면 파일을 열고 작업이 끝난 뒤 자동으로 닫아줌(메모리 누수 방지)
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f) # JSON 텍스트를 파이썬의 딕셔너리(Dict) 구조로 변환
    except FileNotFoundError:
        print("오류: data.json 파일을 찾을 수 없습니다.")
        return

    # .get() 메서드: 키가 없어도 에러를 띄우지 않고 빈 딕셔너리({})를 안전하게 반환
    filters = data.get('filters', {})
    patterns = data.get('patterns', {})
    
    total_tests = len(patterns)
    passed = 0
    failed_cases = [] # 실패한 이유를 모아둘 빈 리스트 생성
    
    print(f"총 {total_tests}개의 패턴을 분석합니다...\n")

    # .items()를 통해 키(key)와 값(pattern_data)을 동시에 뽑아내며 순회
    for key, pattern_data in patterns.items():
        # 문자열 쪼개기. 예: 'size_5_01' -> split('_') -> ['size', '5', '01'] -> [1]번째 인덱스인 '5'를 int로 변환
        try:
            size = int(key.split('_')[1])
        except (IndexError, ValueError):
            failed_cases.append((key, "키 형식 오류 (사이즈 추출 불가)"))
            continue
            
        filter_key = f"size_{size}"
        if filter_key not in filters:
            failed_cases.append((key, f"해당 크기의 필터 누락 ({filter_key})"))
            continue
            
        target_filters = filters[filter_key]
        expected_raw = pattern_data.get('expected', '')
        expected_label = normalize_label(expected_raw)
        input_pattern = pattern_data.get('input', [])
        
        # 데이터 무결성 검증 로직. 
        # any() 함수를 통해 입력 패턴 중 단 한 줄이라도 크기가 맞지 않으면 에러로 분류
        if len(input_pattern) != size or any(len(row) != size for row in input_pattern):
            failed_cases.append((key, f"패턴 크기 불일치 (기대값: {size}x{size})"))
            continue
            
        # JSON 안에 필터 이름이 소문자 'cross'일 수도 있고 대문자 'Cross'일 수도 있어 두 경우 모두 대비
        filter_cross = target_filters.get('cross', target_filters.get('Cross'))
        filter_x = target_filters.get('x', target_filters.get('X'))
        
        # 연산 및 결과 판정
        score_cross = mac_2d(input_pattern, filter_cross, size)
        score_x = mac_2d(input_pattern, filter_x, size)
        result_label = compare_scores(score_cross, score_x)
        
        is_pass = (result_label == expected_label) # bool (True or False)
        
        if is_pass:
            passed += 1
        else:
            failed_cases.append((key, f"판정 실패 (예상: {expected_label}, 결과: {result_label})"))
            
        # 포맷팅 출력: '<6.1f'는 6자리를 확보하고 소수점 1자리까지 출력하며 왼쪽 정렬하라는 뜻
        print(f"[{key}] Cross:{score_cross:<6.1f} | X:{score_x:<6.1f} | 판정:{result_label:<8} | 기대:{expected_label:<8} -> {'PASS' if is_pass else 'FAIL'}")

    print("\n=== [결과 리포트 요약] ===")
    print(f"전체 테스트: {total_tests} | 통과: {passed} | 실패: {len(failed_cases)}")
    if failed_cases:
        print("\n[실패 케이스 목록]")
        for case_id, reason in failed_cases:
            print(f" - {case_id}: {reason}")

# ==========================================
# 5. 보너스: 성능 분석 (2D vs 1D 비교 포함)
# ==========================================

def run_performance_analysis():
    print("\n--- [성능 분석 & 보너스(메모리 최적화)] ---")
    print(f"{'크기(NxN)':<12} | {'2D 평균 시간(ms)':<18} | {'1D 평균 시간(ms)':<18} | {'연산 횟수(N^2)':<15}")
    print("-" * 70)
    
    sizes = [3, 5, 13, 25, 50] 
    iterations = 50 
    
    for size in sizes:
        p_2d = generate_pattern(size, 'Cross')
        f_2d = generate_pattern(size, 'Cross')
        
        # 2차원 데이터를 1차원으로 변환 (메모리를 일렬로 쫙 펴줌)
        p_1d = flatten_matrix(p_2d)
        f_1d = flatten_matrix(f_2d)
        
        # 동일한 데이터에 대해 2D 방식과 1D 방식의 시간을 각각 측정
        time_2d = measure_performance(mac_2d, p_2d, f_2d, size, iterations)
        # 1D 배열은 총 길이가 N*N이므로 size * size를 인자로 넘김
        time_1d = measure_performance(mac_1d, p_1d, f_1d, size * size, iterations)
        
        operations = size * size
        print(f"{size}x{size:<9} | {time_2d:<18.6f} | {time_1d:<18.6f} | {operations:<15}")

# ==========================================
# 메인 실행 흐름 (아두이노의 void loop 역할)
# ==========================================

def main():
    while True: # 무한 루프: 사용자가 0을 입력해 break를 호출할 때까지 계속 메뉴를 띄움
        print("\n=== Mini NPU 시뮬레이터 ===")
        print("1. 사용자 입력 모드 (3x3)")
        print("2. data.json 분석 모드")
        print("3. 성능 분석 및 보너스 과제 테스트")
        print("0. 종료")
        
        choice = input("원하는 메뉴를 선택하세요: ")
        
        if choice == '1':
            mode_1_user_input()
        elif choice == '2':
            mode_2_json_analysis()
        elif choice == '3':
            run_performance_analysis()
        elif choice == '0':
            print("프로그램을 종료합니다.")
            break # while 루프를 강제로 깨고 나옴 -> 프로그램 종료
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")

# 파이썬 특유의 진입점(Entry Point) 설정
# 다른 파일에서 이 코드를 import할 때는 메인 루프가 자동으로 실행되지 않게 막고,
# 사용자가 이 파일을 직접 실행했을 때만 main() 함수를 가동시킴
if __name__ == "__main__":
    main()