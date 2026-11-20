# psycopg 모듈 import
import psycopg
from psycopg.rows import dict_row #?

# DB 접속 정보(DSN: Data Source Name) 작성
# dbname이랑 컨테이너 이름, 커넥션 이름 헷갈리지 말기 --팁? 다 똑같이 하면?
DSN = "host=localhost port=5432 dbname=sportscenter user=postgres password=admin1234"

MONTH = "2026-01"

LIST_SQL = """
SELECT DISTINCT c.course_id, s.sport_name, c.course_name, c.class_days, c.fee
FROM courses c
JOIN sports s ON c.sport_id = s.sport_id
LEFT JOIN enrollments e ON c.course_id = e.course_id
                        AND e.enroll_month = %s
ORDER BY c.course_id                        
"""


# 회원이름으로 id 찾는 SQL 
ID_CHECK_SQL = """
SELECT m.member_id
FROM members m
WHERE m.name = %s
"""



# 수강료 추출 SQL
FEE_CHEKC_SQL = """
SELECT c.fee
FROM courses c
WHERE c.course_id = %s
"""

# 강좌명 검색 SQL
SEARCH_COURSE_SQL ="""
SELECT c.course_name
FROM courses c
WHERE c.course_name = '%수영%'
"""


# 수강 신청가능 목록 조회
def list_courses(conn):
    for c in conn.execute(LIST_SQL, (MONTH,)):
        print(f"{c['course_id']:>3} | {c['sport_name']} | {c['course_name']} | {c['class_days']} | {c['fee']:,}원")

# TODO: 입력 로직 구현

# 1. 회원이름으로 회원 ID 추출
def id_check(conn):
    while True:
        name_input = input("회원 이름을 입력하세요 : ").strip()
        break
    id = conn.execute(ID_CHECK_SQL,(name_input,)).fetchone()
    print(id)
    

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
    fee = conn.execute(FEE_CHEKC_SQL, (course_id_input,)).fetchone()
    print(fee)

# 3. 강좌 검색
def search_courses(conn):
    while True:
        course_keyword = input("찾으시려는 강좌명을 입력하세요 (종료는 q): ")
        if = 'q':
            courses_list = conn.execute(SEARCH_COURSE_SQL, (course_keyword,))
            break

# 수강 신청
def enroll(conn, member_id, course_id):
    # TODO: 신청한 강좌의 수강료 추출
    # fee = 0
    conn.execute(
        "INSERT INTO enrollments (member_id, course_id, enroll_month, status, pay_amount)"
        "VALUES (%s, %s, %s, '수강중', %s)",
        (member_id, course_id, MONTH, fee)
    )
    print("수강신청 완료되었습니다.")

def main():
    # .connect는 db에 접속하겠다라고 하는 메서드(접속 정보) 전달, conn은 connect 의미 별칭
    # 접속 정보는 메모리에 계속 떠있는데 with 구문 벗어나면 접속 끝나고 메모리 해제
    # 접속 중에 해야하는 것 with 안에서 모든 것 해야함(?)
    with psycopg.connect(DSN, row_factory=dict_row) as conn: # row_factory:딕셔너리형태로 튜플가져옴
        # 수강 신청
        # enroll(conn, MEMBER_ID, COURSE_ID)
        # 수강 목록
        # list_courses(conn)
        # select는 from 이하절 생략 가능
        # 하나one row만 넘어오는 경우임, fetchone
        # row = conn.execute("SELECT current_database(), current_user").fetchone() - 튜플로 받아옴
        # print("연결 성공 : ", row) -- 확인용 코드
        # rows = conn.execute("SELECT course_id, course_name, fee FROM courses LIMIT 5").fetchall()
        # # print(rows)
        # for row in rows:
        #     print(row["course_name"], row["fee"])
        id_check(conn)
        fee_check(conn)





         
if __name__ == "__main__":
    main()



# export VIRTUAL_ENV="$(cygpath -w "$VIRTUAL_ENV")"