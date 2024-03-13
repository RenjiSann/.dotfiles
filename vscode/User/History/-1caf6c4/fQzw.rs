use crate::ast::word::Word;

#[derive(Debug, PartialEq, Eq)]
pub struct Command<'a> {
    command_name: Word<'a>,
    arguments: Vec<Word<'a>>,
}

impl<'a> Command<'a> {
    pub fn new<W: Into<Word<'a>>>(cmd: W, args: Vec<W>) -> Self {
        Self {
            command_name: cmd.into(),
            arguments: args.into_iter().map(|w| w.into()).collect(),
        }
    }
}
