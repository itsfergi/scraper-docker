FROM archlinux

RUN pacman -Syu --noconfirm gcc qt5-tools wget make sudo python python-pip

RUN mkdir skysource && \
    cd skysource && \
    wget -q -O - https://raw.githubusercontent.com/muldjord/skyscraper/master/update_skyscraper.sh | bash

COPY config.ini /root/.skyscraper/config.ini

COPY artwork.xml /root/.skyscraper/artwork.xml

WORKDIR /usr/src/app
COPY Pipfile ./
RUN pip install --no-cache-dir pipenv && pipenv install
COPY *.py ./
CMD [ "pipenv", "run", "python", "-m", "flask", "run", "--host=0.0.0.0" ]

