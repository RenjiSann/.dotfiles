package Week is
    -- This is a declarative part. You can put only
    -- declarations here, no statements
    type Days is (Monday, Tuesday, Wednesday,
    Thursday, Friday, Saturday, Sunday);
    type WorkLoad_Type is array (Days range <>) of Natural;
    Workload : constant Workload_Type :=
    (Monday .. Friday => 8, Friday => 7, Saturday | Sunday => 0);
end Week;