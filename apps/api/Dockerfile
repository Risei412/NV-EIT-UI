FROM public.ecr.aws/lambda/python:3.12
COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY nveit_runtime ${LAMBDA_TASK_ROOT}/nveit_runtime
COPY apps/api/handler.py ${LAMBDA_TASK_ROOT}/handler.py
CMD ["handler.lambda_handler"]
