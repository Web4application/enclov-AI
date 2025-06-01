#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

void print_banner() {
    printf("\n=== enclov-AI CLI Diagnostic Tool ===\n\n");
}

void usage() {
    printf("Usage: enclov-cli [OPTION]\n");
    printf("Options:\n");
    printf("  --sys     Run local system diagnostics\n");
    printf("  --api     Query enclov-AI backend API\n");
    printf("  --all     Run all diagnostics (default)\n");
    printf("  --help    Show this help message\n");
}

void run_command(const char* label, const char* cmd) {
    printf(">> %s:\n", label);
    int result = system(cmd);
    if (result != 0) {
        printf("   [!] Error running: %s\n", cmd);
    }
    printf("\n");
}

size_t write_callback(void *ptr, size_t size, size_t nmemb, void *userdata) {
    size_t total_size = size * nmemb;
    fwrite(ptr, size, nmemb, stdout);
    return total_size;
}

void check_api() {
    CURL *curl = curl_easy_init();
    if (!curl) {
        fprintf(stderr, "[!] Failed to initialize libcurl\n");
        return;
    }

    printf(">> enclov-AI Backend Response:\n");

    curl_easy_setopt(curl, CURLOPT_URL, "https://api.kubu-hai.com/status");
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        fprintf(stderr, "   [!] curl error: %s\n", curl_easy_strerror(res));
    }
    curl_easy_cleanup(curl);
    printf("\n");
}

void run_sys_checks() {
    run_command("System Info", "uname -a");
    run_command("CPU Info", "lscpu | head -n 10");
    run_command("Memory Info", "free -h");
    run_command("Git Repo Status", "git status");
    run_command("Installed Python Packages", "python3 -m pip list | head -n 10");
}

int main(int argc, char *argv[]) {
    print_banner();

    if (argc < 2 || strcmp(argv[1], "--all") == 0) {
        run_sys_checks();
        check_api();
    } else if (strcmp(argv[1], "--sys") == 0) {
        run_sys_checks();
    } else if (strcmp(argv[1], "--api") == 0) {
        check_api();
    } else if (strcmp(argv[1], "--help") == 0) {
        usage();
    } else {
        fprintf(stderr, "[!] Unknown option: %s\n\n", argv[1]);
        usage();
        return 1;
    }

    printf("=== enclov-AI CLI complete ===\n");
    return 0;
}
