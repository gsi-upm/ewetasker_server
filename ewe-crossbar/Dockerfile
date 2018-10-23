FROM crossbario/crossbar

# copy over our own node directory from the host into the image
# set user "root" before copy and change owner afterwards
USER root

RUN pip install -U pytest
RUN pip install objectpath
RUN pip install voluptuous
RUN pip install elasticsearch
RUN pip install pytz

COPY ./crossbar /crossbar
RUN chown -R crossbar:crossbar /crossbar




ENTRYPOINT ["crossbar", "start", "--cbdir", "/crossbar/.crossbar"]
