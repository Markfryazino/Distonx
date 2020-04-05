FROM sphericalpotatoinvacuum/distonx:latest

WORKDIR /Distonx

COPY docs docs
COPY settings settings
COPY stonks stonks
COPY trash trash
COPY data_collection.py fit.py test.py ./

EXPOSE 42069
