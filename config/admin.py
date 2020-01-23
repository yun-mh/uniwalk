from datetime import datetime, timedelta
import operator
from functools import reduce
from django.shortcuts import render, redirect, render_to_response
from django.db.models import Q
from django.urls import path, reverse
from django.contrib.admin import AdminSite
from django.views.decorators.cache import never_cache
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from designs import models as designs_model
from orders import models as orders_model
from products import models as products_model
from users import models as users_model


class ConfigAdminSite(AdminSite):
    index_template = "admin/base.html"

    @never_cache
    def index(self, request, extra_context=None):
        app_list = self.get_app_list(request)
        orders = orders_model.Order.objects.all()
        products = products_model.Product.objects.all()
        designs = designs_model.Design.objects.all()
        users = users_model.User.objects.all()
        sales_total_month = orders.filter(
            Q(
                order_date__year=datetime.now().year,
                order_date__month=datetime.now().month,
            )
            & reduce(
                operator.or_,
                (Q(step__step_code__contains=step) for step in ["T03", "T11", "T21"]),
            )
        )
        total_revenue_month = 0
        for sale_month in sales_total_month:
            total_revenue_month += sale_month.amount

        sales_total_today = orders.filter(
            Q(
                order_date__year=datetime.now().year,
                order_date__month=datetime.now().month,
                order_date__day=datetime.now().day,
            )
            & reduce(
                operator.or_,
                (Q(step__step_code__contains=step) for step in ["T03", "T11", "T21"]),
            )
        )
        total_revenue_today = 0
        for sale_today in sales_total_today:
            total_revenue_today += sale_today.amount

        sales_total_yesterday = orders.filter(
            Q(
                order_date__year=datetime.now().year,
                order_date__month=datetime.now().month,
                order_date__day=(datetime.now() - timedelta(days=1)).day,
            )
            & reduce(
                operator.or_,
                (Q(step__step_code__contains=step) for step in ["T03", "T11", "T21"]),
            )
        )
        total_revenue_yesterday = 0
        for sale_yesterday in sales_total_yesterday:
            total_revenue_yesterday += sale_yesterday.amount

        context = {
            **self.each_context(request),
            "title": self.index_title,
            "before_payment": orders.filter(step__step_code__contains="T01"),
            "paying": orders.filter(step__step_code__contains="T02"),
            "payment_checked": orders.filter(step__step_code__contains="T03"),
            "dealing_with": orders.filter(step__step_code__contains="T11"),
            "products": products.filter(is_active=True),
            "designs": designs,
            "users": users,
            "total_revenue_for_month": total_revenue_month,
            "total_orders_for_month": sales_total_month,
            "total_revenue_for_today": total_revenue_today,
            "total_orders_for_today": sales_total_today,
            "total_revenue_for_yesterday": total_revenue_yesterday,
            "total_orders_for_yesterday": sales_total_yesterday,
            "app_list": app_list,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.index_template, context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "analytics/members/",
                self.admin_view(self.member_analytics),
                name="member-analytics",
            ),
            path(
                "analytics/sales/",
                self.admin_view(self.sales_analytics),
                name="sales-analytics",
            ),
            path(
                "analytics/footsize/",
                self.admin_view(self.footsize_analytics),
                name="footsize-analytics",
            ),
        ]
        return custom_urls + urls

    # 会員分析
    def member_analytics(self, request):
        guests = users_model.Guest.objects.all()
        users = users_model.User.objects.all()
        all_users = len(users) + len(guests)
        male = users.filter(gender="M")
        female = users.filter(gender="F")
        other = users.filter(gender="O")
        kids = []
        tens = []
        twenties = []
        thirties = []
        forties = []
        fifties = []
        over_sixties = []
        for user in users:
            age = user.calculate_age()
            if age < 10:
                kids.append(age)
            elif age >= 10 and age < 20:
                tens.append(age)
            elif age >= 20 and age < 30:
                twenties.append(age)
            elif age >= 30 and age < 40:
                thirties.append(age)
            elif age >= 40 and age < 50:
                forties.append(age)
            elif age >= 50 and age < 60:
                fifties.append(age)
            elif age >= 60:
                over_sixties.append(age)
        context = {
            "kids": kids,
            "tens": tens,
            "twenties": twenties,
            "thirties": thirties,
            "forties": forties,
            "fifties": fifties,
            "over_sixties": over_sixties,
            "all_users": all_users,
            "users": users,
            "guests": guests,
            "male": male,
            "female": female,
            "other": other,
            "site_title": self.site_title,
            "site_header": self.site_header,
            "site_url": self.site_url,
            "has_permission": self.has_permission(request),
            "available_apps": self.get_app_list(request),
            "is_popup": False,
        }
        return render(request, "admin/member-analytics.html", context)

    # 販売分析
    def sales_analytics(self, request):
        # if request.method == "POST":
        products = products_model.Product.objects.all()
        context = {
            "products": products,
            "site_title": self.site_title,
            "site_header": self.site_header,
            "site_url": self.site_url,
            "has_permission": self.has_permission(request),
            "available_apps": self.get_app_list(request),
            "is_popup": False,
        }
        return render(request, "admin/sales-analytics.html", context)

    # 足サイズ分析
    def footsize_analytics(self, request):
        context = {
            "site_title": self.site_title,
            "site_header": self.site_header,
            "site_url": self.site_url,
            "has_permission": self.has_permission(request),
            "available_apps": self.get_app_list(request),
            "is_popup": False,
        }
        return render(request, "admin/footsize-analytics.html", context)

    # 人気デザイン分析
    def design_analytics(self, request):
        context = {
            "site_title": self.site_title,
            "site_header": self.site_header,
            "site_url": self.site_url,
            "has_permission": self.has_permission(request),
            "available_apps": self.get_app_list(request),
            "is_popup": False,
        }
        return render(request, "admin/design-analytics.html", context)

