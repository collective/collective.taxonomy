FROM plone:5.2.1
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qy                                                              \
    && apt-get install -qy make                                                     \
    && pip install -q virtualenv==16.7.9                                            \
    && mkdir /plone/.buildout                                                       \
    && echo "[buildout]" > /plone/.buildout/default.cfg                             \
    && echo "download-cache = /app/cache/downloads" >> /plone/.buildout/default.cfg \
    && echo "eggs-directory = /app/cache/eggs" >> /plone/.buildout/default.cfg      \
    && usermod -u 1000 plone                                                        \
    && groupmod -g 1000 plone                                                       \
    && chown -R plone:plone /plone                                                  \
    && mkdir /app                                                                   \
    && chown -R plone:plone /app                                                    \
    && apt-get autoremove -y                                                        \
    && rm -rf /var/lib/apt/lists/*

USER plone
VOLUME /app
WORKDIR /app
ENTRYPOINT ["/bin/sh", "-c"]
CMD ["make start-backend"]
