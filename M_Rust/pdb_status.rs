use hyper::Client;
use hyper_tls::HttpsConnector;
use bytes::Buf;
use serde_json::{self, Value};
use std::env;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let pdb_id = match env::args().nth(1) {
        Some(pdb_id) => pdb_id,
        None => {
            println!("Usage: <pdb_id>");
            return Ok(());
        }
    };
    let pdb_id = pdb_id.as_str();
    // This is where we will setup our HTTP client requests.
    let https = HttpsConnector::new();
    let client = Client::builder().build::<_, hyper::Body>(https);
    // Parse an `http::Uri`...
    let uri = format!("https://www.ebi.ac.uk/pdbe/api/pdb/entry/status/{}", pdb_id).parse()?;
    // Await the response...
    let resp = client.get(uri).await?;
    println!("Response: {}", resp.status());
    // And now...
    let body = hyper::body::aggregate(resp).await?;
    // try to parse as json with serde_json
    let json_data: Value = serde_json::from_reader(body.reader())?;
    if let Value::String(status_code) = &json_data[pdb_id][0]["status_code"]{
        let status_code = &status_code[..];
        match status_code {
            "REL" => {
                if let Value::Array(obsoletes_array) = &json_data[pdb_id][0]["obsoletes"] {
                    if obsoletes_array.len() == 0 {
                        println!("REL: {}", pdb_id);
                    } else {
                        for obsoletes_pdb_id in obsoletes_array {
                            if let Value::String(o_pdb_id) = obsoletes_pdb_id {
                                println!("REL: {}, OBS: {}", pdb_id, o_pdb_id);
                            }
                        }
                        println!("len(obsoletes): {}", obsoletes_array.len());
                    }
                }
            },
            "OBS" => {
                if let Value::Array(superceded_array) = &json_data[pdb_id][0]["superceded_by"] {
                    if superceded_array.len() == 0 {
                        println!("OBS: {}", pdb_id);
                    } else {
                        for superceded_pdb_id in superceded_array {
                            if let Value::String(s_pdb_id) = superceded_pdb_id {
                                println!("OBS: {}, REL: {}", pdb_id, s_pdb_id);
                            }
                        }
                        println!("len(superceded_by): {}", superceded_array.len());
                    }
                }
            },
            _ => {}
        }
    }
    Ok(())
}
