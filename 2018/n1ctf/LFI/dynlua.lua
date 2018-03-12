slot2 = slot1(function (slot0, ...)
	slot1 = math.floor
	slot2, slot3 = nil

	return {
		bnot = bit.bnot,
		band = bit.band,
		bor = bit.bor,
		bxor = bit.bxor,
		rshift = function (slot0, slot1)
			return slot0(slot0%4294967296.0/2^slot1)
		end,
		lshift = function (slot0, slot1)
			return (slot0*2^slot1)%4294967296.0
		end
	}
end)
slot3 = slot1(function (slot0, ...)
	slot1 = slot0.bxor
	slot2 = slot0.lshift
	slot3 = 256
	slot4 = 255
	slot5 = 283
	slot6 = {}
	slot7 = {}

	function slot12(slot0, slot1)
		if slot0 == 0 then
			return 0
		end

		if slot0[slot0] - slot0[slot1] < 0 then
			slot2 = slot2 + slot1
		end

		return slot2[slot2]
	end

	slot15()

	return {
		add = function (slot0, slot1)
			return slot0(slot0, slot1)
		end,
		sub = function (slot0, slot1)
			return slot0(slot0, slot1)
		end,
		invert = function (slot0)
			if slot0 == 1 then
				return 1
			end

			return slot1[slot0][slot0 - slot1[slot0]]
		end,
		mul = function (slot0, slot1)
			if slot0 == 0 or slot1 == 0 then
				return 0
			end

			if slot1 <= slot0[slot0] + slot0[slot1] then
				slot2 = slot2 - slot1
			end

			return slot2[slot2]
		end,
		div = dib,
		printLog = function ()
			for slot3 = 1, , 1 do
				print("log(", slot3 - 1, ")=", slot1[slot3 - 1])
			end

			return 
		end,
		printExp = function ()
			for slot3 = 1, , 1 do
				print("exp(", slot3 - 1, ")=", slot1[slot3 - 1])
			end

			return 
		end
	}
end)
util = slot1(function (slot0, ...)
	slot1 = slot0.bxor
	slot2 = slot0.rshift
	slot3 = slot0.band
	slot4 = slot0.lshift
	slot5 = nil
	slot19 = os.queueEvent
	slot20 = coroutine.yield
	slot22 = slot21()

	return {
		byteParity = function (slot0)
			return slot0(slot0(slot0, slot0(slot0, 4)), slot0(slot0(slot0, slot0(slot0, 4)), 2))(slot0(slot0(slot0(slot0, slot0(slot0, 4)), slot0(slot0(slot0, slot0(slot0, 4)), 2)), slot0(slot0(slot0(slot0, slot0(slot0, 4)), slot0(slot0(slot0, slot0(slot0, 4)), 2)), 1)), 1)
		end,
		getByte = function (slot0, slot1)
			if slot1 == 0 then
				return slot0(slot0, 255)
			else
				return slot0(slot1(slot0, slot1*8), 255)
			end

			return 
		end,
		putByte = function (slot0, slot1)
			if slot1 == 0 then
				return slot0(slot0, 255)
			else
				return slot1(slot0(slot0, 255), slot1*8)
			end

			return 
		end,
		bytesToInts = function (slot0, slot1, slot2)
			slot3 = {}

			for slot7 = 0, slot2 - 1, 1 do
				slot3[slot7 + 1] = slot0(slot0[slot1 + slot7*4], 3) + slot0(slot0[slot1 + slot7*4 + 1], 2) + slot0(slot0[slot1 + slot7*4 + 2], 1) + slot0(slot0[slot1 + slot7*4 + 3], 0)

				if slot2%10000 == 0 then
					slot1()
				end
			end

			return slot3
		end,
		intsToBytes = function (slot0, slot1, slot2, slot3)
			slot3 = slot3 or #slot0

			for slot7 = 0, slot3 - 1, 1 do
				for slot11 = 0, 3, 1 do
					slot1[slot2 + slot7*4 + slot11 - 3] = slot0(slot0[slot7 + 1], slot11)
				end

				if slot3%10000 == 0 then
					slot1()
				end
			end

			return slot1
		end,
		bytesToHex = function (slot0)
			slot1 = ""

			for slot5, slot6 in ipairs(slot0) do
				slot1 = slot1 .. string.format("%02x ", slot6)
			end

			return slot1
		end,
		hexToBytes = function (slot0)
			slot1 = {}

			for slot5 = 1, #slot0, 2 do
				slot1[#slot1 + 1] = tonumber(slot0.sub(slot0, slot5, slot5 + 1), 16)
			end

			return slot1
		end,
		toHexString = function (slot0)
			if type(slot0) == "number" then
				return string.format("%08x", slot0)
			elseif slot1 == "table" then
				return slot0(slot0)
			elseif slot1 == "string" then
				return slot0({
					string.byte(slot0, 1, #slot0)
				})
			else
				return slot0
			end

			return 
		end,
		padByteString = function (slot0)
			slot6 = ""

			for slot10 = 1, math.ceil(#(slot4 .. slot0)/16)*16 - #(slot4 .. slot0), 1 do
				slot6 = slot6 .. string.char(math.random(0, 255))
			end

			return slot0 .. slot6
		end,
		properlyDecrypted = function (slot0)
			if ({
				string.byte(slot0, 1, 4)
			})[1] == ()[3] and slot1[2] == slot1[4] then
				return true
			end

			return false
		end,
		unpadByteString = function (slot0)
			if not slot0(slot0) then
				return nil
			end

			return string.sub(slot0, 9, slot1(string.byte(slot0, 5), 3) + slot1(string.byte(slot0, 6), 2) + slot1(string.byte(slot0, 7), 1) + slot1(string.byte(slot0, 8), 0) + 8)
		end,
		xorIV = function (slot0, slot1)
			for slot5 = 1, 16, 1 do
				slot0[slot5] = slot0(slot0[slot5], slot1[slot5])
			end

			return 
		end,
		increment = function (slot0)
			slot1 = 16

			while true do
				if 256 <= slot0[slot1] + 1 then
					slot0[slot1] = slot2 - 256
					slot1 = (slot1 - 2)%16 + 1
				else
					slot0[slot1] = slot2

					break
				end
			end

			return 
		end,
		sleepCheckIn = function ()
			if 0.03 <= slot0() - slot1 then
				slot1 = slot0

				slot2("sleep")
				slot3("sleep")
			end

			return 
		end,
		getRandomData = function (slot0)
			slot1 = string.char
			slot2 = math.random
			slot3 = slot0
			slot4 = table.insert
			slot5 = {}

			for slot9 = 1, slot0, 1 do
				slot4(slot5, slot2(0, 255))

				if slot9%10240 == 0 then
					slot3()
				end
			end

			return slot5
		end,
		getRandomString = function (slot0)
			slot1 = string.char
			slot2 = math.random
			slot3 = slot0
			slot4 = table.insert
			slot5 = {}

			for slot9 = 1, slot0, 1 do
				slot4(slot5, slot1(slot2(0, 255)))

				if slot9%10240 == 0 then
					slot3()
				end
			end

			return table.concat(slot5)
		end
	}
end)
aes = slot1(function (slot0, ...)
	slot1 = util.putByte
	slot2 = util.getByte
	slot7 = {}
	slot8 = {}
	slot9 = {}
	slot10 = {}
	slot11 = {}
	slot12 = {}
	slot13 = {}
	slot14 = {}
	slot15 = {}
	slot16 = {}
	slot17 = {
		16777216,
		33554432,
		67108864,
		134217728,
		268435456,
		536870912,
		1073741824,
		2147483648.0,
		452984832,
		905969664,
		1811939328,
		3623878656.0,
		2868903936.0,
		1291845632,
		2583691264.0,
		788529152
	}

	function slot18(slot0)
		mask = 248
		result = 0

		for slot4 = 1, 8, 1 do
			result = slot0.lshift(result, 1)
			parity = util.byteParity(slot0.band(slot0, mask))
			result = result + parity
			lastbit = slot0.band(mask, 1)
			mask = slot0.band(slot0.rshift(mask, 1), 255)

			if lastbit ~= 0 then
				mask = slot0.bor(mask, 128)
			else
				mask = slot0.band(mask, 127)
			end
		end

		return slot0.bxor(result, 99)
	end

	function slot22(slot0)
		return slot0.lshift(slot0, 8) + slot0.rshift(slot0.band(slot0, 4278190080.0), 24)
	end

	function slot23(slot0)
		return slot0(slot1[slot2(slot0, 0)], 0) + slot0(slot1[slot2(slot0, 1)], 1) + slot0(slot1[slot2(slot0, 2)], 2) + slot0(slot1[slot2(slot0, 3)], 3)
	end

	function slot25(slot0)
		slot1 = slot0(slot0, 3)
		slot2 = slot0(slot0, 2)
		slot3 = slot0(slot0, 1)
		slot4 = slot0(slot0, 0)

		return slot1(slot2.add(slot2.add(slot2.add(slot2.mul(11, slot2), slot2.mul(13, slot3)), slot2.mul(9, slot4)), slot2.mul(14, slot1)), 3) + slot1(slot2.add(slot2.add(slot2.add(slot2.mul(11, slot3), slot2.mul(13, slot4)), slot2.mul(9, slot1)), slot2.mul(14, slot2)), 2) + slot1(slot2.add(slot2.add(slot2.add(slot2.mul(11, slot4), slot2.mul(13, slot1)), slot2.mul(9, slot2)), slot2.mul(14, slot3)), 1) + slot1(slot2.add(slot2.add(slot2.add(slot2.mul(11, slot1), slot2.mul(13, slot2)), slot2.mul(9, slot3)), slot2.mul(14, slot4)), 0)
	end

	function slot26(slot0)
		slot1 = slot0(slot0, 3)
		slot2 = slot0(slot0, 2)
		slot3 = slot0(slot0, 1)
		slot4 = slot0(slot0, 0)
		w = slot1.bxor(slot7, slot2.mul(4, slot1.bxor(slot3, slot1)))

		return slot3(slot1.bxor(slot1.bxor(slot4, slot7), slot2.mul(2, slot1.bxor(slot1, slot4))), 0) + slot3(slot1.bxor(slot1.bxor(slot3, w), slot2.mul(2, slot5)), 1) + slot3(slot1.bxor(slot1.bxor(slot2, slot7), slot2.mul(2, slot1.bxor(slot1, slot4))), 2) + slot3(slot1.bxor(slot1.bxor(slot1, w), slot2.mul(2, slot1.bxor(slot2, slot1))), 3)
	end

	function slot28(slot0, slot1, slot2)
		for slot6 = 0, 3, 1 do
			slot0[slot6 + 1] = slot0.bxor(slot0[slot6 + 1], slot1[slot2*4 + slot6])
		end

		return 
	end

	function slot29(slot0, slot1)
		slot1[1] = slot0.bxor(slot0.bxor(slot0.bxor(slot1[slot2(slot0[1], 3)], slot3[slot2(slot0[2], 2)]), slot4[slot2(slot0[3], 1)]), slot4[slot2(slot0[3], 1)][slot2(slot0[4], 0)])
		slot1[2] = slot0.bxor(slot0.bxor(slot0.bxor(slot1[slot2(slot0[2], 3)], slot3[slot2(slot0[3], 2)]), slot4[slot2(slot0[4], 1)]), slot4[slot2(slot0[4], 1)][slot2(slot0[1], 0)])
		slot1[3] = slot0.bxor(slot0.bxor(slot0.bxor(slot1[slot2(slot0[3], 3)], slot3[slot2(slot0[4], 2)]), slot4[slot2(slot0[1], 1)]), slot4[slot2(slot0[1], 1)][slot2(slot0[2], 0)])
		slot1[4] = slot0.bxor(slot0.bxor(slot0.bxor(slot1[slot2(slot0[4], 3)], slot3[slot2(slot0[1], 2)]), slot4[slot2(slot0[2], 1)]), slot4[slot2(slot0[2], 1)][slot2(slot0[3], 0)])

		return 
	end

	function slot30(slot0, slot1)
		slot1[1] = slot0(slot1[slot2(slot0[1], 3)], 3) + slot0(slot1[slot2(slot0[2], 2)], 2) + slot0(slot1[slot2(slot0[3], 1)], 1) + slot0(slot1[slot2(slot0[4], 0)], 0)
		slot1[2] = slot0(slot1[slot2(slot0[2], 3)], 3) + slot0(slot1[slot2(slot0[3], 2)], 2) + slot0(slot1[slot2(slot0[4], 1)], 1) + slot0(slot1[slot2(slot0[1], 0)], 0)
		slot1[3] = slot0(slot1[slot2(slot0[3], 3)], 3) + slot0(slot1[slot2(slot0[4], 2)], 2) + slot0(slot1[slot2(slot0[1], 1)], 1) + slot0(slot1[slot2(slot0[2], 0)], 0)
		slot1[4] = slot0(slot1[slot2(slot0[4], 3)], 3) + slot0(slot1[slot2(slot0[1], 2)], 2) + slot0(slot1[slot2(slot0[2], 1)], 1) + slot0(slot1[slot2(slot0[3], 0)], 0)

		return 
	end

	function slot31(slot0, slot1)
		slot1[1] = slot0.bxor(slot0.bxor(slot0.bxor(slot1[slot2(slot0[1], 3)], slot3[slot2(slot0[4], 2)]), slot4[slot2(slot0[3], 1)]), slot4[slot2(slot0[3], 1)][slot2(slot0[2], 0)])
		slot1[2] = slot0.bxor(slot0.bxor(slot0.bxor(slot1[slot2(slot0[2], 3)], slot3[slot2(slot0[1], 2)]), slot4[slot2(slot0[4], 1)]), slot4[slot2(slot0[4], 1)][slot2(slot0[3], 0)])
		slot1[3] = slot0.bxor(slot0.bxor(slot0.bxor(slot1[slot2(slot0[3], 3)], slot3[slot2(slot0[2], 2)]), slot4[slot2(slot0[1], 1)]), slot4[slot2(slot0[1], 1)][slot2(slot0[4], 0)])
		slot1[4] = slot0.bxor(slot0.bxor(slot0.bxor(slot1[slot2(slot0[4], 3)], slot3[slot2(slot0[3], 2)]), slot4[slot2(slot0[2], 1)]), slot4[slot2(slot0[2], 1)][slot2(slot0[1], 0)])

		return 
	end

	function slot32(slot0, slot1)
		slot1[1] = slot0(slot1[slot2(slot0[1], 3)], 3) + slot0(slot1[slot2(slot0[4], 2)], 2) + slot0(slot1[slot2(slot0[3], 1)], 1) + slot0(slot1[slot2(slot0[2], 0)], 0)
		slot1[2] = slot0(slot1[slot2(slot0[2], 3)], 3) + slot0(slot1[slot2(slot0[1], 2)], 2) + slot0(slot1[slot2(slot0[4], 1)], 1) + slot0(slot1[slot2(slot0[3], 0)], 0)
		slot1[3] = slot0(slot1[slot2(slot0[3], 3)], 3) + slot0(slot1[slot2(slot0[2], 2)], 2) + slot0(slot1[slot2(slot0[1], 1)], 1) + slot0(slot1[slot2(slot0[4], 0)], 0)
		slot1[4] = slot0(slot1[slot2(slot0[4], 3)], 3) + slot0(slot1[slot2(slot0[3], 2)], 2) + slot0(slot1[slot2(slot0[2], 1)], 1) + slot0(slot1[slot2(slot0[1], 0)], 0)

		return 
	end

	slot19()
	slot20()
	slot21()

	return {
		ROUNDS = "rounds",
		KEY_TYPE = "type",
		ENCRYPTION_KEY = 1,
		DECRYPTION_KEY = 2,
		expandEncryptionKey = function (slot0)
			slot1 = {}

			if (math.floor(#slot0/4) ~= 4 and slot2 ~= 6 and slot2 ~= 8) or slot2*4 ~= #slot0 then
				error("Invalid key size: " .. tostring(slot2))

				return nil
			end

			slot1[slot0] = slot2 + 6
			slot1[slot1] = slot2

			for slot6 = 0, slot2 - 1, 1 do
				slot1[slot6] = slot3(slot0[slot6*4 + 1], 3) + slot3(slot0[slot6*4 + 2], 2) + slot3(slot0[slot6*4 + 3], 1) + slot3(slot0[slot6*4 + 4], 0)
			end

			for slot6 = slot2, (slot1[slot0] + 1)*4 - 1, 1 do
				slot7 = slot1[slot6 - 1]

				if slot6%slot2 == 0 then
					slot7 = slot6.bxor(slot5(slot4(slot7)), slot7[math.floor(slot6/slot2)])
				elseif 6 < slot2 and slot6%slot2 == 4 then
					slot7 = slot5(slot7)
				end

				slot1[slot6] = slot6.bxor(slot1[slot6 - slot2], slot7)
			end

			return slot1
		end,
		expandDecryptionKey = function (slot0)
			if slot0(slot0) == nil then
				return nil
			end

			slot1[slot1] = slot1

			for slot5 = 4, (slot1[slot1] + 1)*4 - 5, 1 do
				slot1[slot5] = slot4(slot1[slot5])
			end

			return slot1
		end,
		encrypt = function (slot0, slot1, slot2, slot3, slot4)
			slot2 = slot2 or 1
			slot3 = slot3 or {}
			slot4 = slot4 or 1
			slot5 = {}
			slot6 = {}

			if slot0[slot0] ~= slot1 then
				error("No encryption key: " .. tostring(slot0[slot0]) .. ", expected " .. slot1)

				return 
			end

			slot2(slot5, slot0, 0)

			slot7 = 1

			while slot7 < slot0[slot3] - 1 do
				slot4(slot5, slot6)
				slot2(slot6, slot0, slot7)
				slot4(slot6, slot5)
				slot2(slot5, slot0, slot7 + 1)

				slot7 = slot7 + 1 + 1
			end

			slot4(slot5, slot6)
			slot2(slot6, slot0, slot7)
			slot5(slot6, slot5)
			slot2(slot5, slot0, slot7)
			util.sleepCheckIn()

			return util.intsToBytes(slot5, slot3, slot4)
		end,
		decrypt = function (slot0, slot1, slot2, slot3, slot4)
			slot2 = slot2 or 1
			slot3 = slot3 or {}
			slot4 = slot4 or 1
			slot5 = {}
			slot6 = {}

			if slot0[slot0] ~= slot1 then
				error("No decryption key: " .. tostring(slot0[slot0]))

				return 
			end

			slot2(slot5, slot0, slot0[slot3])

			slot7 = slot0[slot3] - 1

			while 2 < slot7 do
				slot4(slot5, slot6)
				slot2(slot6, slot0, slot7)
				slot4(slot6, slot5)
				slot2(slot5, slot0, slot7 - 1)

				slot7 = slot7 - 1 - 1
			end

			slot4(slot5, slot6)
			slot2(slot6, slot0, slot7)
			slot5(slot6, slot5)
			slot2(slot5, slot0, slot7)
			util.sleepCheckIn()

			return util.intsToBytes(slot5, slot3, slot4)
		end
	}
end)
slot4 = slot1(function (slot0, ...)
	return {
		new = function ()
			return {}
		end,
		addString = function (slot0, slot1)
			table.insert(slot0, slot1)

			return 
		end,
		toString = function (slot0)
			return table.concat(slot0)
		end
	}
end)
ciphermode = slot1(function (slot0, ...)
	slot2 = math.random

	return {
		encryptString = function (slot0, slot1, slot2, slot3)
			--- BLOCK #0 1-2, warpins: 1 ---
			--- END OF BLOCK #0 ---

			slot3 = if slot3 then
			JUMP TO BLOCK #1
			else
			JUMP TO BLOCK #4
			end


			--- BLOCK #1 3-7, warpins: 1 ---
			slot4 = {}

			--- END OF BLOCK #1 ---

			FLOW; TARGET BLOCK #2


			--- BLOCK #2 8-10, warpins: 0 ---
			for slot8 = 1, 16, 1 do
				--- BLOCK #0 8-10, warpins: 2 ---
				slot4[slot8] = slot3[slot8]
				--- END OF BLOCK #0 ---



			end

			--- END OF BLOCK #2 ---

			FLOW; TARGET BLOCK #3


			--- BLOCK #3 11-12, warpins: 1 ---
			slot3 = slot4 or {
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0
			}
			slot4 = aes.expandEncryptionKey(slot0)
			slot5 = slot0.new()

			--- END OF BLOCK #3 ---

			FLOW; TARGET BLOCK #4


			--- BLOCK #4 14-25, warpins: 2 ---
			--- END OF BLOCK #4 ---

			FLOW; TARGET BLOCK #5


			--- BLOCK #5 26-53, warpins: 0 ---
			for slot9 = 1, #slot1/16, 1 do
				--- BLOCK #0 26-53, warpins: 2 ---
				slot3 = slot2(slot4, slot11, slot3)

				slot0.addString(slot5, string.char(unpack(slot11)))
				--- END OF BLOCK #0 ---



			end

			--- END OF BLOCK #5 ---

			FLOW; TARGET BLOCK #6


			--- BLOCK #6 54-57, warpins: 1 ---
			return slot0.toString(slot5)
			--- END OF BLOCK #6 ---



		end,
		encryptECB = function (slot0, slot1, slot2)
			--- BLOCK #0 1-9, warpins: 1 ---
			aes.encrypt(slot0, slot1, 1, slot1, 1)

			return 
			--- END OF BLOCK #0 ---



		end,
		encryptCBC = function (slot0, slot1, slot2)
			--- BLOCK #0 1-14, warpins: 1 ---
			util.xorIV(slot1, slot2)
			aes.encrypt(slot0, slot1, 1, slot1, 1)

			return slot1
			--- END OF BLOCK #0 ---



		end,
		encryptOFB = function (slot0, slot1, slot2)
			--- BLOCK #0 1-14, warpins: 1 ---
			aes.encrypt(slot0, slot2, 1, slot2, 1)
			util.xorIV(slot1, slot2)

			return slot2
			--- END OF BLOCK #0 ---



		end,
		encryptCFB = function (slot0, slot1, slot2)
			--- BLOCK #0 1-14, warpins: 1 ---
			aes.encrypt(slot0, slot2, 1, slot2, 1)
			util.xorIV(slot1, slot2)

			return slot1
			--- END OF BLOCK #0 ---



		end,
		encryptCTR = function (slot0, slot1, slot2)
			--- BLOCK #0 1-5, warpins: 1 ---
			slot3 = {}

			--- END OF BLOCK #0 ---

			FLOW; TARGET BLOCK #1


			--- BLOCK #1 6-8, warpins: 0 ---
			for slot7 = 1, 16, 1 do
				--- BLOCK #0 6-8, warpins: 2 ---
				slot3[slot7] = slot2[slot7]
				--- END OF BLOCK #0 ---



			end

			--- END OF BLOCK #1 ---

			FLOW; TARGET BLOCK #2


			--- BLOCK #2 9-26, warpins: 1 ---
			aes.encrypt(slot0, slot2, 1, slot2, 1)
			util.xorIV(slot1, slot2)
			util.increment(slot3)

			return slot3
			--- END OF BLOCK #2 ---



		end,
		decryptString = function (slot0, slot1, slot2, slot3)
			--- BLOCK #0 1-2, warpins: 1 ---
			--- END OF BLOCK #0 ---

			slot3 = if slot3 then
			JUMP TO BLOCK #1
			else
			JUMP TO BLOCK #4
			end


			--- BLOCK #1 3-7, warpins: 1 ---
			slot4 = {}

			--- END OF BLOCK #1 ---

			FLOW; TARGET BLOCK #2


			--- BLOCK #2 8-10, warpins: 0 ---
			for slot8 = 1, 16, 1 do
				--- BLOCK #0 8-10, warpins: 2 ---
				slot4[slot8] = slot3[slot8]
				--- END OF BLOCK #0 ---



			end

			--- END OF BLOCK #2 ---

			FLOW; TARGET BLOCK #3


			--- BLOCK #3 11-12, warpins: 1 ---
			slot3 = slot4 or {
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0,
				0
			}
			slot4 = nil
			slot4 = ((slot2 ~= slot0.decryptOFB and slot2 ~= slot0.decryptCFB and slot2 ~= slot0.decryptCTR) or aes.expandEncryptionKey(slot0)) and aes.expandDecryptionKey(slot0)
			slot5 = slot1.new()

			--- END OF BLOCK #3 ---

			FLOW; TARGET BLOCK #4


			--- BLOCK #4 14-18, warpins: 2 ---
			--- END OF BLOCK #4 ---

			FLOW; TARGET BLOCK #5


			--- BLOCK #5 38-45, warpins: 2 ---
			--- END OF BLOCK #5 ---

			FLOW; TARGET BLOCK #6


			--- BLOCK #6 46-73, warpins: 0 ---
			for slot9 = 1, #slot1/16, 1 do
				--- BLOCK #0 46-73, warpins: 2 ---
				slot3 = slot2(slot4, slot11, slot3)

				slot1.addString(slot5, string.char(unpack(slot11)))
				--- END OF BLOCK #0 ---



			end

			--- END OF BLOCK #6 ---

			FLOW; TARGET BLOCK #7


			--- BLOCK #7 74-77, warpins: 1 ---
			return slot1.toString(slot5)
			--- END OF BLOCK #7 ---



		end,
		decryptECB = function (slot0, slot1, slot2)
			--- BLOCK #0 1-9, warpins: 1 ---
			aes.decrypt(slot0, slot1, 1, slot1, 1)

			return slot2
			--- END OF BLOCK #0 ---



		end,
		decryptCBC = function (slot0, slot1, slot2)
			--- BLOCK #0 1-5, warpins: 1 ---
			slot3 = {}

			--- END OF BLOCK #0 ---

			FLOW; TARGET BLOCK #1


			--- BLOCK #1 6-8, warpins: 0 ---
			for slot7 = 1, 16, 1 do
				--- BLOCK #0 6-8, warpins: 2 ---
				slot3[slot7] = slot1[slot7]
				--- END OF BLOCK #0 ---



			end

			--- END OF BLOCK #1 ---

			FLOW; TARGET BLOCK #2


			--- BLOCK #2 9-22, warpins: 1 ---
			aes.decrypt(slot0, slot1, 1, slot1, 1)
			util.xorIV(slot1, slot2)

			return slot3
			--- END OF BLOCK #2 ---



		end,
		decryptOFB = function (slot0, slot1, slot2)
			--- BLOCK #0 1-14, warpins: 1 ---
			aes.encrypt(slot0, slot2, 1, slot2, 1)
			util.xorIV(slot1, slot2)

			return slot2
			--- END OF BLOCK #0 ---



		end,
		decryptCFB = function (slot0, slot1, slot2)
			--- BLOCK #0 1-5, warpins: 1 ---
			slot3 = {}

			--- END OF BLOCK #0 ---

			FLOW; TARGET BLOCK #1


			--- BLOCK #1 6-8, warpins: 0 ---
			for slot7 = 1, 16, 1 do
				--- BLOCK #0 6-8, warpins: 2 ---
				slot3[slot7] = slot1[slot7]
				--- END OF BLOCK #0 ---



			end

			--- END OF BLOCK #1 ---

			FLOW; TARGET BLOCK #2


			--- BLOCK #2 9-22, warpins: 1 ---
			aes.encrypt(slot0, slot2, 1, slot2, 1)
			util.xorIV(slot1, slot2)

			return slot3
			--- END OF BLOCK #2 ---



		end,
		decryptCTR = ()["encryptCTR"]
	}
end)
AES128 = 16
AES192 = 24
AES256 = 32
ECBMODE = 1
CBCMODE = 2
OFBMODE = 3
CFBMODE = 4
CTRMODE = 4

function slot5(slot0, slot1, slot2)
	--- BLOCK #0 1-9, warpins: 1 ---
	return {
		string.byte(slot0, 1, #slot0)
	}
	--- END OF BLOCK #0 ---



end

function encrypt(slot0, slot1, slot2, slot3, slot4)
	--- BLOCK #0 1-3, warpins: 1 ---
	assert(slot0 ~= nil, "Empty password.")
	assert(slot0 ~= nil, "Empty data.")

	slot5 = slot3 or CBCMODE
	slot7 = slot0(slot0, slot2 or AES128, slot4)
	slot8 = slot1

	--- END OF BLOCK #0 ---

	FLOW; TARGET BLOCK #1


	--- BLOCK #1 7-11, warpins: 2 ---
	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 15-18, warpins: 2 ---
	--- END OF BLOCK #2 ---

	FLOW; TARGET BLOCK #3


	--- BLOCK #3 20-21, warpins: 2 ---
	--- END OF BLOCK #3 ---

	FLOW; TARGET BLOCK #4


	--- BLOCK #4 23-31, warpins: 2 ---
	--- END OF BLOCK #4 ---

	if slot5 == ECBMODE then
	JUMP TO BLOCK #5
	else
	JUMP TO BLOCK #6
	end


	--- BLOCK #5 32-40, warpins: 1 ---
	return ciphermode.encryptString(slot7, slot8, ciphermode.encryptECB, slot4)
	--- END OF BLOCK #5 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #15


	--- BLOCK #6 41-43, warpins: 1 ---
	--- END OF BLOCK #6 ---

	if slot5 == CBCMODE then
	JUMP TO BLOCK #7
	else
	JUMP TO BLOCK #8
	end


	--- BLOCK #7 44-52, warpins: 1 ---
	return ciphermode.encryptString(slot7, slot8, ciphermode.encryptCBC, slot4)
	--- END OF BLOCK #7 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #15


	--- BLOCK #8 53-55, warpins: 1 ---
	--- END OF BLOCK #8 ---

	if slot5 == OFBMODE then
	JUMP TO BLOCK #9
	else
	JUMP TO BLOCK #10
	end


	--- BLOCK #9 56-64, warpins: 1 ---
	return ciphermode.encryptString(slot7, slot8, ciphermode.encryptOFB, slot4)
	--- END OF BLOCK #9 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #15


	--- BLOCK #10 65-67, warpins: 1 ---
	--- END OF BLOCK #10 ---

	if slot5 == CFBMODE then
	JUMP TO BLOCK #11
	else
	JUMP TO BLOCK #12
	end


	--- BLOCK #11 68-76, warpins: 1 ---
	return ciphermode.encryptString(slot7, slot8, ciphermode.encryptCFB, slot4)
	--- END OF BLOCK #11 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #15


	--- BLOCK #12 77-79, warpins: 1 ---
	--- END OF BLOCK #12 ---

	if slot5 == CTRMODE then
	JUMP TO BLOCK #13
	else
	JUMP TO BLOCK #14
	end


	--- BLOCK #13 80-88, warpins: 1 ---
	return ciphermode.encryptString(slot7, slot8, ciphermode.encryptCTR, slot4)

	--- END OF BLOCK #13 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #15


	--- BLOCK #14 89-92, warpins: 1 ---
	error("Unknown mode", 2)

	--- END OF BLOCK #14 ---

	FLOW; TARGET BLOCK #15


	--- BLOCK #15 93-93, warpins: 6 ---
	return 
	--- END OF BLOCK #15 ---



end

function decrypt(slot0, slot1, slot2, slot3, slot4)
	--- BLOCK #0 1-2, warpins: 1 ---
	slot5 = slot3 or CBCMODE
	slot7 = slot0(slot0, slot2 or AES128, slot4)
	slot8 = nil
	--- END OF BLOCK #0 ---

	FLOW; TARGET BLOCK #1


	--- BLOCK #1 4-5, warpins: 2 ---
	--- END OF BLOCK #1 ---

	FLOW; TARGET BLOCK #2


	--- BLOCK #2 7-15, warpins: 2 ---
	--- END OF BLOCK #2 ---

	if slot5 == ECBMODE then
	JUMP TO BLOCK #3
	else
	JUMP TO BLOCK #4
	end


	--- BLOCK #3 16-25, warpins: 1 ---
	slot8 = ciphermode.decryptString(slot7, slot1, ciphermode.decryptECB, slot4)
	--- END OF BLOCK #3 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #13


	--- BLOCK #4 26-28, warpins: 1 ---
	--- END OF BLOCK #4 ---

	if slot5 == CBCMODE then
	JUMP TO BLOCK #5
	else
	JUMP TO BLOCK #6
	end


	--- BLOCK #5 29-38, warpins: 1 ---
	slot8 = ciphermode.decryptString(slot7, slot1, ciphermode.decryptCBC, slot4)
	--- END OF BLOCK #5 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #13


	--- BLOCK #6 39-41, warpins: 1 ---
	--- END OF BLOCK #6 ---

	if slot5 == OFBMODE then
	JUMP TO BLOCK #7
	else
	JUMP TO BLOCK #8
	end


	--- BLOCK #7 42-51, warpins: 1 ---
	slot8 = ciphermode.decryptString(slot7, slot1, ciphermode.decryptOFB, slot4)
	--- END OF BLOCK #7 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #13


	--- BLOCK #8 52-54, warpins: 1 ---
	--- END OF BLOCK #8 ---

	if slot5 == CFBMODE then
	JUMP TO BLOCK #9
	else
	JUMP TO BLOCK #10
	end


	--- BLOCK #9 55-64, warpins: 1 ---
	slot8 = ciphermode.decryptString(slot7, slot1, ciphermode.decryptCFB, slot4)
	--- END OF BLOCK #9 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #13


	--- BLOCK #10 65-67, warpins: 1 ---
	--- END OF BLOCK #10 ---

	if slot5 == CTRMODE then
	JUMP TO BLOCK #11
	else
	JUMP TO BLOCK #12
	end


	--- BLOCK #11 68-77, warpins: 1 ---
	slot8 = ciphermode.decryptString(slot7, slot1, ciphermode.decryptCTR, slot4)

	--- END OF BLOCK #11 ---

	UNCONDITIONAL JUMP; TARGET BLOCK #13


	--- BLOCK #12 78-81, warpins: 1 ---
	error("Unknown mode", 2)

	--- END OF BLOCK #12 ---

	FLOW; TARGET BLOCK #13


	--- BLOCK #13 82-85, warpins: 6 ---
	result = slot8

	--- END OF BLOCK #13 ---

	if result == nil then
	JUMP TO BLOCK #14
	else
	JUMP TO BLOCK #15
	end


	--- BLOCK #14 86-87, warpins: 1 ---
	return nil
	--- END OF BLOCK #14 ---

	FLOW; TARGET BLOCK #15


	--- BLOCK #15 88-89, warpins: 2 ---
	return result
	--- END OF BLOCK #15 ---



end

function tohex(slot0)
	--- BLOCK #0 1-8, warpins: 1 ---
	return string.gsub(slot0, ".", function (slot0)
		--- BLOCK #0 1-8, warpins: 1 ---
		return string.format("%02X", string.byte(slot0))
		--- END OF BLOCK #0 ---



	end)
	--- END OF BLOCK #0 ---



end

result = encrypt(slot0, "HaveFunWithN1CTF", AES128, CTRMODE)

return tohex(result)
