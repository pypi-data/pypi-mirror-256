from django.contrib import admin
from rest_framework_api_key.admin import APIKey

from aw.models import Job, JobExecution, \
    JobPermission, JobPermissionMemberUser, JobPermissionMemberGroup, JobPermissionMapping, \
    JobExecutionResult, JobError, AwAPIKey, JobUserCredentials, JobExecutionResultHost

admin.site.unregister(APIKey)

admin.site.register(Job)
admin.site.register(JobExecution)
admin.site.register(JobPermission)
admin.site.register(JobPermissionMemberUser)
admin.site.register(JobPermissionMemberGroup)
admin.site.register(JobPermissionMapping)
admin.site.register(JobExecutionResult)
admin.site.register(JobExecutionResultHost)
admin.site.register(JobError)
admin.site.register(JobUserCredentials)
admin.site.register(AwAPIKey)
