use super::command::Command;

struct List<'a>(Vec<Command<'a>>);

impl<'a, CV> From<CV> for List<'a>
where CV: impl IntoIterator<Command<'a>>
{
    fn from(value: impl IntoIterator<Item = Command<'a>>) -> Self {
        Self(
            value.into_iter().collect()
        )
    }
}