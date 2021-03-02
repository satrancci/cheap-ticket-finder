FROM selenium/standalone-chrome

USER root
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN sudo apt-get update -y
RUN sudo apt-get install -y python3-distutils
RUN sudo apt-get install -y python3-apt
RUN python3 get-pip.py
RUN python3 -m pip install selenium

RUN mkdir run_dir
WORKDIR /run_dir
ENTRYPOINT python3 run_selenium.py