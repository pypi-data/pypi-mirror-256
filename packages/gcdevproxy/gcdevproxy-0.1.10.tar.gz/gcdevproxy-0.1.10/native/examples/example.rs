use std::{
    io::Write,
    net::{Ipv4Addr, SocketAddr},
};

use async_trait::async_trait;
use gcdevproxy::{
    auth::BasicAuthorization,
    hyper::{Request, Response},
    Body, ClientHandlerResult, ConnectionInfo, DeviceHandlerResult, Error, ProxyBuilder,
    RequestHandler,
};
use log::LevelFilter;

/// Proxy request handler.
struct MyRequestHandler;

#[async_trait]
impl RequestHandler for MyRequestHandler {
    async fn handle_device_request(
        &self,
        _: BasicAuthorization,
    ) -> Result<DeviceHandlerResult, Error> {
        // Do not use this in production! You should always check the device ID
        // and key against your device database.
        Ok(DeviceHandlerResult::Accept)
    }

    async fn handle_client_request(
        &self,
        request: Request<Body>,
    ) -> Result<ClientHandlerResult, Error> {
        let is_local_client = request
            .extensions()
            .get::<ConnectionInfo>()
            .map(|info| info.remote_addr().ip().is_loopback())
            .unwrap_or(false);

        // Here we accept only requests from localhost. In practice there would
        // be probably some sort of client authentication mechanism (e.g. JWT).
        if !is_local_client {
            return Ok(ClientHandlerResult::block(empty_response(403)));
        }

        let device_id = request
            .headers()
            .get("x-device")
            .map(|id| id.to_str())
            .and_then(|res| res.ok());

        if let Some(device_id) = device_id {
            Ok(ClientHandlerResult::forward(device_id.to_string(), request))
        } else {
            Ok(ClientHandlerResult::block(empty_response(400)))
        }
    }
}

#[tokio::main]
async fn main() {
    env_logger::builder()
        .filter(None, LevelFilter::Debug)
        .format(|buf, record| {
            writeln!(
                buf,
                "{} {} {}",
                buf.timestamp_millis(),
                record.level(),
                record.args()
            )
        })
        .init();

    let hostname = std::env::var("HOSTNAME").unwrap_or_else(|_| String::from("localhost"));

    let mut builder = ProxyBuilder::new();

    builder
        .hostname(hostname)
        .http_bind_address(SocketAddr::from((Ipv4Addr::UNSPECIFIED, 8080)));
    //.https_bind_address(SocketAddr::from((Ipv4Addr::UNSPECIFIED, 8443)))
    //.lets_encrypt();

    builder
        .build(MyRequestHandler)
        .await
        .unwrap()
        .await
        .unwrap();
}

/// Create an empty HTTP response with a given status code.
fn empty_response(status: u16) -> Response<Body> {
    Response::builder()
        .status(status)
        .body(Body::empty())
        .unwrap()
}
