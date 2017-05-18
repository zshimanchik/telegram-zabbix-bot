FROM nginx:1.11.6

RUN rm -rf /etc/nginx/nginx.conf
COPY /conf/ /etc/nginx/
CMD ["nginx", "-g", "daemon off;"]
