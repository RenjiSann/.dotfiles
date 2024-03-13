use super::command::Command;

struct List<'a>(Vec<Command<'a>>);