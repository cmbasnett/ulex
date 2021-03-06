//==============================================================================
// Darklight Games (c) 2008-2015
//==============================================================================

class ArrayList extends Object
  template(T, U);

var array<T> Items;

function Add(T Item)
{
    Items[Items.Length] = Item;
}

function AddAtIndex(int Index, T Item)
{
    Items.Insert(Index, 1);

    Items[Index] = Item;
}

function Clear()
{
    Items.Length = 0;
}

function bool Contains(T Item)
{
    return IndexOf(Item) != -1;
}

function string Get(int Index)
{
    return Items[Index];
}

function int IndexOf(T Item)
{
    local int i;

    for (i = 0; i < Items.Length; ++i)
    {
        if (Items[i] == Item)
        {
            return i;
        }
    }

    return -1;
}

function bool IsEmpty()
{
    return Items.Length == 0;
}

function int LastIndexOf(T Item)
{
    local int i;

    for (i = Items.Length - 1; i >= 0; --i)
    {
        if (Items[i] == Item)
        {
            return i;
        }
    }

    return -1;
}

function Remove(int Index)
{
    Items.Remove(Index, 1);
}

function RemoveRange(int FromIndex, int ToIndex)
{
    local int Count;

    Count = ToIndex - FromIndex + 1;

    Items.Remove(FromIndex, Count);
}

simulated function Resize(int Length)
{
    Items.Length = Length;
}

function Set(int Index, T Item)
{
    Items[Index] = Item;
}

function int Size()
{
    return Items.Length;
}

function array<T> ToArray()
{
    return Items;
}
