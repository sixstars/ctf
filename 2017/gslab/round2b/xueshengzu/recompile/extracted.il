.assembly extern mscorlib
{
  .ver 4:0:0:0
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 ) // .z\V.4..
}
.assembly 'encrypt'
{
  .custom instance void class [mscorlib]System.Reflection.AssemblyTitleAttribute::'.ctor'(string) =  (01 00 07 65 6E 63 72 79 70 74 00 00 ) // ...encrypt..

  .custom instance void class [mscorlib]System.Reflection.AssemblyDescriptionAttribute::'.ctor'(string) =  (01 00 00 00 00 ) // .....

  .custom instance void class [mscorlib]System.Reflection.AssemblyConfigurationAttribute::'.ctor'(string) =  (01 00 00 00 00 ) // .....

  .custom instance void class [mscorlib]System.Reflection.AssemblyCompanyAttribute::'.ctor'(string) =  (01 00 00 00 00 ) // .....

  .custom instance void class [mscorlib]System.Reflection.AssemblyProductAttribute::'.ctor'(string) =  (01 00 00 00 00 ) // .....

  .custom instance void class [mscorlib]System.Reflection.AssemblyCopyrightAttribute::'.ctor'(string) =  (01 00 0A 7A 65 65 77 69 6E 70 65 6E 67 00 00 ) // ...zeewinpeng..

  .custom instance void class [mscorlib]System.Reflection.AssemblyTrademarkAttribute::'.ctor'(string) =  (01 00 00 00 00 ) // .....

  .custom instance void class [mscorlib]System.Runtime.CompilerServices.RuntimeCompatibilityAttribute::'.ctor'() =  (
		01 00 01 00 54 02 16 57 72 61 70 4E 6F 6E 45 78   // ....T..WrapNonEx
		63 65 70 74 69 6F 6E 54 68 72 6F 77 73 01       ) // ceptionThrows.

  .hash algorithm 0x00008004
  .ver  1:0:6314:35005
}
.module encrypt.dll // GUID = {9FA2911E-D747-492C-BCD2-3B92DA22FE17}

  .class private auto ansi beforefieldinit Hello
        extends [mscorlib]System.Object
  {

    // method line 1
    .method public hidebysig  specialname  rtspecialname
           instance default void .ctor()  cil managed
    {
        // Method begins at RVA 0x20ec
        // Code size 7 (0x7)
        .maxstack 8
        IL_0000: ldarg.0
        IL_0001: call instance void valuetype [corlib]System.Object::.ctor()
        IL_0006: ret
    } // end of method instance default void .ctor()

    // method line 2
    .method public static
           default void Main()  cil managed
    {
        // Method begins at RVA 0x20f4
        .entrypoint
        // Code size 11 (0xb)
        .maxstack 8
        IL_0000: ldstr "Hello Mono World!"
        IL_0005: call void class [corlib]System.Console::WriteLine(string)
        IL_000a: ret
    } // end of method default void Main()

  }
.namespace encrypt
{
  .class public auto ansi beforefieldinit MyClass
  	extends [mscorlib]System.Object
  {

    // method line 1
    .method public hidebysig specialname rtspecialname
           instance default void '.ctor' ()  cil managed
    {
        // Method begins at RVA 0x20ec
	// Code size 7 (0x7)
	.maxstack 8
	IL_0000:  ldarg.0
	IL_0001:  call instance void object::'.ctor'()
	IL_0006:  ret
    } // end of method MyClass::.ctor

    // method line 2
    .method public static hidebysig
           default void EncryptDataFile ()  cil managed
    {
        // Method begins at RVA 0x20f4
	// Code size 147 (0x93)
	.maxstack 16
	.locals init (
		unsigned int8[]	V_0,
		class [mscorlib]System.IO.FileStream	V_1,
		class [mscorlib]System.IO.BinaryReader	V_2,
		class [mscorlib]System.IO.FileStream	V_3,
		class [mscorlib]System.IO.BinaryWriter	V_4)
	IL_0000:  ldstr "areyouok.png"
	IL_0005:  ldc.i4.3
	IL_0006:  newobj instance void class [mscorlib]System.IO.FileStream::'.ctor'(string, valuetype [mscorlib]System.IO.FileMode)
	IL_000b:  stloc.1
	.try { // 3
	  IL_000c:  ldloc.1
	  IL_000d:  newobj instance void class [mscorlib]System.IO.BinaryReader::'.ctor'(class [mscorlib]System.IO.Stream)
	  IL_0012:  stloc.2
	  .try { // 2
	    IL_0013:  ldloc.2
	    IL_0014:  ldloc.1
	    IL_0015:  callvirt instance int64 class [mscorlib]System.IO.Stream::get_Length()
	    IL_001a:  call int32 class [mscorlib]System.Convert::ToInt32(int64)
	    IL_001f:  callvirt instance unsigned int8[] class [mscorlib]System.IO.BinaryReader::ReadBytes(int32)
	    IL_0024:  stloc.0
	    IL_0025:  ldloc.0
	    IL_0026:  call unsigned int8[] class encrypt.MyClass::Encrypt(unsigned int8[])
	    IL_002b:  stloc.0
	    IL_002c:  leave IL_003e

	  } // end .try 2
	  finally  { // 2
	    IL_0031:  ldloc.2
	    IL_0032:  brfalse IL_003d

	    IL_0037:  ldloc.2
	    IL_0038:  callvirt instance void class [mscorlib]System.IDisposable::Dispose()
	    IL_003d:  endfinally
	  } // end handler 2
	  IL_003e:  leave IL_0050

	} // end .try 3
	finally  { // 3
	  IL_0043:  ldloc.1
	  IL_0044:  brfalse IL_004f

	  IL_0049:  ldloc.1
	  IL_004a:  callvirt instance void class [mscorlib]System.IDisposable::Dispose()
	  IL_004f:  endfinally
	} // end handler 3
	IL_0050:  ldstr "areyouok_encrypted"
	IL_0055:  ldc.i4.2
	IL_0056:  newobj instance void class [mscorlib]System.IO.FileStream::'.ctor'(string, valuetype [mscorlib]System.IO.FileMode)
	IL_005b:  stloc.3
	.try { // 1
	  IL_005c:  ldloc.3
	  IL_005d:  newobj instance void class [mscorlib]System.IO.BinaryWriter::'.ctor'(class [mscorlib]System.IO.Stream)
	  IL_0062:  stloc.s 4
	  .try { // 0
	    IL_0064:  ldloc.s 4
	    IL_0066:  ldloc.0
	    IL_0067:  callvirt instance void class [mscorlib]System.IO.BinaryWriter::Write(unsigned int8[])
	    IL_006c:  leave IL_0080

	  } // end .try 0
	  finally  { // 0
	    IL_0071:  ldloc.s 4
	    IL_0073:  brfalse IL_007f

	    IL_0078:  ldloc.s 4
	    IL_007a:  callvirt instance void class [mscorlib]System.IDisposable::Dispose()
	    IL_007f:  endfinally
	  } // end handler 0
	  IL_0080:  leave IL_0092

	} // end .try 1
	finally  { // 1
	  IL_0085:  ldloc.3
	  IL_0086:  brfalse IL_0091

	  IL_008b:  ldloc.3
	  IL_008c:  callvirt instance void class [mscorlib]System.IDisposable::Dispose()
	  IL_0091:  endfinally
	} // end handler 1
	IL_0092:  ret
    } // end of method MyClass::EncryptDataFile

    // method line 3
    .method public static hidebysig
           default unsigned int8[] Encrypt (unsigned int8[] input)  cil managed
    {
        // Method begins at RVA 0x21f8
	// Code size 332 (0x14c)
	.maxstack 18
	.locals init (
		unsigned int32[]	V_0,
		unsigned int8[]	V_1,
		int32	V_2,
		int32	V_3,
		int32	V_4,
		unsigned int8[]	V_5,
		unsigned int32[]	V_6,
		int32	V_7,
		int32	V_8)
	IL_0000:  ldc.i4.4
	IL_0001:  newarr [mscorlib]System.UInt32
	IL_0006:  dup
	IL_0007:  ldtoken field valuetype '<PrivateImplementationDetails>{9fa2911e-d747-492c-bcd2-3b92da22fe17}'/'$ArrayType=16' '<PrivateImplementationDetails>{9fa2911e-d747-492c-bcd2-3b92da22fe17}'::'$field-0'
	IL_000c:  call void class [mscorlib]System.Runtime.CompilerServices.RuntimeHelpers::InitializeArray(class [mscorlib]System.Array, valuetype [mscorlib]System.RuntimeFieldHandle)
	IL_0011:  stloc.0
	IL_0012:  ldc.i4.0
	IL_0013:  newarr [mscorlib]System.Byte
	IL_0018:  stloc.1
	IL_0019:  ldarg.0
	IL_001a:  ldlen
	IL_001b:  conv.i4
	IL_001c:  stloc.2
	IL_001d:  ldc.i4.8
	IL_001e:  newarr [mscorlib]System.Byte
	IL_0023:  stloc.s 5
	IL_0025:  ldc.i4.7
	IL_0026:  ldloc.2
	IL_0027:  ldc.i4.8
	IL_0028:  rem
	IL_0029:  sub
	IL_002a:  stloc.3
	IL_002b:  ldloc.s 5
	IL_002d:  ldc.i4.0
	IL_002e:  ldloc.3
	IL_002f:  conv.u1
	IL_0030:  stelem.i1
	IL_0031:  ldc.i4.0
	IL_0032:  stloc.s 7
	IL_0034:  br IL_0051

	IL_0039:  ldloc.s 5
	IL_003b:  ldloc.s 7
	IL_003d:  ldc.i4.1
	IL_003e:  add
	IL_003f:  ldc.i4 200
	IL_0044:  ldloc.3
	IL_0045:  add
	IL_0046:  ldloc.s 7
	IL_0048:  sub
	IL_0049:  conv.u1
	IL_004a:  stelem.i1
	IL_004b:  ldloc.s 7
	IL_004d:  ldc.i4.1
	IL_004e:  add
	IL_004f:  stloc.s 7
	IL_0051:  ldloc.s 7
	IL_0053:  ldloc.3
	IL_0054:  blt IL_0039

	IL_0059:  ldc.i4.0
	IL_005a:  stloc.s 8
	IL_005c:  br IL_0074

	IL_0061:  ldloc.s 5
	IL_0063:  ldloc.s 8
	IL_0065:  ldloc.3
	IL_0066:  add
	IL_0067:  ldc.i4.1
	IL_0068:  add
	IL_0069:  ldarg.0
	IL_006a:  ldloc.s 8
	IL_006c:  ldelem.u1
	IL_006d:  stelem.i1
	IL_006e:  ldloc.s 8
	IL_0070:  ldc.i4.1
	IL_0071:  add
	IL_0072:  stloc.s 8
	IL_0074:  ldloc.s 8
	IL_0076:  ldc.i4.7
	IL_0077:  ldloc.3
	IL_0078:  sub
	IL_0079:  blt IL_0061

	IL_007e:  ldc.i4.2
	IL_007f:  newarr [mscorlib]System.UInt32
	IL_0084:  dup
	IL_0085:  ldc.i4.0
	IL_0086:  ldloc.s 5
	IL_0088:  ldc.i4.0
	IL_0089:  call unsigned int32 class encrypt.MyClass::ConvertBytesToUInt(unsigned int8[], int32)
	IL_008e:  stelem.i4
	IL_008f:  dup
	IL_0090:  ldc.i4.1
	IL_0091:  ldloc.s 5
	IL_0093:  ldc.i4.4
	IL_0094:  call unsigned int32 class encrypt.MyClass::ConvertBytesToUInt(unsigned int8[], int32)
	IL_0099:  stelem.i4
	IL_009a:  stloc.s 6
	IL_009c:  ldloc.s 6
	IL_009e:  ldc.i4.0
	IL_009f:  ldloc.s 6
	IL_00a1:  ldc.i4.0
	IL_00a2:  ldelem.u4
	IL_00a3:  ldloc.0
	IL_00a4:  ldc.i4.0
	IL_00a5:  ldelem.u4
	IL_00a6:  xor
	IL_00a7:  stelem.i4
	IL_00a8:  ldloc.s 6
	IL_00aa:  ldc.i4.1
	IL_00ab:  ldloc.s 6
	IL_00ad:  ldc.i4.1
	IL_00ae:  ldelem.u4
	IL_00af:  ldloc.0
	IL_00b0:  ldc.i4.2
	IL_00b1:  ldelem.u4
	IL_00b2:  xor
	IL_00b3:  stelem.i4
	IL_00b4:  ldloc.s 6
	IL_00b6:  ldloc.0
	IL_00b7:  call unsigned int32[] class encrypt.MyClass::Code(unsigned int32[], unsigned int32[])
	IL_00bc:  stloc.s 6
	IL_00be:  ldloc.1
	IL_00bf:  ldloc.s 6
	IL_00c1:  ldc.i4.0
	IL_00c2:  ldelem.u4
	IL_00c3:  call unsigned int8[] class encrypt.MyClass::ConvertUIntToBytes(unsigned int32)
	IL_00c8:  call unsigned int8[] class encrypt.MyClass::CombineBytes(unsigned int8[], unsigned int8[])
	IL_00cd:  stloc.1
	IL_00ce:  ldloc.1
	IL_00cf:  ldloc.s 6
	IL_00d1:  ldc.i4.1
	IL_00d2:  ldelem.u4
	IL_00d3:  call unsigned int8[] class encrypt.MyClass::ConvertUIntToBytes(unsigned int32)
	IL_00d8:  call unsigned int8[] class encrypt.MyClass::CombineBytes(unsigned int8[], unsigned int8[])
	IL_00dd:  stloc.1
	IL_00de:  ldc.i4.7
	IL_00df:  ldloc.3
	IL_00e0:  sub
	IL_00e1:  stloc.s 4
	IL_00e3:  br IL_0142

	IL_00e8:  ldloc.s 6
	IL_00ea:  ldc.i4.0
	IL_00eb:  ldelema [mscorlib]System.UInt32
	IL_00f0:  dup
	IL_00f1:  ldind.u4
	IL_00f2:  ldarg.0
	IL_00f3:  ldloc.s 4
	IL_00f5:  call unsigned int32 class encrypt.MyClass::ConvertBytesToUInt(unsigned int8[], int32)
	IL_00fa:  xor
	IL_00fb:  stind.i4
	IL_00fc:  ldloc.s 6
	IL_00fe:  ldc.i4.1
	IL_00ff:  ldelema [mscorlib]System.UInt32
	IL_0104:  dup
	IL_0105:  ldind.u4
	IL_0106:  ldarg.0
	IL_0107:  ldloc.s 4
	IL_0109:  ldc.i4.4
	IL_010a:  add
	IL_010b:  call unsigned int32 class encrypt.MyClass::ConvertBytesToUInt(unsigned int8[], int32)
	IL_0110:  xor
	IL_0111:  stind.i4
	IL_0112:  ldloc.s 6
	IL_0114:  ldloc.0
	IL_0115:  call unsigned int32[] class encrypt.MyClass::Code(unsigned int32[], unsigned int32[])
	IL_011a:  stloc.s 6
	IL_011c:  ldloc.1
	IL_011d:  ldloc.s 6
	IL_011f:  ldc.i4.0
	IL_0120:  ldelem.u4
	IL_0121:  call unsigned int8[] class encrypt.MyClass::ConvertUIntToBytes(unsigned int32)
	IL_0126:  call unsigned int8[] class encrypt.MyClass::CombineBytes(unsigned int8[], unsigned int8[])
	IL_012b:  stloc.1
	IL_012c:  ldloc.1
	IL_012d:  ldloc.s 6
	IL_012f:  ldc.i4.1
	IL_0130:  ldelem.u4
	IL_0131:  call unsigned int8[] class encrypt.MyClass::ConvertUIntToBytes(unsigned int32)
	IL_0136:  call unsigned int8[] class encrypt.MyClass::CombineBytes(unsigned int8[], unsigned int8[])
	IL_013b:  stloc.1
	IL_013c:  ldloc.s 4
	IL_013e:  ldc.i4.8
	IL_013f:  add
	IL_0140:  stloc.s 4
	IL_0142:  ldloc.s 4
	IL_0144:  ldloc.2
	IL_0145:  blt IL_00e8

	IL_014a:  ldloc.1
	IL_014b:  ret
    } // end of method MyClass::Encrypt

    // method line 4
    .method private static hidebysig
           default unsigned int32[] Code (unsigned int32[] v, unsigned int32[] k)  cil managed
    {
        // Method begins at RVA 0x2350
	// Code size 164 (0xa4)
	.maxstack 11
	.locals init (
		unsigned int32	V_0,
		unsigned int32	V_1,
		unsigned int32	V_2,
		unsigned int32	V_3,
		unsigned int32	V_4)
	IL_0000:  ldarg.0
	IL_0001:  ldc.i4.0
	IL_0002:  ldelem.u4
	IL_0003:  stloc.0
	IL_0004:  ldarg.0
	IL_0005:  ldc.i4.1
	IL_0006:  ldelem.u4
	IL_0007:  stloc.1
	IL_0008:  ldc.i4.0
	IL_0009:  stloc.2
	IL_000a:  ldc.r8 5.
	IL_0013:  ldc.r8 0.5
	IL_001c:  call float64 class [mscorlib]System.Math::Pow(float64, float64)
	IL_0021:  ldc.r8 1.
	IL_002a:  sub
	IL_002b:  ldc.r8 2.
	IL_0034:  ldc.r8 31.
	IL_003d:  call float64 class [mscorlib]System.Math::Pow(float64, float64)
	IL_0042:  mul
	IL_0043:  call float64 class [mscorlib]System.Math::Floor(float64)
	IL_0048:  call unsigned int32 class [mscorlib]System.Convert::ToUInt32(float64)
	IL_004d:  stloc.3
	IL_004e:  ldc.i4.s 0x20
	IL_0050:  stloc.s 4
	IL_0052:  br IL_0088

	IL_0057:  ldloc.0
	IL_0058:  ldloc.1
	IL_0059:  ldc.i4.4
	IL_005a:  shl
	IL_005b:  ldloc.1
	IL_005c:  ldc.i4.5
	IL_005d:  shr.un
	IL_005e:  ldloc.1
	IL_005f:  add
	IL_0060:  xor
	IL_0061:  ldloc.2
	IL_0062:  ldarg.1
	IL_0063:  ldloc.2
	IL_0064:  ldc.i4.3
	IL_0065:  and
	IL_0066:  conv.u
	IL_0067:  ldelem.u4
	IL_0068:  add
	IL_0069:  xor
	IL_006a:  add
	IL_006b:  stloc.0
	IL_006c:  ldloc.2
	IL_006d:  ldloc.3
	IL_006e:  add
	IL_006f:  stloc.2
	IL_0070:  ldloc.1
	IL_0071:  ldloc.0
	IL_0072:  ldc.i4.4
	IL_0073:  shl
	IL_0074:  ldloc.0
	IL_0075:  ldc.i4.5
	IL_0076:  shr.un
	IL_0077:  ldloc.0
	IL_0078:  add
	IL_0079:  xor
	IL_007a:  ldloc.2
	IL_007b:  ldarg.1
	IL_007c:  ldloc.2
	IL_007d:  ldc.i4.s 0x0b
	IL_007f:  shr.un
	IL_0080:  ldc.i4.3
	IL_0081:  and
	IL_0082:  conv.u
	IL_0083:  ldelem.u4
	IL_0084:  add
	IL_0085:  xor
	IL_0086:  add
	IL_0087:  stloc.1
	IL_0088:  ldloc.s 4
	IL_008a:  dup
	IL_008b:  ldc.i4.1
	IL_008c:  sub
	IL_008d:  stloc.s 4
	IL_008f:  ldc.i4.0
	IL_0090:  bgt.un IL_0057

	IL_0095:  ldc.i4.2
	IL_0096:  newarr [mscorlib]System.UInt32
	IL_009b:  dup
	IL_009c:  ldc.i4.0
	IL_009d:  ldloc.0
	IL_009e:  stelem.i4
	IL_009f:  dup
	IL_00a0:  ldc.i4.1
	IL_00a1:  ldloc.1
	IL_00a2:  stelem.i4
	IL_00a3:  ret
    } // end of method MyClass::Code

    // method line 5
    .method private static hidebysig
           default unsigned int8[] ConvertUIntToBytes (unsigned int32 input)  cil managed
    {
        // Method begins at RVA 0x2400
	// Code size 61 (0x3d)
	.maxstack 5
	.locals init (
		unsigned int8[]	V_0)
	IL_0000:  ldc.i4.4
	IL_0001:  newarr [mscorlib]System.Byte
	IL_0006:  stloc.0
	IL_0007:  ldloc.0
	IL_0008:  ldc.i4.0
	IL_0009:  ldarg.0
	IL_000a:  ldc.i4 255
	IL_000f:  and
	IL_0010:  conv.u1
	IL_0011:  stelem.i1
	IL_0012:  ldloc.0
	IL_0013:  ldc.i4.1
	IL_0014:  ldarg.0
	IL_0015:  ldc.i4.8
	IL_0016:  shr.un
	IL_0017:  ldc.i4 255
	IL_001c:  and
	IL_001d:  conv.u1
	IL_001e:  stelem.i1
	IL_001f:  ldloc.0
	IL_0020:  ldc.i4.2
	IL_0021:  ldarg.0
	IL_0022:  ldc.i4.s 0x10
	IL_0024:  shr.un
	IL_0025:  ldc.i4 255
	IL_002a:  and
	IL_002b:  conv.u1
	IL_002c:  stelem.i1
	IL_002d:  ldloc.0
	IL_002e:  ldc.i4.3
	IL_002f:  ldarg.0
	IL_0030:  ldc.i4.s 0x18
	IL_0032:  shr.un
	IL_0033:  ldc.i4 255
	IL_0038:  and
	IL_0039:  conv.u1
	IL_003a:  stelem.i1
	IL_003b:  ldloc.0
	IL_003c:  ret
    } // end of method MyClass::ConvertUIntToBytes

    // method line 6
    .method private static hidebysig
           default unsigned int32 ConvertBytesToUInt (unsigned int8[] input, int32 pos)  cil managed
    {
        // Method begins at RVA 0x244c
	// Code size 38 (0x26)
	.maxstack 5
	.locals init (
		unsigned int32	V_0)
	IL_0000:  ldarg.0
	IL_0001:  ldarg.1
	IL_0002:  ldelem.u1
	IL_0003:  stloc.0
	IL_0004:  ldloc.0
	IL_0005:  ldarg.0
	IL_0006:  ldarg.1
	IL_0007:  ldc.i4.1
	IL_0008:  add
	IL_0009:  ldelem.u1
	IL_000a:  ldc.i4.8
	IL_000b:  shl
	IL_000c:  add
	IL_000d:  stloc.0
	IL_000e:  ldloc.0
	IL_000f:  ldarg.0
	IL_0010:  ldarg.1
	IL_0011:  ldc.i4.2
	IL_0012:  add
	IL_0013:  ldelem.u1
	IL_0014:  ldc.i4.s 0x10
	IL_0016:  shl
	IL_0017:  add
	IL_0018:  stloc.0
	IL_0019:  ldloc.0
	IL_001a:  ldarg.0
	IL_001b:  ldarg.1
	IL_001c:  ldc.i4.3
	IL_001d:  add
	IL_001e:  ldelem.u1
	IL_001f:  ldc.i4.s 0x18
	IL_0021:  shl
	IL_0022:  add
	IL_0023:  stloc.0
	IL_0024:  ldloc.0
	IL_0025:  ret
    } // end of method MyClass::ConvertBytesToUInt

    // method line 7
    .method private static hidebysig
           default unsigned int8[] CombineBytes (unsigned int8[] bytes1, unsigned int8[] bytes2)  cil managed
    {
        // Method begins at RVA 0x2480
	// Code size 41 (0x29)
	.maxstack 7
	.locals init (
		unsigned int8[]	V_0)
	IL_0000:  ldarg.0
	IL_0001:  ldlen
	IL_0002:  conv.i4
	IL_0003:  ldarg.1
	IL_0004:  ldlen
	IL_0005:  conv.i4
	IL_0006:  add
	IL_0007:  newarr [mscorlib]System.Byte
	IL_000c:  stloc.0
	IL_000d:  ldarg.0
	IL_000e:  ldc.i4.0
	IL_000f:  ldloc.0
	IL_0010:  ldc.i4.0
	IL_0011:  ldarg.0
	IL_0012:  ldlen
	IL_0013:  conv.i4
	IL_0014:  call void class [mscorlib]System.Buffer::BlockCopy(class [mscorlib]System.Array, int32, class [mscorlib]System.Array, int32, int32)
	IL_0019:  ldarg.1
	IL_001a:  ldc.i4.0
	IL_001b:  ldloc.0
	IL_001c:  ldarg.0
	IL_001d:  ldlen
	IL_001e:  conv.i4
	IL_001f:  ldarg.1
	IL_0020:  ldlen
	IL_0021:  conv.i4
	IL_0022:  call void class [mscorlib]System.Buffer::BlockCopy(class [mscorlib]System.Array, int32, class [mscorlib]System.Array, int32, int32)
	IL_0027:  ldloc.0
	IL_0028:  ret
    } // end of method MyClass::CombineBytes

  } // end of class encrypt.MyClass
}

.namespace encrypt
{
  .class public auto ansi beforefieldinit Hello
  	extends [mscorlib]System.Object
  {

    // method line 8
    .method public hidebysig specialname rtspecialname
           instance default void '.ctor' ()  cil managed
    {
        // Method begins at RVA 0x24b8
	// Code size 7 (0x7)
	.maxstack 8
	IL_0000:  ldarg.0
	IL_0001:  call instance void object::'.ctor'()
	IL_0006:  ret
    } // end of method Hello::.ctor

    // method line 9
    .method public static hidebysig
           default void SayHello ()  cil managed
    {
        // Method begins at RVA 0x24c0
	// Code size 11 (0xb)
	.maxstack 8
	IL_0000:  ldstr "Hello GSLab!"
	IL_0005:  call void class [mscorlib]System.Console::WriteLine(string)
	IL_000a:  ret
    } // end of method Hello::SayHello

  } // end of class encrypt.Hello
}

  .class private auto ansi abstract sealed beforefieldinit '<PrivateImplementationDetails>{9fa2911e-d747-492c-bcd2-3b92da22fe17}'
  	extends [mscorlib]System.Object
  {
    .custom instance void class [mscorlib]System.Runtime.CompilerServices.CompilerGeneratedAttribute::'.ctor'() =  (01 00 00 00 ) // ....

    .field  assembly static  valuetype '<PrivateImplementationDetails>{9fa2911e-d747-492c-bcd2-3b92da22fe17}'/'$ArrayType=16' '$field-0' at D_000024cc

  .class nested private explicit ansi sealed beforefieldinit '$ArrayType=16'
  	extends [mscorlib]System.ValueType
  {
    .pack 1
    .size 16

  } // end of class $ArrayType=16

  } // end of class <PrivateImplementationDetails>{9fa2911e-d747-492c-bcd2-3b92da22fe17}

.data D_000024cc = bytearray (
	 5D 3F AC 15 FC 5A 86 1E B1 A5 83 65 EA F3 D6 54) // size: 16
