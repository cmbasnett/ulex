class TestClass extends Object;

var ArrayList<int> Integers;
var class<ROVehicle> A;

function Okay()
{
    local class<ROVehicle> B;

    B = class<ROVehicle>(A);
}

DefaultProperties
{
    A=(A=30,B=40,C=(X=7,Y=1,Z=5))
}