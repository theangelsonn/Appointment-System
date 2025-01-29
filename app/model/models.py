import mysql.connector


def get_db_connection():
    # 建立與 MySQL 資料庫的連接
    connection = mysql.connector.connect(
        # 資料庫主機位置
        host='localhost',
        # 資料庫使用者名稱
        user='root',
        # 資料庫密碼
        password='REDACTED_PASSWORD',
        # 要連接的資料庫名稱
        database='appointment_system'
    )
    # 返回資料庫連接物件
    return connection


class Account:
    """
    帳號類別：用於管理使用者帳號資訊
    """

    def __init__(self, accountID, account, password, role):
        """
        初始化帳號物件
        參數說明：
        accountID: 帳號唯一識別碼
        account: 使用者帳號名稱（通常是電子郵件）
        password: 帳號密碼
        role: 使用者角色 (0:學生, 1:教授, 2:秘書)
        """
        self.accountID = accountID    # 帳號ID
        self.account = account        # 帳號名稱
        self.password = password      # 帳號密碼
        self.role = role             # 使用者角色


def get_account_by_account(account):
    """
    根據帳號名稱查詢使用者帳號資訊
    參數：
    account: 使用者帳號名稱（通常是電子郵件）
    返回：
    如果找到帳號，返回 Account 物件
    如果未找到，返回 None
    """
    # 建立資料庫連接
    connection = get_db_connection()
    # 建立游標物件，設定返回字典格式的結果
    cursor = connection.cursor(dictionary=True)
    # SQL 查詢語句，使用參數化查詢防止 SQL 注入
    query = "SELECT * FROM account WHERE account = %s"
    # 執行查詢，傳入帳號參數
    cursor.execute(query, (account,))
    # 獲取查詢結果的第一行
    row = cursor.fetchone()
    # 關閉游標
    cursor.close()
    # 關閉資料庫連接
    connection.close()
    # 印出查詢的帳號（用於除錯）
    print(f"user_account: {account}")
    # 如果找到帳號資料
    if row:
        # 將查詢結果轉換為 Account 物件並返回
        return Account(**row)
    # 如果未找到帳號資料，返回 None
    return None


def get_professors():
    """
    獲取所有教授的基本資訊
    返回：
    包含所有教授資料的列表，每個教授包含：
    - name: 教授姓名
    - professorship: 教授職稱
    - photo: 教授照片
    - professorID: 教授ID
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT name, professorship, photo, professorID FROM professor")
    # 獲取所有查詢結果
    professors = cursor.fetchall()
    connection.close()
    # 返回教授資料列表
    return professors


def get_account_by_account_id(account_id):
    """
    根據帳號ID查詢使用者帳號資訊
    參數：
    account_id: 帳號唯一識別碼
    返回：
    如果找到帳號，返回帳號資訊元組
    如果未找到，返回 None
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM account where accountID = %s", (account_id,))
    account = cursor.fetchone()
    connection.close()
    return account


def get_professor_by_id(professor_id):
    """
    根據教授ID查詢教授資訊
    參數：
    professor_id: 教授唯一識別碼
    返回：
    如果找到教授，返回教授資訊元組
    如果未找到，返回 None
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM professor WHERE professorID = %s", (professor_id,))
    professor = cursor.fetchone()
    connection.close()
    return professor


def get_otherinfo(professor_id):
    """
    獲取教授的其他相關資訊（如實驗室資訊、研究領域等）
    參數：
    professor_id: 教授唯一識別碼
    返回：
    如果找到資訊，返回包含其他資訊的元組
    如果未找到，返回 None
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM otherinfo WHERE professorID = %s", (professor_id,))
    otherinfo = cursor.fetchone()
    connection.close()
    return otherinfo


def get_appointmentslot(professor_id):
    """
    獲取教授的預約時段資訊
    參數：
    professor_id: 教授唯一識別碼
    返回：
    如果找到資訊，返回包含預約時段的元組
    如果未找到，返回 None
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM appointmentslot WHERE professorID = %s", (professor_id,))
    appointmentslot = cursor.fetchone()
    connection.close()
    return appointmentslot


def get_professor_by_account_id(account_id):
    """
    根據帳號ID查詢對應的教授資訊
    參數：
    account_id: 帳號唯一識別碼
    返回：
    如果找到教授，返回教授資訊元組
    如果未找到，返回 None
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM professor WHERE accountID = %s", (account_id,))
    professor = cursor.fetchone()
    connection.close()
    return professor


def update_appointment_slots(professor_id, new_slot):
    """
    更新教授的預約時段資訊
    參數：
    professor_id: 教授唯一識別碼
    new_slot: 新的預約時段資訊
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE appointmentslot SET availableTimeInfo = %s WHERE professorID = %s", (new_slot, professor_id))
    # 提交資料庫變更
    connection.commit()
    connection.close()


def update_notice(professor_id, new_notice):
    """
    更新教授的面試注意事項
    參數：
    professor_id: 教授唯一識別碼
    new_notice: 新的面試注意事項內容
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE otherinfo SET interviewPrecautions = %s WHERE professorID = %s", (new_notice, professor_id))
    connection.commit()
    connection.close()


def update_lab_rule(professor_id, new_lab_rule):
    """
    更新教授的實驗室規則/說明
    參數：
    professor_id: 教授唯一識別碼
    new_lab_rule: 新的實驗室規則/說明內容
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE otherinfo SET labDescription = %s WHERE professorID = %s",
                   (new_lab_rule, professor_id))
    connection.commit()
    connection.close()


def update_research_area(professor_id, new_research_area):
    """
    更新教授的研究領域資訊
    參數：
    professor_id: 教授唯一識別碼
    new_research_area: 新的研究領域內容
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE otherinfo SET researchField = %s WHERE professorID = %s",
                   (new_research_area, professor_id))
    connection.commit()
    connection.close()


def update_reservationOpen_status(professor_id, new_status):
    """
    更新教授的預約開放狀態
    參數：
    professor_id: 教授唯一識別碼
    new_status: 新的預約開放狀態 (0:關閉預約, 1:開放預約）
    """
    # 印出更新資訊（用於除錯）
    print(f"professor_id: {professor_id}, new_status: {new_status}")
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE otherinfo SET reservationOpen = %s WHERE professorID = %s", (new_status, professor_id))
    connection.commit()
    connection.close()


def get_student_count(professor_id):
    """
    獲取特定教授目前指導的學生人數
    參數：
    professor_id: 教授唯一識別碼
    返回：
    已接受指導的學生人數 (status = 1 表示已接受指導）
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM mentorshiprequest WHERE professorID = %s AND status = 1", (professor_id,))
    # 獲取查詢結果（計數值）
    student_count = cursor.fetchone()[0]
    connection.close()
    return student_count


def get_student_by_account_id(account_id):
    """
    根據帳號ID查詢對應的學生資訊
    參數：
    account_id: 帳號唯一識別碼
    返回：
    如果找到學生，返回學生資訊元組
    如果未找到，返回 None
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT name, email, phone, department, admissionYear, rankType, rank, studentID, photo FROM student WHERE accountID = %s", (account_id,))
    student = cursor.fetchone()
    connection.close()
    return student


def update_student_profile(account_id, name, password, account, email, phone, photo):
    connection = get_db_connection()
    cursor = connection.cursor()
    if photo:
        cursor.execute("UPDATE student SET name = %s, email = %s, phone = %s, photo = %s WHERE accountID = %s",
                       (name, email, phone, photo, account_id))
    else:
        cursor.execute("UPDATE student SET name = %s, email = %s, phone = %s WHERE accountID = %s",
                       (name, email, phone, account_id))
    connection.commit()
    cursor = connection.cursor()
    cursor.execute("UPDATE account SET account = %s, password = %s WHERE accountID = %s",
                   (account, password, account_id))
    connection.commit()
    connection.close()


def update_professor_profile(account_id, name, password, account, professorship, email, phone, photo):
    connection = get_db_connection()
    cursor = connection.cursor()
    if photo:
        cursor.execute("UPDATE professor SET name = %s, professorship = %s, email = %s, phone = %s, photo = %s WHERE accountID = %s",
                       (name, professorship, email, phone, photo, account_id))
    else:
        cursor.execute("UPDATE professor SET name = %s, professorship = %s, email = %s, phone = %s WHERE accountID = %s",
                       (name, professorship, email, phone, account_id))
    connection.commit()
    cursor = connection.cursor()
    cursor.execute("UPDATE account SET account = %s, password = %s WHERE accountID = %s",
                   (account, password, account_id))
    connection.commit()
    connection.close()

# 從這開始多申請預約功能


def create_appointment(professor_id, student_id, start_time, end_time, resume_filename, note=''):
    """
    創建預約面談記錄
    參數說明：
    professor_id: 教授ID
    student_id: 學生帳號ID
    start_time: 預約開始時間
    end_time: 預約結束時間
    resume_filename: 履歷檔案名稱
    note: 備註(可選)
    """
    connection = get_db_connection()
    cursor = connection.cursor(buffered=True)
    try:
        # 檢查學生是否已存在於資料庫
        cursor.execute("""
            SELECT studentID, name FROM student WHERE accountID = %s
        """, (student_id,))
        student_result = cursor.fetchone()

        if student_result:
            # 如果學生存在，直接使用現有的學生ID
            actual_student_id = student_result[0]
        else:
            # 如果學生不存在，則創建新的學生記錄
            cursor.execute(
                "SELECT account FROM account WHERE accountID = %s", (student_id,))
            account_info = cursor.fetchone()
            student_email = account_info[0]
            student_name = student_email.split('@')[0]

            # 插入新學生資料，設定預設的考試資訊
            cursor.execute("""
                INSERT INTO student 
                (accountID, name, email, phone, department, admissionYear, rankType, `rank`)
                VALUES 
                (%s, %s, %s, '09REDACTED_PASSWORD', '資管系', '113', '考試-備取', 1)
            """, (student_id, student_name, student_email))
            connection.commit()
            actual_student_id = cursor.lastrowid

        # 創建預約記錄
        cursor.execute("""
            INSERT INTO appointment 
            (professorID, studentID, startTime, endTime, resume, note, status, requestDate, approvalDate)
            VALUES 
            (%s, %s, %s, %s, %s, %s, 0, CURDATE(), NULL)
        """, (professor_id, actual_student_id, start_time, end_time, resume_filename, note))
        connection.commit()
        return True

    except Exception as e:
        print(f"預約創建錯誤: {str(e)}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def get_appointments_by_professor(professor_id):
    """
    獲取特定教授的所有預約記錄
    按照申請日期降序排列，並根據考試類型排序
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                a.*,
                s.name as student_name,  # 學生姓名
                s.rankType,              # 考試類型
                s.rank,                  # 名次
                CASE 
                    WHEN s.rankType IS NOT NULL AND s.rank IS NOT NULL 
                    THEN CONCAT(
                        s.rankType,      # 組合考試類型
                        
                        CAST(s.rank as CHAR)
                        
                    )
                    ELSE '尚未設定'
                END as rank_info,        # 完整排名資訊
                s.email                  # 學生信箱
            FROM appointment a
            JOIN student s ON a.studentID = s.studentID
            WHERE a.professorID = %s
            ORDER BY 
                a.requestDate DESC,      # 優先按申請日期排序
                s.rank ASC               # 再按名次排序
        """
        cursor.execute(query, (professor_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_student_appointments(account_id):
    """
    獲取特定學生的所有預約記錄
    包含教授資訊和預約狀態
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                a.*,                     # 預約相關資訊
                p.name as professor_name, # 教授姓名
                p.photo                  # 教授照片
            FROM appointment a
            JOIN professor p ON a.professorID = p.professorID
            JOIN student s ON a.studentID = s.studentID
            WHERE s.accountID = %s       # 篩選特定學生的預約
            ORDER BY a.requestDate DESC   # 按申請日期做降序排序
        """
        cursor.execute(query, (account_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def update_appointment_status(appointment_id, new_status, approval_date=None):
    """
    更新預約狀態
    new_status: 0-待回覆, 1-已確認, 2-已拒絕
    approval_date: 審核日期(可選)
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    if approval_date:
        query = """
            UPDATE appointment 
            SET status = %s, approvalDate = %s 
            WHERE appointmentID = %s
        """
        cursor.execute(query, (new_status, approval_date, appointment_id))
    else:
        query = "UPDATE appointment SET status = %s WHERE appointmentID = %s"
        cursor.execute(query, (new_status, appointment_id))
    connection.commit()
    cursor.close()
    connection.close()


def get_all_professors():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT p.*, a.account, a.password, o.*
        FROM professor p
        JOIN account a ON p.accountID = a.accountID
        JOIN otherInfo o ON p.professorID = o.professorID;
    """)
    professors = cursor.fetchall()
    connection.close()
    return professors


def get_all_students():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT s.*, a.account, a.password
        FROM student s
        JOIN account a ON s.accountID = a.accountID
    """)
    students = cursor.fetchall()
    connection.close()
    return students


def delete_student(account_id):
    # print(f"account_id: {account_id}")
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM student WHERE accountID = %s", (account_id,))
    cursor.execute("DELETE FROM account WHERE accountID = %s", (account_id,))
    connection.commit()
    connection.close()


def delete_professor(account_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM professor WHERE accountID = %s", (account_id,))
    cursor.execute("DELETE FROM account WHERE accountID = %s", (account_id,))
    connection.commit()
    connection.close()


def create_student_account(name, email, rankType, rank, department, admissionYear):
    print(f"name: {name, email, rankType, rank, department, admissionYear}")
    connection = get_db_connection()
    cursor = connection.cursor()

    # 插入帳號資料
    cursor.execute(
        "INSERT INTO account (account, role) VALUES (%s, %s)", (email, 0,))
    account_id = cursor.lastrowid

    # 插入學生資料
    cursor.execute("""
        INSERT INTO student (accountID, name, rankType, rank, department, admissionYear, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (account_id, name, rankType, rank, department, admissionYear, email))

    connection.commit()
    connection.close()


def create_pro_account(name, email, department, professorship, location, labStudentNum):
    print(f"name: {name, email, department, professorship}")
    connection = get_db_connection()
    cursor = connection.cursor()

    # 插入帳號資料
    cursor.execute(
        "INSERT INTO account (account, role) VALUES (%s, %s)", (email, 1,))
    account_id = cursor.lastrowid

    # 插入教授資料
    cursor.execute("""
        INSERT INTO professor (accountID, name, email, department, professorship)
        VALUES (%s, %s, %s, %s, %s)
    """, (account_id, name, email, department, professorship,))
    professor_id = cursor.lastrowid
    print(f"professor_id: {professor_id}")
    cursor.execute("""
        INSERT INTO otherInfo (professorID, location, labStudentNum)
        VALUES (%s, %s, %s)
    """, (professor_id, location, labStudentNum,))
    cursor.execute("""
        INSERT INTO appointmentslot (professorID)
        VALUES (%s)
    """, (professor_id,))

    connection.commit()
    connection.close()

# 秉謙
# 獲取所有教授的名字


def get_all_professor_names():
    connection = get_db_connection()
    cursor = connection.cursor()

    # 從 professor 表中獲取所有教授的名字
    cursor.execute("SELECT name FROM professor")
    professors = cursor.fetchall()

    cursor.close()
    connection.close()

    # 將查詢結果轉換為名字列表並返回
    return [professor[0] for professor in professors]


# 創建指導邀請
def create_mentorship_request(professor_id, student_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # SQL 查詢：插入新的指導邀請記錄
        # status = 0 表示待回覆狀態
        # CURDATE() 獲取當前日期作為請求日期
        query = """
            INSERT INTO mentorshiprequest (professorID, studentID, status, requestDate)
            VALUES (%s, %s, 0, CURDATE())
        """
        # 執行 SQL 查詢，插入新記錄
        cursor.execute(query, (professor_id, student_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


# 獲取教授ID
def get_professor_id_by_name(name):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT professorID FROM professor WHERE name = %s", (name,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] if result else None


def check_existing_student(rankType, rank):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM student WHERE rankType = %s AND rank = %s", (rankType, rank,))
    count = cursor.fetchone()[0]
    # print(f"count: {count}")
    connection.close()
    return count > 0


def check_existing_account(account):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM account WHERE account = %s", (account,))
    count = cursor.fetchone()[0]
    # print(f"account_count: {count}")
    connection.close()
    return count > 0


def check_existing_location(location):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM otherinfo WHERE location = %s", (location,))
    count = cursor.fetchone()[0]
    print(f"location_count: {count}")
    connection.close()
    return count > 0

# 獲取學生指導邀請紀錄


def get_student_mentorship_requests(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 執行 SQL 查詢，獲取學生的指導邀請記錄
        # 查詢包含：教授名字、邀請狀態、申請日期和審核日期
        cursor.execute("""
            SELECT p.name, 
                   CASE m.status 
                       WHEN 0 THEN '待回覆'
                       WHEN 1 THEN '同意邀請'
                       WHEN 2 THEN '拒絕邀請'
                   END as status,
                   m.requestDate,
                   m.approvalDate
            FROM mentorshiprequest m
            JOIN professor p ON m.professorID = p.professorID
            WHERE m.studentID = %s
            ORDER BY m.requestDate DESC
        """, (student_id,))

        records = []
        for row in cursor.fetchall():
            records.append({
                'professorName': row[0],
                'status': row[1],
                'submissionTime': row[2].strftime('%Y-%m-%d') if row[2] else '',
                'reviewTime': row[3].strftime('%Y-%m-%d') if row[3] else '尚未審核'
            })
        return records
    finally:
        cursor.close()
        connection.close()


# 獲取學生ID
def get_student_id_by_account_id(account_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 查詢 student 表中與 accountID 對應的 studentID
        cursor.execute("""
            SELECT studentID 
            FROM student 
            WHERE accountID = %s
        """, (account_id,))
        result = cursor.fetchone()
        # 如果查詢結果存在，返回 studentID，否則返回 None
        return result[0] if result else None
    finally:
        cursor.close()
        connection.close()


# 獲取教授的指導請求記錄
def get_professor_mentorship_requests(professor_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT 
                s.name,
                s.email,
                s.rankType,
                s.rank,
                m.requestDate,
                m.status,
                s.studentID,
                m.professorID,
                m.mentorshipRequestID
            FROM mentorshiprequest m
            JOIN student s ON m.studentID = s.studentID
            WHERE m.professorID = %s AND m.status = 0
            ORDER BY m.requestDate DESC
        """, (professor_id,))

        records = []
        for row in cursor.fetchall():
            records.append({
                'name': row[0],
                'email': row[1],
                'rankType': row[2],
                'rank': row[3],
                'requestDate': row[4].strftime('%Y-%m-%d') if row[4] else '',
                'status': row[5],
                'studentID': row[6],
                'professorID': row[7],
                'requestID': row[8]  # 新增 mentorshipRequestID
            })
        return records
    finally:
        cursor.close()
        connection.close()


def update_mentorship_request_status(studentID, professorID, student_name, new_status, request_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 更新狀態和審核日期，增加 mentorshipRequestID 的條件
        cursor.execute("""
            UPDATE mentorshiprequest
            SET status = %s, approvalDate = CURDATE()
            WHERE studentID = %s 
            AND professorID = %s 
            AND mentorshipRequestID = %s
        """, (new_status, studentID, professorID, request_id))
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def get_professor_mentorship_history(professor_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT 
                s.name,
                CASE m.status 
                    WHEN 1 THEN '同意邀請'
                    WHEN 2 THEN '拒絕邀請'
                END as status,
                m.approvalDate
            FROM mentorshiprequest m
            JOIN student s ON m.studentID = s.studentID
            WHERE m.professorID = %s 
            AND m.status IN (1, 2)
            ORDER BY m.approvalDate DESC
        """, (professor_id,))

        records = []
        for row in cursor.fetchall():
            records.append({
                'name': row[0],
                'status': row[1],
                'approvalDate': row[2].strftime('%Y-%m-%d') if row[2] else ''
            })
        return records
    finally:
        cursor.close()
        connection.close()


# 檢查學生是否有待回覆或已同意的指導邀請
def check_student_mentorship_status(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 分別檢查待回覆(0)和已同意(1)的狀態
        cursor.execute("""
            SELECT status 
            FROM mentorshiprequest 
            WHERE studentID = %s AND status IN (0, 1)
            LIMIT 1
        """, (student_id,))
        result = cursor.fetchone()

        if result:
            status = result[0]
            if status == 0:
                return "pending"  # 待回覆
            elif status == 1:
                return "accepted"  # 已同意
        return None  # 沒有待回覆或已同意的邀請
    finally:
        cursor.close()
        connection.close()
