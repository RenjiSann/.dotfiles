use amiquip::{
    Channel, Connection, ConsumerMessage, ConsumerOptions, Exchange, Publish,
    QueueDeclareOptions,
};
use log::{info, trace};
use serde::{Serialize, Deserialize};

use std::{
    fs,
    path::{Path, PathBuf},
};

use crate::browser::Browser;
use crate::utils::check_or_write_file;

static ROUTING_KEY: &str = "ENSURER";

#[derive(Serialize, Deserialize)]
struct Message {
    directory: PathBuf
}

pub(crate) struct DistributedBrowser(Option<Connection>, Channel);

impl DistributedBrowser {
    pub(crate) fn new(broker_url: &str) -> anyhow::Result<Self> {
        let mut conn = Connection::insecure_open(broker_url)?;
        let channel = conn.open_channel(None)?;

        Ok(Self(Some(conn), channel))
    }
}

impl Drop for DistributedBrowser {
    fn drop(&mut self) {
        self.0.take().map(|conn| conn.close());
    }
}

impl Browser for DistributedBrowser {
    fn _browse(&self, path: &Path) -> anyhow::Result<()> {
        // Schedule directory scanning with a message to the queue
        let msg = Message {
            directory: path.to_owned()
        };
        let payload = serde_json::to_vec(&msg)?;

        info!("Payload: {}", serde_json::to_string_pretty(&payload)?);

        let exchange = Exchange::direct(&self.1);
        exchange
            .publish(Publish::new(&payload, ROUTING_KEY))?;

        // Recurse in other dirs
        for entry in fs::read_dir(path)? {
            let path = entry?.path();
            if path.is_dir() && !path.is_symlink() {
                self._browse(&path)?;
            }
        }

        Ok(())
    }
}

pub struct DistributedEnsurer(Option<Connection>, Channel);

impl Drop for DistributedEnsurer {
    fn drop(&mut self) {
        self.0.take().map(|conn| conn.close());
    }
}

impl DistributedEnsurer {
    pub(crate) fn new(broker_url: &str) -> anyhow::Result<Self> {
        let mut conn = Connection::insecure_open(broker_url)?;
        let channel = conn.open_channel(None)?;

        Ok(Self(Some(conn), channel))
    }

    pub(crate) fn run(&self) -> anyhow::Result<()> {
        let queue = self
            .1
            .queue_declare(ROUTING_KEY, QueueDeclareOptions::default())?;
        let consumer = queue.consume(ConsumerOptions::default())?;

        info!("Waiting for messages");

        while let Some(ConsumerMessage::Delivery(delivery)) =
            consumer.receiver().iter().next()
        {
            let msg: Message = serde_json::from_slice(&delivery.body)?;

            check_or_write_file(&msg.directory)?;
        }

        info!("Communication closed");
        Ok(())
    }
}
