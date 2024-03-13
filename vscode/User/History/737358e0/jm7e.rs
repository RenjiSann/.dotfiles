pub struct Stack {
    vec: Vec<i32>,
}

impl Stack {
    pub fn new(size: usize) -> Self {
        Stack { vec: vec![], index: 0 }
    }

    pub fn pop(&mut self) -> Option<i32> {
        self.vec.pop()
    }

    pub fn peek(&self) -> Option<i32> {
        if let Some(x) = self.vec.pop() {
            self.vec.push(x);
            Some(x)
        } else {
            None
        }
    }

    pub fn push(&mut self, i: i32) {
        self.vec.push(i)
    }
}




#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let mut stack = Stack::new();
        stack.push(1), Ok(());
        stack.push(2), Ok(());
        stack.push(3), Ok(());
        assert_eq!(stack.pop(), Some(3));
        assert_eq!(stack.peek(), Some(2));
        assert_eq!(stack.pop(), Some(2));
        assert_eq!(stack.pop(), Some(1));
        assert_eq!(stack.pop(), None);
    }
}
