
//
//      This file contains the user-defined type definitions.
//      To use it press F2 in IDA and enter the name of this file.
//

#define UNLOADED_FILE   1
#include <idc.idc>

static main(void)
{
  Enums();              // enumerations
  Structures();         // structure types
  ApplyStrucTInfos();
	LowVoids(0x7EF0);
	HighVoids(0xAA224);
}

//------------------------------------------------------------------------
// Information about enum types

static Enums(void) {
        auto id;
        BeginTypeUpdating(UTP_ENUM);
        EndTypeUpdating(UTP_ENUM);
}

static ApplyStrucTInfos_0(void) {
        auto id;
	id = GetStrucIdByName("pollfd");
	SetType(GetMemberId(id, 0x0), "int");
	SetType(GetMemberId(id, 0x4), "__int16");
	SetType(GetMemberId(id, 0x6), "__int16");
	id = GetStrucIdByName("string");
	SetType(GetMemberId(id, 0xC), "char[]");
	id = GetStrucIdByName("stat");
	SetType(GetMemberId(id, 0x0), "__dev_t");
	SetType(GetMemberId(id, 0x8), "unsigned __int16");
	SetType(GetMemberId(id, 0xC), "__ino_t");
	SetType(GetMemberId(id, 0x10), "__mode_t");
	SetType(GetMemberId(id, 0x14), "__nlink_t");
	SetType(GetMemberId(id, 0x18), "__uid_t");
	SetType(GetMemberId(id, 0x1C), "__gid_t");
	SetType(GetMemberId(id, 0x20), "__dev_t");
	SetType(GetMemberId(id, 0x28), "unsigned __int16");
	SetType(GetMemberId(id, 0x2C), "__off_t");
	SetType(GetMemberId(id, 0x30), "__blksize_t");
	SetType(GetMemberId(id, 0x34), "__blkcnt_t");
	SetType(GetMemberId(id, 0x38), "timespec");
	SetType(GetMemberId(id, 0x40), "timespec");
	SetType(GetMemberId(id, 0x48), "timespec");
	SetType(GetMemberId(id, 0x50), "unsigned __int32");
	SetType(GetMemberId(id, 0x54), "unsigned __int32");
	id = GetStrucIdByName("timespec");
	SetType(GetMemberId(id, 0x0), "__time_t");
	SetType(GetMemberId(id, 0x4), "__int32");
	id = GetStrucIdByName("mbstate_t");
	SetType(GetMemberId(id, 0x0), "int");
	SetType(GetMemberId(id, 0x4), "$1A16B277A945B8F62DE8883A2D91AFD9::$0740F39446D5E828B16B7363880DB674");
	id = GetStrucIdByName("$1A16B277A945B8F62DE8883A2D91AFD9::$0740F39446D5E828B16B7363880DB674");
	SetType(GetMemberId(id, 0x0), "wint_t");
	SetType(GetMemberId(id, 0x1), "char[4]");
	return id;
}

//------------------------------------------------------------------------
// Information about type information for structure members

static ApplyStrucTInfos() {
	ApplyStrucTInfos_0();
}

static Structures_0(id) {
        auto mid;

	id = AddStrucEx(-1,"pollfd",0);
	id = AddStrucEx(-1,"string",0);
	id = AddStrucEx(-1,"stat",0);
	id = AddStrucEx(-1,"timespec",0);
	id = AddStrucEx(-1,"mbstate_t",0);
	id = AddStrucEx(-1,"$1A16B277A945B8F62DE8883A2D91AFD9::$0740F39446D5E828B16B7363880DB674",1);

	id = GetStrucIdByName("pollfd");
	mid = AddStrucMember(id,"fd",	0,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"events",	0X4,	0x10000400,	-1,	2);
	mid = AddStrucMember(id,"revents",	0X6,	0x10000400,	-1,	2);
	SetStrucAlign(id,2);

	id = GetStrucIdByName("string");
	mid = AddStrucMember(id,"size",	0,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"malloc_size",	0X4,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"field_8",	0X8,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"buf",	0XC,	0x000400,	-1,	1);

	id = GetStrucIdByName("timespec");
	mid = AddStrucMember(id,"tv_sec",	0,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"tv_nsec",	0X4,	0x20000400,	-1,	4);
	SetStrucAlign(id,2);

	id = GetStrucIdByName("stat");
	mid = AddStrucMember(id,"st_dev",	0,	0x30000400,	-1,	8);
	mid = AddStrucMember(id,"__pad1",	0X8,	0x10000400,	-1,	2);
	mid = AddStrucMember(id,"st_ino",	0XC,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"st_mode",	0X10,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"st_nlink",	0X14,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"st_uid",	0X18,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"st_gid",	0X1C,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"st_rdev",	0X20,	0x30000400,	-1,	8);
	mid = AddStrucMember(id,"__pad2",	0X28,	0x10000400,	-1,	2);
	mid = AddStrucMember(id,"st_size",	0X2C,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"st_blksize",	0X30,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"st_blocks",	0X34,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"st_atim",	0X38,	0x60000400,	GetStrucIdByName("timespec"),	8);
	mid = AddStrucMember(id,"st_mtim",	0X40,	0x60000400,	GetStrucIdByName("timespec"),	8);
	mid = AddStrucMember(id,"st_ctim",	0X48,	0x60000400,	GetStrucIdByName("timespec"),	8);
	mid = AddStrucMember(id,"__unused4",	0X50,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"__unused5",	0X54,	0x20000400,	-1,	4);
	SetStrucAlign(id,2);

	id = GetStrucIdByName("$1A16B277A945B8F62DE8883A2D91AFD9::$0740F39446D5E828B16B7363880DB674");
	mid = AddStrucMember(id,"__wch",	0,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"__wchb",	0,	0x000400,	-1,	4);
	SetStrucAlign(id,2);

	id = GetStrucIdByName("mbstate_t");
	mid = AddStrucMember(id,"__count",	0,	0x20000400,	-1,	4);
	mid = AddStrucMember(id,"__value",	0X4,	0x60000400,	GetStrucIdByName("$1A16B277A945B8F62DE8883A2D91AFD9::$0740F39446D5E828B16B7363880DB674"),	4);
	SetStrucAlign(id,2);
	return id;
}

//------------------------------------------------------------------------
// Information about structure types

static Structures(void) {
        auto id;
        BeginTypeUpdating(UTP_STRUCT);
	id = Structures_0(id);
        EndTypeUpdating(UTP_STRUCT);
}

// End of file.
