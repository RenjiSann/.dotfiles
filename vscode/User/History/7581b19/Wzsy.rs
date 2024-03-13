use crate::ast::command::Command;

#[derive(Debug, PartialEq, Eq)]
pub struct List<'a>(Vec<Command<'a>>);

impl<'a, CV> From<CV> for List<'a>
where CV: IntoIterator<Item = Command<'a>>
{
    fn from(value: CV) -> Self {
        Self(
            value.into_iter().collect()
        )
    }
}