use super::command::Command;

struct List<'a>(Vec<Command<'a>>);

impl<'a> From<IntoIterator<>> for List<'a> {
    fn from(value: impl IntoIterator<Item = Command<'a>>) -> Self {
        Self(
            value.into_iter().collect()
        )
    }
}