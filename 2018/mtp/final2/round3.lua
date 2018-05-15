Validate error.
bs = {}
slot1 = require("bit").lshift
bs.new = function (slot0, slot1)
	o = {
		data = slot1 or {}
	}

	if type(slot1[1]) == "number" then
		t = {}

		for slot5, slot6 in pairs(slot1) do
			t[#t + 1] = string.char(slot6)
		end

		o.data = t
	end

	o.i = 1
	o.length = #slot1

	setmetatable(o, slot0)

	slot0.__index = slot0

	return o
end
bs.move = function (slot0, slot1)
	if slot0.length + 1 < slot0.i + slot1 then
		return false
	elseif slot0.i + slot1 < 1 then
		return false
	else
		slot0.i = slot0.i + slot1

		return true
	end

	return 
end
bs.pop = function (slot0, slot1)
	slot6, slot3 = slot0.pop_raw(slot0, slot1)
	slot4 = {}

	for slot8, slot9 in pairs(slot2) do
		slot4[#slot4 + 1] = string.byte(slot9, 1)
	end

	return slot4, slot3
end
bs.pop_raw = function (slot0, slot1)
	return {
		unpack(slot0.data, slot0.i, (slot0.i + slot1) - 1)
	}, slot0.move(slot0, slot1)
end
bs.readByte = function (slot0)
	slot1, slot4 = slot0.pop(slot0, 1)

	return slot1[1], slot2
end
bs.readInt = function (slot0)
	slot1 = 0

	for slot6, slot7 in pairs(slot2) do
		slot1 = slot1 + slot0(slot7, (slot6 - 1)*8)
	end

	if 2147483648.0 < slot1 then
		slot1 = (slot1 + 2147483648.0)%4294967296.0 - 2147483648.0
	end

	return slot1
end
bs.readStr = function (slot0)
	slot1 = ""

	for slot7, slot8 in pairs(slot3) do
		slot1 = slot1 .. slot8
	end

	return slot1
end
bs.bPos = function (slot0)
	return slot0.i - 1
end
c34c179c = {
	new = function (slot0)
		setmetatable({
			a455d1c9 = {}
		}, slot0)

		slot0.__index = slot0

		return 
	end,
	push = function (slot0, slot1)
		table.insert(slot0.a455d1c9, slot1)

		return 
	end,
	pop = function (slot0, slot1)
		slot2 = slot1 or 1
		slot3 = {}

		for slot7 = 1, slot2, 1 do
			slot3[#slot3 + 1] = table.remove(slot0.a455d1c9, #slot0.a455d1c9)
		end

		return unpack(slot3)
	end
}
RADIX = 10000000
RADIX_LEN = math.floor(math.log10(RADIX))
BigNum = {
	mt = {}
}
BigNum.new = function (slot0)
	setmetatable(slot1, BigNum.mt)
	BigNum.change({}, slot0)

	return 
end
BigNum.mt.sub = function (slot0, slot1)
	BigNum.sub(BigNum.new(slot0), BigNum.new(slot1), BigNum.new())

	return BigNum.new()
end
BigNum.mt.add = function (slot0, slot1)
	BigNum.add(BigNum.new(slot0), BigNum.new(slot1), BigNum.new())

	return BigNum.new()
end
BigNum.mt.mul = function (slot0, slot1)
	BigNum.mul(BigNum.new(slot0), BigNum.new(slot1), BigNum.new())

	return BigNum.new()
end
BigNum.mt.div = function (slot0, slot1)
	slot2 = {}
	slot3 = {}

	BigNum.div(slot2, BigNum.new(slot1), BigNum.new(), BigNum.new())

	return BigNum.new(), BigNum.new()
end
BigNum.mt.tostring = function (slot0)
	slot1 = 0
	slot2 = 0
	slot3 = ""
	slot4 = ""

	if slot0 == nil then
		return "nil"
	elseif 0 < slot0.len then
		for slot8 = slot0.len - 2, 0, -1 do
			for slot12 = 0, RADIX_LEN - string.len(slot0[slot8]) - 1, 1 do
				slot4 = slot4 .. "0"
			end

			slot4 = slot4 .. slot0[slot8]
		end

		slot4 = slot0[slot0.len - 1] .. slot4

		if slot0.signal == "-" then
			slot4 = slot0.signal .. slot4
		end

		return slot4
	else
		return ""
	end

	return 
end
BigNum.mt.pow = function (slot0, slot1)
	return BigNum.pow(BigNum.new(slot0), BigNum.new(slot1))
end
BigNum.mt.eq = function (slot0, slot1)
	return BigNum.eq(BigNum.new(slot0), BigNum.new(slot1))
end
BigNum.mt.lt = function (slot0, slot1)
	return BigNum.lt(BigNum.new(slot0), BigNum.new(slot1))
end
BigNum.mt.le = function (slot0, slot1)
	return BigNum.le(BigNum.new(slot0), BigNum.new(slot1))
end
BigNum.mt.unm = function (slot0)
	if BigNum.new(slot0).signal == "+" then
		slot1.signal = "-"
	else
		slot1.signal = "+"
	end

	return slot1
end
BigNum.mt.__metatable = "hidden"
BigNum.mt.__tostring = BigNum.mt.tostring
BigNum.mt.__add = BigNum.mt.add
BigNum.mt.__sub = BigNum.mt.sub
BigNum.mt.__mul = BigNum.mt.mul
BigNum.mt.__div = BigNum.mt.div
BigNum.mt.__pow = BigNum.mt.pow
BigNum.mt.__unm = BigNum.mt.unm
BigNum.mt.__eq = BigNum.mt.eq
BigNum.mt.__le = BigNum.mt.le
BigNum.mt.__lt = BigNum.mt.lt

setmetatable(BigNum.mt, {
	__index = "inexistent field",
	__metatable = "hidden",
	__newindex = "not available"
})

BigNum.add = function (slot0, slot1, slot2)
	slot3 = 0
	slot4 = 0
	slot5 = 0
	slot6 = "+"
	slot7 = 0

	if slot0 == nil or slot1 == nil or slot2 == nil then
		error("Function BigNum.add: parameter nil")
	elseif slot0.signal == "-" and slot1.signal == "+" then
		slot0.signal = "+"

		BigNum.sub(slot1, slot0, slot2)

		if not rawequal(slot0, slot2) then
			slot0.signal = "-"
		end

		return 0
	elseif slot0.signal == "+" and slot1.signal == "-" then
		slot1.signal = "+"

		BigNum.sub(slot0, slot1, slot2)

		if not rawequal(slot1, slot2) then
			slot1.signal = "-"
		end

		return 0
	elseif slot0.signal == "-" and slot1.signal == "-" then
		slot6 = "-"
	end

	slot7 = slot2.len

	if slot1.len < slot0.len then
		slot3 = slot0.len
	else
		slot3 = slot1.len
		slot1 = slot0
		slot0 = slot1
	end

	for slot11 = 0, slot3 - 1, 1 do
		--- BLOCK #0 88-90, warpins: 2 ---
		if slot1[slot11] ~= nil then
			--- BLOCK #1 91-96, warpins: 1 ---
			slot2[slot11] = slot0[slot11] + slot1[slot11] + slot5
			--- END OF BLOCK #1 ---



		else
			--- BLOCK #2 97-99, warpins: 1 ---
			slot2[slot11] = slot0[slot11] + slot5
			--- END OF BLOCK #2 ---



		end

		--- END OF BLOCK #0 ---

		FLOW; TARGET BLOCK #3


		--- BLOCK #1 91-96, warpins: 1 ---
		slot2[slot11] = slot0[slot11] + slot1[slot11] + slot5
		--- END OF BLOCK #1 ---



		--- BLOCK #2 97-99, warpins: 1 ---
		slot2[slot11] = slot0[slot11] + slot5
		--- END OF BLOCK #2 ---



		--- BLOCK #3 100-103, warpins: 2 ---
		--- END OF BLOCK #3 ---

		if RADIX <= slot2[slot11] then
		JUMP TO BLOCK #4
		else
		JUMP TO BLOCK #5
		end


		--- BLOCK #4 104-109, warpins: 1 ---
		slot2[slot11] = slot2[slot11] - RADIX
		slot5 = 1 or 0
		--- END OF BLOCK #4 ---

		FLOW; TARGET BLOCK #6


		--- BLOCK #6 111-111, warpins: 2 ---
		--- END OF BLOCK #6 ---



	end

	if slot5 == 1 then
		--- BLOCK #23 114-115, warpins: 1 ---
		slot2[slot3] = 1
		--- END OF BLOCK #23 ---



	end

	slot2.len = slot3 + slot5
	slot2.signal = slot6

	for slot11 = slot2.len, slot7, 1 do
		--- BLOCK #0 123-125, warpins: 2 ---
		slot2[slot11] = nil
		--- END OF BLOCK #0 ---



	end

	return 0
end
BigNum.sub = function (slot0, slot1, slot2)
	--- BLOCK #0 1-6, warpins: 1 ---
	slot3 = 0
	slot4 = 0
	slot5 = 0
	slot6 = 0

	--- END OF BLOCK #0 ---

	if slot0 ~= nil then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #3
	end


	--- BLOCK #1 7-8, warpins: 1 ---
	--- END OF BLOCK #1 ---

	if slot1 ~= nil then
	JUMP TO BLOCK #2
	else
	JUMP TO BLOCK #3
	end


	--- BLOCK #2 9-10, warpins: 1 ---
	--- END OF BLOCK #2 ---

	if slot2 == nil then
	JUMP TO BLOCK #3
	else
	JUMP TO BLOCK #4
	end


	--- BLOCK #3 11-14, warpins: 3 ---
	error("Function BigNum.sub: parameter nil")

	--- END OF BLOCK #3 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #21


	--- BLOCK #4 15-17, warpins: 1 ---
	--- END OF BLOCK #4 ---

	if slot0.signal == "-" then
	JUMP TO BLOCK #5
	else
	JUMP TO BLOCK #9
	end


	--- BLOCK #5 18-20, warpins: 1 ---
	--- END OF BLOCK #5 ---

	if slot1.signal == "+" then
	JUMP TO BLOCK #6
	else
	JUMP TO BLOCK #9
	end


	--- BLOCK #6 21-36, warpins: 1 ---
	slot0.signal = "+"

	BigNum.add(slot0, slot1, slot2)

	slot2.signal = "-"

	--- END OF BLOCK #6 ---

	slot7 = if not rawequal(slot0, slot2)

	 then
	JUMP TO BLOCK #7
	else
	JUMP TO BLOCK #8
	end


	--- BLOCK #7 37-38, warpins: 1 ---
	slot0.signal = "-"

	--- END OF BLOCK #7 ---

	FLOW; TARGET BLOCK #8


	--- BLOCK #8 39-41, warpins: 2 ---
	return 0

	--- END OF BLOCK #8 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #21


	--- BLOCK #9 42-44, warpins: 2 ---
	--- END OF BLOCK #9 ---

	if slot0.signal == "-" then
	JUMP TO BLOCK #10
	else
	JUMP TO BLOCK #16
	end


	--- BLOCK #10 45-47, warpins: 1 ---
	--- END OF BLOCK #10 ---

	if slot1.signal == "-" then
	JUMP TO BLOCK #11
	else
	JUMP TO BLOCK #16
	end


	--- BLOCK #11 48-63, warpins: 1 ---
	slot0.signal = "+"
	slot1.signal = "+"

	BigNum.sub(slot1, slot0, slot2)
	--- END OF BLOCK #11 ---

	slot7 = if not rawequal(slot0, slot2)

	 then
	JUMP TO BLOCK #12
	else
	JUMP TO BLOCK #13
	end


	--- BLOCK #12 64-65, warpins: 1 ---
	slot0.signal = "-"

	--- END OF BLOCK #12 ---

	FLOW; TARGET BLOCK #13


	--- BLOCK #13 66-71, warpins: 2 ---
	--- END OF BLOCK #13 ---

	slot7 = if not rawequal(slot1, slot2)

	 then
	JUMP TO BLOCK #14
	else
	JUMP TO BLOCK #15
	end


	--- BLOCK #14 72-73, warpins: 1 ---
	slot1.signal = "-"

	--- END OF BLOCK #14 ---

	FLOW; TARGET BLOCK #15


	--- BLOCK #15 74-76, warpins: 2 ---
	return 0

	--- END OF BLOCK #15 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #21


	--- BLOCK #16 77-79, warpins: 2 ---
	--- END OF BLOCK #16 ---

	if slot0.signal == "+" then
	JUMP TO BLOCK #17
	else
	JUMP TO BLOCK #21
	end


	--- BLOCK #17 80-82, warpins: 1 ---
	--- END OF BLOCK #17 ---

	if slot1.signal == "-" then
	JUMP TO BLOCK #18
	else
	JUMP TO BLOCK #21
	end


	--- BLOCK #18 83-96, warpins: 1 ---
	slot1.signal = "+"

	BigNum.add(slot0, slot1, slot2)
	--- END OF BLOCK #18 ---

	slot7 = if not rawequal(slot1, slot2)

	 then
	JUMP TO BLOCK #19
	else
	JUMP TO BLOCK #20
	end


	--- BLOCK #19 97-98, warpins: 1 ---
	slot1.signal = "-"

	--- END OF BLOCK #19 ---

	FLOW; TARGET BLOCK #20


	--- BLOCK #20 99-100, warpins: 2 ---
	return 0

	--- END OF BLOCK #20 ---

	FLOW; TARGET BLOCK #21


	--- BLOCK #21 101-107, warpins: 6 ---
	--- END OF BLOCK #21 ---

	if BigNum.compareAbs(slot0, slot1)
	 == 2 then
	JUMP TO BLOCK #22
	else
	JUMP TO BLOCK #23
	end


	--- BLOCK #22 108-118, warpins: 1 ---
	BigNum.sub(slot1, slot0, slot2)

	slot2.signal = "-"

	return 0

	--- END OF BLOCK #22 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #24


	--- BLOCK #23 119-119, warpins: 1 ---
	slot3 = slot0.len
	--- END OF BLOCK #23 ---

	FLOW; TARGET BLOCK #24


	--- BLOCK #24 120-126, warpins: 2 ---
	slot6 = slot2.len
	slot2.len = 0

	--- END OF BLOCK #24 ---

	FLOW; TARGET BLOCK #25


	--- BLOCK #25 127-155, warpins: 0 ---
	for slot10 = 0, slot3 - 1, 1 do
		--- BLOCK #0 127-129, warpins: 2 ---
		--- END OF BLOCK #0 ---

		if slot1[slot10] ~= nil then
		JUMP TO BLOCK #1
		else
		JUMP TO BLOCK #2
		end


		--- BLOCK #1 130-135, warpins: 1 ---
		slot2[slot10] = slot0[slot10] - slot1[slot10] - slot5
		--- END OF BLOCK #1 ---

		UNCONDITIONAL JUMP; TARGET BLOCK #3


		--- BLOCK #2 136-138, warpins: 1 ---
		slot2[slot10] = slot0[slot10] - slot5
		--- END OF BLOCK #2 ---

		FLOW; TARGET BLOCK #3


		--- BLOCK #3 139-142, warpins: 2 ---
		--- END OF BLOCK #3 ---

		if slot2[slot10] < 0 then
		JUMP TO BLOCK #4
		else
		JUMP TO BLOCK #5
		end


		--- BLOCK #4 143-148, warpins: 1 ---
		slot2[slot10] = RADIX + slot2[slot10]
		slot5 = 1
		--- END OF BLOCK #4 ---

		UNCONDITIONAL JUMP; TARGET BLOCK #6


		--- BLOCK #5 149-149, warpins: 1 ---
		slot5 = 0
		--- END OF BLOCK #5 ---

		FLOW; TARGET BLOCK #6


		--- BLOCK #6 150-152, warpins: 2 ---
		--- END OF BLOCK #6 ---

		if slot2[slot10] ~= 0 then
		JUMP TO BLOCK #7
		else
		JUMP TO BLOCK #8
		end


		--- BLOCK #7 153-154, warpins: 1 ---
		slot2.len = slot10 + 1
		--- END OF BLOCK #7 ---

		FLOW; TARGET BLOCK #8


		--- BLOCK #8 155-155, warpins: 2 ---
		--- END OF BLOCK #8 ---



	end

	--- END OF BLOCK #25 ---

	FLOW; TARGET BLOCK #26


	--- BLOCK #26 156-160, warpins: 1 ---
	slot2.signal = "+"
	--- END OF BLOCK #26 ---

	if slot2.len == 0 then
	JUMP TO BLOCK #27
	else
	JUMP TO BLOCK #28
	end


	--- BLOCK #27 161-164, warpins: 1 ---
	slot2.len = 1
	slot2[0] = 0

	--- END OF BLOCK #27 ---

	FLOW; TARGET BLOCK #28


	--- BLOCK #28 165-166, warpins: 2 ---
	--- END OF BLOCK #28 ---

	if slot5 == 1 then
	JUMP TO BLOCK #29
	else
	JUMP TO BLOCK #30
	end


	--- BLOCK #29 167-169, warpins: 1 ---
	error("Error in function sub")

	--- END OF BLOCK #29 ---

	FLOW; TARGET BLOCK #30


	--- BLOCK #30 170-176, warpins: 2 ---
	--- END OF BLOCK #30 ---

	FLOW; TARGET BLOCK #31


	--- BLOCK #31 177-179, warpins: 0 ---
	for slot10 = slot2.len, max(slot6, slot3 - 1), 1 do
		--- BLOCK #0 177-179, warpins: 2 ---
		slot2[slot10] = nil
		--- END OF BLOCK #0 ---



	end

	--- END OF BLOCK #31 ---

	FLOW; TARGET BLOCK #32


	--- BLOCK #32 180-181, warpins: 1 ---
	return 0
	--- END OF BLOCK #32 ---



end
BigNum.mul = function (slot0, slot1, slot2)
	--- BLOCK #0 1-11, warpins: 1 ---
	slot3 = 0
	j = 0
	slot4 = BigNum.new()
	slot5 = 0
	slot6 = 0
	slot7 = slot2.len

	--- END OF BLOCK #0 ---

	if slot0 ~= nil then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #3
	end


	--- BLOCK #1 12-13, warpins: 1 ---
	--- END OF BLOCK #1 ---

	if slot1 ~= nil then
	JUMP TO BLOCK #2
	else
	JUMP TO BLOCK #3
	end


	--- BLOCK #2 14-15, warpins: 1 ---
	--- END OF BLOCK #2 ---

	if slot2 == nil then
	JUMP TO BLOCK #3
	else
	JUMP TO BLOCK #4
	end


	--- BLOCK #3 16-19, warpins: 3 ---
	error("Function BigNum.mul: parameter nil")
	--- END OF BLOCK #3 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #6


	--- BLOCK #4 20-23, warpins: 1 ---
	--- END OF BLOCK #4 ---

	if slot0.signal ~= slot1.signal then
	JUMP TO BLOCK #5
	else
	JUMP TO BLOCK #6
	end


	--- BLOCK #5 24-33, warpins: 1 ---
	BigNum.mul(slot0, -slot1, slot2)

	slot2.signal = "-"

	return 0

	--- END OF BLOCK #5 ---

	FLOW; TARGET BLOCK #6


	--- BLOCK #6 34-41, warpins: 3 ---
	slot2.len = slot0.len + slot1.len

	--- END OF BLOCK #6 ---

	FLOW; TARGET BLOCK #7


	--- BLOCK #7 42-45, warpins: 0 ---
	for slot11 = 1, slot2.len, 1 do
		--- BLOCK #0 42-45, warpins: 2 ---
		slot2[slot11 - 1] = 0
		--- END OF BLOCK #0 ---



	end

	--- END OF BLOCK #7 ---

	FLOW; TARGET BLOCK #8


	--- BLOCK #8 46-49, warpins: 1 ---
	--- END OF BLOCK #8 ---

	FLOW; TARGET BLOCK #9


	--- BLOCK #9 50-52, warpins: 0 ---
	for slot11 = slot2.len, slot7, 1 do
		--- BLOCK #0 50-52, warpins: 2 ---
		slot2[slot11] = nil
		--- END OF BLOCK #0 ---



	end

	--- END OF BLOCK #9 ---

	FLOW; TARGET BLOCK #10


	--- BLOCK #10 53-57, warpins: 1 ---
	--- END OF BLOCK #10 ---

	FLOW; TARGET BLOCK #11


	--- BLOCK #11 58-92, warpins: 0 ---
	for slot11 = 0, slot0.len - 1, 1 do
		--- BLOCK #0 58-62, warpins: 2 ---
		--- END OF BLOCK #0 ---

		FLOW; TARGET BLOCK #1


		--- BLOCK #1 63-85, warpins: 0 ---
		for slot15 = 0, slot1.len - 1, 1 do
			--- BLOCK #0 63-85, warpins: 2 ---
			slot2[slot11 + slot15] = math.mod(slot0[slot11]*slot1[slot15] + slot6 + slot2[slot11 + slot15], RADIX)
			slot5 = slot2[slot11 + slot15]
			slot6 = math.floor((slot0[slot11]*slot1[slot15] + slot6 + slot2[slot11 + slot15])/RADIX)
			--- END OF BLOCK #0 ---



		end

		--- END OF BLOCK #1 ---

		FLOW; TARGET BLOCK #2


		--- BLOCK #2 86-87, warpins: 1 ---
		--- END OF BLOCK #2 ---

		if slot6 ~= 0 then
		JUMP TO BLOCK #3
		else
		JUMP TO BLOCK #4
		end


		--- BLOCK #3 88-90, warpins: 1 ---
		slot2[slot11 + slot1.len] = slot6
		--- END OF BLOCK #3 ---

		FLOW; TARGET BLOCK #4


		--- BLOCK #4 91-92, warpins: 2 ---
		slot6 = 0
		--- END OF BLOCK #4 ---



	end

	--- END OF BLOCK #11 ---

	FLOW; TARGET BLOCK #12


	--- BLOCK #12 93-97, warpins: 1 ---
	--- END OF BLOCK #12 ---

	FLOW; TARGET BLOCK #13


	--- BLOCK #13 98-111, warpins: 0 ---
	for slot11 = slot2.len - 1, 1, -1 do
		--- BLOCK #0 98-100, warpins: 2 ---
		--- END OF BLOCK #0 ---

		if slot2[slot11] ~= nil then
		JUMP TO BLOCK #1
		else
		JUMP TO BLOCK #5
		end


		--- BLOCK #1 101-103, warpins: 1 ---
		--- END OF BLOCK #1 ---

		if slot2[slot11] ~= 0 then
		JUMP TO BLOCK #2
		else
		JUMP TO BLOCK #5
		end


		--- BLOCK #2 104-104, warpins: 1 ---
		--- END OF BLOCK #2 ---

		FLOW; TARGET BLOCK #3


		--- BLOCK #3 105-105, warpins: 1 ---
		break

		--- END OF BLOCK #3 ---

		FLOW; TARGET BLOCK #4


		--- BLOCK #4 105-105, warpins: 0 ---
		--- END OF BLOCK #4 ---

		UNCONDITIONAL JUMP; TARGET BLOCK #6


		--- BLOCK #5 106-107, warpins: 2 ---
		slot2[slot11] = nil
		--- END OF BLOCK #5 ---

		FLOW; TARGET BLOCK #6


		--- BLOCK #6 108-111, warpins: 2 ---
		slot2.len = slot2.len - 1
		--- END OF BLOCK #6 ---



	end

	--- END OF BLOCK #13 ---

	FLOW; TARGET BLOCK #14


	--- BLOCK #14 112-113, warpins: 2 ---
	return 0
	--- END OF BLOCK #14 ---



end
BigNum.div = function (slot0, slot1, slot2, slot3)
	--- BLOCK #0 1-21, warpins: 1 ---
	slot4 = BigNum.new()
	slot5 = BigNum.new()
	slot6 = BigNum.new("1")

	--- END OF BLOCK #0 ---

	if BigNum.compareAbs(slot1, BigNum.new("0"))
	 == 0 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 22-24, warpins: 1 ---
	error("Function BigNum.div: Division by zero")
	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 25-26, warpins: 2 ---
	--- END OF BLOCK #2 ---

	if slot0 ~= nil then
	JUMP TO BLOCK #3
	else
	JUMP TO BLOCK #6
	end


	--- BLOCK #3 27-28, warpins: 1 ---
	--- END OF BLOCK #3 ---

	if slot1 ~= nil then
	JUMP TO BLOCK #4
	else
	JUMP TO BLOCK #6
	end


	--- BLOCK #4 29-30, warpins: 1 ---
	--- END OF BLOCK #4 ---

	if slot2 ~= nil then
	JUMP TO BLOCK #5
	else
	JUMP TO BLOCK #6
	end


	--- BLOCK #5 31-32, warpins: 1 ---
	--- END OF BLOCK #5 ---

	if slot3 == nil then
	JUMP TO BLOCK #6
	else
	JUMP TO BLOCK #7
	end


	--- BLOCK #6 33-36, warpins: 4 ---
	error("Function BigNum.div: parameter nil")

	--- END OF BLOCK #6 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #20


	--- BLOCK #7 37-39, warpins: 1 ---
	--- END OF BLOCK #7 ---

	if slot0.signal == "+" then
	JUMP TO BLOCK #8
	else
	JUMP TO BLOCK #10
	end


	--- BLOCK #8 40-42, warpins: 1 ---
	--- END OF BLOCK #8 ---

	if slot1.signal == "-" then
	JUMP TO BLOCK #9
	else
	JUMP TO BLOCK #10
	end


	--- BLOCK #9 43-58, warpins: 1 ---
	slot1.signal = "+"

	BigNum.div(slot0, slot1, slot2, slot3)

	slot1.signal = "-"
	slot2.signal = "-"

	return 0

	--- END OF BLOCK #9 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #20


	--- BLOCK #10 59-61, warpins: 2 ---
	--- END OF BLOCK #10 ---

	if slot0.signal == "-" then
	JUMP TO BLOCK #11
	else
	JUMP TO BLOCK #15
	end


	--- BLOCK #11 62-64, warpins: 1 ---
	--- END OF BLOCK #11 ---

	if slot1.signal == "+" then
	JUMP TO BLOCK #12
	else
	JUMP TO BLOCK #15
	end


	--- BLOCK #12 65-77, warpins: 1 ---
	slot0.signal = "+"

	BigNum.div(slot0, slot1, slot2, slot3)

	slot0.signal = "-"

	--- END OF BLOCK #12 ---

	if slot3 < slot7 then
	JUMP TO BLOCK #13
	else
	JUMP TO BLOCK #14
	end


	--- BLOCK #13 78-89, warpins: 1 ---
	BigNum.add(slot2, slot6, slot2)
	BigNum.sub(slot1, slot3, slot3)

	--- END OF BLOCK #13 ---

	FLOW; TARGET BLOCK #14


	--- BLOCK #14 90-94, warpins: 2 ---
	slot2.signal = "-"

	return 0

	--- END OF BLOCK #14 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #20


	--- BLOCK #15 95-97, warpins: 2 ---
	--- END OF BLOCK #15 ---

	if slot0.signal == "-" then
	JUMP TO BLOCK #16
	else
	JUMP TO BLOCK #20
	end


	--- BLOCK #16 98-100, warpins: 1 ---
	--- END OF BLOCK #16 ---

	if slot1.signal == "-" then
	JUMP TO BLOCK #17
	else
	JUMP TO BLOCK #20
	end


	--- BLOCK #17 101-115, warpins: 1 ---
	slot0.signal = "+"
	slot1.signal = "+"

	BigNum.div(slot0, slot1, slot2, slot3)

	slot0.signal = "-"

	--- END OF BLOCK #17 ---

	if slot3 < slot7 then
	JUMP TO BLOCK #18
	else
	JUMP TO BLOCK #19
	end


	--- BLOCK #18 116-127, warpins: 1 ---
	BigNum.add(slot2, slot6, slot2)
	BigNum.sub(slot1, slot3, slot3)

	--- END OF BLOCK #18 ---

	FLOW; TARGET BLOCK #19


	--- BLOCK #19 128-131, warpins: 2 ---
	slot1.signal = "-"

	return 0

	--- END OF BLOCK #19 ---

	FLOW; TARGET BLOCK #20


	--- BLOCK #20 132-151, warpins: 6 ---
	slot4.len = slot0.len - slot1.len - 1

	BigNum.change(slot2, "0")
	BigNum.change(slot3, "0")
	BigNum.copy(slot0, slot3)

	--- END OF BLOCK #20 ---

	FLOW; TARGET BLOCK #21


	--- BLOCK #21 152-158, warpins: 2 ---
	--- END OF BLOCK #21 ---

	FLOW; TARGET BLOCK #22


	--- BLOCK #22 159-242, warpins: 0 ---
	while BigNum.compareAbs(slot3, slot1) ~= 2 do
		--- BLOCK #0 159-159, warpins: 1 ---
		--- END OF BLOCK #0 ---

		FLOW; TARGET BLOCK #1


		--- BLOCK #1 160-167, warpins: 1 ---
		--- END OF BLOCK #1 ---

		if slot1[slot1.len - 1] <= slot3[slot3.len - 1] then
		JUMP TO BLOCK #2
		else
		JUMP TO BLOCK #3
		end


		--- BLOCK #2 168-190, warpins: 1 ---
		BigNum.put(slot4, math.floor(slot3[slot3.len - 1]/slot1[slot1.len - 1]), slot3.len - slot1.len)

		slot4.len = slot3.len - slot1.len + 1

		--- END OF BLOCK #2 ---

		UNCONDITIONAL JUMP; TARGET BLOCK #4


		--- BLOCK #3 191-218, warpins: 1 ---
		BigNum.put(slot4, math.floor((slot3[slot3.len - 1]*RADIX + slot3[slot3.len - 2])/slot1[slot1.len - 1]), slot3.len - slot1.len - 1)

		slot4.len = slot3.len - slot1.len
		--- END OF BLOCK #3 ---

		FLOW; TARGET BLOCK #4


		--- BLOCK #4 219-222, warpins: 2 ---
		--- END OF BLOCK #4 ---

		if slot3.signal ~= slot1.signal then
		JUMP TO BLOCK #5
		else
		JUMP TO BLOCK #6
		end


		--- BLOCK #5 223-225, warpins: 1 ---
		slot4.signal = "-"
		--- END OF BLOCK #5 ---

		UNCONDITIONAL JUMP; TARGET BLOCK #7


		--- BLOCK #6 226-227, warpins: 1 ---
		slot4.signal = "+"

		--- END OF BLOCK #6 ---

		FLOW; TARGET BLOCK #7


		--- BLOCK #7 228-241, warpins: 2 ---
		BigNum.add(slot4, slot2, slot2)
		BigNum.sub(slot3, slot4*slot1, slot3)
		--- END OF BLOCK #7 ---

		FLOW; TARGET BLOCK #8


		--- BLOCK #8 242-242, warpins: 2 ---
		--- END OF BLOCK #8 ---



	end

	--- END OF BLOCK #22 ---

	FLOW; TARGET BLOCK #23


	--- BLOCK #23 242-244, warpins: 1 ---
	--- END OF BLOCK #23 ---

	if slot3.signal == "-" then
	JUMP TO BLOCK #24
	else
	JUMP TO BLOCK #25
	end


	--- BLOCK #24 245-253, warpins: 1 ---
	decr(slot2)
	BigNum.add(slot1, slot3, slot3)

	--- END OF BLOCK #24 ---

	FLOW; TARGET BLOCK #25


	--- BLOCK #25 254-255, warpins: 2 ---
	return 0
	--- END OF BLOCK #25 ---



end
BigNum.pow = function (slot0, slot1)
	--- BLOCK #0 1-18, warpins: 1 ---
	slot2 = BigNum.new(slot1)
	slot3 = BigNum.new(1)
	slot4 = BigNum.new(slot0)

	--- END OF BLOCK #0 ---

	if slot1 < BigNum.new("0")
	 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 19-22, warpins: 1 ---
	error("Function BigNum.exp: domain error")

	--- END OF BLOCK #1 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #4


	--- BLOCK #2 23-24, warpins: 1 ---
	--- END OF BLOCK #2 ---

	if slot1 == slot5 then
	JUMP TO BLOCK #3
	else
	JUMP TO BLOCK #4
	end


	--- BLOCK #3 25-25, warpins: 1 ---
	return slot3

	--- END OF BLOCK #3 ---

	FLOW; TARGET BLOCK #4


	--- BLOCK #4 26-26, warpins: 4 ---
	--- END OF BLOCK #4 ---

	FLOW; TARGET BLOCK #5


	--- BLOCK #5 27-43, warpins: 0 ---
	while true do
		--- BLOCK #0 27-33, warpins: 1 ---
		--- END OF BLOCK #0 ---

		if math.mod(slot2[0], 2)

		 == 0 then
		JUMP TO BLOCK #1
		else
		JUMP TO BLOCK #2
		end


		--- BLOCK #1 34-35, warpins: 1 ---
		slot2 = slot2/2
		--- END OF BLOCK #1 ---

		UNCONDITIONAL JUMP; TARGET BLOCK #4


		--- BLOCK #2 36-39, warpins: 1 ---
		slot3 = slot4*slot3

		--- END OF BLOCK #2 ---

		if slot2/2 == slot5 then
		JUMP TO BLOCK #3
		else
		JUMP TO BLOCK #4
		end


		--- BLOCK #3 40-40, warpins: 1 ---
		return slot3

		--- END OF BLOCK #3 ---

		FLOW; TARGET BLOCK #4


		--- BLOCK #4 41-42, warpins: 3 ---
		slot4 = slot4*slot4
		--- END OF BLOCK #4 ---

		FLOW; TARGET BLOCK #5


		--- BLOCK #5 43-43, warpins: 3 ---
		--- END OF BLOCK #5 ---



	end

	--- END OF BLOCK #5 ---

	FLOW; TARGET BLOCK #6


	--- BLOCK #6 43-43, warpins: 0 ---
	return 
	--- END OF BLOCK #6 ---



end
BigNum.exp = BigNum.pow
BigNum.gcd = function (slot0, slot1)
	--- BLOCK #0 1-12, warpins: 1 ---
	slot2 = {}
	slot3 = {}
	slot4 = {}
	slot5 = {}
	slot6 = {}

	--- END OF BLOCK #0 ---

	if slot0 ~= BigNum.new("0")

	 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 13-14, warpins: 1 ---
	--- END OF BLOCK #1 ---

	if slot1 == slot6 then
	JUMP TO BLOCK #2
	else
	JUMP TO BLOCK #3
	end


	--- BLOCK #2 15-18, warpins: 2 ---
	return BigNum.new("1")

	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 19-40, warpins: 2 ---
	BigNum.new(slot0).signal = "+"
	BigNum.new(slot1).signal = "+"
	slot4 = BigNum.new()
	slot5 = BigNum.new()

	--- END OF BLOCK #3 ---

	FLOW; TARGET BLOCK #4


	--- BLOCK #4 41-42, warpins: 2 ---
	--- END OF BLOCK #4 ---

	FLOW; TARGET BLOCK #5


	--- BLOCK #5 43-57, warpins: 0 ---
	while slot6 < slot3 do
		--- BLOCK #0 43-43, warpins: 1 ---
		--- END OF BLOCK #0 ---

		FLOW; TARGET BLOCK #1


		--- BLOCK #1 44-56, warpins: 1 ---
		BigNum.div(slot2, slot3, slot4, slot5)

		slot5 = slot2
		slot3 = slot5
		slot2 = slot3
		--- END OF BLOCK #1 ---

		FLOW; TARGET BLOCK #2


		--- BLOCK #2 57-57, warpins: 1 ---
		--- END OF BLOCK #2 ---



	end

	--- END OF BLOCK #5 ---

	FLOW; TARGET BLOCK #6


	--- BLOCK #6 57-57, warpins: 1 ---
	return slot2
	--- END OF BLOCK #6 ---



end
BigNum.mmc = BigNum.gcd
BigNum.eq = function (slot0, slot1)
	--- BLOCK #0 1-7, warpins: 1 ---
	--- END OF BLOCK #0 ---

	if BigNum.compare(slot0, slot1)

	 == 0 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 8-10, warpins: 1 ---
	return true
	--- END OF BLOCK #1 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #3


	--- BLOCK #2 11-12, warpins: 1 ---
	return false
	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 13-13, warpins: 2 ---
	return 
	--- END OF BLOCK #3 ---



end
BigNum.lt = function (slot0, slot1)
	--- BLOCK #0 1-7, warpins: 1 ---
	--- END OF BLOCK #0 ---

	if BigNum.compare(slot0, slot1)

	 == 2 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 8-10, warpins: 1 ---
	return true
	--- END OF BLOCK #1 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #3


	--- BLOCK #2 11-12, warpins: 1 ---
	return false
	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 13-13, warpins: 2 ---
	return 
	--- END OF BLOCK #3 ---



end
BigNum.le = function (slot0, slot1)
	--- BLOCK #0 1-9, warpins: 1 ---
	slot2 = -1

	--- END OF BLOCK #0 ---

	if BigNum.compare(slot0, slot1)

	 ~= 0 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 10-11, warpins: 1 ---
	--- END OF BLOCK #1 ---

	if slot2 == 2 then
	JUMP TO BLOCK #2
	else
	JUMP TO BLOCK #3
	end


	--- BLOCK #2 12-14, warpins: 2 ---
	return true
	--- END OF BLOCK #2 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #4


	--- BLOCK #3 15-16, warpins: 1 ---
	return false
	--- END OF BLOCK #3 ---

	FLOW; TARGET BLOCK #4


	--- BLOCK #4 17-17, warpins: 2 ---
	return 
	--- END OF BLOCK #4 ---



end
BigNum.compareAbs = function (slot0, slot1)
	--- BLOCK #0 1-2, warpins: 1 ---
	--- END OF BLOCK #0 ---

	if slot0 ~= nil then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 3-4, warpins: 1 ---
	--- END OF BLOCK #1 ---

	if slot1 == nil then
	JUMP TO BLOCK #2
	else
	JUMP TO BLOCK #3
	end


	--- BLOCK #2 5-8, warpins: 2 ---
	error("Function compare: parameter nil")

	--- END OF BLOCK #2 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #9


	--- BLOCK #3 9-12, warpins: 1 ---
	--- END OF BLOCK #3 ---

	if slot1.len < slot0.len then
	JUMP TO BLOCK #4
	else
	JUMP TO BLOCK #5
	end


	--- BLOCK #4 13-15, warpins: 1 ---
	return 1
	--- END OF BLOCK #4 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #9


	--- BLOCK #5 16-19, warpins: 1 ---
	--- END OF BLOCK #5 ---

	if slot0.len < slot1.len then
	JUMP TO BLOCK #6
	else
	JUMP TO BLOCK #7
	end


	--- BLOCK #6 20-22, warpins: 1 ---
	return 2

	--- END OF BLOCK #6 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #9


	--- BLOCK #7 23-28, warpins: 1 ---
	slot2 = nil

	--- END OF BLOCK #7 ---

	FLOW; TARGET BLOCK #8


	--- BLOCK #8 29-42, warpins: 0 ---
	for slot6 = slot0.len - 1, 0, -1 do
		--- BLOCK #0 29-32, warpins: 2 ---
		--- END OF BLOCK #0 ---

		if slot1[slot6] < slot0[slot6] then
		JUMP TO BLOCK #1
		else
		JUMP TO BLOCK #2
		end


		--- BLOCK #1 33-35, warpins: 1 ---
		return 1
		--- END OF BLOCK #1 ---

		UNCONDITIONAL JUMP; TARGET BLOCK #4


		--- BLOCK #2 36-39, warpins: 1 ---
		--- END OF BLOCK #2 ---

		if slot0[slot6] < slot1[slot6] then
		JUMP TO BLOCK #3
		else
		JUMP TO BLOCK #4
		end


		--- BLOCK #3 40-41, warpins: 1 ---
		return 2
		--- END OF BLOCK #3 ---

		FLOW; TARGET BLOCK #4


		--- BLOCK #4 42-42, warpins: 3 ---
		--- END OF BLOCK #4 ---



	end

	--- END OF BLOCK #8 ---

	FLOW; TARGET BLOCK #9


	--- BLOCK #9 43-44, warpins: 4 ---
	return 0
	--- END OF BLOCK #9 ---



end
BigNum.compare = function (slot0, slot1)
	--- BLOCK #0 1-3, warpins: 1 ---
	slot2 = 0

	--- END OF BLOCK #0 ---

	if slot0 ~= nil then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 4-5, warpins: 1 ---
	--- END OF BLOCK #1 ---

	if slot1 == nil then
	JUMP TO BLOCK #2
	else
	JUMP TO BLOCK #3
	end


	--- BLOCK #2 6-9, warpins: 2 ---
	error("Funtion BigNum.compare: parameter nil")

	--- END OF BLOCK #2 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #12


	--- BLOCK #3 10-12, warpins: 1 ---
	--- END OF BLOCK #3 ---

	if slot0.signal == "+" then
	JUMP TO BLOCK #4
	else
	JUMP TO BLOCK #6
	end


	--- BLOCK #4 13-15, warpins: 1 ---
	--- END OF BLOCK #4 ---

	if slot1.signal == "-" then
	JUMP TO BLOCK #5
	else
	JUMP TO BLOCK #6
	end


	--- BLOCK #5 16-18, warpins: 1 ---
	return 1
	--- END OF BLOCK #5 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #12


	--- BLOCK #6 19-21, warpins: 2 ---
	--- END OF BLOCK #6 ---

	if slot0.signal == "-" then
	JUMP TO BLOCK #7
	else
	JUMP TO BLOCK #9
	end


	--- BLOCK #7 22-24, warpins: 1 ---
	--- END OF BLOCK #7 ---

	if slot1.signal == "+" then
	JUMP TO BLOCK #8
	else
	JUMP TO BLOCK #9
	end


	--- BLOCK #8 25-27, warpins: 1 ---
	return 2

	--- END OF BLOCK #8 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #12


	--- BLOCK #9 28-30, warpins: 2 ---
	--- END OF BLOCK #9 ---

	if slot0.signal == "-" then
	JUMP TO BLOCK #10
	else
	JUMP TO BLOCK #12
	end


	--- BLOCK #10 31-33, warpins: 1 ---
	--- END OF BLOCK #10 ---

	if slot1.signal == "-" then
	JUMP TO BLOCK #11
	else
	JUMP TO BLOCK #12
	end


	--- BLOCK #11 34-34, warpins: 1 ---
	slot2 = 1

	--- END OF BLOCK #11 ---

	FLOW; TARGET BLOCK #12


	--- BLOCK #12 35-38, warpins: 6 ---
	--- END OF BLOCK #12 ---

	if slot1.len < slot0.len then
	JUMP TO BLOCK #13
	else
	JUMP TO BLOCK #14
	end


	--- BLOCK #13 39-41, warpins: 1 ---
	return slot2 + 1
	--- END OF BLOCK #13 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #18


	--- BLOCK #14 42-45, warpins: 1 ---
	--- END OF BLOCK #14 ---

	if slot0.len < slot1.len then
	JUMP TO BLOCK #15
	else
	JUMP TO BLOCK #16
	end


	--- BLOCK #15 46-48, warpins: 1 ---
	return slot2 - 2

	--- END OF BLOCK #15 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #18


	--- BLOCK #16 49-54, warpins: 1 ---
	slot3 = nil

	--- END OF BLOCK #16 ---

	FLOW; TARGET BLOCK #17


	--- BLOCK #17 55-68, warpins: 0 ---
	for slot7 = slot0.len - 1, 0, -1 do
		--- BLOCK #0 55-58, warpins: 2 ---
		--- END OF BLOCK #0 ---

		if slot1[slot7] < slot0[slot7] then
		JUMP TO BLOCK #1
		else
		JUMP TO BLOCK #2
		end


		--- BLOCK #1 59-61, warpins: 1 ---
		return slot2 + 1
		--- END OF BLOCK #1 ---

		UNCONDITIONAL JUMP; TARGET BLOCK #4


		--- BLOCK #2 62-65, warpins: 1 ---
		--- END OF BLOCK #2 ---

		if slot0[slot7] < slot1[slot7] then
		JUMP TO BLOCK #3
		else
		JUMP TO BLOCK #4
		end


		--- BLOCK #3 66-67, warpins: 1 ---
		return slot2 - 2
		--- END OF BLOCK #3 ---

		FLOW; TARGET BLOCK #4


		--- BLOCK #4 68-68, warpins: 3 ---
		--- END OF BLOCK #4 ---



	end

	--- END OF BLOCK #17 ---

	FLOW; TARGET BLOCK #18


	--- BLOCK #18 69-70, warpins: 3 ---
	return 0
	--- END OF BLOCK #18 ---



end
BigNum.copy = function (slot0, slot1)
	--- BLOCK #0 1-2, warpins: 1 ---
	--- END OF BLOCK #0 ---

	if slot0 ~= nil then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #5
	end


	--- BLOCK #1 3-4, warpins: 1 ---
	--- END OF BLOCK #1 ---

	if slot1 ~= nil then
	JUMP TO BLOCK #2
	else
	JUMP TO BLOCK #5
	end


	--- BLOCK #2 5-10, warpins: 1 ---
	slot2 = nil

	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 11-13, warpins: 0 ---
	for slot6 = 0, slot0.len - 1, 1 do
		--- BLOCK #0 11-13, warpins: 2 ---
		slot1[slot6] = slot0[slot6]
		--- END OF BLOCK #0 ---



	end

	--- END OF BLOCK #3 ---

	FLOW; TARGET BLOCK #4


	--- BLOCK #4 14-16, warpins: 1 ---
	slot1.len = slot0.len

	--- END OF BLOCK #4 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #6


	--- BLOCK #5 17-19, warpins: 2 ---
	error("Function BigNum.copy: parameter nil")

	--- END OF BLOCK #5 ---

	FLOW; TARGET BLOCK #6


	--- BLOCK #6 20-20, warpins: 2 ---
	return 
	--- END OF BLOCK #6 ---



end
BigNum.change = function (slot0, slot1)
	--- BLOCK #0 1-7, warpins: 1 ---
	slot2 = 0
	slot3 = 0
	slot4 = slot1
	slot5 = nil
	slot6 = 0

	--- END OF BLOCK #0 ---

	if slot0 == nil then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 8-11, warpins: 1 ---
	error("BigNum.change: parameter nil")
	--- END OF BLOCK #1 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #42


	--- BLOCK #2 12-16, warpins: 1 ---
	--- END OF BLOCK #2 ---

	if type(slot0)
	 ~= "table" then
	JUMP TO BLOCK #3
	else
	JUMP TO BLOCK #4
	end


	--- BLOCK #3 17-20, warpins: 1 ---
	error("BigNum.change: parameter error, type unexpected")

	--- END OF BLOCK #3 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #42


	--- BLOCK #4 21-22, warpins: 1 ---
	--- END OF BLOCK #4 ---

	if slot4 == nil then
	JUMP TO BLOCK #5
	else
	JUMP TO BLOCK #6
	end


	--- BLOCK #5 23-29, warpins: 1 ---
	slot0.len = 1
	slot0[0] = 0
	slot0.signal = "+"

	--- END OF BLOCK #5 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #42


	--- BLOCK #6 30-34, warpins: 1 ---
	--- END OF BLOCK #6 ---

	if type(slot4)

	 == "table" then
	JUMP TO BLOCK #7
	else
	JUMP TO BLOCK #15
	end


	--- BLOCK #7 35-37, warpins: 1 ---
	--- END OF BLOCK #7 ---

	if slot4.len ~= nil then
	JUMP TO BLOCK #8
	else
	JUMP TO BLOCK #15
	end


	--- BLOCK #8 38-41, warpins: 1 ---
	--- END OF BLOCK #8 ---

	FLOW; TARGET BLOCK #9


	--- BLOCK #9 42-44, warpins: 0 ---
	for slot10 = 0, slot4.len, 1 do
		--- BLOCK #0 42-44, warpins: 2 ---
		slot0[slot10] = slot4[slot10]
		--- END OF BLOCK #0 ---



	end

	--- END OF BLOCK #9 ---

	FLOW; TARGET BLOCK #10


	--- BLOCK #10 45-47, warpins: 1 ---
	--- END OF BLOCK #10 ---

	if slot4.signal ~= "-" then
	JUMP TO BLOCK #11
	else
	JUMP TO BLOCK #13
	end


	--- BLOCK #11 48-50, warpins: 1 ---
	--- END OF BLOCK #11 ---

	if slot4.signal ~= "+" then
	JUMP TO BLOCK #12
	else
	JUMP TO BLOCK #13
	end


	--- BLOCK #12 51-53, warpins: 1 ---
	slot0.signal = "+"
	--- END OF BLOCK #12 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #14


	--- BLOCK #13 54-55, warpins: 2 ---
	slot0.signal = slot4.signal
	--- END OF BLOCK #13 ---

	FLOW; TARGET BLOCK #14


	--- BLOCK #14 56-59, warpins: 2 ---
	slot6 = slot0.len
	slot0.len = slot4.len

	--- END OF BLOCK #14 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #42


	--- BLOCK #15 60-64, warpins: 2 ---
	--- END OF BLOCK #15 ---

	if type(slot4)
	 ~= "string" then
	JUMP TO BLOCK #16
	else
	JUMP TO BLOCK #17
	end


	--- BLOCK #16 65-69, warpins: 1 ---
	--- END OF BLOCK #16 ---

	if type(slot4)
	 == "number" then
	JUMP TO BLOCK #17
	else
	JUMP TO BLOCK #41
	end


	--- BLOCK #17 70-77, warpins: 2 ---
	--- END OF BLOCK #17 ---

	if string.sub(slot4, 1, 1)
	 ~= "+" then
	JUMP TO BLOCK #18
	else
	JUMP TO BLOCK #19
	end


	--- BLOCK #18 78-85, warpins: 1 ---
	--- END OF BLOCK #18 ---

	if string.sub(slot4, 1, 1)

	 == "-" then
	JUMP TO BLOCK #19
	else
	JUMP TO BLOCK #20
	end


	--- BLOCK #19 86-99, warpins: 2 ---
	slot0.signal = string.sub(slot4, 1, 1)
	slot4 = string.sub(slot4, 2)
	--- END OF BLOCK #19 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #21


	--- BLOCK #20 100-101, warpins: 1 ---
	slot0.signal = "+"

	--- END OF BLOCK #20 ---

	FLOW; TARGET BLOCK #21


	--- BLOCK #21 102-115, warpins: 2 ---
	--- END OF BLOCK #21 ---

	if string.find(string.gsub(slot4, " ", ""), "e")
	 ~= nil then
	JUMP TO BLOCK #22
	else
	JUMP TO BLOCK #29
	end


	--- BLOCK #22 116-133, warpins: 1 ---
	--- END OF BLOCK #22 ---

	if tonumber(string.sub(slot4, slot7 + 1))

	 ~= nil then
	JUMP TO BLOCK #23
	else
	JUMP TO BLOCK #25
	end


	--- BLOCK #23 134-136, warpins: 1 ---
	--- END OF BLOCK #23 ---

	if 0 < slot8 then
	JUMP TO BLOCK #24
	else
	JUMP TO BLOCK #25
	end


	--- BLOCK #24 137-141, warpins: 1 ---
	slot8 = tonumber(slot8)

	--- END OF BLOCK #24 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #26


	--- BLOCK #25 142-144, warpins: 2 ---
	error("Function BigNum.change: string is not a valid number")

	--- END OF BLOCK #25 ---

	FLOW; TARGET BLOCK #26


	--- BLOCK #26 145-158, warpins: 2 ---
	--- END OF BLOCK #26 ---

	FLOW; TARGET BLOCK #27


	--- BLOCK #27 159-162, warpins: 0 ---
	for slot12 = string.len(slot4), slot8, 1 do
		--- BLOCK #0 159-162, warpins: 2 ---
		slot4 = slot4 .. "0"
		--- END OF BLOCK #0 ---



	end

	--- END OF BLOCK #27 ---

	FLOW; TARGET BLOCK #28


	--- BLOCK #28 163-163, warpins: 1 ---
	--- END OF BLOCK #28 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #31


	--- BLOCK #29 164-171, warpins: 1 ---
	--- END OF BLOCK #29 ---

	if string.find(slot4, "%.")

	 ~= nil then
	JUMP TO BLOCK #30
	else
	JUMP TO BLOCK #31
	end


	--- BLOCK #30 172-178, warpins: 1 ---
	slot4 = string.sub(slot4, 1, slot7 - 1)
	--- END OF BLOCK #30 ---

	FLOW; TARGET BLOCK #31


	--- BLOCK #31 179-187, warpins: 3 ---
	slot6 = slot0.len

	--- END OF BLOCK #31 ---

	if RADIX_LEN < string.len(slot4)

	 then
	JUMP TO BLOCK #32
	else
	JUMP TO BLOCK #40
	end


	--- BLOCK #32 188-199, warpins: 1 ---
	--- END OF BLOCK #32 ---

	FLOW; TARGET BLOCK #33


	--- BLOCK #33 200-224, warpins: 0 ---
	for slot12 = 1, slot5 - slot5 - math.floor(slot5/RADIX_LEN)*RADIX_LEN, RADIX_LEN do
		--- BLOCK #0 200-214, warpins: 2 ---
		slot0[slot2] = tonumber(string.sub(slot4, -((slot12 + RADIX_LEN) - 1), -slot12))

		--- END OF BLOCK #0 ---

		if slot0[slot2] == nil then
		JUMP TO BLOCK #1
		else
		JUMP TO BLOCK #2
		end


		--- BLOCK #1 215-221, warpins: 1 ---
		error("Function BigNum.change: string is not a valid number")

		slot0.len = 0

		return 1

		--- END OF BLOCK #1 ---

		FLOW; TARGET BLOCK #2


		--- BLOCK #2 222-224, warpins: 2 ---
		slot2 = slot2 + 1
		slot3 = slot3 + 1
		--- END OF BLOCK #2 ---



	end

	--- END OF BLOCK #33 ---

	FLOW; TARGET BLOCK #34


	--- BLOCK #34 225-226, warpins: 1 ---
	--- END OF BLOCK #34 ---

	if slot8 ~= 0 then
	JUMP TO BLOCK #35
	else
	JUMP TO BLOCK #36
	end


	--- BLOCK #35 227-238, warpins: 1 ---
	slot0[slot2] = tonumber(string.sub(slot4, 1, slot8))
	slot0.len = slot3 + 1
	--- END OF BLOCK #35 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #37


	--- BLOCK #36 239-239, warpins: 1 ---
	slot0.len = slot3

	--- END OF BLOCK #36 ---

	FLOW; TARGET BLOCK #37


	--- BLOCK #37 240-244, warpins: 2 ---
	--- END OF BLOCK #37 ---

	FLOW; TARGET BLOCK #38


	--- BLOCK #38 245-255, warpins: 0 ---
	for slot12 = slot0.len - 1, 1, -1 do
		--- BLOCK #0 245-247, warpins: 2 ---
		--- END OF BLOCK #0 ---

		if slot0[slot12] == 0 then
		JUMP TO BLOCK #1
		else
		JUMP TO BLOCK #2
		end


		--- BLOCK #1 248-253, warpins: 1 ---
		slot0[slot12] = nil
		slot0.len = slot0.len - 1

		--- END OF BLOCK #1 ---

		UNCONDITIONAL JUMP; TARGET BLOCK #3


		--- BLOCK #2 254-254, warpins: 0 ---
		break
		--- END OF BLOCK #2 ---

		FLOW; TARGET BLOCK #3


		--- BLOCK #3 255-255, warpins: 1 ---
		--- END OF BLOCK #3 ---



	end

	--- END OF BLOCK #38 ---

	FLOW; TARGET BLOCK #39


	--- BLOCK #39 256-256, warpins: 1 ---
	--- END OF BLOCK #39 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #42


	--- BLOCK #40 257-263, warpins: 1 ---
	slot0[slot2] = tonumber(slot4)
	slot0.len = 1

	--- END OF BLOCK #40 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #42


	--- BLOCK #41 264-266, warpins: 1 ---
	error("Function BigNum.change: parameter error, type unexpected")

	--- END OF BLOCK #41 ---

	FLOW; TARGET BLOCK #42


	--- BLOCK #42 267-268, warpins: 9 ---
	--- END OF BLOCK #42 ---

	if slot6 ~= nil then
	JUMP TO BLOCK #43
	else
	JUMP TO BLOCK #45
	end


	--- BLOCK #43 269-272, warpins: 1 ---
	--- END OF BLOCK #43 ---

	FLOW; TARGET BLOCK #44


	--- BLOCK #44 273-275, warpins: 0 ---
	for slot10 = slot0.len, slot6, 1 do
		--- BLOCK #0 273-275, warpins: 2 ---
		slot0[slot10] = nil
		--- END OF BLOCK #0 ---



	end

	--- END OF BLOCK #44 ---

	FLOW; TARGET BLOCK #45


	--- BLOCK #45 276-277, warpins: 2 ---
	return 0
	--- END OF BLOCK #45 ---



end
BigNum.put = function (slot0, slot1, slot2)
	--- BLOCK #0 1-2, warpins: 1 ---
	--- END OF BLOCK #0 ---

	if slot0 == nil then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 3-5, warpins: 1 ---
	error("Function BigNum.put: parameter nil")

	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 6-10, warpins: 2 ---
	slot3 = 0

	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 11-13, warpins: 0 ---
	for slot7 = 0, slot2 - 1, 1 do
		--- BLOCK #0 11-13, warpins: 2 ---
		slot0[slot7] = 0
		--- END OF BLOCK #0 ---



	end

	--- END OF BLOCK #3 ---

	FLOW; TARGET BLOCK #4


	--- BLOCK #4 14-18, warpins: 1 ---
	slot0[slot2] = slot1

	--- END OF BLOCK #4 ---

	FLOW; TARGET BLOCK #5


	--- BLOCK #5 19-21, warpins: 0 ---
	for slot7 = slot2 + 1, slot0.len, 1 do
		--- BLOCK #0 19-21, warpins: 2 ---
		slot0[slot7] = nil
		--- END OF BLOCK #0 ---



	end

	--- END OF BLOCK #5 ---

	FLOW; TARGET BLOCK #6


	--- BLOCK #6 22-24, warpins: 1 ---
	slot0.len = slot2

	return 0
	--- END OF BLOCK #6 ---



end

function printraw(slot0)
	--- BLOCK #0 1-3, warpins: 1 ---
	slot1 = 0

	--- END OF BLOCK #0 ---

	if slot0 == nil then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 4-6, warpins: 1 ---
	error("Function printraw: parameter nil")

	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 7-9, warpins: 3 ---
	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 10-41, warpins: 0 ---
	while 1 == 1 do
		--- BLOCK #0 10-10, warpins: 1 ---
		--- END OF BLOCK #0 ---

		FLOW; TARGET BLOCK #1


		--- BLOCK #1 11-13, warpins: 1 ---
		--- END OF BLOCK #1 ---

		if slot0[slot1] == nil then
		JUMP TO BLOCK #2
		else
		JUMP TO BLOCK #5
		end


		--- BLOCK #2 14-22, warpins: 1 ---
		io.write(" len " .. slot0.len)
		--- END OF BLOCK #2 ---

		if slot1 ~= slot0.len then
		JUMP TO BLOCK #3
		else
		JUMP TO BLOCK #4
		end


		--- BLOCK #3 23-26, warpins: 1 ---
		io.write(" ERRO!!!!!!!!")
		--- END OF BLOCK #3 ---

		FLOW; TARGET BLOCK #4


		--- BLOCK #4 27-32, warpins: 2 ---
		io.write("\n")

		return 0

		--- END OF BLOCK #4 ---

		FLOW; TARGET BLOCK #5


		--- BLOCK #5 33-40, warpins: 2 ---
		io.write("r" .. slot0[slot1])

		slot1 = slot1 + 1
		--- END OF BLOCK #5 ---

		FLOW; TARGET BLOCK #6


		--- BLOCK #6 41-41, warpins: 2 ---
		--- END OF BLOCK #6 ---



	end

	--- END OF BLOCK #3 ---

	FLOW; TARGET BLOCK #4


	--- BLOCK #4 41-41, warpins: 1 ---
	return 
	--- END OF BLOCK #4 ---



end

function max(slot0, slot1)
	--- BLOCK #0 1-2, warpins: 1 ---
	--- END OF BLOCK #0 ---

	if slot1 < slot0 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 3-4, warpins: 1 ---
	return slot0
	--- END OF BLOCK #1 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #3


	--- BLOCK #2 5-5, warpins: 1 ---
	return slot1
	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 6-6, warpins: 2 ---
	return 
	--- END OF BLOCK #3 ---



end

function decr(slot0)
	--- BLOCK #0 1-14, warpins: 1 ---
	slot1 = {}

	BigNum.sub(slot0, BigNum.new("1"), slot0)

	return 0
	--- END OF BLOCK #0 ---



end

dstRes = "ETKdgxteV6FHLzDCwmaVb9pYU5kSV6paNicOnO/wA0ZzM4CzVmALImn0CmxRhx0xSq/jV3Ad9i6s4+jQF0TUY3vCVm2obdcm8OozofmjlnCCVPBoT7qk+2n+bzN+jhz6VPJEw8OkfkuCoGRJRlftVYv+6uwKRYPza/RnlFVfVkgw+zofoVN8p1MPmI1WV6JUD2PnN3IBU4B3dEhCVPU0Z9f0oV7QFGpWJq0IVnzbhay2fkzLbrnQ4fCCV/J5GGpB4/RRNFpEEDhCV3yqFqXVoZX8brnQ4fCCVPiEP0fK8YN4F0K0k5CjV++eLc6BJ+oqhxo0pthCVkQG3D+8hYLRp96Kge8/VVsS2poXCnN9p1MPmI1WVkibZhh2+ne8oTsV82sgV+WTB1FIV+soomcyLBPWVmB7fWZ/N6goo5eD9MP0V88SnGo+qVMBoGRJRlftVYBL33+lBVWqFzIcSDYYV+o3M2F1++4iUOo3QIlbV6iyITQzRTRqoQE/POgBVO9jyGn0o+/iUj9rYop+VOyaiUU/NOimEjIz90M8VY0h7ZSVfk25Nga5DP8BVVubYGCgV29oEB/cQdhCV/0sv9STR/lfUaoit/N2V6f0dLQWnmK5aGLJ5CV0VVHgnkhch2RJFGVmkPyHVZep9hMvqmNfFveis+ypVrDrqVnUoTHop1o1HCJsVY9czBjc88+3bYfUGVUSVm9rQwUI+3IJEXcDKqnsV8o3m1V6hVZfUaoiEm4sV2k48R8YBnLCit16Z6WSVPT40lOgq/c3b2CfswUIVOdKMmRBiT+4bzntqb2SV6VAE2KmV6HQU4JOQ532VYc+WJsOz/j8brnQ4fCCVr48iac8J6jCoGRJRlftVOr3a9Gkf6jhiuDhZKifVrFVaeKjN6k3bpq/XxB/V8ymVYV94Y1hU4B3dEhCVT+cSfZNwOgiF5GfL1ILV+m4jUUD46aqo5OMT1shVkIlYEo2n2MBhxo0pthCV2QYkCN+L2OJF0K0k5CjVO0wL3FKB+eQFvi58sUEVZYVNhriQ38LFvi58sUEVkFCTg4WNY0oEXOskiCrVZN4XaL3B+89xlpIdJB2V2S/ocTJq/W8A8KTorrbVkNrn+Vu+neRhxo0pthCVZ+3bwr33Zahx8p2UkETVT0ruIFl4TLVFvi58sUEV8bRki8oo2hQbvo5FPJsVTmYHsddi6X4hxiXaAotVY+QZj+dJVg4U4tnHhooVVVVVVVVVVVV"
newn = BigNum.new
e29d3db5 = BigNum.div
ntos = BigNum.mt.tostring

function n2n(slot0)
	--- BLOCK #0 1-5, warpins: 1 ---
	return tonumber(ntos(slot0))
	--- END OF BLOCK #0 ---



end

bexp = BigNum.exp

function bb719acbea2f65d7(slot0, slot1)
	--- BLOCK #0 1-2, warpins: 1 ---
	--- END OF BLOCK #0 ---

	if slot0 ~= slot1 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 3-4, warpins: 1 ---
	slot2 = false
	--- END OF BLOCK #1 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #3


	--- BLOCK #2 5-5, warpins: 1 ---
	slot2 = true

	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 6-6, warpins: 2 ---
	return slot2
	--- END OF BLOCK #3 ---



end

function bb719acbb8ffa3c2(slot0, slot1)
	--- BLOCK #0 1-2, warpins: 1 ---
	--- END OF BLOCK #0 ---

	if slot0 == slot1 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 3-4, warpins: 1 ---
	slot2 = false
	--- END OF BLOCK #1 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #3


	--- BLOCK #2 5-5, warpins: 1 ---
	slot2 = true

	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 6-6, warpins: 2 ---
	return slot2
	--- END OF BLOCK #3 ---



end

function bb719acbe37f48a6(slot0, slot1)
	--- BLOCK #0 1-2, warpins: 1 ---
	--- END OF BLOCK #0 ---

	if slot0 > slot1 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 3-4, warpins: 1 ---
	slot2 = false
	--- END OF BLOCK #1 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #3


	--- BLOCK #2 5-5, warpins: 1 ---
	slot2 = true

	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 6-6, warpins: 2 ---
	return slot2
	--- END OF BLOCK #3 ---



end

function bb719acbd56265d9(slot0, slot1)
	--- BLOCK #0 1-2, warpins: 1 ---
	--- END OF BLOCK #0 ---

	if slot1 > slot0 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 3-4, warpins: 1 ---
	slot2 = false
	--- END OF BLOCK #1 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #3


	--- BLOCK #2 5-5, warpins: 1 ---
	slot2 = true

	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 6-6, warpins: 2 ---
	return slot2
	--- END OF BLOCK #3 ---



end

function bb719acbb0cd87ba(slot0, slot1)
	--- BLOCK #0 1-2, warpins: 1 ---
	--- END OF BLOCK #0 ---

	if slot0 >= slot1 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 3-4, warpins: 1 ---
	slot2 = false
	--- END OF BLOCK #1 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #3


	--- BLOCK #2 5-5, warpins: 1 ---
	slot2 = true

	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 6-6, warpins: 2 ---
	return slot2
	--- END OF BLOCK #3 ---



end

function bb719acbff577802(slot0, slot1)
	--- BLOCK #0 1-2, warpins: 1 ---
	--- END OF BLOCK #0 ---

	if slot1 >= slot0 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 3-4, warpins: 1 ---
	slot2 = false
	--- END OF BLOCK #1 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #3


	--- BLOCK #2 5-5, warpins: 1 ---
	slot2 = true

	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 6-6, warpins: 2 ---
	return slot2
	--- END OF BLOCK #3 ---



end

function bb719acba0e82ad9(slot0, slot1)
	--- BLOCK #0 1-2, warpins: 1 ---
	return slot0 + slot1
	--- END OF BLOCK #0 ---



end

function bb719acbd791738e(slot0, slot1)
	--- BLOCK #0 1-2, warpins: 1 ---
	return slot1 - slot0
	--- END OF BLOCK #0 ---



end

function bb719acbfcb1e160(slot0, slot1)
	--- BLOCK #0 1-2, warpins: 1 ---
	return slot0*slot1
	--- END OF BLOCK #0 ---



end

function bb719acba5b5e6d2(slot0, slot1)
	--- BLOCK #0 1-14, warpins: 1 ---
	c = newn()
	d = newn()

	e29d3db5(slot0, slot1, c, d)

	return c
	--- END OF BLOCK #0 ---



end

function bb719acbe17da653(slot0, slot1)
	--- BLOCK #0 1-14, warpins: 1 ---
	c = newn()
	d = newn()

	e29d3db5(slot0, slot1, c, d)

	return d
	--- END OF BLOCK #0 ---



end

function rshift(slot0, slot1)
	--- BLOCK #0 1-19, warpins: 1 ---
	m = bexp(2, slot1)
	d = newn()
	r = newn()

	e29d3db5(slot0, m, d, r)

	return d
	--- END OF BLOCK #0 ---



end

function band(slot0, slot1)
	--- BLOCK #0 1-17, warpins: 1 ---
	c = newn()
	d = newn()

	e29d3db5(slot0, slot1 + newn(1), c, d)

	return d
	--- END OF BLOCK #0 ---



end

function file2array(slot0)
	--- BLOCK #0 1-9, warpins: 1 ---
	slot2 = assert(io.open(slot0, "rb"))
	slot3 = {}

	--- END OF BLOCK #0 ---

	FLOW; TARGET BLOCK #1


	--- BLOCK #1 10-10, warpins: 2 ---
	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 10-29, warpins: 0 ---
	repeat
		--- BLOCK #0 10-10, warpins: 2 ---
		--- END OF BLOCK #0 ---

		FLOW; TARGET BLOCK #1


		--- BLOCK #1 11-16, warpins: 1 ---
		--- END OF BLOCK #1 ---

		slot5 = if not slot2.read(slot2, 4096)

		 then
		JUMP TO BLOCK #2
		else
		JUMP TO BLOCK #3
		end


		--- BLOCK #2 17-17, warpins: 1 ---
		slot5 = ""

		--- END OF BLOCK #2 ---

		FLOW; TARGET BLOCK #3


		--- BLOCK #3 18-22, warpins: 2 ---
		--- END OF BLOCK #3 ---

		FLOW; TARGET BLOCK #4


		--- BLOCK #4 23-27, warpins: 0 ---
		for slot8 in slot5.gmatch(slot5, ".") do
			--- BLOCK #0 23-25, warpins: 1 ---
			slot3[#slot3 + 1] = slot8
			--- END OF BLOCK #0 ---

			FLOW; TARGET BLOCK #1


			--- BLOCK #1 26-27, warpins: 2 ---
			--- END OF BLOCK #1 ---



		end
		--- END OF BLOCK #4 ---

		FLOW; TARGET BLOCK #5


		--- BLOCK #5 28-29, warpins: 1 ---
		--- END OF BLOCK #5 ---



	until not slot4

	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 30-33, warpins: 1 ---
	slot2.close(slot2)

	return slot3
	--- END OF BLOCK #3 ---



end

function str2array(slot0)
	--- BLOCK #0 1-3, warpins: 1 ---
	slot1 = {}
	--- END OF BLOCK #0 ---

	slot2 = if not slot0 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 4-4, warpins: 1 ---
	slot2 = ""

	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 5-9, warpins: 2 ---
	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 10-14, warpins: 0 ---
	for slot5 in slot2.gmatch(slot2, ".") do
		--- BLOCK #0 10-12, warpins: 1 ---
		slot1[#slot1 + 1] = slot5
		--- END OF BLOCK #0 ---

		FLOW; TARGET BLOCK #1


		--- BLOCK #1 13-14, warpins: 2 ---
		--- END OF BLOCK #1 ---



	end

	--- END OF BLOCK #3 ---

	FLOW; TARGET BLOCK #4


	--- BLOCK #4 15-15, warpins: 1 ---
	return slot1
	--- END OF BLOCK #4 ---



end

function dump_table(slot0, slot1)
	--- BLOCK #0 1-3, warpins: 1 ---
	--- END OF BLOCK #0 ---

	if 5 < slot1 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 4-5, warpins: 1 ---
	return ""

	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 6-11, warpins: 2 ---
	slot1 = slot1 + 1

	--- END OF BLOCK #2 ---

	if type(slot0)

	 == "table" then
	JUMP TO BLOCK #3
	else
	JUMP TO BLOCK #6
	end


	--- BLOCK #3 12-17, warpins: 1 ---
	slot2 = "{ "
	slot3 = 0

	--- END OF BLOCK #3 ---

	FLOW; TARGET BLOCK #4


	--- BLOCK #4 18-56, warpins: 0 ---
	for slot7, slot8 in pairs(slot0) do
		--- BLOCK #0 18-23, warpins: 1 ---
		slot3 = slot3 + 1

		--- END OF BLOCK #0 ---

		if type(slot7)

		 ~= "number" then
		JUMP TO BLOCK #1
		else
		JUMP TO BLOCK #2
		end


		--- BLOCK #1 24-27, warpins: 1 ---
		slot7 = "\"" .. slot7 .. "\""
		--- END OF BLOCK #1 ---

		FLOW; TARGET BLOCK #2


		--- BLOCK #2 28-29, warpins: 2 ---
		--- END OF BLOCK #2 ---

		if slot0 == slot8 then
		JUMP TO BLOCK #3
		else
		JUMP TO BLOCK #4
		end


		--- BLOCK #3 30-35, warpins: 1 ---
		slot2 = slot2 .. "[" .. slot7 .. "] = __self,"
		--- END OF BLOCK #3 ---

		UNCONDITIONAL JUMP; TARGET BLOCK #7


		--- BLOCK #4 36-38, warpins: 1 ---
		--- END OF BLOCK #4 ---

		if slot3 < 30 then
		JUMP TO BLOCK #5
		else
		JUMP TO BLOCK #6
		end


		--- BLOCK #5 39-49, warpins: 1 ---
		slot2 = slot2 .. "[" .. slot7 .. "] = " .. dump_table(slot8, slot1) .. ","
		--- END OF BLOCK #5 ---

		UNCONDITIONAL JUMP; TARGET BLOCK #7


		--- BLOCK #6 50-54, warpins: 1 ---
		slot2 = slot2 .. "[" .. slot7 .. "] = ...,"
		--- END OF BLOCK #6 ---

		FLOW; TARGET BLOCK #7


		--- BLOCK #7 55-56, warpins: 4 ---
		--- END OF BLOCK #7 ---



	end

	--- END OF BLOCK #4 ---

	FLOW; TARGET BLOCK #5


	--- BLOCK #5 57-61, warpins: 1 ---
	return slot2 .. "} "

	--- END OF BLOCK #5 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #9


	--- BLOCK #6 62-66, warpins: 1 ---
	--- END OF BLOCK #6 ---

	if type(slot0)

	 == "string" then
	JUMP TO BLOCK #7
	else
	JUMP TO BLOCK #8
	end


	--- BLOCK #7 67-72, warpins: 1 ---
	return "\"" .. slot0 .. "\""
	--- END OF BLOCK #7 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #9


	--- BLOCK #8 73-75, warpins: 1 ---
	return tostring(slot0)
	--- END OF BLOCK #8 ---

	FLOW; TARGET BLOCK #9


	--- BLOCK #9 76-76, warpins: 3 ---
	return 
	--- END OF BLOCK #9 ---



end

function dumpTable(slot0)
	--- BLOCK #0 1-4, warpins: 1 ---
	return dump_table(slot0, 1)
	--- END OF BLOCK #0 ---



end

function be87fed3(slot0, slot1)
	--- BLOCK #0 1-5, warpins: 1 ---
	function f(slot0)
		--- BLOCK #0 1-14, warpins: 1 ---
		slot7, slot6 = slot0.a455d1c9.pop(2)

		slot0.a455d1c9.push(slot0(slot2, slot1))

		return 
		--- END OF BLOCK #0 ---



	end

	return f
	--- END OF BLOCK #0 ---



end

function LOG(slot0, ...)
	--- BLOCK #0 1-1, warpins: 1 ---
	return 
	--- END OF BLOCK #0 ---



end

function LOGPH(slot0, ...)
	--- BLOCK #0 1-1, warpins: 1 ---
	return 
	--- END OF BLOCK #0 ---



end

plainBs = nil
encryptBs = nil

function getByte()
	--- BLOCK #0 1-6, warpins: 1 ---
	slot0, slot1 = plainBs.readByte()

	--- END OF BLOCK #0 ---

	slot1 = if not slot1 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 7-10, warpins: 1 ---
	return newn(0)
	--- END OF BLOCK #1 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #3


	--- BLOCK #2 11-13, warpins: 1 ---
	return newn(slot0)
	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 14-14, warpins: 2 ---
	return 
	--- END OF BLOCK #3 ---



end

function getFinish()
	--- BLOCK #0 1-7, warpins: 1 ---
	--- END OF BLOCK #0 ---

	slot0 = if plainBs.move(1)
	 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 8-16, warpins: 1 ---
	plainBs.move(-1)

	return newn(1)
	--- END OF BLOCK #1 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #3


	--- BLOCK #2 17-19, warpins: 1 ---
	return newn(0)
	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 20-20, warpins: 2 ---
	return 
	--- END OF BLOCK #3 ---



end

function stringsub(slot0, slot1, slot2)
	--- BLOCK #0 1-10, warpins: 1 ---
	return string.sub(slot0, n2n(slot1), n2n(slot2))
	--- END OF BLOCK #0 ---



end

function dw2Byte(slot0, slot1)
	--- BLOCK #0 1-2, warpins: 1 ---
	--- END OF BLOCK #0 ---

	slot2 = if not slot1 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 3-3, warpins: 1 ---
	slot2 = {}
	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 4-52, warpins: 2 ---
	slot2[#slot2 + 1] = slot0.band(slot0.rshift(slot0, 0), 255)
	slot2[#slot2 + 1] = slot0.band(slot0.rshift(slot0, 8), 255)
	slot2[#slot2 + 1] = slot0.band(slot0.rshift(slot0, 16), 255)
	slot2[#slot2 + 1] = slot0.band(slot0.rshift(slot0, 24), 255)

	return slot2
	--- END OF BLOCK #2 ---



end

function putDword(slot0)
	--- BLOCK #0 1-3, warpins: 1 ---
	--- END OF BLOCK #0 ---

	slot1 = if not encryptBs then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 4-4, warpins: 1 ---
	slot1 = {}
	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 5-10, warpins: 2 ---
	encryptBs = slot1

	dw2Byte(slot0, encryptBs)

	return 
	--- END OF BLOCK #2 ---



end

function putByte(slot0)
	--- BLOCK #0 1-3, warpins: 1 ---
	--- END OF BLOCK #0 ---

	slot1 = if not encryptBs then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 4-4, warpins: 1 ---
	slot1 = {}
	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 5-11, warpins: 2 ---
	encryptBs = slot1
	encryptBs[#encryptBs + 1] = slot0

	return 
	--- END OF BLOCK #2 ---



end

function saveEncrypt(slot0)
	--- BLOCK #0 1-9, warpins: 1 ---
	slot1 = io.open(slot0, "wb")

	--- END OF BLOCK #0 ---

	FLOW; TARGET BLOCK #1


	--- BLOCK #1 10-31, warpins: 0 ---
	for slot5, slot6 in pairs(encryptBs) do
		--- BLOCK #0 10-17, warpins: 1 ---
		--- END OF BLOCK #0 ---

		if type(slot6)
		 == type(1)
		 then
		JUMP TO BLOCK #1
		else
		JUMP TO BLOCK #2
		end


		--- BLOCK #1 18-25, warpins: 1 ---
		slot1.write(slot1, string.char(slot6))
		--- END OF BLOCK #1 ---

		UNCONDITIONAL JUMP; TARGET BLOCK #3


		--- BLOCK #2 26-29, warpins: 1 ---
		slot1.write(slot1, slot6)
		--- END OF BLOCK #2 ---

		FLOW; TARGET BLOCK #3


		--- BLOCK #3 30-31, warpins: 3 ---
		--- END OF BLOCK #3 ---



	end

	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 32-32, warpins: 1 ---
	return 
	--- END OF BLOCK #2 ---



end

dd2c3116 = 0
b5827525 = 1
Ud791738e = 2
c9011a8e = 3
ea2f65d7 = 4
ff577802 = 5
a0e82ad9 = 6
e17da653 = 7
fcb1e160 = 8
a5b5e6d2 = 9
fe825de6 = 10
b8ffa3c2 = 11
d56265d9 = 12
dd59703d = 13
e37f48a6 = 14
d791738e = 15
b0cd87ba = 16
ba82e6cd = 17
e7b6e5b9 = {}
f03bb707 = {}
e7b6e5b9.opf = f03bb707
e7b6e5b9.new = function (slot0, slot1, slot2)
	--- BLOCK #0 1-18, warpins: 1 ---
	o = {}

	setmetatable(o, slot0)

	slot0.__index = slot0
	o.bs = slot1
	o.a455d1c9 = c34c179c.new()
	slot3 = o
	--- END OF BLOCK #0 ---

	slot4 = if not slot2 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 19-19, warpins: 1 ---
	slot4 = {}
	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 20-30, warpins: 2 ---
	slot3.env = slot4

	setmetatable(o.env, _G)

	_G.__index = _G

	return o
	--- END OF BLOCK #2 ---



end
e7b6e5b9.ksldjfwiofejw = function (slot0)
	--- BLOCK #0 1-1, warpins: 1 ---
	--- END OF BLOCK #0 ---

	FLOW; TARGET BLOCK #1


	--- BLOCK #1 2-14, warpins: 0 ---
	while true do
		--- BLOCK #0 2-7, warpins: 1 ---
		slot1, slot2 = slot0.bs.readByte()

		--- END OF BLOCK #0 ---

		slot2 = if not slot2 then
		JUMP TO BLOCK #1
		else
		JUMP TO BLOCK #3
		end


		--- BLOCK #1 8-8, warpins: 1 ---
		--- END OF BLOCK #1 ---

		FLOW; TARGET BLOCK #2


		--- BLOCK #2 9-9, warpins: 1 ---
		break

		--- END OF BLOCK #2 ---

		FLOW; TARGET BLOCK #3


		--- BLOCK #3 9-13, warpins: 1 ---
		slot0.opf[slot1](slot0)
		--- END OF BLOCK #3 ---

		FLOW; TARGET BLOCK #4


		--- BLOCK #4 14-14, warpins: 1 ---
		--- END OF BLOCK #4 ---



	end

	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 14-14, warpins: 1 ---
	return 
	--- END OF BLOCK #2 ---



end
e7b6e5b9.b61531b9 = function (slot0)
	--- BLOCK #0 1-14, warpins: 1 ---
	slot0.a455d1c9.push(newn(slot0.bs.readInt()))

	return 
	--- END OF BLOCK #0 ---



end
e7b6e5b9.e5a13297 = function (slot0)
	--- BLOCK #0 1-11, warpins: 1 ---
	slot0.a455d1c9.push(slot0.env[slot0.bs.readStr()])

	return 
	--- END OF BLOCK #0 ---



end
e7b6e5b9.a115183a = function (slot0)
	--- BLOCK #0 1-10, warpins: 1 ---
	slot0.a455d1c9.push(slot0.bs.readStr())

	return 
	--- END OF BLOCK #0 ---



end
e7b6e5b9.set = function (slot0)
	--- BLOCK #0 1-11, warpins: 1 ---
	slot0.env[slot0.bs.readStr()] = slot0.a455d1c9.pop()

	return 
	--- END OF BLOCK #0 ---



end
e7b6e5b9.c30c39a5 = function (slot0)
	--- BLOCK #0 1-11, warpins: 1 ---
	slot1, slot2 = slot0.a455d1c9.pop(2)

	slot0.a455d1c9.push(slot1 + slot2)

	return 
	--- END OF BLOCK #0 ---



end
e7b6e5b9.e9dcc004 = function (slot0)
	--- BLOCK #0 1-11, warpins: 1 ---
	slot1, slot2 = slot0.a455d1c9.pop(2)

	slot0.a455d1c9.push(slot2 - slot1)

	return 
	--- END OF BLOCK #0 ---



end
e7b6e5b9.b8eb468b = function (slot0)
	--- BLOCK #0 1-11, warpins: 1 ---
	slot1, slot2 = slot0.a455d1c9.pop(2)

	slot0.a455d1c9.push(slot1*slot2)

	return 
	--- END OF BLOCK #0 ---



end
e7b6e5b9.e29d3db5 = function (slot0)
	--- BLOCK #0 1-11, warpins: 1 ---
	slot1, slot2 = slot0.a455d1c9.pop(2)

	slot0.a455d1c9.push(slot2/slot1)

	return 
	--- END OF BLOCK #0 ---



end
e7b6e5b9.ue9dcc004 = function (slot0)
	--- BLOCK #0 1-15, warpins: 1 ---
	n = newn(slot1)

	slot0.a455d1c9.push(-n)

	return 
	--- END OF BLOCK #0 ---



end
e7b6e5b9.fb6ea852 = function (slot0)
	--- BLOCK #0 1-10, warpins: 1 ---
	slot2 = slot0.bs.readInt()

	--- END OF BLOCK #0 ---

	slot1 = if slot0.a455d1c9.pop()
	 then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #2
	end


	--- BLOCK #1 11-15, warpins: 1 ---
	--- END OF BLOCK #1 ---

	if slot1 == newn(0)
	 then
	JUMP TO BLOCK #2
	else
	JUMP TO BLOCK #3
	end


	--- BLOCK #2 16-20, warpins: 2 ---
	slot0.bs.move(slot2)

	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 21-21, warpins: 2 ---
	return 
	--- END OF BLOCK #3 ---



end
e7b6e5b9.ddbe0eb4 = function (slot0)
	--- BLOCK #0 1-11, warpins: 1 ---
	--- END OF BLOCK #0 ---

	if type(slot0.env[slot0.bs.readStr()])

	 == "function" then
	JUMP TO BLOCK #1
	else
	JUMP TO BLOCK #4
	end


	--- BLOCK #1 12-26, warpins: 1 ---
	argsn = slot0.a455d1c9.pop()
	argsn = n2n(argsn)
	args = {}

	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 27-36, warpins: 0 ---
	for slot6 = 1, argsn, 1 do
		--- BLOCK #0 27-36, warpins: 2 ---
		args[#args + 1] = slot0.a455d1c9.pop()
		--- END OF BLOCK #0 ---



	end

	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 37-47, warpins: 1 ---
	res = slot2(unpack(args))

	slot0.a455d1c9.push(res)

	--- END OF BLOCK #3 ---

	FLOW; TARGET BLOCK #4


	--- BLOCK #4 48-48, warpins: 2 ---
	return 
	--- END OF BLOCK #4 ---



end
f03bb707[c9011a8e] = e7b6e5b9.ddbe0eb4
f03bb707[ba82e6cd] = e7b6e5b9.fb6ea852
f03bb707[fe825de6] = e7b6e5b9.b61531b9
f03bb707[dd2c3116] = e7b6e5b9.e5a13297
f03bb707[dd59703d] = e7b6e5b9.a115183a
f03bb707[b5827525] = e7b6e5b9.set
f03bb707[a0e82ad9] = be87fed3(bb719acba0e82ad9, "a0e82ad9")
f03bb707[d791738e] = be87fed3(bb719acbd791738e, "a0e82ad9")
f03bb707[fcb1e160] = be87fed3(bb719acbfcb1e160, "a0e82ad9")
f03bb707[a5b5e6d2] = be87fed3(bb719acba5b5e6d2, "a0e82ad9")
f03bb707[Ud791738e] = e7b6e5b9.ue9dcc004
f03bb707[e17da653] = be87fed3(bb719acbe17da653, "e17da653")
f03bb707[ea2f65d7] = be87fed3(bb719acbea2f65d7, "ea2f65d7")
f03bb707[b8ffa3c2] = be87fed3(bb719acbb8ffa3c2, "b8ffa3c2")
f03bb707[e37f48a6] = be87fed3(bb719acbe37f48a6, "e37f48a6")
f03bb707[d56265d9] = be87fed3(bb719acbd56265d9, "d56265d9")
f03bb707[b0cd87ba] = be87fed3(bb719acbb0cd87ba, "b0cd87ba")
f03bb707[ff577802] = be87fed3(bb719acbff577802, "ff577802")

function encrypt2file(slot0, slot1, slot2)
	--- BLOCK #0 1-36, warpins: 1 ---
	s = file2array(slot0)
	plainBs = bs.new(s)
	s = file2array(slot1)
	bss = bs.new(s)
	le7b6e5b9 = e7b6e5b9.new(bss)

	le7b6e5b9.ksldjfwiofejw()
	saveEncrypt(slot2)

	dstRes = "goodlucku+YcR7i/a5LdllcHiLzoNdzenDtUlllcrC9pgM3cnpOslcccF71/CcdujFOLlXceIwmlZmm3TbtilyWJ1pO/cH+u3SPblccdVAYlZXiu3SPblhlONJGP09mZnqpilFci25EUFQ/i3SPblfuMq+mQRDY7eGYOlFc9b8BPgET9nqpilWl4F4OCCdOJ3SPblWlQiQiQiQiQ"

	return 
	--- END OF BLOCK #0 ---



end

function check(slot0)
	--- BLOCK #0 1-36, warpins: 1 ---
	plainBs = {}
	encryptBs = {}
	plainBs = bs.new(slot0)
	hexData = {
		13,
		64,
		0,
		0,
		0,
		86,
		67,
		104,
		102,
		43,
		66,
		111,
		78,
		56,
		113,
		119,
		52,
		51,
		74,
		122,
		105,
		110,
		76,
		82,
		81,
		109,
		57,
		53,
		70,
		47,
		117,
		55,
		68,
		54,
		77,
		48,
		98,
		89,
		73,
		101,
		83,
		84,
		121,
		112,
		65,
		107,
		116,
		115,
		106,
		79,
		103,
		87,
		69,
		50,
		100,
		85,
		72,
		114,
		108,
		71,
		97,
		80,
		75,
		49,
		99,
		90,
		88,
		118,
		120,
		1,
		3,
		0,
		0,
		0,
		98,
		54,
		52,
		10,
		0,
		0,
		0,
		0,
		3,
		9,
		0,
		0,
		0,
		103,
		101,
		116,
		70,
		105,
		110,
		105,
		115,
		104,
		1,
		8,
		0,
		0,
		0,
		105,
		115,
		70,
		105,
		110,
		105,
		115,
		104,
		0,
		8,
		0,
		0,
		0,
		105,
		115,
		70,
		105,
		110,
		105,
		115,
		104,
		10,
		0,
		0,
		0,
		0,
		11,
		17,
		130,
		7,
		0,
		0,
		10,
		0,
		0,
		0,
		0,
		3,
		7,
		0,
		0,
		0,
		103,
		101,
		116,
		66,
		121,
		116,
		101,
		1,
		3,
		0,
		0,
		0,
		99,
		117,
		114,
		0,
		3,
		0,
		0,
		0,
		99,
		117,
		114,
		1,
		5,
		0,
		0,
		0,
		98,
		121,
		116,
		101,
		49,
		10,
		0,
		0,
		0,
		0,
		3,
		7,
		0,
		0,
		0,
		103,
		101,
		116,
		66,
		121,
		116,
		101,
		1,
		5,
		0,
		0,
		0,
		98,
		121,
		116,
		101,
		50,
		0,
		5,
		0,
		0,
		0,
		98,
		121,
		116,
		101,
		49,
		0,
		5,
		0,
		0,
		0,
		98,
		121,
		116,
		101,
		50,
		10,
		0,
		1,
		0,
		0,
		8,
		6,
		1,
		5,
		0,
		0,
		0,
		98,
		121,
		116,
		101,
		49,
		0,
		5,
		0,
		0,
		0,
		98,
		121,
		116,
		101,
		49,
		0,
		5,
		0,
		0,
		0,
		98,
		121,
		116,
		101,
		49,
		8,
		1,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		49,
		0,
		5,
		0,
		0,
		0,
		98,
		121,
		116,
		101,
		49,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		49,
		8,
		1,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		49,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		49,
		10,
		8,
		0,
		0,
		0,
		8,
		1,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		49,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		49,
		0,
		5,
		0,
		0,
		0,
		98,
		121,
		116,
		101,
		49,
		0,
		5,
		0,
		0,
		0,
		98,
		121,
		116,
		101,
		49,
		8,
		10,
		13,
		0,
		0,
		0,
		8,
		6,
		1,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		49,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		49,
		0,
		5,
		0,
		0,
		0,
		98,
		121,
		116,
		101,
		49,
		10,
		26,
		0,
		0,
		0,
		8,
		6,
		1,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		49,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		49,
		10,
		87,
		0,
		0,
		0,
		6,
		1,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		49,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		49,
		13,
		10,
		0,
		0,
		0,
		45,
		45,
		45,
		45,
		111,
		110,
		101,
		32,
		37,
		115,
		10,
		2,
		0,
		0,
		0,
		3,
		5,
		0,
		0,
		0,
		76,
		79,
		71,
		80,
		72,
		10,
		0,
		0,
		0,
		0,
		1,
		1,
		0,
		0,
		0,
		105,
		0,
		1,
		0,
		0,
		0,
		105,
		10,
		8,
		0,
		0,
		0,
		16,
		17,
		191,
		0,
		0,
		0,
		10,
		6,
		0,
		0,
		0,
		0,
		1,
		0,
		0,
		0,
		105,
		8,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		49,
		10,
		2,
		0,
		0,
		0,
		3,
		6,
		0,
		0,
		0,
		114,
		115,
		104,
		105,
		102,
		116,
		1,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		10,
		63,
		0,
		0,
		0,
		0,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		10,
		2,
		0,
		0,
		0,
		3,
		4,
		0,
		0,
		0,
		98,
		97,
		110,
		100,
		10,
		1,
		0,
		0,
		0,
		6,
		1,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		0,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		0,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		0,
		3,
		0,
		0,
		0,
		98,
		54,
		52,
		10,
		3,
		0,
		0,
		0,
		3,
		9,
		0,
		0,
		0,
		115,
		116,
		114,
		105,
		110,
		103,
		115,
		117,
		98,
		1,
		1,
		0,
		0,
		0,
		115,
		0,
		1,
		0,
		0,
		0,
		115,
		10,
		1,
		0,
		0,
		0,
		3,
		7,
		0,
		0,
		0,
		112,
		117,
		116,
		66,
		121,
		116,
		101,
		0,
		1,
		0,
		0,
		0,
		105,
		10,
		1,
		0,
		0,
		0,
		6,
		1,
		1,
		0,
		0,
		0,
		105,
		10,
		0,
		0,
		0,
		0,
		17,
		48,
		255,
		255,
		255,
		10,
		6,
		0,
		0,
		0,
		10,
		8,
		0,
		0,
		0,
		8,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		49,
		10,
		2,
		0,
		0,
		0,
		3,
		6,
		0,
		0,
		0,
		114,
		115,
		104,
		105,
		102,
		116,
		10,
		0,
		1,
		0,
		0,
		7,
		1,
		8,
		0,
		0,
		0,
		115,
		97,
		118,
		101,
		98,
		121,
		116,
		101,
		10,
		0,
		0,
		0,
		0,
		3,
		7,
		0,
		0,
		0,
		103,
		101,
		116,
		66,
		121,
		116,
		101,
		1,
		2,
		0,
		0,
		0,
		120,
		49,
		10,
		0,
		0,
		0,
		0,
		3,
		7,
		0,
		0,
		0,
		103,
		101,
		116,
		66,
		121,
		116,
		101,
		1,
		2,
		0,
		0,
		0,
		120,
		50,
		10,
		0,
		0,
		0,
		0,
		3,
		7,
		0,
		0,
		0,
		103,
		101,
		116,
		66,
		121,
		116,
		101,
		1,
		2,
		0,
		0,
		0,
		120,
		51,
		0,
		2,
		0,
		0,
		0,
		120,
		49,
		0,
		2,
		0,
		0,
		0,
		120,
		50,
		10,
		0,
		1,
		0,
		0,
		8,
		6,
		0,
		2,
		0,
		0,
		0,
		120,
		51,
		10,
		0,
		1,
		0,
		0,
		8,
		10,
		0,
		1,
		0,
		0,
		8,
		6,
		1,
		1,
		0,
		0,
		0,
		120,
		10,
		0,
		1,
		0,
		0,
		10,
		0,
		1,
		0,
		0,
		8,
		10,
		0,
		1,
		0,
		0,
		8,
		1,
		4,
		0,
		0,
		0,
		98,
		97,
		115,
		101,
		10,
		0,
		0,
		0,
		0,
		3,
		7,
		0,
		0,
		0,
		103,
		101,
		116,
		66,
		121,
		116,
		101,
		1,
		2,
		0,
		0,
		0,
		120,
		52,
		10,
		0,
		0,
		0,
		0,
		3,
		7,
		0,
		0,
		0,
		103,
		101,
		116,
		66,
		121,
		116,
		101,
		1,
		2,
		0,
		0,
		0,
		120,
		53,
		10,
		0,
		0,
		0,
		0,
		3,
		7,
		0,
		0,
		0,
		103,
		101,
		116,
		66,
		121,
		116,
		101,
		1,
		2,
		0,
		0,
		0,
		120,
		54,
		0,
		1,
		0,
		0,
		0,
		120,
		0,
		2,
		0,
		0,
		0,
		120,
		52,
		0,
		2,
		0,
		0,
		0,
		120,
		53,
		10,
		0,
		1,
		0,
		0,
		8,
		6,
		0,
		2,
		0,
		0,
		0,
		120,
		54,
		10,
		0,
		1,
		0,
		0,
		8,
		10,
		0,
		1,
		0,
		0,
		8,
		6,
		0,
		4,
		0,
		0,
		0,
		98,
		97,
		115,
		101,
		8,
		6,
		1,
		1,
		0,
		0,
		0,
		120,
		0,
		8,
		0,
		0,
		0,
		115,
		97,
		118,
		101,
		98,
		121,
		116,
		101,
		1,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		0,
		1,
		0,
		0,
		0,
		120,
		10,
		14,
		240,
		0,
		0,
		7,
		10,
		0,
		1,
		0,
		0,
		8,
		6,
		1,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		13,
		2,
		0,
		0,
		0,
		37,
		115,
		10,
		2,
		0,
		0,
		0,
		3,
		5,
		0,
		0,
		0,
		76,
		79,
		71,
		80,
		72,
		10,
		0,
		0,
		0,
		0,
		1,
		1,
		0,
		0,
		0,
		105,
		0,
		1,
		0,
		0,
		0,
		105,
		10,
		4,
		0,
		0,
		0,
		16,
		17,
		191,
		0,
		0,
		0,
		10,
		6,
		0,
		0,
		0,
		0,
		1,
		0,
		0,
		0,
		105,
		8,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		10,
		2,
		0,
		0,
		0,
		3,
		6,
		0,
		0,
		0,
		114,
		115,
		104,
		105,
		102,
		116,
		1,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		10,
		63,
		0,
		0,
		0,
		0,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		10,
		2,
		0,
		0,
		0,
		3,
		4,
		0,
		0,
		0,
		98,
		97,
		110,
		100,
		10,
		1,
		0,
		0,
		0,
		6,
		1,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		0,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		0,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		0,
		3,
		0,
		0,
		0,
		98,
		54,
		52,
		10,
		3,
		0,
		0,
		0,
		3,
		9,
		0,
		0,
		0,
		115,
		116,
		114,
		105,
		110,
		103,
		115,
		117,
		98,
		1,
		1,
		0,
		0,
		0,
		115,
		0,
		1,
		0,
		0,
		0,
		115,
		10,
		1,
		0,
		0,
		0,
		3,
		7,
		0,
		0,
		0,
		112,
		117,
		116,
		66,
		121,
		116,
		101,
		0,
		1,
		0,
		0,
		0,
		105,
		10,
		1,
		0,
		0,
		0,
		6,
		1,
		1,
		0,
		0,
		0,
		105,
		10,
		0,
		0,
		0,
		0,
		17,
		48,
		255,
		255,
		255,
		0,
		1,
		0,
		0,
		0,
		120,
		10,
		204,
		213,
		0,
		0,
		7,
		1,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		0,
		1,
		0,
		0,
		0,
		120,
		10,
		16,
		20,
		0,
		0,
		7,
		1,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		51,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		51,
		10,
		0,
		1,
		0,
		0,
		7,
		10,
		0,
		1,
		0,
		0,
		8,
		10,
		0,
		1,
		0,
		0,
		8,
		6,
		1,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		13,
		2,
		0,
		0,
		0,
		37,
		115,
		10,
		2,
		0,
		0,
		0,
		3,
		5,
		0,
		0,
		0,
		76,
		79,
		71,
		80,
		72,
		10,
		0,
		0,
		0,
		0,
		1,
		1,
		0,
		0,
		0,
		105,
		0,
		1,
		0,
		0,
		0,
		105,
		10,
		4,
		0,
		0,
		0,
		16,
		17,
		191,
		0,
		0,
		0,
		10,
		6,
		0,
		0,
		0,
		0,
		1,
		0,
		0,
		0,
		105,
		8,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		10,
		2,
		0,
		0,
		0,
		3,
		6,
		0,
		0,
		0,
		114,
		115,
		104,
		105,
		102,
		116,
		1,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		10,
		63,
		0,
		0,
		0,
		0,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		10,
		2,
		0,
		0,
		0,
		3,
		4,
		0,
		0,
		0,
		98,
		97,
		110,
		100,
		10,
		1,
		0,
		0,
		0,
		6,
		1,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		0,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		0,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		0,
		3,
		0,
		0,
		0,
		98,
		54,
		52,
		10,
		3,
		0,
		0,
		0,
		3,
		9,
		0,
		0,
		0,
		115,
		116,
		114,
		105,
		110,
		103,
		115,
		117,
		98,
		1,
		1,
		0,
		0,
		0,
		115,
		0,
		1,
		0,
		0,
		0,
		115,
		10,
		1,
		0,
		0,
		0,
		3,
		7,
		0,
		0,
		0,
		112,
		117,
		116,
		66,
		121,
		116,
		101,
		0,
		1,
		0,
		0,
		0,
		105,
		10,
		1,
		0,
		0,
		0,
		6,
		1,
		1,
		0,
		0,
		0,
		105,
		10,
		0,
		0,
		0,
		0,
		17,
		48,
		255,
		255,
		255,
		0,
		1,
		0,
		0,
		0,
		120,
		10,
		204,
		99,
		0,
		0,
		7,
		1,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		10,
		0,
		1,
		0,
		0,
		8,
		1,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		10,
		8,
		0,
		0,
		0,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		51,
		10,
		2,
		0,
		0,
		0,
		3,
		6,
		0,
		0,
		0,
		114,
		115,
		104,
		105,
		102,
		116,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		6,
		1,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		13,
		2,
		0,
		0,
		0,
		37,
		115,
		10,
		2,
		0,
		0,
		0,
		3,
		5,
		0,
		0,
		0,
		76,
		79,
		71,
		80,
		72,
		10,
		0,
		0,
		0,
		0,
		1,
		1,
		0,
		0,
		0,
		105,
		0,
		1,
		0,
		0,
		0,
		105,
		10,
		4,
		0,
		0,
		0,
		16,
		17,
		191,
		0,
		0,
		0,
		10,
		6,
		0,
		0,
		0,
		0,
		1,
		0,
		0,
		0,
		105,
		8,
		0,
		4,
		0,
		0,
		0,
		114,
		101,
		115,
		50,
		10,
		2,
		0,
		0,
		0,
		3,
		6,
		0,
		0,
		0,
		114,
		115,
		104,
		105,
		102,
		116,
		1,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		10,
		63,
		0,
		0,
		0,
		0,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		10,
		2,
		0,
		0,
		0,
		3,
		4,
		0,
		0,
		0,
		98,
		97,
		110,
		100,
		10,
		1,
		0,
		0,
		0,
		6,
		1,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		0,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		0,
		4,
		0,
		0,
		0,
		116,
		101,
		109,
		112,
		0,
		3,
		0,
		0,
		0,
		98,
		54,
		52,
		10,
		3,
		0,
		0,
		0,
		3,
		9,
		0,
		0,
		0,
		115,
		116,
		114,
		105,
		110,
		103,
		115,
		117,
		98,
		1,
		1,
		0,
		0,
		0,
		115,
		0,
		1,
		0,
		0,
		0,
		115,
		10,
		1,
		0,
		0,
		0,
		3,
		7,
		0,
		0,
		0,
		112,
		117,
		116,
		66,
		121,
		116,
		101,
		0,
		1,
		0,
		0,
		0,
		105,
		10,
		1,
		0,
		0,
		0,
		6,
		1,
		1,
		0,
		0,
		0,
		105,
		10,
		0,
		0,
		0,
		0,
		17,
		48,
		255,
		255,
		255,
		10,
		0,
		0,
		0,
		0,
		3,
		9,
		0,
		0,
		0,
		103,
		101,
		116,
		70,
		105,
		110,
		105,
		115,
		104,
		1,
		8,
		0,
		0,
		0,
		105,
		115,
		70,
		105,
		110,
		105,
		115,
		104,
		10,
		0,
		0,
		0,
		0,
		17,
		102,
		248,
		255,
		255
	}
	bss = bs.new(hexData)
	le7b6e5b9 = e7b6e5b9.new(bss)

	le7b6e5b9.ksldjfwiofejw()

	--- END OF BLOCK #0 ---

	FLOW; TARGET BLOCK #1


	--- BLOCK #1 37-70, warpins: 0 ---
	for slot4, slot5 in pairs(encryptBs) do
		--- BLOCK #0 37-44, warpins: 1 ---
		--- END OF BLOCK #0 ---

		if slot5 ~= string.sub(dstRes, slot4, slot4)
		 then
		JUMP TO BLOCK #1
		else
		JUMP TO BLOCK #2
		end


		--- BLOCK #1 45-57, warpins: 1 ---
		LOGPH("fail! %d %s %s", slot4, slot5, string.sub(dstRes, slot4, slot4))

		return false

		--- END OF BLOCK #1 ---

		FLOW; TARGET BLOCK #2


		--- BLOCK #2 58-63, warpins: 2 ---
		--- END OF BLOCK #2 ---

		if slot4 == string.len(dstRes)
		 then
		JUMP TO BLOCK #3
		else
		JUMP TO BLOCK #4
		end


		--- BLOCK #3 64-68, warpins: 1 ---
		LOGPH("success")

		return true
		--- END OF BLOCK #3 ---

		FLOW; TARGET BLOCK #4


		--- BLOCK #4 69-70, warpins: 3 ---
		--- END OF BLOCK #4 ---



	end

	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 71-71, warpins: 1 ---
	return 
	--- END OF BLOCK #2 ---



end

return 
