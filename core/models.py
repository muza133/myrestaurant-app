import resend
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Booking(models.Model):
    # Borish sabablari tanlovi
    REASON_CHOICES = [
        ('birthday', "Tug'ilgan kun"),
        ('romantic', "Romantik kechki ovqat"),
        ('business', "Biznes uchrashuv"),
        ('family', "Oila bilan kechki ovqat"),
        ('other', "Boshqa sabab"),
    ]

    # Status tanlovi (Admin tasdiqlashi uchun)
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('confirmed', 'Tasdiqlandi'),
        ('rejected', 'Rad etildi'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Foydalanuvchi")
    name = models.CharField(max_length=100, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email pochta")
    date = models.DateField(verbose_name="Kelingan sana")
    time = models.TimeField(verbose_name="Vaqt / Soat")
    guests_count = models.IntegerField(default=1, verbose_name="Odamlar soni")
    reason = models.CharField(max_length=50, choices=REASON_CHOICES, default='other', verbose_name="Tashrif sababi")
    special_request = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha istaklar")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")

    def __str__(self):
        return f"{self.name} - {self.date} {self.time} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        # Agar obyekt ma'lumotlar bazasida mavjud bo'lsa (ya'ni yangilanayotgan bo'lsa)
        if self.pk:
            old_booking = Booking.objects.get(pk=self.pk)
            # Status 'confirmed' ga o'zgarganda avtomatik email ketadi
            if old_booking.status != 'confirmed' and self.status == 'confirmed':
                resend.api_key = getattr(settings, 'RESEND_API_KEY', '')

                params = {
                    "from": "Restoran <onboarding@resend.dev>",
                    "to": [self.email],
                    "subject": "Restoran — Broningiz tasdiqlandi! 🎉",
                    "html": f"""
                        <h3>Hurmatli {self.name}!</h3>
                        <p>Sizning <b>{self.date}</b> kunidagi soat <b>{self.time}</b> uchun qilgan broningiz admin tomonidan <b>TASDIQLANDI</b>.</p>
                        <p>Sizni restoran xonalarida kutib qolamiz!</p>
                    """,
                }

                try:
                    resend.Emails.send(params)
                except Exception as e:
                    print(f"Resend orqali email yuborishda xatolik: {e}")

        super().save(*args, **kwargs)