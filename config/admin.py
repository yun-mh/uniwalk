from datetime import datetime, timedelta
import operator
from functools import reduce
from django.views.generic import ListView
from django.shortcuts import render, redirect, render_to_response
from django.db.models import Q
from django.http import HttpResponse
from django.urls import path, reverse
from django.contrib.admin import AdminSite
from django.views.decorators.cache import never_cache
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from designs import models as designs_model
from feet import models as feet_model
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
            path(
                "analytics/rank/",
                self.admin_view(self.DesignAnalyticsView.as_view()),
                name="design-analytics",
            ),
            path(
                "analytics/rank/category-<int:pk>/",
                self.admin_view(self.DesignAnalyticsByCategoryView.as_view()),
                name="design-analytics-category",
            ),
            path(
                "analytics/rank/product-<int:pk>/",
                self.admin_view(self.DesignAnalyticsByProductView.as_view()),
                name="design-analytics-product",
            ),
            path(
                "switch-year/",
                self.admin_view(self.switch_year),
                name="switch-year",
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
        try:
            year = request.session["year"]
        except KeyError:
            year = 2020
        products = products_model.Product.objects.all()
        orders_by_year = orders_model.Order.objects.filter(Q(step__step_code__contains="T03") | Q(step__step_code__contains="T11") | Q(step__step_code__contains="T21")).filter(order_date__year=year)
        profit_by_month = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
        }
        for month in range(1, 13):
            orders = orders_by_year.filter(order_date__month=month)
            profit = 0
            for order in orders:
                profit += order.amount
            profit_by_month[month] = profit
        context = {
            "profit_by_month": profit_by_month,
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
        footsizes = feet_model.Footsize.objects.all()
        male_sizes = footsizes.filter(user__gender__contains="M")
        female_sizes = footsizes.filter(user__gender__contains="F")
        ## 男性のサイズ分類
        # 足長
        length_male_left = {
            230: 0,
            240: 0,
            250: 0,
            260: 0,
            270: 0,
            280: 0,
            290: 0,
            300: 0,
        }
        for size in range(230, 290, 10):
            items_num = len(male_sizes.filter(length_left__gte=size, length_left__lt=size+10))
            length_male_left[size+10] = items_num
        left_under230 = len(male_sizes.filter(length_left__lt=230))
        length_male_left[230] = left_under230
        left_over290 = len(male_sizes.filter(length_left__gte=290))
        length_male_left[300] = left_over290

        length_male_right = {
            230: 0,
            240: 0,
            250: 0,
            260: 0,
            270: 0,
            280: 0,
            290: 0,
            300: 0,
        }
        for size in range(230, 290, 10):
            items_num = len(male_sizes.filter(length_right__gte=size, length_right__lt=size+10))
            length_male_right[size+10] = items_num
        right_under230 = len(male_sizes.filter(length_right__lt=230))
        length_male_right[230] = right_under230
        right_over290 = len(male_sizes.filter(length_right__gte=290))
        length_male_right[300] = right_over290

        # 足幅
        width_male_left = {
            80: 0,
            90: 0,
            100: 0,
            110: 0,
            120: 0,
        }
        for size in range(80, 110, 10):
            items_num = len(male_sizes.filter(width_left__gte=size, width_left__lt=size+10))
            width_male_left[size+10] = items_num
        left_under80 = len(male_sizes.filter(width_left__lt=80))
        width_male_left[80] = left_under80
        left_over110 = len(male_sizes.filter(width_left__gte=110))
        width_male_left[120] = left_over110

        width_male_right = {
            80: 0,
            90: 0,
            100: 0,
            110: 0,
            120: 0,
        }
        for size in range(80, 110, 10):
            items_num = len(male_sizes.filter(width_right__gte=size, width_right__lt=size+10))
            width_male_right[size+10] = items_num
        right_under80 = len(male_sizes.filter(width_right__lt=80))
        width_male_right[80] = right_under80
        right_over110 = len(male_sizes.filter(width_right__gte=110))
        width_male_right[120] = right_over110

        ## 女性のサイズ分類
        # 足長
        length_female_left = {
            230: 0,
            240: 0,
            250: 0,
            260: 0,
            270: 0,
            280: 0,
            290: 0,
            300: 0,
        }
        for size in range(230, 290, 10):
            items_num = len(female_sizes.filter(length_left__gte=size, length_left__lt=size+10))
            length_female_left[size+10] = items_num
        left_under230 = len(female_sizes.filter(length_left__lt=230))
        length_female_left[230] = left_under230
        left_over290 = len(female_sizes.filter(length_left__gte=290))
        length_female_left[300] = left_over290

        length_female_right = {
            230: 0,
            240: 0,
            250: 0,
            260: 0,
            270: 0,
            280: 0,
            290: 0,
            300: 0,
        }
        for size in range(230, 290, 10):
            items_num = len(female_sizes.filter(length_right__gte=size, length_right__lt=size+10))
            length_female_right[size+10] = items_num
        right_under230 = len(female_sizes.filter(length_right__lt=230))
        length_female_right[230] = right_under230
        right_over290 = len(female_sizes.filter(length_right__gte=290))
        length_female_right[300] = right_over290

        # 足幅
        width_female_left = {
            80: 0,
            90: 0,
            100: 0,
            110: 0,
            120: 0,
        }
        for size in range(80, 110, 10):
            items_num = len(female_sizes.filter(width_left__gte=size, width_left__lt=size+10))
            width_female_left[size+10] = items_num
        left_under80 = len(female_sizes.filter(width_left__lt=80))
        width_female_left[80] = left_under80
        left_over110 = len(female_sizes.filter(width_left__gte=110))
        width_female_left[120] = left_over110

        width_female_right = {
            80: 0,
            90: 0,
            100: 0,
            110: 0,
            120: 0,
        }
        for size in range(80, 110, 10):
            items_num = len(female_sizes.filter(width_right__gte=size, width_right__lt=size+10))
            width_female_right[size+10] = items_num
        right_under80 = len(female_sizes.filter(width_right__lt=80))
        width_female_right[80] = right_under80
        right_over110 = len(female_sizes.filter(width_right__gte=110))
        width_female_right[120] = right_over110

        context = {
            "length_male_left": length_male_left,
            "length_male_right": length_male_right,
            "width_male_left": width_male_left,
            "width_male_right": width_male_right,
            "length_female_left": length_female_left,
            "length_female_right": length_female_right,
            "width_female_left": width_female_left,
            "width_female_right": width_female_right,
            "site_title": self.site_title,
            "site_header": self.site_header,
            "site_url": self.site_url,
            "has_permission": self.has_permission(request),
            "available_apps": self.get_app_list(request),
            "is_popup": False,
        }
        return render(request, "admin/footsize-analytics.html", context)

    ## 人気デザイン分析
    # 全体表示
    class DesignAnalyticsView(ListView):
        model = designs_model.Design
        paginate_by = 5
        context_object_name = "designs"
        extra_context = {
            "designs_all": designs_model.Design.objects.all().exclude(user__isnull=True),
            "products": products_model.Product.objects.all(),
            "count": len(products_model.Product.objects.all()),
            "categories": products_model.Category.objects.all(),
        }
        template_name = "admin/design-analytics.html"

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            if self.request.user.is_active and self.request.user.is_staff:
                has_permission = True
            else:
                has_permission = False
            context["site_title"] = ConfigAdminSite.site_title
            context["site_header"] = ConfigAdminSite.site_header
            context["site_url"] = ConfigAdminSite.site_url
            context["has_permission"] = has_permission
            context["is_popup"] = False
            return context

        def get_queryset(self):
            designs = designs_model.Design.objects.all().exclude(user__isnull=True)
            return sorted(designs, key= lambda design: design.total_likes, reverse=True)

    # カテゴリー別表示
    class DesignAnalyticsByCategoryView(ListView):
        model = designs_model.Design
        paginate_by = 5
        context_object_name = "designs"
        extra_context = {
            "designs_all": designs_model.Design.objects.all().exclude(user__isnull=True),
            "products": products_model.Product.objects.all(),
            "count": len(products_model.Product.objects.all()),
            "categories": products_model.Category.objects.all(),
        }
        template_name = "admin/design-analytics.html"

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            if self.request.user.is_active and self.request.user.is_staff:
                has_permission = True
            else:
                has_permission = False
            context["site_title"] = ConfigAdminSite.site_title
            context["site_header"] = ConfigAdminSite.site_header
            context["site_url"] = ConfigAdminSite.site_url
            context["has_permission"] = has_permission
            context["is_popup"] = False
            return context

        def get_queryset(self):
            pk = self.kwargs.get("pk")
            designs = designs_model.Design.objects.filter(product__category=pk).exclude(user__isnull=True)
            return sorted(designs, key= lambda design: design.total_likes, reverse=True)

    # 商品別表示
    class DesignAnalyticsByProductView(ListView):
        model = designs_model.Design
        paginate_by = 5
        context_object_name = "designs"
        extra_context = {
            "designs_all": designs_model.Design.objects.all().exclude(user__isnull=True),
            "products": products_model.Product.objects.all(),
            "count": len(products_model.Product.objects.all()),
            "categories": products_model.Category.objects.all(),
        }
        template_name = "admin/design-analytics.html"

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            if self.request.user.is_active and self.request.user.is_staff:
                has_permission = True
            else:
                has_permission = False
            context["site_title"] = ConfigAdminSite.site_title
            context["site_header"] = ConfigAdminSite.site_header
            context["site_url"] = ConfigAdminSite.site_url
            context["has_permission"] = has_permission
            context["is_popup"] = False
            return context

        def get_queryset(self):
            pk = self.kwargs.get("pk")
            designs = designs_model.Design.objects.filter(product=pk).exclude(user__isnull=True)
            return sorted(designs, key= lambda design: design.total_likes, reverse=True)

    def switch_year(self, request):
        year = request.GET.get("year", None)
        if year is not None:
            request.session["year"] = year
        return HttpResponse(status=200)