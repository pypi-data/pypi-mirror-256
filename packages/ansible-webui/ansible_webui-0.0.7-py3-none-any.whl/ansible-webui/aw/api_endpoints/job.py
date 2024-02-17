from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from aw.config.hardcoded import JOB_EXECUTION_LIMIT
from aw.model.job import Job, JobExecution, BaseJobCredentials, \
    CHOICE_JOB_PERMISSION_READ, CHOICE_JOB_PERMISSION_WRITE, CHOICE_JOB_PERMISSION_EXECUTE, \
    CHOICE_JOB_PERMISSION_FULL
from aw.api_endpoints.base import API_PERMISSION, get_api_user, BaseResponse, GenericResponse
from aw.api_endpoints.job_util import get_viewable_jobs_serialized, JobReadResponse, get_job_executions_serialized, \
    JobExecutionReadResponse, get_viewable_jobs, get_job_execution_serialized
from aw.utils.permission import has_job_permission
from aw.execute.queue import queue_add
from aw.execute.util import update_execution_status, is_execution_status
from aw.utils.util import is_null


class JobWriteRequest(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = Job.api_fields_write

    vault_pass = serializers.CharField(max_length=100, required=False, default=None)
    become_pass = serializers.CharField(max_length=100, required=False, default=None)
    connect_pass = serializers.CharField(max_length=100, required=False, default=None)


def _find_job(job_id: int) -> (Job, None):
    # pylint: disable=E1101
    try:
        return Job.objects.get(id=job_id)

    except ObjectDoesNotExist:
        return None


def _find_job_and_execution(job_id: int, exec_id: int) -> tuple[Job, (JobExecution, None)]:
    # pylint: disable=E1101
    job = _find_job(job_id)
    try:
        return job, JobExecution.objects.get(id=exec_id, job=job)

    except ObjectDoesNotExist:
        return job, None


def _job_execution_count(request) -> (int, None):
    max_count = None
    if 'execution_count' in request.GET:
        max_count = int(request.GET['execution_count'])
        max_count = min(max_count, 1000)

    return max_count


def _want_job_executions(request) -> tuple:
    max_count = None
    if 'executions' in request.GET and request.GET['executions'] == 'true':
        try:
            return True, _job_execution_count(request)

        except TypeError:
            pass

    return False, max_count


class APIJob(APIView):
    http_method_names = ['post', 'get']
    serializer_class = JobReadResponse
    permission_classes = API_PERMISSION

    @staticmethod
    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(JobReadResponse, description='Return list of jobs'),
        },
        summary='Return list of all jobs the current user is privileged to view.',
        operation_id='job_list',
        parameters=[
            OpenApiParameter(
                name='executions', type=bool, default=False, description='Return list of job-executions',
                required=False,
            ),
            OpenApiParameter(
                name='execution_count', type=int, default=JOB_EXECUTION_LIMIT,
                description='Maximum count of job-executions to return',
                required=False,
            ),
        ],
    )
    def get(request):
        want_exec, exec_count = _want_job_executions(request)
        if want_exec:
            data = get_viewable_jobs_serialized(
                user=get_api_user(request),
                executions=True,
                execution_count=exec_count,
            )

        else:
            data = get_viewable_jobs_serialized(get_api_user(request))

        return Response(data=data, status=200)

    @extend_schema(
        request=JobWriteRequest,
        responses={
            200: OpenApiResponse(GenericResponse, description='Job created'),
            400: OpenApiResponse(GenericResponse, description='Invalid job data provided'),
            403: OpenApiResponse(GenericResponse, description='Not privileged to create jobs'),
        },
        summary='Create a new job.',
        operation_id='job_create'
    )
    def post(self, request):
        if not get_api_user(request).is_staff:
            return Response(data={'msg': 'Not privileged to create jobs'}, status=403)

        serializer = JobWriteRequest(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={'msg': f"Provided job data is not valid: '{serializer.errors}'"},
                status=400,
            )

        for field in BaseJobCredentials.PWD_ATTRS:
            value = serializer.validated_data[field]
            if field in BaseJobCredentials.PWD_ATTRS and \
                    (is_null(value) or value == BaseJobCredentials.PWD_HIDDEN):
                serializer.validated_data[field] = None

        try:
            serializer.save()

        except IntegrityError as err:
            return Response(
                data={'msg': f"Provided job data is not valid: '{err}'"},
                status=400,
            )

        return Response(data={'msg': 'Job created'}, status=200)


class APIJobItem(APIView):
    http_method_names = ['get', 'delete', 'put', 'post']
    serializer_class = GenericResponse
    permission_classes = API_PERMISSION

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(JobReadResponse, description='Return job information'),
            400: OpenApiResponse(GenericResponse, description='Bad parameters provided'),
            403: OpenApiResponse(GenericResponse, description='Not privileged to view the job'),
            404: OpenApiResponse(JobReadResponse, description='Job does not exist'),
        },
        summary='Return information about a job.',
        operation_id='job_view',
        parameters=[
            OpenApiParameter(
                name='executions', type=bool, default=False, description='Return list of job-executions',
                required=False,
            ),
            OpenApiParameter(
                name='execution_count', type=int, default=JOB_EXECUTION_LIMIT,
                description='Maximum count of job-executions to return',
                required=False,
            ),
        ],
    )
    def get(self, request, job_id: int):
        self.serializer_class = JobReadResponse
        user = get_api_user(request)
        job = _find_job(job_id)
        if job is None:
            return Response(data={'msg': f"Job with ID {job_id} does not exist"}, status=404)

        if not has_job_permission(user=user, job=job, permission_needed=CHOICE_JOB_PERMISSION_READ):
            return Response(data={'msg': f"Job '{job.name}' is not viewable"}, status=403)

        data = JobReadResponse(instance=job).data

        want_exec, exec_count = _want_job_executions(request)
        if want_exec:
            data['executions'] = get_job_executions_serialized(job=job, execution_count=exec_count)

        return Response(data=data, status=200)

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(GenericResponse, description='Job deleted'),
            403: OpenApiResponse(GenericResponse, description='Not privileged to delete the job'),
            404: OpenApiResponse(GenericResponse, description='Job does not exist'),
        },
        summary='Delete a job.',
        operation_id='job_delete'
    )
    def delete(self, request, job_id: int):
        user = get_api_user(request)
        try:
            job = _find_job(job_id)

            if job is not None:
                if not has_job_permission(user=user, job=job, permission_needed=CHOICE_JOB_PERMISSION_FULL):
                    return Response(data={'msg': f"Not privileged to delete the job '{job.name}'"}, status=403)

                job.delete()
                return Response(data={'msg': f"Job '{job.name}' deleted"}, status=200)

        except ObjectDoesNotExist:
            pass

        return Response(data={'msg': f"Job with ID {job_id} does not exist"}, status=404)

    @extend_schema(
        request=JobWriteRequest,
        responses={
            200: OpenApiResponse(GenericResponse, description='Job updated'),
            400: OpenApiResponse(GenericResponse, description='Invalid job data provided'),
            403: OpenApiResponse(GenericResponse, description='Not privileged to modify the job'),
            404: OpenApiResponse(GenericResponse, description='Job does not exist'),
        },
        summary='Modify a job.',
        operation_id='job_edit'
    )
    def put(self, request, job_id: int):
        user = get_api_user(request)
        try:
            job = _find_job(job_id)

            if job is not None:
                if not has_job_permission(user=user, job=job, permission_needed=CHOICE_JOB_PERMISSION_WRITE):
                    return Response(data={'msg': f"Not privileged to modify the job '{job.name}'"}, status=403)

                serializer = JobWriteRequest(data=request.data)
                if not serializer.is_valid():
                    return Response(
                        data={'msg': f"Provided job data is not valid: '{serializer.errors}'"},
                        status=400,
                    )

                # pylint: disable=E1101
                try:
                    # not working with password properties: 'Job.objects.filter(id=job_id).update(**serializer.data)'
                    for field, value in serializer.data.items():
                        if field in BaseJobCredentials.PWD_ATTRS and \
                                (is_null(value) or value == BaseJobCredentials.PWD_HIDDEN):
                            value = getattr(job, field)

                        setattr(job, field, value)

                    job.save()

                except IntegrityError as err:
                    return Response(
                        data={'msg': f"Provided job data is not valid: '{err}'"},
                        status=400,
                    )

                return Response(data={'msg': f"Job '{job.name}' updated"}, status=200)

        except ObjectDoesNotExist:
            pass

        return Response(data={'msg': f"Job with ID {job_id} does not exist"}, status=404)

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(JobReadResponse, description='Job execution queued'),
            403: OpenApiResponse(JobReadResponse, description='Not privileged to execute the job'),
            404: OpenApiResponse(JobReadResponse, description='Job does not exist'),
        },
        summary='Execute a job.',
        operation_id='job_execute'
    )
    def post(self, request, job_id: int):
        user = get_api_user(request)
        try:
            job = _find_job(job_id)

            if job is not None:
                if not has_job_permission(user=user, job=job, permission_needed=CHOICE_JOB_PERMISSION_EXECUTE):
                    return Response(data={'msg': f"Not privileged to execute the job '{job.name}'"}, status=403)

                queue_add(job=job, user=user)
                return Response(data={'msg': f"Job '{job.name}' execution queued"}, status=200)

        except ObjectDoesNotExist:
            pass

        return Response(data={'msg': f"Job with ID '{job_id}' does not exist"}, status=404)


class APIJobExecutionItem(APIView):
    http_method_names = ['delete']
    serializer_class = GenericResponse
    permission_classes = API_PERMISSION

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(JobReadResponse, description='Job execution stopping'),
            400: OpenApiResponse(JobReadResponse, description='Job execution is not running'),
            403: OpenApiResponse(JobReadResponse, description='Not privileged to stop the job'),
            404: OpenApiResponse(JobReadResponse, description='Job or execution does not exist'),
        },
        summary='Stop a running job execution.',
        operation_id='job_exec_stop'
    )
    def delete(self, request, job_id: int, exec_id: int):
        user = get_api_user(request)
        try:
            job, execution = _find_job_and_execution(job_id, exec_id)

            if job is not None and execution is not None:
                if not has_job_permission(user=user, job=job, permission_needed=CHOICE_JOB_PERMISSION_EXECUTE):
                    return Response(data={'msg': f"Not privileged to stop the job '{job.name}'"}, status=403)

                if not is_execution_status(execution, 'Running'):
                    return Response(data={'msg': f"Job execution '{job.name}' is not running"}, status=400)

                update_execution_status(execution, 'Stopping')
                return Response(data={'msg': f"Job execution '{job.name}' stopping"}, status=200)

        except ObjectDoesNotExist:
            pass

        return Response(data={'msg': f"Job with ID '{job_id}' or execution does not exist"}, status=404)


class JobExecutionLogReadResponse(BaseResponse):
    lines = serializers.ListSerializer(child=serializers.CharField())


class APIJobExecutionLogs(APIView):
    http_method_names = ['get']
    serializer_class = JobExecutionLogReadResponse
    permission_classes = API_PERMISSION

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(JobExecutionLogReadResponse, description='Return job logs'),
            403: OpenApiResponse(JobExecutionLogReadResponse, description='Not privileged to view the job logs'),
            404: OpenApiResponse(JobExecutionLogReadResponse, description='Job, execution or log-file do not exist'),
        },
        summary='Get logs of a job execution.',
        operation_id='job_exec_logs'
    )
    def get(self, request, job_id: int, exec_id: int, line_start: int = 0):
        user = get_api_user(request)
        try:
            job, execution = _find_job_and_execution(job_id, exec_id)

            if job is not None and execution is not None:
                if not has_job_permission(user=user, job=job, permission_needed=CHOICE_JOB_PERMISSION_READ):
                    return Response(data={'msg': f"Not privileged to view logs of the job '{job.name}'"}, status=403)

                if execution.log_stdout is None:
                    return Response(data={'msg': f"No logs found for job '{job.name}'"}, status=404)

                with open(execution.log_stdout, 'r', encoding='utf-8') as logfile:
                    lines = logfile.readlines()
                    return Response(data={'lines': lines[line_start:]}, status=200)

        except (ObjectDoesNotExist, FileNotFoundError):
            pass

        return Response(
            data={'msg': f"Job with ID '{job_id}', execution with ID '{exec_id}' or log-file does not exist"},
            status=404,
        )


class APIJobExecutionLogFile(APIView):
    http_method_names = ['get']
    serializer_class = JobExecutionLogReadResponse
    permission_classes = API_PERMISSION

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(GenericResponse, description='Download job log-file'),
            403: OpenApiResponse(GenericResponse, description='Not privileged to view the job logs'),
            404: OpenApiResponse(GenericResponse, description='Job, execution or log-file do not exist'),
        },
        summary='Download log-file of a job execution.',
        operation_id='job_exec_logfile',
        parameters=[
            OpenApiParameter(
                name='type', type=str, default='stdout',
                description="Type of log-file to download. Either 'stdout' or 'stderr'",
                required=False,
            ),
        ],
    )
    def get(self, request, job_id: int, exec_id: int):
        user = get_api_user(request)
        try:
            job, execution = _find_job_and_execution(job_id, exec_id)

            if job is not None and execution is not None:
                if not has_job_permission(user=user, job=job, permission_needed=CHOICE_JOB_PERMISSION_READ):
                    return Response(data={'msg': f"Not privileged to view logs of the job '{job.name}'"}, status=403)

                logfile = execution.log_stdout
                if 'type' in request.GET:
                    logfile = execution.log_stderr if request.GET['type'] == 'stderr' else logfile

                if logfile is None:
                    return Response(data={'msg': f"No logs found for job '{job.name}'"}, status=404)

                with open(logfile, 'rb') as _logfile:
                    content_b = _logfile.read()
                    if content_b == b'':
                        return Response(data={'msg': f"Job log-file is empty: '{logfile}'"}, status=404)

                    response = HttpResponse(content_b, content_type='text/plain', status=200)
                    response['Content-Disposition'] = f"inline; filename={logfile.rsplit('/', 1)[1]}"
                    return response

        except (ObjectDoesNotExist, FileNotFoundError):
            pass

        return Response(
            data={'msg': f"Job with ID '{job_id}', execution with ID '{exec_id}' or log-file does not exist"},
            status=404,
        )


class APIJobExecution(APIView):
    http_method_names = ['get']
    serializer_class = JobExecutionReadResponse
    permission_classes = API_PERMISSION

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(JobExecutionReadResponse, description='Return job-execution information'),
        },
        summary='Return list of job-executions the current user is privileged to view.',
        operation_id='job_exec_list',
        parameters=[
            OpenApiParameter(
                name='execution_count', type=int, default=JOB_EXECUTION_LIMIT,
                description='Maximum count of job-executions to return',
                required=False,
            ),
        ],
    )
    def get(self, request):
        # pylint: disable=E1101
        jobs = get_viewable_jobs(get_api_user(request))
        exec_count = _job_execution_count(request)
        if exec_count is None:
            exec_count = JOB_EXECUTION_LIMIT

        serialized = []
        for execution in JobExecution.objects.filter(job__in=jobs).order_by('updated')[:exec_count]:
            serialized.append(get_job_execution_serialized(execution))

        return Response(data=serialized, status=200)
