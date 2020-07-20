# Plone + make + virtualenv
FROM plone:5.2.1
ARG DEBIAN_FRONTEND=noninteractive

COPY . /plone/app

RUN apt-get update -qy                                                              \
    && apt-get install -qy                                                          \
               make                                                                 \
    && pip install -q virtualenv==16.7.9                                            \
    && mkdir /plone/.buildout                                                       \
    && echo "[buildout]" > /plone/.buildout/default.cfg                             \
    && echo "download-cache = /app/cache/downloads" >> /plone/.buildout/default.cfg \
    && echo "eggs-directory = /app/cache/eggs" >> /plone/.buildout/default.cfg      \
    && mkdir /app                                                                   \
    && ln -sf /plone/buildout-cache /app/cache                                      \
    && usermod -u 1000 plone                                                        \
    && groupmod -g 1000 plone                                                       \
    && chown -R plone:plone /plone                                                  \
    && chown -R plone:plone /app                                                    \
    && su - plone -c 'cd /plone/app && make build-backend'                          \
    && apt-get autoremove -y                                                        \
    && rm -rf /var/lib/apt/lists/*                                                  \
    && rm -rf /plone/buildout-cache/downloads/*

USER plone
VOLUME /app
WORKDIR /plone/app
ENTRYPOINT ["/usr/bin/make"]
CMD ["start-backend"]
