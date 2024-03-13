use std::collections::HashMap;

use lazy_static::lazy_static;
use maplit::hashmap;

lazy_static! {
    pub static ref MAPPINGS: HashMap<char, char> = hashmap! {
       '−' => '-',
    };
}

#[macro_export]
macro_rules! array_match {
    ($(($x:literal, $y:literal)),*) => {
        $($x => Some($y),)*
    };
}

#[inline]
pub(crate) fn match_char(c: char) -> Option<char> {
    match c {
        array_match!(
            ('−', '-'),
        ),
        _ => None
    }
}