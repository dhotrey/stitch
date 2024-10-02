FROM redis:7.4.0-alpine
COPY redis.conf /usr/local/etc/redis/redis.conf
EXPOSE 6379
VOLUME /data
CMD ["redis-server","/usr/local/etc/redis/redis.conf"]
