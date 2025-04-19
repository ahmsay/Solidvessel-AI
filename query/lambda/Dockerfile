FROM public.ecr.aws/lambda/python:3.12
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY query_lambda.py ${LAMBDA_TASK_ROOT}
CMD ["query_lambda.lambda_handler"]