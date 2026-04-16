import json
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Student, StudentResult
from .EmailBackend import EmailBackend
from .models import Attendance, AttendanceReport, Session, Subject


# ===============================
# LOGIN PAGE
# ===============================
def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_home"))
        elif request.user.user_type == '2':
            return redirect(reverse("staff_home"))
        else:
            return redirect(reverse("student_home"))
    return render(request, 'main_app/login.html')


# ===============================
# LOGIN FUNCTION
# ===============================
def doLogin(request, **kwargs):
    if request.method != 'POST':
        return HttpResponse("<h4>Denied</h4>")
    else:
        captcha_token = request.POST.get('g-recaptcha-response')
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        captcha_key = "6LfswtgZAAAAABX9gbLqe-d97qE2g1JP8oUYritJ"

        data = {'secret': captcha_key, 'response': captcha_token}

        try:
            captcha_server = requests.post(url=captcha_url, data=data)
            response = json.loads(captcha_server.text)
            if response['success'] == False:
                messages.error(request, 'Invalid Captcha. Try Again')
                return redirect('/')
        except:
            messages.error(request, 'Captcha error')
            return redirect('/')

        user = EmailBackend.authenticate(
            request,
            username=request.POST.get('email'),
            password=request.POST.get('password')
        )

        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("admin_home"))
            elif user.user_type == '2':
                return redirect(reverse("staff_home"))
            else:
                return redirect(reverse("student_home"))
        else:
            messages.error(request, "❌ Enter valid email or password")
            return redirect("/")


# ===============================
# LOGOUT
# ===============================
def logout_user(request):
    logout(request)
    return redirect("/")


# ===============================
# GET ATTENDANCE
# ===============================
@csrf_exempt
def get_attendance(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')

    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)

        attendance = Attendance.objects.filter(subject=subject, session=session)

        attendance_list = []
        for attd in attendance:
            attendance_list.append({
                "id": attd.id,
                "attendance_date": str(attd.date),
                "session": attd.session.id
            })

        return JsonResponse(json.dumps(attendance_list), safe=False)

    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({"status": "error"})


# ===============================
# UPDATE ATTENDANCE
# ===============================
@csrf_exempt
def update_attendance(request):
    try:
        print("POST:", request.POST)

        student_data = request.POST.get('student_ids')
        date = request.POST.get('date')

        print("DATE:", date)
        print("STUDENT DATA:", student_data)

        students = json.loads(student_data)

        attendance = get_object_or_404(Attendance, date=date)

        for student_dict in students:
            print("Processing:", student_dict)

            student = get_object_or_404(Student, id=student_dict.get('id'))

            attendance_report, created = AttendanceReport.objects.get_or_create(
                student=student,
                attendance=attendance
            )

            attendance_report.status = student_dict.get('status')
            attendance_report.save()

        print("✅ SUCCESS")
        return JsonResponse({"status": "error", "message": str(e)})

    except Exception as e:
        print("🔥 ERROR:", e)
        return JsonResponse({"status": "error"})


# ===============================
# STUDENT VIEW RESULT 
# ===============================
@login_required
def student_view_result(request):

    if not hasattr(request.user, 'student'):
        return HttpResponse("No student profile found")

    student = request.user.student
    results = StudentResult.objects.filter(student=student)

    context = {
        'results': results,
        'page_title': 'My Results',
    }

    return render(request, 'student/student_view_result.html', context)

# ===============================
# FIREBASE
# ===============================
def showFirebaseJS(request):
    data = """
    importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-app.js');
    importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-messaging.js');

    firebase.initializeApp({
        apiKey: "AIzaSyBarDWWHTfTMSrtc5Lj3Cdw5dEvjAkFwtM",
        authDomain: "sms-with-django.firebaseapp.com",
        databaseURL: "https://sms-with-django.firebaseio.com",
        projectId: "sms-with-django",
        storageBucket: "sms-with-django.appspot.com",
        messagingSenderId: "945324593139",
        appId: "1:945324593139:web:03fa99a8854bbd38420c86",
        measurementId: "G-2F2RXTL9GT"
    });

    const messaging = firebase.messaging();

    messaging.setBackgroundMessageHandler(function (payload) {
        const notification = JSON.parse(payload);
        return self.registration.showNotification(
            payload.notification.title,
            {
                body: notification.body,
                icon: notification.icon
            }
        );
    });
    """
    return HttpResponse(data, content_type='application/javascript')