SELECT DISTINCT c.course_id, s.sport_name, c.course_name, c.class_days, c.fee
FROM courses c
JOIN sports s ON c.sport_id = s.sport_id
LEFT JOIN enrollments e ON c.course_id = e.course_id
                        AND e.enroll_month = '2026-11'
ORDER BY c.course_id                        
;


SELECT COUNT(m.member_id)
FROM members m
WHERE EXISTS (SELECT 1 FROM members m WHERE m.name = '김하늘');


SELECT m.member_id
FROM members m
WHERE m.name = '박서윤';


SELECT m.member_id
FROM members m
WHERE m.name = '이지혜'; ---결과 없음

SELECT c.fee
FROM courses c
WHERE c.course_id = 1;


SELECT c.course_name
FROM courses c
WHERE c.course_name LIKE '%수영%';







-- 해당 회원 아이디가 수강신청  + 입력받은 강좌 id가 그 신청 id와 똑같으면 / 11월=> 반려


-- 1. 해당 회원의 아이디가 수강신청 테이블에 있고 11월꺼인가???


SELECT m.member_id, e.enroll_month
FROM members m
INNER JOIN enrollments e ON m.member_id = e.member_id AND e.enroll_month = '2026-11'; 

-- 2. 입력받은 숫자 (강좌id)가 그 표에 있는 신청 id와 같은가??

SELECT m.member_id, e.enroll_month, c.course_id, COUNT(c.course_id)
FROM members m
INNER JOIN enrollments e ON m.member_id = e.member_id AND e.enroll_month = '2026-11'
LEFT JOIN courses c ON e.course_id = c.course_id
GROUP BY m.member_id; 
 


SELECT COUNT(*)
FROM enrollments e
LEFT JOIN courses c ON e.course_id = c.course_id
LEFT JOIN members m ON e.member_id = m.member_id
WHERE e.member_id = 2 AND e.enroll_month = '2026-11' AND e.course_id = 2;


SELECT COUNT(*)
FROM enrollments e
WHERE e.member_id = 2 AND e.enroll_month = '2026-11' AND e.course_id = 2;

SELECT c.course_id, c.course_name
FROM courses c
WHERE c.course_name LIKE '%수영%'
ORDER BY c.course_id;