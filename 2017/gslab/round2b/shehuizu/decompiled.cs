using System;
using System.IO;

namespace encrypt
{
	public class MyClass
	{
		public static void EncryptDataFile()
		{
			byte[] array;
			using (FileStream fileStream = new FileStream("areyouok.png", FileMode.Open))
			{
				using (BinaryReader binaryReader = new BinaryReader(fileStream))
				{
					array = binaryReader.ReadBytes(Convert.ToInt32(fileStream.Length));
					array = MyClass.Encrypt(array);
				}
			}
			using (FileStream fileStream2 = new FileStream("areyouok_encrypted", FileMode.Create))
			{
				using (BinaryWriter binaryWriter = new BinaryWriter(fileStream2))
				{
					binaryWriter.Write(array);
				}
			}
		}

		public static byte[] Encrypt(byte[] input)
		{
			uint[] array = new uint[]
			{
				1423373290u,
				363609949u,
				512121596u,
				1703126449u
			};
			byte[] array2 = new byte[0];
			int num = input.Length;
			byte[] array3 = new byte[8];
			int num2 = 7 - num % 8;
			array3[0] = (byte)num2;
			for (int i = 0; i < num2; i++)
			{
				array3[i + 1] = (byte)(200 + num2 - i);
			}
			for (int j = 0; j < 7 - num2; j++)
			{
				array3[j + num2 + 1] = input[j];
			}
			uint[] array4 = new uint[]
			{
				MyClass.ConvertBytesToUInt(array3, 0),
				MyClass.ConvertBytesToUInt(array3, 4)
			};
			array4[0] = (array4[0] ^ array[0]);
			array4[1] = (array4[1] ^ array[2]);
			array4 = MyClass.Code(array4, array);
			array2 = MyClass.CombineBytes(array2, MyClass.ConvertUIntToBytes(array4[0]));
			array2 = MyClass.CombineBytes(array2, MyClass.ConvertUIntToBytes(array4[1]));
			for (int k = 7 - num2; k < num; k += 8)
			{
				array4[0] ^= MyClass.ConvertBytesToUInt(input, k);
				array4[1] ^= MyClass.ConvertBytesToUInt(input, k + 4);
				array4 = MyClass.Code(array4, array);
				array2 = MyClass.CombineBytes(array2, MyClass.ConvertUIntToBytes(array4[0]));
				array2 = MyClass.CombineBytes(array2, MyClass.ConvertUIntToBytes(array4[1]));
			}
			return array2;
		}

		private static uint ConvertBytesToUInt(byte[] input, int pos)
		{
			uint num = (uint)input[pos];
			num += (uint)((uint)input[pos + 1] << 8);
			num += (uint)((uint)input[pos + 2] << 16);
			return num + (uint)((uint)input[pos + 3] << 24);
		}

		private static uint[] Code(uint[] v, uint[] k)
		{
			uint num = v[0];
			uint num2 = v[1];
			uint num3 = 0u;
			uint num4 = Convert.ToUInt32(Math.Floor((Math.Pow(5.0, 0.5) - 1.0) * Math.Pow(2.0, 31.0)));
			uint num5 = 32u;
			while (num5-- > 0u)
			{
				num += (num2 << 4 ^ (num2 >> 5) + num2 ^ num3 + k[(int)((UIntPtr)(num3 & 3u))]);
				num3 += num4;
				num2 += (num << 4 ^ (num >> 5) + num ^ num3 + k[(int)((UIntPtr)(num3 >> 11 & 3u))]);
			}
			return new uint[]
			{
				num,
				num2
			};
		}

		private static byte[] ConvertUIntToBytes(uint input)
		{
			return new byte[]
			{
				(byte)(input & 255u),
				(byte)(input >> 8 & 255u),
				(byte)(input >> 16 & 255u),
				(byte)(input >> 24 & 255u)
			};
		}

		private static byte[] CombineBytes(byte[] bytes1, byte[] bytes2)
		{
			byte[] array = new byte[bytes1.Length + bytes2.Length];
			Buffer.BlockCopy(bytes1, 0, array, 0, bytes1.Length);
			Buffer.BlockCopy(bytes2, 0, array, bytes1.Length, bytes2.Length);
			return array;
		}
	}
}
