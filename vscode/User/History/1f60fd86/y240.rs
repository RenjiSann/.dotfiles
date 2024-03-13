pub trait Stack {
    fn new() -> Self;
    fn pop(&mut self) -> Option<i32>;
    fn push(&mut self, value : i32) -> bool;
    fn peek(&self) -> Option<i32>;
}
struct StackImplem {
    vec: Vec<i32>
}

impl Stack for StackImplem {
    fn new() -> Self {
        StackImplem { vec: vec![] }
    }

    fn pop(&mut self) -> Option<i32> {
        self.vec.pop()
    }

    fn peek(&self) -> Option<i32> {
        self.vec.last().copied()
    }

    fn push(&mut self, i: i32) -> bool {
        self.vec.push(i);
        true
    }
}

pub fn new_stack() -> impl Stack {
    return StackImplem::new();
}

#[cfg(test)]
mod tests {
    use super::Stack;

    #[test]
    fn it_works() {
        let mut stack: _ = Stack::new();
        stack.push(1);
        stack.push(2);
        stack.push(3);
        assert_eq!(stack.pop(), Some(3));
        assert_eq!(stack.peek(), Some(2));
        assert_eq!(stack.pop(), Some(2));
        assert_eq!(stack.pop(), Some(1));
        assert_eq!(stack.pop(), None);
    }
}
