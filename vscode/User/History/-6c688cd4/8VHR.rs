use std::collections::BTreeSet;

struct SortedList<T>
where T: PartialOrd + Ord {
    elements: BTreeSet<T>
}