use super::command::Command;

struct List<'a>(Vec<Command<'a>>);

impl<'a, CV> From<CV> for List<'a>
where CV: 'a + IntoIterator<Item = Command<'a>>
{
}