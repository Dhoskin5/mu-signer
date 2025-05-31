# syntax=docker/dockerfile:1.4

FROM python:3.11-slim AS signer

WORKDIR /signer

# Install build tools and dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    curl \
    jq \
    ca-certificates \
    pkg-config \
    libsodium-dev && \
    git clone https://github.com/jedisct1/minisign.git && \
    cd minisign && \
    cmake . && \
    make && \
    make install && \
    cd .. && rm -rf minisign && \
    rm -rf /var/lib/apt/lists/*


# Python packages
RUN pip install --no-cache-dir pexpect

# Add your signer script
COPY signer.py ./signer.py

# Default entrypoint (can override)
ENTRYPOINT ["python3", "signer.py"]

