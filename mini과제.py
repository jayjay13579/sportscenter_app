import psycopg
from psycopg.rows import dict_row

DSN = "host=localhost port=5432 dbname=sportscenter user=postgres password=admin1234"

MONTH = "2026-11"

LIST_SQL = """
SELECT DISTINCT c.course_id, s.sport_name, c.course_name, c.class_days, c.fee
FROM courses c
JOIN sports s ON c.sport_id = s.sport_id
LEFT JOIN enrollments e ON c.course_id = e.course_id
                        AND e.enroll_month = %s
ORDER BY c.course_id                        
"""

# 기존 회원인지 확인
MEMBER_CHECK_SQL = """
SELECT COUNT(*)
FROM members m
WHERE m.name = %s
"""

# 회원이름으로 id 찾는 SQL 
ID_CHECK_SQL = """
SELECT m.member_id
FROM members m
WHERE m.name = %s
"""

# 중복 확인
DUPLICATE_CHECK_SQL = """
SELECT COUNT(*)
FROM enrollments e
WHERE e.member_id = %s AND e.enroll_month = %s AND e.course_id = %s
"""

# 수강료 추출 SQL
FEE_CHEKC_SQL = """
SELECT c.course_id, c.fee
FROM courses c
WHERE c.course_id = %s
"""

# 강좌명 검색 SQL
SEARCH_COURSE_SQL ="""
SELECT c.course_id, c.course_name
FROM courses c
WHERE c.course_name LIKE %s
ORDER BY c.course_id
"""

# 수강 신청가능 목록 조회
def list_courses(conn):
    for c in conn.execute(LIST_SQL, (MONTH,)):
        print(f"{c['course_id']:>3} | {c['sport_name']} | {c['course_name']} | {c['class_days']} | {c['fee']:,}원")


# 1. 회원이름으로 회원 ID 추출
def id_check(conn):
    name_input = input("회원 이름을 입력하세요 : ").strip()

    already_member = conn.execute(MEMBER_CHECK_SQL, (name_input,)).fetchone()
    
    if already_member['count'] == 0:
        print("새로운 회원으로 등록합니다.")
        gender = input("성별을 입력하세요 (M/F): ").strip()
        birth_year = int(input("생년을 입력하세요 (ex: 2026) : ").strip())
        # null해도 괜찮은 phone, email, region은 생략
        conn.execute(
                "INSERT INTO members (name, gender, birth_year, join_date)"
                "VALUES (%s, %s, %s, CURRENT_DATE)",
                (name_input, gender, birth_year)
            )
        print("등록완료되셨습니다.")
    
    id = conn.execute(ID_CHECK_SQL,(name_input,)).fetchone()
        # insert 시키고 id 가져오기 

    return id
    

# 2. 신청한 강좌의 수강료 추출
def fee_check(conn):
    while True:
        course_id_input = input("신청할 강좌의 id를 입력하세요 (1~14): ").strip()
        if course_id_input.isdigit() and int(course_id_input) in range(1,15):
            course_id_input = int(course_id_input)
            break
        else:
            print("1~14까지의 숫자만 입력해주세요")
            continue
    course_info = conn.execute(FEE_CHEKC_SQL, (course_id_input,)).fetchone()
    print(f"해당 강좌의 수강료는 {course_info['fee']}원 입니다.")
    return course_info


# 3. 강좌 검색
def search_courses(conn):
    while True:
        course_keyword = input("찾으시려는 강좌명을 입력하세요 (종료는 q): ").strip()
        if course_keyword.lower() == 'q' :
            break
        courses_list = conn.execute(SEARCH_COURSE_SQL, (f"%{course_keyword}%",)).fetchall()
        for row in courses_list:
            print(f"{row['course_id']:<3} | {row['course_name']}")


# 4. 등록 전 중복여부 검사
def duplicate_check(conn, MEMBER_ID, MONTH, COURSE_ID):
    check_result = conn.execute(DUPLICATE_CHECK_SQL,(MEMBER_ID, MONTH, COURSE_ID)).fetchone()
    if check_result['count'] == 0 : # 등록가능
        return True
    else:
        print("이미 동일 강좌를 신청하셨습니다.")
        return False

# 5. 수강 신청
def enroll(conn, member_id, course_id, fee):
    conn.execute(
        "INSERT INTO enrollments (member_id, course_id, enroll_month, status, pay_amount)"
        "VALUES (%s, %s, %s, '수강중', %s)",
        (member_id, course_id, MONTH, fee)
    )
    print("수강신청 완료되었습니다.")


# 메인 함수

def main():
    with psycopg.connect(DSN, row_factory=dict_row) as conn:
        list_courses(conn) 
        search_courses(conn)
        MEMBER_ID = id_check(conn)['member_id']
        while True:
            result = fee_check(conn)
            COURSE_ID = result['course_id']
            FEE = result['fee']
            if duplicate_check(conn, MEMBER_ID, MONTH, COURSE_ID) == False:
                continue
            enroll(conn, MEMBER_ID, COURSE_ID, FEE)
            break




         
if __name__ == "__main__":
    main()

