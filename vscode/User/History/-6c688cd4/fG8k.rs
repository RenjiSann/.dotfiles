use std::collections::BinaryHeap;

struct SortedList<T>
where
    T: PartialOrd + Ord,
{
    vec: BinaryHeap<T>,
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
