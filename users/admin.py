# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.html import format_html
# from .models import User, UserProfiles


# class UserProfilesInline(admin.StackedInline):
#     model = UserProfiles
#     can_delete = False
#     verbose_name_plural = "Profile"
#     fk_name = "user"
#     extra = 0


# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     list_display = ("username", "email", "is_staff", "created_at", "get_role", "get_subscription")
#     search_fields = ("username", "email")
#     list_filter = ("is_staff", "is_superuser", "profile__role", "profile__subscription_status")
#     readonly_fields = ("created_at",)

#     fieldsets = (
#         ("Credentials", {"fields": ("username", "email", "password")}),
#         ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
#         ("Important dates", {"fields": ("last_login", "created_at")}),
#     )

#     inlines = [UserProfilesInline]

#     def get_role(self, obj):
#         return obj.profile.role if hasattr(obj, 'profile') else "-"
#     get_role.short_description = "Role"

#     def get_subscription(self, obj):
#         return obj.profile.subscription_status if hasattr(obj, 'profile') else "-"
#     get_subscription.short_description = "Subscription"


# @admin.register(UserProfiles)
# class UserProfilesAdmin(admin.ModelAdmin):
#     list_display = ("user", "phone_number", "role", "subscription_status", "updated_at", "profile_image")
#     list_filter = ("role", "subscription_status", "updated_at")
#     search_fields = ("user__username", "phone_number", "state")
#     readonly_fields = ("profile_image",)

#     fieldsets = (
#         ("User Profile", {
#             "fields": ("user", "bio", "phone_number", "state", "role", "subscription_status")
#         }),
#         ("Photo", {
#             "fields": ("profile_photo", "profile_image")
#         }),
#     )

#     def profile_image(self, obj):
#         if obj.profile_photo:
#             return format_html(f'<img src="{obj.profile_photo.url}" width="50" style="border-radius: 50%;" />')
#         return "-"
#     profile_image.short_description = "Photo"

# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfiles
from reportlab.pdfgen import canvas
from django.http import HttpResponse


class UserProfilesInline(admin.StackedInline):
    model = UserProfiles
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"
    extra = 0
    classes = ['collapse']  # collapsible section


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "is_staff", "created_at", "get_role", "get_subscription")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_superuser", "profile__role", "profile__subscription_status")
    readonly_fields = ("created_at",)
    inlines = [UserProfilesInline]

    fieldsets = (
        ("Credentials", {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "created_at")}),
    )

    def get_role(self, obj):
        return obj.profile.role if hasattr(obj, 'profile') else "-"
    get_role.short_description = "Role"

    def get_subscription(self, obj):
        return obj.profile.subscription_status if hasattr(obj, 'profile') else "-"
    get_subscription.short_description = "Subscription"
def export_profiles_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="user_profiles.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    y = 800
    for profile in queryset:
        user = profile.user.username
        phone = profile.phone_number or "-"
        role = profile.role
        subs = profile.subscription_status
        state = profile.state or "-"

        line = f"{user} | {phone} | {role} | {subs} | {state}"
        p.drawString(100, y, line)
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    return response


@admin.register(UserProfiles)
class UserProfilesAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "role", "subscription_status", "updated_at", "profile_image")
    list_filter = ("role", "subscription_status", "updated_at")
    search_fields = ("user__username", "phone_number", "state")
    readonly_fields = ("profile_image",)
    actions = [export_profiles_pdf]  # 👈 Add this line

    fieldsets = (
        ("User Profile", {
            "fields": ("user", "bio", "phone_number", "state", "role", "subscription_status")
        }),
        ("Profile Photo", {
            "fields": ("profile_photo", "profile_image")
        }),
    )

    def profile_image(self, obj):
        if obj.profile_photo:
            return format_html(
                '<img src="{}" style="height:50px;width:50px;object-fit:cover;border-radius:50%;" />',
                obj.profile_photo.url
            )
        return "-"
    profile_image.short_description = "Photo"




export_profiles_pdf.short_description = "📄 Export selected profiles to PDF"
