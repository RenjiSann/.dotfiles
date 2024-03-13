use super::command::Command;

struct List<'a>(Vec<Command<'a>>);

impl<'a> From<IntoIterator<Item = Command<'a>>> for List<'a> {
}