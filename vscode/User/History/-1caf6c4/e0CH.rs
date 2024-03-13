use crate::ast::word::Word;

#[derive(Debug, PartialEq, Eq)]
pub struct Command<'a>{
    command_name: Word<'a>,
    arguments: Vec<Word<'a>>
};

impl<'a, W: Into<Word<'a>>> TryFrom<Vec<W>> for Command<'a>
{
    fn from(value: Vec<W>) -> Self {
        let iter = value.into_iter().map(|w| w.into());
        let name = iter.f
        Self()
    }
}