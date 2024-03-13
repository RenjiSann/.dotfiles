pub struct Stack {
    vec: Vec<i32>,
}

impl Stack {
    pub fn new() -> Self {
        Stack { vec: vec![] }
    }

    pub fn pop(&mut self) -> Option<i32> {
        self.vec.pop()
    }

    pub fn peek(&self) -> Option<i32> {
        self.vec.last().copied()
    }

    pub fn push(&mut self, i: i32) -> bool{
        self.vec.push(i);
        true
    }
}




#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let mut stack = Stack::new();
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
