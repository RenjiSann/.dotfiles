use crate::ast::word::Word;

#[derive(Debug, PartialEq, Eq)]
pub struct Command<'a>{
    command_name: Word<'a>,
    arguments: Vec<Word<'a>>
};

impl<'a, W: Into<Word<'a>>> From<Vec<W>> for Command<'a>
{
    fn from(value: Vec<W>) -> Self {
        Self(value.into_iter().map(|w| w.into()).collect())
    }
}