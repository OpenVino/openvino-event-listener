FROM python:3.8.2

WORKDIR openvino-event-listener/

RUN python3 -m pip install web3 mysql-connector-python
COPY contracts/contract.abi contracts/contract.abi
COPY listener.py .

CMD python3 -u listener.py