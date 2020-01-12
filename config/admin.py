from datetime import datetime
import operator
from functools import reduce
from django.db.models import Q
from django.contrib.admin import AdminSite
from django.views.decorators.cache import never_cache
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from orders import models as orders_model
from products import models as products_model
from users import models as users_model


class ConfigAdminSite(AdminSite):
    site_title = _("Hello World")
    index_template = "admin/base.html"

    @never_cache
    def index(self, request, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        today = datetime.today()
        app_list = self.get_app_list(request)
        orders = orders_model.Order.objects.all()
        products = products_model.Product.objects.all()
        users = users_model.User.objects.all()
        context = {
            **self.each_context(request),
            "title": self.index_title,
            "before_payment": orders.filter(step__step_code__contains="T01"),
            "paying": orders.filter(step__step_code__contains="T02"),
            "payment_checked": orders.filter(step__step_code__contains="T03"),
            "dealing_with": orders.filter(step__step_code__contains="T11"),
            "products": products.filter(is_active=True),
            "users": users,
            "total_revenue_for_month": orders.filter(
                reduce(
                    operator.and_,
                    (
                        Q(step__step_code__contains=step)
                        for step in ["T03", "T11", "T21"]
                    ),
                )
                & Q(
                    order_date__year=datetime(today.year),
                    order_date__month=datetime(today.month),
                )
            ),
            "app_list": app_list,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.index_template, context)
