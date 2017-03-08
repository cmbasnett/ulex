class TestClass extends Object;

simulated state TestState extends ParentState
{
    simulated function Okay()
    {
        GotoState('Okay');
    }
Begin:
    SaySomething();

    if (A)
    {
        B();
    }
}