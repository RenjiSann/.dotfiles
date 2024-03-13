use std::collections::BinaryHeap;

struct SortedList<T>
where
    T: PartialOrd + Ord,
{
    pub vec: BinaryHeap<T>,
}

impl<T> SortedList<T>
where
    T: PartialOrd + Ord,
{
    pub fn new() -> Self {
        SortedList { vec: BinaryHeap::new() }
    }

    pub fn insert(&mut self, v: T) {
        self.vec.push(v);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let mut heap: SortedList<i32> = SortedList::new();
        heap.insert(45);
        heap.insert(12);
        heap.insert(18);
        println!("{:?}", heap.vec);
    }
}