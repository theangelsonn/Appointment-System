import os
import re
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, render_template_string, send_from_directory, current_app, flash
from ..model.models import get_account_by_account, get_professors, get_professor_by_id, get_otherinfo, get_professor_by_account_id, get_appointmentslot, update_appointment_slots, update_notice, update_lab_rule, update_research_area, get_student_count, get_student_by_account_id, update_student_profile, update_professor_profile, get_account_by_account_id, update_appointment_status, get_appointments_by_student, get_appointments_by_professor, create_appointment, get_all_professors, get_all_students, delete_student, delete_professor, create_student_account, create_pro_account,  get_all_professor_names, create_mentorship_request, get_professor_id_by_name, get_student_mentorship_requests, get_student_id_by_account_id, get_professor_mentorship_requests, update_mentorship_request_status, get_professor_mentorship_history, check_student_mentorship_status, update_reservationOpen_status, check_existing_student, check_existing_account, check_existing_location
from werkzeug.utils import secure_filename
from datetime import datetime
main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'app/static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route("/")
def index():
    return redirect(url_for('main.login'))

# 學生修改資料


@main.route('/profile_stu_fix')
def profile_stu_fix():
    account_id = session.get('user_id')
    student = get_student_by_account_id(account_id)
    account = get_account_by_account_id(account_id)
    return render_template('profile_stu_fix.html', student=student, account=account)


@main.route('/profile_stu')
def profile_stu():
    account_id = session.get('user_id')
    student = get_student_by_account_id(account_id)
    return render_template('profile_stu.html', student=student)


@main.route('/update_profile', methods=['POST'])
def update_profile():
    account_id = session.get('user_id')
    name = request.form['name']
    password = request.form['password']
    account = request.form['account']
    email = request.form['email']
    phone = request.form['phone']

    # 獲取教授資料
    student = get_student_by_account_id(account_id)
    student_id = student[7]  # 假設 professorID 是第一個字段

    photo = None

    # 處理文件上傳
    if 'photo' in request.files:
        file = request.files['photo']
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            print(f"ext: {ext}")
            filename = f"student_{student_id}.{ext}"

            # filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            photo = filename
        else:
            photo = None
    else:
        photo = None

    update_student_profile(account_id, name, password,
                           account, email, phone, photo)
    return redirect(url_for('main.profile_stu'))

# 教授修改資料


@main.route('/profile_pro')
def profile_pro():
    account_id = session.get('user_id')
    professor = get_professor_by_account_id(account_id)
    return render_template('profile_pro.html', professor=professor)


@main.route('/profile_pro_fix')
def profile_pro_fix():
    account_id = session.get('user_id')
    professor = get_professor_by_account_id(account_id)
    account = get_account_by_account_id(account_id)
    # print(f"account: {account}")
    # print(f"professor: {professor}")
    return render_template('profile_pro_fix.html', professor=professor, account=account)


@main.route('/update_pro_profile', methods=['POST'])
def update_pro_profile():
    account_id = session.get('user_id')
    name = request.form['name']
    password = request.form['password']
    account = request.form['account']
    professorship = request.form['professorship']
    email = request.form['email']
    phone = request.form['phone']
    # print(f"request.files: {request.files}")

    # 獲取教授資料
    professor = get_professor_by_account_id(account_id)
    professor_id = professor[0]  # 假設 professorID 是第一個字段

    photo = None

    # 處理文件上傳
    if 'photo' in request.files:
        file = request.files['photo']
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            print(f"ext: {ext}")
            filename = f"professor_{professor_id}.{ext}"

            # filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            photo = filename
        else:
            photo = None
    else:
        photo = None

    update_professor_profile(account_id, name, password,
                             account, professorship, email, phone, photo)
    return redirect(url_for('main.profile_pro'))

# 新增登入功能


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        user = get_account_by_account(account)
        # print(f"user_account: {user.account}")
        # print(f"user_password: {user.password}")
        # print(f"password: {password}")
        # print(user.password==password)
        if user and user.password == password:
            session['user_id'] = user.accountID
            session['role'] = user.role
            if user.role == 0:
                return redirect(url_for('main.student_dashboard'))
            elif user.role == 1:
                return redirect(url_for('main.teacher_dashboard'))
            elif user.role == 2:
                return redirect(url_for('main.account_stu'))
        elif user:
            return render_template_string('''
                    <script>
                        alert('密碼錯誤');
                        window.location.href = '/';
                    </script>
                ''')
        elif user == None:
            return render_template_string('''
                <script>
                    alert('查無此帳號');
                    window.location.href = '/';
                </script>
            ''')
    return render_template('login.html')

# 登出


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))


# 學生登入後介面
@main.route('/student_dashboard')
def student_dashboard():
    if 'role' in session and session['role'] == 0:
        p = get_professors()
        professors = get_all_professors()
        # print(professors)
        # print(p)
        return render_template('student_dashboard.html', professors=professors)
    return redirect(url_for('main.login'))


@main.route("/view_pro_detail/<int:professor_id>")
def view_pro_detail(professor_id):
    professor = get_professor_by_id(professor_id)
    otherinfo = get_otherinfo(professor_id)
    appointmentslot = get_appointmentslot(professor_id)
    student_count = get_student_count(professor_id)
    # print(professor)
    # print(otherinfo)
    # print(appointmentslot)
    return render_template('view_pro_detail.html', professor=professor, otherinfo=otherinfo, appointmentslot=appointmentslot, student_count=student_count)

# 老師登入後介面


@main.route('/teacher_dashboard')
def teacher_dashboard():
    if 'role' in session and session['role'] == 1:
        account_id = session.get('user_id')
        professor = get_professor_by_account_id(account_id)
        otherinfo = get_otherinfo(professor[0])
        appointmentslot = get_appointmentslot(professor[0])
        student_count = get_student_count(professor[0])
        # print(professor)
        # print(appointmentslot)
        return render_template('teacher_dashboard.html', professor=professor, otherinfo=otherinfo, appointmentslot=appointmentslot, student_count=student_count)
    return redirect(url_for('main.login'))


@main.route('/update_appointment_slots', methods=['POST'])
def update_appointment_slots_route():
    account_id = session.get('user_id')
    professor = get_professor_by_account_id(account_id)
    new_slot = request.form['appointment_slot']
    # professor[0] 是 professorID
    update_appointment_slots(professor[0], new_slot)
    return redirect(url_for('main.teacher_dashboard'))


@main.route('/update_lab_rule', methods=['POST'])
def update_lab_rule_route():
    account_id = session.get('user_id')
    professor = get_professor_by_account_id(account_id)
    new_lab_rule = request.form['lab_rule_content']
    update_lab_rule(professor[0], new_lab_rule)  # professor[0] 是 professorID
    return redirect(url_for('main.teacher_dashboard'))


@main.route('/update_notice', methods=['POST'])
def update_notice_route():
    account_id = session.get('user_id')
    professor = get_professor_by_account_id(account_id)
    new_notice = request.form['notice_content']
    update_notice(professor[0], new_notice)  # professor[0] 是 professorID
    return redirect(url_for('main.teacher_dashboard'))


@main.route('/update_research_area', methods=['POST'])
def update_research_area_route():
    account_id = session.get('user_id')
    professor = get_professor_by_account_id(account_id)
    new_research_area = request.form['research_area_content']
    # professor[0] 是 professorID
    update_research_area(professor[0], new_research_area)
    return redirect(url_for('main.teacher_dashboard'))


@main.route('/update_reservationOpen_status', methods=['POST'])
def update_reservationOpen_status_route():
    account_id = session.get('user_id')
    professor = get_professor_by_account_id(account_id)
    new_status = request.form['appointment_status']
    # professor[0] 是 professorID
    print("預約狀態", new_status)
    update_reservationOpen_status(professor[0], new_status)
    return redirect(url_for('main.teacher_dashboard'))


@main.route('/appointment_create/<int:professor_id>', methods=['GET', 'POST'])
def appointment_create(professor_id):
    if request.method == 'POST':
        try:
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            resume = request.files['resume']
            resume_filename = secure_filename(resume.filename)

            # 檢查時間格式
            try:
                start_datetime = datetime.strptime(
                    start_time, '%Y-%m-%dT%H:%M')
                end_datetime = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
                if end_datetime <= start_datetime:
                    return render_template('appointment_create.html',
                                           professor_id=professor_id,
                                           professor=get_professor_by_id(
                                               professor_id),
                                           error="結束時間必須晚於開始時間")
            except ValueError:
                return render_template('appointment_create.html',
                                       professor_id=professor_id,
                                       professor=get_professor_by_id(
                                           professor_id),
                                       error="時間格式錯誤")

            # 檢查檔案類型
            if not resume.filename.lower().endswith('.pdf'):
                return render_template('appointment_create.html',
                                       professor_id=professor_id,
                                       professor=get_professor_by_id(
                                           professor_id),
                                       error="請上傳 PDF 格式的履歷檔案")

            # 儲存檔案
            upload_dir = os.path.join(current_app.root_path, 'static/resumes')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            resume.save(os.path.join(upload_dir, resume_filename))

            # 創建預約
            student_id = session.get('user_id')
            if not student_id:
                return redirect(url_for('main.login'))

            # 嘗試創建預約並捕獲具體錯誤
            try:
                create_appointment(professor_id, student_id,
                                   start_time, end_time, resume_filename)
                return redirect(url_for('main.appointment_student'))
            except Exception as e:
                print(f"Error creating appointment: {str(e)}")
                return render_template('appointment_create.html',
                                       professor_id=professor_id,
                                       professor=get_professor_by_id(
                                           professor_id),
                                       error=f"預約創建失敗: {str(e)}")

        except Exception as e:
            print(f"Error in appointment_create: {str(e)}")
            return render_template('appointment_create.html',
                                   professor_id=professor_id,
                                   professor=get_professor_by_id(professor_id),
                                   error=f"處理請求時發生錯誤: {str(e)}")

    # GET 請求顯示表單
    professor = get_professor_by_id(professor_id)
    return render_template('appointment_create.html',
                           professor_id=professor_id,
                           professor=professor)


@main.route('/appointment/teacher')
def appointment_teacher():
    # 從 session 獲取教授 ID
    professor = get_professor_by_account_id(session.get('user_id'))
    if not professor:
        return redirect(url_for('main.login'))

    # 獲取該教授的所有預約
    appointments = get_appointments_by_professor(professor[0])

    return render_template('appointment_pro.html', appointments=appointments)


@main.route('/download/resume/<filename>')
def download_resume(filename):
    return send_from_directory(os.path.join(current_app.root_path, 'static/resumes'),
                               filename, as_attachment=True)

# 教授更新是否開放預約的狀態


@main.route('/update_professor_appointment_status', methods=['POST'])  # 修改路由路徑
def update_professor_appointment_status():
    account_id = session.get('user_id')
    professor = get_professor_by_account_id(account_id)
    new_status = request.form['appointment_status']
    update_appointment_status(professor[0], new_status)
    return redirect(url_for('main.teacher_dashboard'))

# 教授處理學生預約請求的狀態


# 修改路由路徑
@main.route('/appointment/student_request/<int:appointment_id>', methods=['POST'])
def handle_student_appointment_request(appointment_id):  # 修改函數名稱
    new_status = request.form.get('status')
    update_appointment_status(appointment_id, new_status, datetime.now())
    return redirect(url_for('main.appointment_teacher'))


# 教授刪除預約的功能
@main.route('/delete_appointment/<int:appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    try:
        from ..model.models import get_db_connection
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM appointment WHERE appointmentID = %s", (appointment_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('main.appointment_teacher'))
    except Exception as e:
        print(f"刪除預約時發生錯誤: {str(e)}")
        return redirect(url_for('main.appointment_teacher'))


# 取消預約


@main.route('/appointment/cancel/<int:appointment_id>', methods=['POST'])
def cancel_appointment(appointment_id):
    update_appointment_status(appointment_id, 2)
    return redirect(url_for('main.appointment_teacher'))


# 學生查看預約


@main.route('/appointment/student')
def appointment_student():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    student_id = session.get('user_id')
    appointments = get_appointments_by_student(student_id)
    return render_template('appointment_stu.html', appointments=appointments)

# 系密登入後介面
# @main.route('/secretary_dashboard')
# def secretary_dashboard():
#     if 'role' in session and session['role'] == 2:
#         return render_template('secretary_dashboard.html')
#     return redirect(url_for('main.login'))


@main.route('/account_stu')
def account_stu():
    if 'role' in session and session['role'] == 2:
        students = get_all_students()
        return render_template('account_stu.html', students=students)
    return redirect(url_for('main.login'))


@main.route('/delete_student/<int:account_id>', methods=['POST'])
def delete_student_route(account_id):
    delete_student(account_id)
    return redirect(url_for('main.account_stu'))


@main.route('/account_pro')
def account_pro():
    professors = get_all_professors()
    return render_template('account_pro.html', professors=professors)


@main.route('/delete_professor/<int:account_id>', methods=['POST'])
def delete_professor_route(account_id):
    delete_professor(account_id)
    return redirect(url_for('main.account_pro'))


@main.route('/check_rank', methods=['POST'])
def check_rank():
    data = request.get_json()
    rankType = data.get('rankType')
    rank = data.get('rank')

    # 检查是否存在于数据库
    exists = check_existing_student(rankType, rank)
    # print(exists,exists)
    return jsonify({'exists': exists})


@main.route('/check_account', methods=['POST'])
def check_account():
    data = request.get_json()
    account = data.get('account')

    # 检查是否存在于数据库
    exists = check_existing_account(account)
    return jsonify({'exists': exists})


@main.route('/check_location', methods=['POST'])
def check_location():
    data = request.get_json()
    location = data.get('location')

    # 检查是否存在于数据库
    exists = check_existing_location(location)
    print(exists)

    return jsonify({'exists': exists})


@main.route('/account_create_stu', methods=['GET', 'POST'])
def account_create_stu():
    if request.method == 'POST':
        name = request.form['student-name']
        # print(name)
        email = request.form['account-email']
        # password = request.form['password']  # 假設表單中有一個密碼字段
        rankType = request.form['rankType']
        rank = request.form['rank']
        department = request.form['department']
        admissionYear = request.form['admissionYear']
        print(name, email, rankType, rank, department, admissionYear)

        if re.search(r'\d', name):
            return redirect(url_for('main.account_create_stu'))

        if check_existing_account(email):
            print('該帳號已存在')
            return redirect(url_for('main.account_create_stu'))

        if check_existing_student(rankType, rank):
            print('該入學方式和排名的學生已存在')
            return redirect(url_for('main.account_create_stu'))

        create_student_account(name, email, rankType,
                               rank, department, admissionYear)

        return redirect(url_for('main.account_stu'))

    return render_template('account_create_stu.html')


@main.route('/account_create_pro', methods=['GET', 'POST'])
def account_create_pro():
    if request.method == 'POST':
        name = request.form['student-name']
        email = request.form['account-email']
        department = request.form['department']
        professorship = request.form['professorship']
        location = request.form['location']
        labStudentNum = request.form['labStudentNum']

        if re.search(r'\d', name):
            return redirect(url_for('main.account_create_pro'))

        if check_existing_account(email):
            print('該帳號已存在')
            return redirect(url_for('main.account_create_pro'))

        if check_existing_location(location):
            print('該辦公室已存在')
            return redirect(url_for('main.account_create_pro'))

        create_pro_account(name, email, department,
                           professorship, location, labStudentNum)

        return redirect(url_for('main.account_pro'))

    return render_template('account_create_pro.html')


# 學生查看指導邀請
@main.route('/mentorship_stu')
def mentorship_stu():
    account_id = session.get('user_id')
    if not account_id:
        return redirect(url_for('main.login'))

    # 根據 account_id 獲取對應的 student_id
    student_id = get_student_id_by_account_id(account_id)
    if not student_id:
        return redirect(url_for('main.login'))

    # 獲取所有教授的名字列表，用於下拉選單
    professors = get_all_professor_names()
    # 獲取該學生的所有指導邀請記錄
    records = get_student_mentorship_requests(student_id)

    return render_template('mentorship_stu.html',
                           professors=professors,
                           records=records)


# 學生查看指導邀請紀錄
@main.route('/mentorship_stu_detail')
def mentorship_stu_detail():
    account_id = session.get('user_id')
    if not account_id:
        return redirect(url_for('main.login'))

    # 根據 account_id 獲取對應的 student_id
    student_id = get_student_id_by_account_id(account_id)
    if not student_id:
        return redirect(url_for('main.login'))

    # 獲取該學生的所有指導邀請記錄
    records = get_student_mentorship_requests(student_id)

    return render_template('mentorship_stu_detail.html', records=records)


# 學生提交指導邀請
@main.route('/submit_invitation', methods=['POST'])
def submit_invitation():
    professor_name = request.form['professor']
    account_id = session.get('user_id')

    # 獲取學生ID
    student_id = get_student_id_by_account_id(account_id)
    if not student_id:
        return jsonify({'error': '無法找到學生資訊'}), 400

    # 檢查學生當前的指導邀請狀態
    status = check_student_mentorship_status(student_id)
    if status == "pending":
        return jsonify({'error': '你目前有正在等待回覆的指導邀請，暫時無法提出新的申請'}), 400
    elif status == "accepted":
        return jsonify({'error': '你目前已有同意的指導邀請，無法再提出新的申請'}), 400

    professor_id = get_professor_id_by_name(professor_name)
    if professor_id is None:
        return jsonify({'error': '教授不存在'}), 400

    try:
        create_mentorship_request(professor_id, student_id)
        return jsonify({
            'success': '提交成功！',
            'professor_name': professor_name,
            'status': '待回覆',
            'request_date': datetime.now().strftime('%Y-%m-%d'),
            'approval_date': '尚未審核'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/mentorship_pro')
def mentorship_pro():
    account_id = session.get('user_id')
    if not account_id:
        return redirect(url_for('main.login'))

    professor = get_professor_by_account_id(account_id)
    if not professor:
        return redirect(url_for('main.login'))

    requests = get_professor_mentorship_requests(professor[0])
    print(requests)
    return render_template('mentorship_pro.html', requests=requests)


@main.route('/mentorship_pro_detail')
def mentorship_pro_detail():
    account_id = session.get('user_id')
    if not account_id:
        return redirect(url_for('main.login'))

    professor = get_professor_by_account_id(account_id)
    if not professor:
        return redirect(url_for('main.login'))

    history = get_professor_mentorship_history(professor[0])
    return render_template('mentorship_pro_detail.html', records=history)


@main.route('/handle_mentorship_request', methods=['POST'])
def handle_mentorship_request():
    studentID = request.form.get('studentID')
    professorID = request.form.get('professorID')
    student_name = request.form.get('student_name')
    action = request.form.get('action')
    request_id = request.form.get('request_id')  # 新增獲取請求ID

    # 根據動作設置狀態
    new_status = 1 if action == 'accept' else 2

    try:
        update_mentorship_request_status(
            studentID, professorID, student_name, new_status, request_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
