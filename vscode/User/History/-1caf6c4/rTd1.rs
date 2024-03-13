use crate::ast::word::Word;

#[derive(Debug, PartialEq, Eq)]
pub struct Command<'a>{
    command_name: Word<'a>,
    arguments: Vec<Word<'a>>
};

impl<'a, W: Into<Word<'a>>> Command<'a>
{
    pub fn new(cmd: W, args: Vec<W>) -> Self {
        Self { command_name: cmd, arguments: args }
    }
}