from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from aw.api_endpoints.key import APIKey, APIKeyItem
from aw.api_endpoints.job import APIJob, APIJobItem, APIJobExecutionItem, APIJobExecutionLogs, \
    APIJobExecutionLogFile, APIJobExecution
from aw.api_endpoints.permission import APIPermission, APIPermissionItem
from aw.api_endpoints.filesystem import APIFsBrowse

urlpatterns_api = [
    path('api/key/<str:token>', APIKeyItem.as_view()),
    path('api/key', APIKey.as_view()),
    path('api/job/<int:job_id>/<int:exec_id>/log/<int:line_start>', APIJobExecutionLogs.as_view()),
    path('api/job/<int:job_id>/<int:exec_id>/log', APIJobExecutionLogFile.as_view()),
    path('api/job/<int:job_id>/<int:exec_id>', APIJobExecutionItem.as_view()),
    path('api/job/<int:job_id>', APIJobItem.as_view()),
    path('api/job_exec', APIJobExecution.as_view()),
    path('api/job', APIJob.as_view()),
    path('api/permission/<int:perm_id>', APIPermissionItem.as_view()),
    path('api/permission', APIPermission.as_view()),
    path('api/fs/browse/<str:selector>', APIFsBrowse.as_view()),
    path('api/_schema/', SpectacularAPIView.as_view(), name='_schema'),
    path('api/_docs', SpectacularSwaggerView.as_view(url_name='_schema'), name='swagger-ui'),
]
