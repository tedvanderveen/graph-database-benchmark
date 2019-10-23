FROM python:2.7.10
COPY . ./

RUN ./scripts/retrieve_seed_and_unique_node_data_from_s3.sh

RUN python -m pip install -r requirements.txt

ENTRYPOINT ["./kn.py"]