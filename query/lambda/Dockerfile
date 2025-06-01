FROM public.ecr.aws/lambda/python:3.12
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY query.py ${LAMBDA_TASK_ROOT}
CMD ["query.lambda_handler"]