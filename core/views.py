from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import BookingForm

def index(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_obj = form.save(commit=False)
            
            # Agar foydalanuvchi tizimga kirgan bo'lsa, biriktiramiz
            if request.user.is_authenticated:
                booking_obj.user = request.user
                
            booking_obj.save()

            # ---------------- EMAIL YUBORISH KODI ----------------
            try:
                subject = "Restoran — Bron qilish qabul qilindi!"
                message = f"Ism: {booking_obj.name}\nSana: {booking_obj.date}\nVaqt: {booking_obj.time}\n\nSizning broningiz qabul qilindi. Tez orada admin tasdiqlaydi!"
                recipient_list = [booking_obj.email]

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list,
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email yuborishda xatolik bo'ldi: {e}")
            # ----------------------------------------------------

            messages.success(request, "Ajoyib! Stolingiz muvaffaqiyatli bron qilindi va emailga xabar yuborildi.")
            return redirect('index')
        else:
            messages.error(request, "Formani to'ldirishda xatolik bor. Iltimos, ma'lumotlarni qayta tekshiring.")
    else:
        form = BookingForm()
    
    return render(request, 'index.html', {'form': form})

# Boshqa sahifalar uchun ko'rinishlar

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')

def menu(request):
    return render(request, 'menu.html')

def booking(request):
    return render(request, 'booking.html')

def booking_view(request):
    return render(request, 'booking_view.html')

def contact(request):
    return render(request, 'contact.html')

def team(request):
    return render(request, 'team.html')

def testimonial(request):
    return render(request, 'testimonial.html')