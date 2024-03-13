use super::word::Word;

pub struct Command<'a>(Vec<Word<'a>>);

impl<'a> From<Vec<&'a str>> for Command<'a> {
    fn from(value: Vec<&'a str>) -> Self {
        Self(value.iter().map(|&s| Word(s)).collect())
    }
}