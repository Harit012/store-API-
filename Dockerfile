FROM python
WORKDIR /app
COPY requirements.txt  . 
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . . 
CMD ["/bin/sh","dicker-entrypoint.sh"]