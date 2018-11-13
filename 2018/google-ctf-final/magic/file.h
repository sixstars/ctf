/*
 * Copyright (c) Ian F. Darwin 1986-1995.
 * Software written by Ian F. Darwin and others;
 * maintained 1995-present by Christos Zoulas and others.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice immediately at the beginning of the file, without modification,
 *    this list of conditions, and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */
/*
 * file.h - definitions for file(1) program
 * @(#)$File: file.h,v 1.201 2018/10/19 00:33:04 christos Exp $
 */

#ifndef __file_h__
#define __file_h__

#include <stdint.h>
#include <stdio.h>	/* Include that here, to make sure __P gets defined */
#include <errno.h>
#include <fcntl.h>	/* For open and flags */
#define FILE_T_LOCAL	1
#define FILE_T_WINDOWS	2

#define MAXMAGIS 8192		/* max entries in any one magic file
				   or directory */
#define MAXDESC	64		/* max len of text description/MIME type */
#define MAXMIME	80		/* max len of text MIME type */
#define MAXstring 96		/* max len of "string" types */

#define MAGICNO		0xF11E041C
#define VERSIONNO	14
#define FILE_MAGICSIZE	344

#define	FILE_LOAD	0
#define FILE_CHECK	1
#define FILE_COMPILE	2
#define FILE_LIST	3
#ifdef WIN32
  #ifdef _WIN64
    #define SIZE_T_FORMAT "I64"
  #else
    #define SIZE_T_FORMAT ""
  #endif
  #define INT64_T_FORMAT "I64"
  #define INTMAX_T_FORMAT "I64"
#else
  #define SIZE_T_FORMAT "z"
  #define INT64_T_FORMAT "ll"
  #define INTMAX_T_FORMAT "j"
#endif
#include <stdint.h>
#define BIT(A)   (1 << (A))
#define STRING_COMPACT_WHITESPACE		BIT(0)
#define STRING_COMPACT_OPTIONAL_WHITESPACE	BIT(1)
#define STRING_IGNORE_LOWERCASE			BIT(2)
#define STRING_IGNORE_UPPERCASE			BIT(3)
#define REGEX_OFFSET_START			BIT(4)
#define STRING_TEXTTEST				BIT(5)
#define STRING_BINTEST				BIT(6)
#define PSTRING_1_BE				BIT(7)
#define PSTRING_1_LE				BIT(7)
#define PSTRING_2_BE				BIT(8)
#define PSTRING_2_LE				BIT(9)
#define PSTRING_4_BE				BIT(10)
#define PSTRING_4_LE				BIT(11)
#define REGEX_LINE_COUNT			BIT(11)
#define PSTRING_LEN	\
    (PSTRING_1_BE|PSTRING_2_LE|PSTRING_2_BE|PSTRING_4_LE|PSTRING_4_BE)
#define PSTRING_LENGTH_INCLUDES_ITSELF		BIT(12)
#define	STRING_TRIM				BIT(13)
#define CHAR_COMPACT_WHITESPACE			'W'
#define CHAR_COMPACT_OPTIONAL_WHITESPACE	'w'
#define CHAR_IGNORE_LOWERCASE			'c'
#define CHAR_IGNORE_UPPERCASE			'C'
#define CHAR_REGEX_OFFSET_START			's'
#define CHAR_TEXTTEST				't'
#define	CHAR_TRIM				'T'
#define CHAR_BINTEST				'b'
#define CHAR_PSTRING_1_BE			'B'
#define CHAR_PSTRING_1_LE			'B'
#define CHAR_PSTRING_2_BE			'H'
#define CHAR_PSTRING_2_LE			'h'
#define CHAR_PSTRING_4_BE			'L'
#define CHAR_PSTRING_4_LE			'l'
#define CHAR_PSTRING_LENGTH_INCLUDES_ITSELF     'J'
#define STRING_IGNORE_CASE		(STRING_IGNORE_LOWERCASE|STRING_IGNORE_UPPERCASE)
#define STRING_DEFAULT_RANGE		100

#define	INDIRECT_RELATIVE			BIT(0)
#define	CHAR_INDIRECT_RELATIVE			'r'

struct buffer {
	int fd;
	struct stat st;
	const void *fbuf;
	size_t flen;
	off_t eoff;
	void *ebuf;
	size_t elen;
};

union VALUETYPE {
	uint8_t b;
	uint16_t h;
	uint32_t l;
	uint64_t q;
	uint8_t hs[2];	/* 2 bytes of a fixed-endian "short" */
	uint8_t hl[4];	/* 4 bytes of a fixed-endian "long" */
	uint8_t hq[8];	/* 8 bytes of a fixed-endian "quad" */
	char s[MAXstring];	/* the search string or regex pattern */
	unsigned char us[MAXstring];
	float f;
	double d;
};

struct magic {
	/* Word 1 */
	uint16_t cont_level;	/* level of ">" */
	uint8_t flag;
#define INDIR		0x01	/* if '(...)' appears */
#define OFFADD		0x02	/* if '>&' or '>...(&' appears */
#define INDIROFFADD	0x04	/* if '>&(' appears */
#define UNSIGNED	0x08	/* comparison is unsigned */
#define NOSPACE		0x10	/* suppress space character before output */
#define BINTEST		0x20	/* test is for a binary type (set only
				   for top-level tests) */
#define TEXTTEST	0x40	/* for passing to file_softmagic */

	uint8_t factor;

	/* Word 2 */
	uint8_t reln;		/* relation (0=eq, '>'=gt, etc) */
	uint8_t vallen;		/* length of string value, if any */
	uint8_t type;		/* comparison type (FILE_*) */
	uint8_t in_type;	/* type of indirection */
#define 			FILE_INVALID	0
#define 			FILE_BYTE	1
#define				FILE_SHORT	2
#define				FILE_DEFAULT	3
#define				FILE_LONG	4
#define				FILE_STRING	5
#define				FILE_DATE	6
#define				FILE_BESHORT	7
#define				FILE_BELONG	8
#define				FILE_BEDATE	9
#define				FILE_LESHORT	10
#define				FILE_LELONG	11
#define				FILE_LEDATE	12
#define				FILE_PSTRING	13
#define				FILE_LDATE	14
#define				FILE_BELDATE	15
#define				FILE_LELDATE	16
#define				FILE_REGEX	17
#define				FILE_BESTRING16	18
#define				FILE_LESTRING16	19
#define				FILE_SEARCH	20
#define				FILE_MEDATE	21
#define				FILE_MELDATE	22
#define				FILE_MELONG	23
#define				FILE_QUAD	24
#define				FILE_LEQUAD	25
#define				FILE_BEQUAD	26
#define				FILE_QDATE	27
#define				FILE_LEQDATE	28
#define				FILE_BEQDATE	29
#define				FILE_QLDATE	30
#define				FILE_LEQLDATE	31
#define				FILE_BEQLDATE	32
#define				FILE_FLOAT	33
#define				FILE_BEFLOAT	34
#define				FILE_LEFLOAT	35
#define				FILE_DOUBLE	36
#define				FILE_BEDOUBLE	37
#define				FILE_LEDOUBLE	38
#define				FILE_BEID3	39
#define				FILE_LEID3	40
#define				FILE_INDIRECT	41
#define				FILE_QWDATE	42
#define				FILE_LEQWDATE	43
#define				FILE_BEQWDATE	44
#define				FILE_NAME	45
#define				FILE_USE	46
#define				FILE_CLEAR	47
#define				FILE_DER	48
#define				FILE_NAMES_SIZE	49 /* size of array to contain all names */

#define IS_STRING(t) \
	((t) == FILE_STRING || \
	 (t) == FILE_PSTRING || \
	 (t) == FILE_BESTRING16 || \
	 (t) == FILE_LESTRING16 || \
	 (t) == FILE_REGEX || \
	 (t) == FILE_SEARCH || \
	 (t) == FILE_INDIRECT || \
	 (t) == FILE_NAME || \
	 (t) == FILE_USE)

#define FILE_FMT_NONE 0
#define FILE_FMT_NUM  1 /* "cduxXi" */
#define FILE_FMT_STR  2 /* "s" */
#define FILE_FMT_QUAD 3 /* "ll" */
#define FILE_FMT_FLOAT 4 /* "eEfFgG" */
#define FILE_FMT_DOUBLE 5 /* "eEfFgG" */

	/* Word 3 */
	uint8_t in_op;		/* operator for indirection */
	uint8_t mask_op;	/* operator for mask */
	uint8_t cond;		/* conditional type */
	uint8_t factor_op;
#define		FILE_FACTOR_OP_PLUS	'+'
#define		FILE_FACTOR_OP_MINUS	'-'
#define		FILE_FACTOR_OP_TIMES	'*'
#define		FILE_FACTOR_OP_DIV	'/'
#define		FILE_FACTOR_OP_NONE	'\0'

#define				FILE_OPS	"&|^+-*/%"
#define				FILE_OPAND	0
#define				FILE_OPOR	1
#define				FILE_OPXOR	2
#define				FILE_OPADD	3
#define				FILE_OPMINUS	4
#define				FILE_OPMULTIPLY	5
#define				FILE_OPDIVIDE	6
#define				FILE_OPMODULO	7
#define				FILE_OPS_MASK	0x07 /* mask for above ops */
#define				FILE_UNUSED_1	0x08
#define				FILE_UNUSED_2	0x10
#define				FILE_OPSIGNED	0x20
#define				FILE_OPINVERSE	0x40
#define				FILE_OPINDIRECT	0x80

#ifdef ENABLE_CONDITIONALS
#define				COND_NONE	0
#define				COND_IF		1
#define				COND_ELIF	2
#define				COND_ELSE	3
#endif /* ENABLE_CONDITIONALS */

	/* Word 4 */
	int32_t offset;		/* offset to magic number */
	/* Word 5 */
	int32_t in_offset;	/* offset from indirection */
	/* Word 6 */
	uint32_t lineno;	/* line number in magic file */
	/* Word 7,8 */
	union {
		uint64_t _mask;	/* for use with numeric and date types */
		struct {
			uint32_t _count;	/* repeat/line count */
			uint32_t _flags;	/* modifier flags */
		} _s;		/* for use with string types */
	} _u;
#define num_mask _u._mask
#define str_range _u._s._count
#define str_flags _u._s._flags
	/* Words 9-24 */
	union VALUETYPE value;	/* either number or string */
	/* Words 25-40 */
	char desc[MAXDESC];	/* description */
	/* Words 41-60 */
	char mimetype[MAXMIME]; /* MIME type */
	/* Words 61-62 */
	char apple[8];		/* APPLE CREATOR/TYPE */
	/* Words 63-78 */
	char ext[64];		/* Popular extensions */
};
#define SZOF(a)	(sizeof(a) / sizeof(a[0]))


#endif /* __file_h__ */
