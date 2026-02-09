from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Student, Attendance
from django.utils import timezone
import cv2

try:
    import face_recognition
except ImportError:
    face_recognition = None

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
    return render(request, "login.html")
@login_required
def dashboard(request):
    student = Student.objects.get(user=request.user)
    return render(request, "dashboard.html", {"student": student})
@login_required
def face_punch(request):
    cap = cv2.VideoCapture(0)
    known_faces = {request.user.username: []}  # load embeddings here

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb_frame)

        for emb in encodings:
            for name, embeddings in known_faces.items():
                matches = face_recognition.compare_faces(embeddings, emb)
                if True in matches:
                    student = Student.objects.get(user=request.user)
                    Attendance.objects.create(student=student, timestamp=timezone.now())
                    cap.release()
                    cv2.destroyAllWindows()
                    return render(request, "attendance.html", {"student": student})
        cv2.imshow("Face Punch", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return redirect("dashboard")
def attendance_spotline(request):
    today = timezone.now().date()
    students = Student.objects.all()
    attendance_data = []

    for student in students:
        has_attendance = Attendance.objects.filter(
            student=student,
            timestamp__date=today
        ).exists()

        attendance_data.append({
            "name": student.user.username,
            "roll_no": student.roll_no,
            "department": student.department,
            "status": "Present" if has_attendance else "Absent"
        })

    return render(request, "attendance_spotline.html", {"attendance_data": attendance_data})