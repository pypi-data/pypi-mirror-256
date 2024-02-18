# Build stage
FROM python:3.12.2-alpine AS build

# Install tools for build stage
# hadolint ignore=DL3013,DL3018
RUN apk add --no-cache git && pip install --no-cache-dir --upgrade build 

WORKDIR /build
COPY . .
RUN pip install --no-cache-dir .

# Runtime stage
FROM python:3.12.2-alpine

COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /usr/local/bin/blopic /usr/local/bin/blopic

ENTRYPOINT ["blopic"]
