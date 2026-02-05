//multiThreads.c
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

#define NUM_THREADS 10

DWORD Sum = 0; /* shared data */

/* Thread function */
DWORD WINAPI Summation(LPVOID Param)
{
    DWORD Upper = *(DWORD*)Param;

    printf("Thread %lu started - calculating sum from 1 to %lu...\n",
           GetCurrentThreadId(), Upper);

    for (DWORD i = 1; i <= Upper; i++) {
        Sum += i;      // Shared variable (race condition exists)
        Sleep(100);
    }

    printf("Thread %lu completed.\n", GetCurrentThreadId());
    return 0;
}

int main(int argc, char *argv[])
{
    if (argc != 2) {
        printf("Usage: %s <number>\n", argv[0]);
        return 1;
    }

    HANDLE ThreadHandles[NUM_THREADS];
    DWORD ThreadIds[NUM_THREADS];
    DWORD Params[NUM_THREADS];

    DWORD Upper = (DWORD)atoi(argv[1]);

    printf("Main: Creating %d threads...\n", NUM_THREADS);
    Sleep(2000);

    /* Create 10 threads */
    for (int i = 0; i < NUM_THREADS; i++) {
        Params[i] = Upper;   // Each thread gets its own parameter

        ThreadHandles[i] = CreateThread(
            NULL,
            0,
            Summation,
            &Params[i],
            0,
            &ThreadIds[i]
        );

        if (ThreadHandles[i] == NULL) {
            fprintf(stderr, "Error creating thread %d: %lu\n", i, GetLastError());
            return 1;
        }

        printf("Main: Created thread %d with ID %lu\n", i, ThreadIds[i]);
    }

    printf("Main: Waiting for all threads to complete...\n");

    /* Wait for all threads */
    WaitForMultipleObjects(NUM_THREADS, ThreadHandles, TRUE, INFINITE);

    /* Close handles */
    for (int i = 0; i < NUM_THREADS; i++) {
        CloseHandle(ThreadHandles[i]);
    }

    printf("Main: Final sum = %lu\n", Sum);
    printf("Main: Press Enter to exit...\n");
    getchar();

    return 0;
}
