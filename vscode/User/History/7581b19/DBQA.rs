use super::command::Command;

struct List<'a>(Vec<Command<'a>>);

impl<'a> From<Command<'a>> for List<'a> {

}