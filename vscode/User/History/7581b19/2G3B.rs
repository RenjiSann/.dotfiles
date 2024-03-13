use super::command::Command;

struct List<'a>(Vec<Command<'a>>);

impl<'a> From<Command<'a>> for List<'a> {
    fn from(value: Command<'a>) -> Self {
        Self(value)
    }
}