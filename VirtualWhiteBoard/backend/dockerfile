FROM rust as planner

# Build Stage
FROM rust AS builder
WORKDIR /usr/src/

RUN USER=root cargo new ler_2_server
WORKDIR /usr/src/ler_2_server
COPY Cargo.toml Cargo.lock ./
RUN mkdir .cargo
RUN cargo vendor > .cargo/config
COPY ./src ./src
RUN cargo build --release --bin ler_2_server

# Bundle Stage
FROM rust
COPY --from=builder /usr/src/ler_2_server/target/release/ler_2_server /usr/local/bin
USER 1000
ENTRYPOINT ["/usr/local/bin/ler_2_server"]