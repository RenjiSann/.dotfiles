use std::collections::HashMap;

use lazy_static::lazy_static;
use maplit::hashmap;

lazy_static! {
    pub static ref MAPPINGS: HashMap<char, char> = hashmap! {
       '−' => '-',
    };
}

#[macro_export]
macro_rules! matcher {
    ( $c:ident, ) => {
        match $c {
            _ => None
        }
    }
}

#[inline]
pub(crate) fn match_char(c: char) -> Option<char> {
    matcher!(c,)
}