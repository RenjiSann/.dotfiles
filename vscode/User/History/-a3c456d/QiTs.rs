use std::collections::{HashMap};

use lazy_static::lazy_static;
use maplit::hashmap;

lazy_static! {
    pub static ref MAPPINGS: HashMap<char, char> = hashmap! {
       '−' => '-',
    };
}
