Download the attachment, recognize it's a luajit executable.

Try to Google some reverse engineering tutorial about luajit, and you will found a repo <https://github.com/NightNord/ljd>. ljd can do luajit decompilation, but it's tooooo old.

Then I click the `fork` button on that github page, clone another <https://github.com/ammer/ljd>. This repo fix some bugs existing in original ljd.

Decompile the `.luac` file, there are 2 functions, `func1` and `func2`.

`func2` is loaded from a string. Try to dump it and you will find it's another `.luac`, just decompile it and it's an AES module.

`func2` means AES(key=our_input, data="HaveFunWithN1CTF").

Do you want to reverse the `func1` ? 

Nope, the decompiled result, Lua code, is disgusting...

Just have a look and you will recognize it's an white-box AES. 

Search on github, <https://github.com/search?l=JavaScript&q=whitebox+aes+&type=Code&utf8=%E2%9C%93>.

And you will find <https://github.com/tsu-iscd/jcrypto/>.

Aha, look the js code and lua code below:

```javascript
Aes.applyTyTables = function(state) {
    // All computations are aplied to the column vector, as with fixed column No
    var col, newColumn, TyTable, curByte, row;
    for (col = 0; col < 4; col++) {
        newColumn = [0, 0, 0, 0];
        // Compute new column vector
        for (row = 0; row < 4; row++) {
            TyTable = Aes.TyTables[row];
            curByte = state[row][col];
            newColumn = Aes.xorWords(newColumn, TyTable[curByte]);
        }
        // Arrange it in the state
        for (row = 0; row < 4; row++) {
            state[row][col] = newColumn[row];
        }
    }
    return state;
};
```

```Lua
function ()
			slot0.I = function (slot0, slot1)
				slot2, slot3, slot4, slot5, slot6 = nil
				slot6 = 0

				while slot6 < 4 do
					_seq({
						function ()
							return _arr({
								[0] = 0,			0,			0,			0
							}, 4)
						end(),	function ()
							return 0
						end()
					})

					while slot2 < 4 do
						_seq({
							function ()
								return slot1.A[slot2]
							end(),		function ()
								return slot1[slot2][slot3]
							end(),		function ()
								return slot1:S(slot1.S, slot2[])
							end()
						})

						slot2 = slot2 + 1
					end

					slot2 = 0

					while slot2 < 4 do
						slot1[slot2][slot6] = slot5[slot2]
						slot2 = slot2 + 1
					end

					slot6 = slot6 + 1
				end

				return slot1
			end

			return slot0.I
		end()
```

Yes! This JS repo is the source code of this challenge!

Do some modification and use DFA attack mentioned in 34c3ctf, game over!
