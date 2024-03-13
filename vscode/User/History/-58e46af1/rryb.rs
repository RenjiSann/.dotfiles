use super::word::Word;

pub struct Command<'a>(Vec<Word<'a>>);

impl<'a> From<Vec<&'a str>> Command {

}