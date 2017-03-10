class TestClass extends Object;

constructor(int A)
{
    Log(@"The number was {A}");
}

function Foo()
{
    local TestClass B;

    B = new TestClass(3);
}