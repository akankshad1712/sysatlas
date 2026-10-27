#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static int read_cpu(const char *path, unsigned long long v[4]) {
    FILE *f=fopen(path,"r"); if(!f) return -1;
    char label[32]; int n=fscanf(f,"%31s %llu %llu %llu %llu",label,&v[0],&v[1],&v[2],&v[3]);
    fclose(f); if(n!=5 || strcmp(label,"cpu")!=0) return -2; return 0;
}
static int read_mem(const char *path, unsigned long long *total, unsigned long long *available) {
    FILE *f=fopen(path,"r"); if(!f) return -1;
    char key[64],unit[16]; unsigned long long value; int got_total=0,got_available=0;
    while(fscanf(f,"%63s %llu %15s",key,&value,unit)>=2) {
        if(strcmp(unit,"kB")!=0 && strcmp(unit,"")!=0) { /* fscanf's empty-unit edge is harmless for normal procfs lines */ }
        if(strcmp(key,"MemTotal:")==0){*total=value;got_total=1;}
        if(strcmp(key,"MemAvailable:")==0){*available=value;got_available=1;}
        if(got_total&&got_available) break;
    }
    fclose(f); return got_total&&got_available?0:-2;
}
static int read_uptime(const char *path, double *uptime) {
    FILE *f=fopen(path,"r"); if(!f)return -1;
    int n=fscanf(f,"%lf",uptime); fclose(f); return n==1 && *uptime>=0?0:-2;
}
static int read_load(const char *path, double load[3]) {
    FILE *f=fopen(path,"r"); if(!f)return -1;
    int n=fscanf(f,"%lf %lf %lf",&load[0],&load[1],&load[2]); fclose(f);
    return n==3 && load[0]>=0 && load[1]>=0 && load[2]>=0?0:-2;
}
int main(void) {
    const char *root=getenv("SYSATLAS_PROC_ROOT"); if(!root)root="/proc";
    char path[512]; unsigned long long cpu[4]={0},total=0,available=0; double uptime=0,load[3]={0};
    if(snprintf(path,sizeof path,"%s/stat",root)>=(int)sizeof path || read_cpu(path,cpu)) {fprintf(stderr,"collector: failed to parse CPU stats\n");return 2;}
    if(snprintf(path,sizeof path,"%s/meminfo",root)>=(int)sizeof path || read_mem(path,&total,&available)) {fprintf(stderr,"collector: failed to parse memory stats\n");return 2;}
    if(snprintf(path,sizeof path,"%s/uptime",root)>=(int)sizeof path || read_uptime(path,&uptime)) {fprintf(stderr,"collector: failed to parse uptime\n");return 2;}
    if(snprintf(path,sizeof path,"%s/loadavg",root)>=(int)sizeof path || read_load(path,load)) {fprintf(stderr,"collector: failed to parse load average\n");return 2;}
    printf("{\"protocol_version\":1,\"collector_version\":\"1.0.0\",\"cpu\":{\"user\":%llu,\"nice\":%llu,\"system\":%llu,\"idle\":%llu},\"memory\":{\"total_kib\":%llu,\"available_kib\":%llu},\"uptime_seconds\":%.3f,\"load\":[%.3f,%.3f,%.3f]}\n",cpu[0],cpu[1],cpu[2],cpu[3],total,available,uptime,load[0],load[1],load[2]);
    return 0;
}
