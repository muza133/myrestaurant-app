from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'email', 
        'date', 
        'time', 
        'guests_count', 
        'reason', 
        'status', 
        'created_at'
    )
    list_filter = ('status', 'date', 'reason')
    search_fields = ('name', 'email', 'reason')
    list_editable = ('status',)  # Ro'yxatning o'zidan statusni o'zgartirish uchun

    def save_model(self, request, obj, form, change):
        # Agar mavjud bron tahrirlanayotgan bo'lsa (yangi yaratilmayotgan bo'lsa)
        if change:
            try:
                old_obj = Booking.objects.get(pk=obj.pk)
                # Agar avvalgi status 'approved' bo'lmagan va hozir 'approved' ga o'zgargan bo'lsa
                if old_obj.status != 'approved' and obj.status == 'approved':
                    subject = "Restoran — Broningiz tasdiqlandi!"
                    
                    # Sababning o'zbekcha nomini olish (masalan: "Tug'ilgan kun")
                    reason_display = obj.get_reason_display() if hasattr(obj, 'get_reason_display') else obj.reason
                    
                    message = (
                        f"Hurmatli {obj.name},\n\n"
                        f"Sizning {obj.date} kuni soat {obj.time} dagi broningiz muvaffaqiyatli tasdiqlandi!\n\n"
                        f"Odamlar soni: {obj.guests_count}\n"
                        f"Tashrif sababi: {reason_display}\n\n"
                        f"Sizni restoranida kutib qolamiz!"
                    )
                    recipient_list = [obj.email]
                    
                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        recipient_list,
                        fail_silently=False,
                    )
            except Exception as e:
                print(f"Email yuborishda xatolik yuz berdi: {e}")

        super().save_model(request, obj, form, change)