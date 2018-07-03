from django.urls import path, re_path

from sale.views import IndexView, TransferView, PatchView

urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path(r'transfer/<str:status>/', TransferView.as_view(), name='transfer'),
	path(r'transfer/<str:status>/<str:code>/', TransferView.as_view(), name='transfer_filter'),
	path(r'transfer/<str:status>/<str:code>/<str:patch>/', TransferView.as_view(), name='patch_filter'),
	path(r'patch/<str:code>/', PatchView.as_view(), name='patch'),
]