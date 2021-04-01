FROM selenium/standalone-chrome

USER root
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN sudo apt-get update -y
RUN sudo apt-get install -y python3-distutils
RUN sudo apt-get install -y python3-apt
RUN python3 get-pip.py
RUN python3 -m pip install selenium bs4

WORKDIR /run_dir
COPY *.py ./
COPY ./nordvpn_servers ./nordvpn_servers
COPY ./run_selenium.sh .
ENTRYPOINT ["bash", "run_selenium.sh"]
CMD [""]