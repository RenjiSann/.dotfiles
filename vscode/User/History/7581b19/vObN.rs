use std::array::IntoIter;

use super::command::Command;

struct List<'a>(Vec<Command<'a>>);

impl<'a> From<IntoIter<Command<'a>, 6>> for List<'a> {
    fn from(value: IntoIter<Command<'a>, 6>) -> Self {
        todo!()
    }
}