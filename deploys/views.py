from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.response import TemplateResponse
from django.conf import settings

from auth.views import LoginRequiredView

import requests


class ListDeploy(LoginRequiredView):
    def get(self, request):
        authorization = {'authorization': request.session.get('tsuru_token')}
        response = requests.get('%s/deploys' % settings.TSURU_HOST,
                                headers=authorization)
        if response.status_code == 204:
            deploys = []
        else:
            deploys = response.json()

        paginator = Paginator(deploys, 20)
        page = request.GET.get('page')
        try:
            deploys = paginator.page(page)
        except PageNotAnInteger:
            deploys = paginator.page(1)
        except EmptyPage:
            deploys = paginator.page(paginator.num_pages)

        return TemplateResponse(request, "deploys/list_deploys.html",
                                {'deploys': deploys, 'paginator': paginator,
                                 'is_paginated': True})
