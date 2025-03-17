FROM public.ecr.aws/lambda/python:3.12
RUN dnf -y install git
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
ENV OMP_NUM_THREADS=1
ENV CPU_COUNT=1
CMD [ "lambda_function.lambda_handler" ]