// enclov-AI/native/main.c

#include <stdio.h>
#include <stdlib.h>
#include <curl/curl.h>

void print_banner() {
    printf("\n=== enclov-AI CLI Diagnostic Tool ===\n");
    printf("Checking system and API integration...\n\n");
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
    fwrite(ptr, size, nmemb, stdout);  // print response directly
    return total_size;
}

void check_api() {
    CURL *curl = curl_easy_init();
    if (!curl) {
        fprintf(stderr, "[!] Failed to initialize libcurl\n");
        return;
    }

    printf(">> enclov-AI Backend Response:\n");

    curl_easy_setopt(curl, CURLOPT_URL, "https://api.kubu-hai.com/status"); // Replace with your actual endpoint
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        fprintf(stderr, "   [!] curl error: %s\n", curl_easy_strerror(res));
    }
    curl_easy_cleanup(curl);
    printf("\n");
}

int main() {
    print_banner();

    run_command("System Info", "uname -a");
    run_command("Memory Info", "free -h");

    check_api();  // Query your FastAPI backend

    printf("\n=== enclov-AI CLI diagnostics complete ===\n");
    return 0;
}
