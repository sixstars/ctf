/*
 * main.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include "const.h"
#include "file.h"
void file_showstr(FILE *fp, const char *s, size_t len)
{
	char	c;

	for (;;) {
		if (len == ~0U) {
			c = *s++;
			if (c == '\0')
				break;
		}
		else  {
			if (len-- == 0)
				break;
			c = *s++;
		}
		if (c >= 040 && c <= 0176)	/* TODO isprint && !iscntrl */
			(void) fputc(c, fp);
		else {
			(void) fputc('\\', fp);
			switch (c) {
			case '\a':
				(void) fputc('a', fp);
				break;

			case '\b':
				(void) fputc('b', fp);
				break;

			case '\f':
				(void) fputc('f', fp);
				break;

			case '\n':
				(void) fputc('n', fp);
				break;

			case '\r':
				(void) fputc('r', fp);
				break;

			case '\t':
				(void) fputc('t', fp);
				break;

			case '\v':
				(void) fputc('v', fp);
				break;

			default:
				(void) fprintf(fp, "%.3o", c & 0377);
				break;
			}
		}
	}
}
void file_mdump(struct magic *m)
{
	static const char optyp[] = { FILE_OPS };
	char tbuf[26];

	(void) fprintf(stdout, "%u: %.*s %u", m->lineno,
	    (m->cont_level & 7) + 1, ">>>>>>>>", m->offset);

	if (m->flag & INDIR) {
		(void) fprintf(stdout, "(%s,",
		    /* Note: type is unsigned */
		    "*bad in_type*");
		if (m->in_op & FILE_OPINVERSE)
			(void) fputc('~', stdout);
		(void) fprintf(stdout, "%c%u),",
		    ((size_t)(m->in_op & FILE_OPS_MASK) <
		    SZOF(optyp)) ? optyp[m->in_op & FILE_OPS_MASK] : '?',
		    m->in_offset);
	}
	(void) fprintf(stdout, " %s%s", (m->flag & UNSIGNED) ? "u" : "",
	    /* Note: type is unsigned */
	    table[m->type]);
	if (m->mask_op & FILE_OPINVERSE)
		(void) fputc('~', stdout);

	if (IS_STRING(m->type)) {
		if (m->str_flags) {
			(void) fputc('/', stdout);
			if (m->str_flags & STRING_COMPACT_WHITESPACE)
				(void) fputc(CHAR_COMPACT_WHITESPACE, stdout);
			if (m->str_flags & STRING_COMPACT_OPTIONAL_WHITESPACE)
				(void) fputc(CHAR_COMPACT_OPTIONAL_WHITESPACE,
				    stdout);
			if (m->str_flags & STRING_IGNORE_LOWERCASE)
				(void) fputc(CHAR_IGNORE_LOWERCASE, stdout);
			if (m->str_flags & STRING_IGNORE_UPPERCASE)
				(void) fputc(CHAR_IGNORE_UPPERCASE, stdout);
			if (m->str_flags & REGEX_OFFSET_START)
				(void) fputc(CHAR_REGEX_OFFSET_START, stdout);
			if (m->str_flags & STRING_TEXTTEST)
				(void) fputc(CHAR_TEXTTEST, stdout);
			if (m->str_flags & STRING_BINTEST)
				(void) fputc(CHAR_BINTEST, stdout);
			if (m->str_flags & PSTRING_1_BE)
				(void) fputc(CHAR_PSTRING_1_BE, stdout);
			if (m->str_flags & PSTRING_2_BE)
				(void) fputc(CHAR_PSTRING_2_BE, stdout);
			if (m->str_flags & PSTRING_2_LE)
				(void) fputc(CHAR_PSTRING_2_LE, stdout);
			if (m->str_flags & PSTRING_4_BE)
				(void) fputc(CHAR_PSTRING_4_BE, stdout);
			if (m->str_flags & PSTRING_4_LE)
				(void) fputc(CHAR_PSTRING_4_LE, stdout);
			if (m->str_flags & PSTRING_LENGTH_INCLUDES_ITSELF)
				(void) fputc(
				    CHAR_PSTRING_LENGTH_INCLUDES_ITSELF,
				    stdout);
		}
		if (m->str_range)
			(void) fprintf(stdout, "/%u", m->str_range);
	}
	else {
		if ((size_t)(m->mask_op & FILE_OPS_MASK) < SZOF(optyp))
			(void) fputc(optyp[m->mask_op & FILE_OPS_MASK], stdout);
		else
			(void) fputc('?', stdout);

		if (m->num_mask) {
			(void) fprintf(stdout, "%.8llx",
			    (unsigned long long)m->num_mask);
		}
	}
	(void) fprintf(stdout, ",%c", m->reln);

	if (m->reln != 'x') {
		switch (m->type) {
		case FILE_BYTE:
		case FILE_SHORT:
		case FILE_LONG:
		case FILE_LESHORT:
		case FILE_LELONG:
		case FILE_MELONG:
		case FILE_BESHORT:
		case FILE_BELONG:
		case FILE_INDIRECT:
			(void) fprintf(stdout, "%d", m->value.l);
			break;
		case FILE_BEQUAD:
		case FILE_LEQUAD:
		case FILE_QUAD:
			(void) fprintf(stdout, "%" INT64_T_FORMAT "d",
			    (unsigned long long)m->value.q);
			break;
		case FILE_PSTRING:
		case FILE_STRING:
		case FILE_REGEX:
		case FILE_BESTRING16:
		case FILE_LESTRING16:
		case FILE_SEARCH:
			file_showstr(stdout, m->value.s, (size_t)m->vallen);
			break;
		case FILE_FLOAT:
		case FILE_BEFLOAT:
		case FILE_LEFLOAT:
			(void) fprintf(stdout, "%G", m->value.f);
			break;
		case FILE_DOUBLE:
		case FILE_BEDOUBLE:
		case FILE_LEDOUBLE:
			(void) fprintf(stdout, "%G", m->value.d);
			break;
		case FILE_DEFAULT:
			/* XXX - do anything here? */
			break;
		case FILE_USE:
		case FILE_NAME:
		case FILE_DER:
			(void) fprintf(stdout, "'%s'", m->value.s);
			break;
		default:
			(void) fprintf(stdout, "*bad type %d*", m->type);
			break;
		}
	}
	(void) fprintf(stdout, ",\"%s\"]\n", m->desc);
}
const char *file="flag.mgc";
//const char *file="1.mgc";
void show(struct magic* ptr){
    printf("cont_level: %d\t",ptr->cont_level);
    printf("reln:%c, factor: %d\t",ptr->reln,ptr->factor);
    printf("vallen: %d,flag: %d\t",ptr->vallen,ptr->flag);
    printf("type: %s\tin_type: %d,",table[ptr->type],ptr->in_type);
    printf("in_op: %d,mask_op: %d\t",ptr->in_op,ptr->mask_op);
    printf("cond: %d,factor_op:%d,offset: %d,lineno:%d\t",ptr->cond,ptr->factor_op,ptr->offset,ptr->lineno);
    printf("desc: %s,",ptr->desc);
    printf("value:%d,%s\n",ptr->value.b,ptr->value.hs);
}
int main(int argc, char *argv[]){
    struct stat st;
    stat(file,&st);
    size_t len=st.st_size;
    int fd=open(file,0);
    char *ptr=malloc(len);
    if(read(fd,ptr,len)!=len){
        exit(1);
    }
    char *stream=malloc(0x1000);
    struct magic *mg=(struct magic *)ptr;
    size_t size = len/sizeof(struct magic);
    int cnt=0;
    for(int i=1;i<size;i++){

//            file_mdump(&mg[i]);
            show(&mg[i]);
            //show(&mg[i+2]);
            //stream[mg[i+1].offset]=mg[i].value.b;
            cnt++;
    }
//    write(1,stream,0x100);
    printf("%d\n",cnt);
    return 0;
}
