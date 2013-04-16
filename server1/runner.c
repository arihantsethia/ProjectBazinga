#include <assert.h>
#include <getopt.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/resource.h>
#include <sys/types.h>
#include <sys/wait.h>

#ifndef bool
#define bool int
#endif

#ifndef true
#define true 1
#endif

#ifndef false
#define false 0
#endif

/*
 * Options for execution
 */
char   *infile = NULL;
char   *outfile = NULL;
char   *chrootdir = NULL;
bool   debug = false;

/* execution limits */
int    limit_stack = 0;    /* limit on stack, in bytes */
int    limit_mem   = 0;    /* limit on mem, in bytes */
int    limit_fsize = 0;    /* limit on output, in bytes */
float  limit_time  = 0;    /* limit on execution time, in seconds */
int    limit_file  = 0;    /* number of files that can be opened */
int    limit_timehard = 0; /* internal limit in order to achive limit_time */
int    limit_nproc = 0;    /* num of processes */

void init_default_limits () 
{
	limit_stack  = 8*1024*1024;
	limit_mem    = 64*1024*1024;
	limit_fsize  = 50*1024*1024; //specified in bytes?
	limit_time   = 2;

	/*
	 * Under a proper chroot, a limit on number of files
	 * should be not be necessary.
	 */
	limit_file   = 16;
	limit_nproc  = 1 ; /* dangerous don't change */
}


int unformatvalue (char* s) 
{
	char c = '-';
	int val;
	sscanf(s, "%d%c", &val, &c);
	if ( c == '-' ) return val;
	c = tolower (c);
	
	if ( c == 'k' ) return val * 1024;
	else if (c == 'm') return val*1024*1024;
	else {
		//fprintf(stderr, "WARNING: %c: Unknown size specifier in '%s'\n", c, s);
		return val;
	}
	
	return val; //not implemented for time!
}

void print_usage ()
{
	printf (
		"usage: runner [options] progname progarg1 progarg2 ... \n\
									\n\
  options:								\n\
     --input=<file>        redirect program input from file		\n\
     --output=<file>       redirect program output to file		\n\
     --mem=<size>          set the runtime memory limit to <size>	\n\
     --stack=<size>        set the runtime stack limit to <size>	\n\
     --time=<seconds>      set the run time limit in seconds (float)    \n\
     --fsize=<size>        set the limit on amount of data outputted	\n\
     --chroot=<dir>        chroot to the directory before executing     \n\
     --debug               increase verbosity, do not redirect stderr.	\n\
     --help                display this help page			\n\
									\n\
  <size> is in human readable format (12M, 12k etc., case insensitive.) \n\
  If no suffix is provided, it is understood to be bytes. 1k is 1024    \n\
  bytes and 1M is 1024k.						\n\
									\n\
  This program is a part of the CMI Online Programming Contest Judge.	\n\
  Copyright 2007-2009 Chennai Mathematical Institute. This program	\n\
  is licensed under GNU General Public License, version 2.		\n\
									\n\
");
}

int parse_args (int argc, char* argv[])
{
	while (1){
		struct option lopts [] = {
			{"input", 1, NULL, 0},
			{"output", 1, NULL, 0},
			{"stack", 1, NULL, 0},
			{"mem", 1, NULL, 0},
			{"fsize", 1, NULL, 0},
			{"time", 1, NULL, 0},
			{"open-files", 1, NULL, 0},
			{"proc", 1, NULL, 0},
			{"timehard", 1, NULL, 0},
			{"chroot", 1, NULL, 0},
			{"debug", 0, NULL, 0},
			{"help", 0, NULL, 0},
			NULL
		};
		
		int index;
		int c = getopt_long (argc, argv, "", lopts, &index);
		
		if (c == -1) break;
		
		if (c != 0) {
			print_usage ();
			exit (1); /* parsing failed? */
		}
		
		if (strcmp (lopts[index].name, "input") == 0)
			infile = strdup (optarg);
		else if (strcmp (lopts[index].name, "output") == 0)
			outfile = strdup (optarg);
		else if (strcmp (lopts[index].name, "open-files") == 0)
			limit_file = atoi (optarg);
		else if (strcmp (lopts[index].name, "proc") == 0)
			limit_nproc = atoi (optarg);
		else if (strcmp (lopts[index].name, "chroot") == 0)
			chrootdir = strdup (optarg);
		else if (strcmp (lopts[index].name, "debug") == 0)
			debug = 1;
		else if (strcmp (lopts[index].name, "help") == 0) {
			print_usage ();
			exit (0);
		}
		else if (strcmp (lopts[index].name, "time") == 0) {
			limit_time = atof (optarg);
		}
		else if (strcmp (lopts[index].name, "stack") == 0)
			limit_stack = unformatvalue (optarg);
		else if (strcmp (lopts[index].name, "mem") == 0)
			limit_mem = unformatvalue (optarg);
		else if (strcmp (lopts[index].name, "fsize") == 0)
			limit_fsize = unformatvalue (optarg);
		else if (strcmp (lopts[index].name, "timehard") == 0)
			limit_timehard = atoi (optarg);
		else assert (false);
	}
	
	/* return the execute command */
	if (optind == argc) {
		//fprintf (stderr, "No program name given.\n");
		print_usage ();
		exit (0);
	}
	return optind;
}

int subprocess (int argc, char* argv[])
{
	struct rlimit rlp;
	char   **commands;
	int    i; 

	rlp.rlim_cur = (int) ceil (limit_time); 
	rlp.rlim_max = limit_timehard;
	if (setrlimit(RLIMIT_CPU,&rlp) != 0) {
		//perror("setrlimit: RLIMIT_CPU");
		exit (1);
	}
	
	//fprintf(stderr, "Time limit is set to %d (hard:%d) seconds\n", 
		//(int) rlp.rlim_cur, (int) rlp.rlim_max );
	
	rlp.rlim_cur = rlp.rlim_max = limit_mem;
	if ( setrlimit(RLIMIT_DATA ,&rlp) != 0 ) 
		//perror("setrlimit: RLIMIT_DATA: ");
	//fprintf(stderr, "Memory limit is set to %d bytes\n", limit_mem);
	
	rlp.rlim_cur = rlp.rlim_max = limit_mem; 
	if ( setrlimit(RLIMIT_AS,&rlp) != 0 ) 
		//perror("setrlimit: RLIMIT_AS");
	
	rlp.rlim_cur = rlp.rlim_max = limit_fsize; 
	if (setrlimit(RLIMIT_FSIZE,&rlp) != 0)
		//perror("setrlimit: RLIMIT_FSIZE");
	
	rlp.rlim_cur = rlp.rlim_max = limit_file; 
	if (setrlimit(RLIMIT_NOFILE,&rlp) != 0) 
		//perror("setrlimit: RLIMIT_NOFILE");
	
	rlp.rlim_cur = limit_stack; 
	rlp.rlim_max = rlp.rlim_cur + 1024 ; 
	if ( setrlimit(RLIMIT_STACK,&rlp) != 0 ) 
		perror("setrlimit: RLIMIT_STACK");
	
	if(infile && freopen(infile,"r",stdin)==NULL)
	{
		perror("ERRIN ");
		//fprintf(stderr,"Internal error: Couldn't redirect input to stdin\n");
		return 23;
	}
	
	if(outfile && freopen(outfile,"w",stdout)==NULL)
	{
		perror("ERROUT ");
		//fprintf(stderr,"Internal error: Couldn't redirect output to stdout\n");
		return 24;
	}
	
	//if (!chrootdir)
		//fprintf(stderr,"Chroot dir not specified.\n");
	//else {
	//CHANGED ELSE TO IF
	if(!chrootdir){
		//if (chdir(chrootdir) != 0) {
			//perror ("Unable to change directory, chroot will be ineffective");
		//}
		if (chroot(chrootdir)  != 0)  {
			//perror("Chroot failed. Continuing anyway") ; 
			chrootdir = NULL ;
		}
	}
	
	//fprintf(stderr,"Before setres[gu]id: Effective uid=%d gid=%d \n",geteuid(),getegid());
	if ( setresgid(65534,65534,65534) != 0 || setresuid(65534,65534,65534)!=0 ){
		//perror("Unable to set the permissions of the running program\n" 
		     //  "This is a severe security issue! Try chowning runner to "
		      // "root and setting the suid bit on\nContinuing anyway.");
	}
	
	if (debug) 
		fprintf(stderr, "nproc limit: %d\n", limit_nproc);
	rlp.rlim_cur = rlp.rlim_max = limit_nproc;  
	if ( setrlimit(RLIMIT_NPROC,&rlp) != 0 ) 
		//perror("setrlimit: RLIMIT_PROC");
	
	//fprintf(stderr,"Ready to exec with: Effective uid=%d gid=%d \n",geteuid(),getegid());
	
	if (geteuid () == 0 || getegid () == 0) {
		fprintf (stderr, "FATAL: we're running as root!");
		return 1;
	}
	
	if (!debug) {
		if ( freopen("/dev/null", "w", stderr) == NULL ) 
		{
			//perror("freopen");
			//fprintf(stderr,"Internal error: Failed to redirect stderr\n");
			return 25;
		}
		//else
			//fprintf (stderr, "debug: not redirecting stderr on purpose.\n");
	}
	
	commands = (char**) malloc (sizeof (char*)*(argc + 1));
	for (i = 0; i < argc; i++)
		commands [i] = argv[i];
	commands [argc] = NULL;
	execve(argv[0], commands, NULL) ;
	perror("Unable to execute program") ;
	
	exit (26);
}

int main (int argc, char* argv[])
{
	int cmd_start_index;
	int i;
	pid_t pid, hardlimit_monitor;

	init_default_limits ();
	cmd_start_index = parse_args (argc, argv);

	/* be safe on the timehard! */
	if (limit_timehard < 1 + (int) ceil (limit_time))
		limit_timehard = 1 + (int) ceil (limit_time);
	
	/* close inherited file descriptors. Is there a better way? */
	for (i = 3; i < (1<<16); i++)
		close (i);
	
	pid = fork();
	if (pid==0) {
		return subprocess (argc - cmd_start_index, argv + cmd_start_index);
	}
	
	hardlimit_monitor = fork ();
	if (hardlimit_monitor == 0) {
		sleep (6*limit_timehard);
		/* if I reached here, then the main process is still running,
		 * upto some race condition possibilitiy */
		//fprintf (stderr, "Severe hardlimit (%d) reached. Possibly \
malicious, or overloaded system.\n", 6*limit_timehard);
		kill (pid, 9);
		return 0;
	}
	
	int status; 
	struct rusage usage ;  
	
	/*
	 * Correctness: Pid dies on its own or, hardlimit_monitor process
	 * kills it. In both cases, this works, except perhaps the Pid
	 * process can be called for kill twice.
	 */
	wait4(pid,&status, 0, &usage); //Wait for child to terminate
	kill (hardlimit_monitor, 9);
	waitpid (hardlimit_monitor, NULL, 0);
	
	// lets output the limits.
	fflush(stderr) ; /* ordering of output of child and parent should be right */
	
	
	
	double usertime = (float) (usage.ru_utime.tv_sec) + ((float) usage.ru_utime.tv_usec)/1000000 ;
	//fprintf(stderr, "Usertime: %lf\n", usertime);
	
	double systime = (float) (usage.ru_stime.tv_sec) + ((float)usage.ru_stime.tv_usec)/1000000 ;
	//fprintf(stderr, "Systime: %lf\n", systime);

	//fprintf(stderr, "Runtime: %lf\n", usertime+systime);
	
	
	
	if(WIFSIGNALED(status))
	{
		int signal = WTERMSIG(status);
		
		//fprintf(stderr, "Error in program: Status %d Signal %d\n",
			//status,signal);
		
#define die(s) { fprintf(stderr,s) ; exit(0) ; }
   
		if(signal==SIGXCPU) die("TLE Time limit exceeded (H)\n");
		if(signal==SIGFPE)  die("FPE Floating point exception\n");
		if(signal==SIGILL)  die("ILL Illegal instruction\n");
		if(signal==SIGSEGV) die("SEG Segmentation fault\n");
		if(signal==SIGABRT) die("ABRT Aborted (got SIGABRT)\n");
		if(signal==SIGBUS)  die("BUS Bus error (bad memory access)\n");
		if(signal==SIGSYS)  die("SYS Invalid system call\n");
		if(signal==SIGXFSZ) die("XFSZ Output file too large\n");
		if(signal==SIGKILL) die("KILL Your program was killed (probably because of excessive memory usage)\n");
		
		die("UNK Unknown error, possibly your program does not return 0, or maybe its some fault of ours!");
	}
	
	
	
	if (usertime + systime > limit_time) die("TLE Time Limit exceeded\n") ;
	
	if (!WIFEXITED(status)) {
		fprintf (stderr,"EXIT Program exited abnormally. This could be due to excessive memory usage, or any runtime error that is impossible to determine.\n");
		exit (0);
	}
	
	if (WEXITSTATUS(status) != 0) { 
		//fprintf (stderr, "Program return value: %d\n", WEXITSTATUS(status));
		fprintf (stderr,"EXIT Program did not return 0\n", WEXITSTATUS(status));
		exit (0);
	}
	
	
	return 0;
	
}
